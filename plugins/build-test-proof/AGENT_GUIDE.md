# BuildTestProof project-agent guide

Use the installed skill when a task changes website UI or user-facing web behavior. Respect the user's scope, repository instructions, unrelated WIP, dependency approvals and test/deployment gates. Skill installation grants no additional permissions.

## Persistent instructions

Copy the impact-based rule from [AUTO_USE.md](AUTO_USE.md) into the selected host's documented instructions. For Cursor/Claude/Copilot/OpenCode, follow [harness integration](skills/build-test-proof/references/harnesses.md). Do not assume a Codex global AGENTS.md applies to every host; do not edit unrelated project instructions automatically.

## Verification

Identify the route/flow and expected result. Inspect the real rendered state during implementation, perform the actual actions, fix within scope and repeat the same input. Before coordinate drag/resize, wait for stable geometry and obtain fresh bounds. Assert the actual position/size changed within the allowed region.

For server-generated results, retrieve and inspect the completed output/readback through the ordinary user path. HTTP success, job-ready, saved parameters and client preview do not individually prove output correctness. Keep UI passes separate from failed/blocked server assertions.

Capture and view fresh screenshots beside meaningful visual claims. Record actual video for long multi-step flows, finalize/decode it and inspect representative states. Keep evidence outside application source. For a multi-run handoff, select the final run/revision and precise coverage in FINAL_INDEX.json; do not hide previous failures in the final set.

## Installation testing

Distinguish catalog_explicit, catalog_implicit, manual_file and unavailable. Inspect the real fresh-session catalog; then verify explicit use and ordinary-prompt selection separately. Disk search does not prove host discovery. Standalone installations have their own version metadata; a plugin manifest is not required for a standalone skill.

## Optional helpers

- `skills/build-test-proof/scripts/playwright-probe.cjs`: read-only Playwright module + Chromium launch probe; no installation.
- `skills/build-test-proof/scripts/stable-box.cjs`: stable bounds observer; does not control a browser or prove hit testing.
- `skills/build-test-proof/scripts/validate-index.py`: Python 3.9+ structural evidence-index validation; does not run tests or inspect media.

Resolve resources relative to the installed SKILL.md, not an authoring machine's path. Use only supported tools exposed by the current host. If screenshot/video display is unavailable, provide usable file links and disclose that limitation. Report results in the user's language and do not invent collected evidence.
