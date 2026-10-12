# Existing Playwright evidence

Use the project's runner/configuration first. These patterns are for a small temporary script when there is no suitable runner. Resolve the already installed module from the project; do not install a test framework solely for screenshots. Adapt to the actual project/host API rather than assuming these APIs exist in every browser integration.

## Probe outcomes

`node scripts/playwright-probe.cjs --project /abs/project` exits 0 after a successful Chromium launch; exits 2 with JSON identifying a module, binary or launch blocker. It does not navigate, fetch, install or change project dependencies. `--module /abs/path/to/installed/playwright` is an optional explicit reuse path; do not search unrelated private projects automatically. A launch failure is not always a missing dependency: permission/display/sandbox failures need their own diagnosis.

Examples of truthful offers (adapt the command to the repository's manager/version):

- Package missing: “No host browser is available and `playwright`/`@playwright/test` cannot resolve in this project. May I add the compatible Playwright dev dependency here? This will change package and lock files.”
- Chromium missing: “Playwright is installed, but its configured Chromium executable is absent at [reported path]. May I run the existing local CLI's `install chromium`? No package addition is needed.”
- Recorder missing: “The browser can run the flow and export screenshots, but its documented API has no video recording. Video is blocked. May I set up [specific compatible recorder]?”

Offer first, wait, then install only what was approved. Do not copy a binary from an unrelated location to evade approval. If another already supported browser works, it is an acceptable fallback with its identity reported.

## Screenshots and diagnostics

```js
// `chromium` comes from the project's installed Playwright.
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
const page = await context.newPage();
const errors = [];
page.on('pageerror', e => errors.push({ type: 'pageerror', message: e.message }));
page.on('console', m => { if (m.type() === 'error') errors.push({ type: 'console', message: m.text() }); });
page.on('requestfailed', r => errors.push({ type: 'requestfailed', url: r.url(), error: r.failure()?.errorText }));
// HTTP 4xx/5xx do not fire requestfailed: observe response status if relevant.
page.on('response', r => { if (r.status() >= 400) errors.push({ type: 'http', status: r.status(), url: r.url() }); });
await page.goto(localUrl);
// Use locators grounded in actual page/DOM observation, exercise the changed control,
// and assert its visible result before taking a screenshot.
await page.screenshot({ path: absoluteScreenshotPath });
await context.close();
await browser.close();
```

Do not publish raw diagnostic arrays without inspecting URLs/messages for sensitive data. These listeners are useful diagnostics, not proof of full correctness.

## Long-flow recording

Create a fresh context/page dedicated to the target flow so unrelated actions stay out of the recording:

```js
const context = await browser.newContext({
  viewport: { width: 1280, height: 800 },
  recordVideo: { dir: absoluteEvidenceDir, size: { width: 1280, height: 800 } }
});
const page = await context.newPage();
const video = page.video();
try {
  await page.goto(localUrl);
  // Perform the actual scenario, checking visible states along the way.
  // Use short readability pauses only where needed for the delivered video.
} finally {
  await context.close(); // finalizes the video even when the flow fails
}
const videoPath = await video.path();
```

Close the browser in the script's outer `finally`. Label a failure recording as failed; never present it as success proof. Open/decode the file and review representative states (start, transitions, final). A decoder probe alone only proves readability. When available, an existing `ffmpeg` can convert WebM to H.264 MP4 for a host that cannot display WebM; keep the original. Missing conversion tools do not invalidate a playable original, and require approval to install.

Judge duration by legibility and complete flow coverage, not a fixed cap. This prototype's 3-route fixture is legible at 8.48 seconds; longer real tasks need their own review. Screenshots are still needed for meaningful visual changes within a recorded flow.

## Moving dialogs and coordinate gestures

Playwright locator actions such as click/dragTo perform relevant stability checks; low-level mouse coordinates are captured by the driver and can become stale while a modal moves. [Official actionability reference](https://playwright.dev/docs/actionability).

For a coordinate gesture that cannot use a suitable locator action:

```js
const { waitForStableBox } = require('/absolute/path/to/skill/scripts/stable-box.cjs');
await panel.waitFor({ state: 'visible' });
await panel.scrollIntoViewIfNeeded();
await waitForStableBox(() => panel.boundingBox());
const handleBox = await waitForStableBox(() => resizeHandle.boundingBox());
// Perform the supported mouse gesture using fresh handleBox. Recheck the intended
// size/position and polygon constraints afterwards; a click/drag call is not proof.
```

The helper accepts a callback returning `{x,y,width,height}` or null. It only reads geometry, requires positive size, waits for 300 ms of stability within 0.5 CSS px by default, detects cumulative drift, and fails within a bounded budget. Those values are driver defaults, not a claim that every animation ends in 300 ms. Adapt to actual motion. It cannot establish hit testing, visibility, readiness of the app or a successful gesture. With a host browser, use its documented state/geometry APIs rather than assuming Playwright boundingBox is exposed.

## Actual asynchronous result

Map the expected outcome to the generated result: a server-rendered overlay needs inspection of the returned media, while a saved preference needs readback after the supported navigation/reload lifecycle. Distinguish intended draft-discard behavior from a persistence bug before using F5 as acceptance.

Exercise browser → request → job/state → completed output → user-visible playback/display. Retain request/job correlation only if safe to share. Wait with a bounded timeout and inspect pending/error states; do not infer completion from HTTP 202/201 or a button label. Use existing decoders/tools when the output is media. Capture the visible completed result, then compare an appropriate part of the output to the expected content/duration. For a claimed failure fix, retain failing evidence and rerun the same inputs on the corrected revision. Label UI, persistence and actual-output checks separately. Do not broaden a website change into a backend audit or payment operation.
