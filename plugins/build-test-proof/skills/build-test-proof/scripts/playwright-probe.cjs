#!/usr/bin/env node
// Read-only local probe. Host tool discovery remains the agent's responsibility.
const fs = require('node:fs');
const path = require('node:path');
const { createRequire } = require('node:module');
async function main() {
  const args = process.argv.slice(2);
  let project, explicitModule;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' && args[i + 1]) project = path.resolve(args[++i]);
    else if (args[i] === '--module' && args[i + 1]) explicitModule = path.resolve(args[++i]);
    else throw new Error('Usage: playwright-probe.cjs --project /abs/project [--module /abs/installed/playwright]');
  }
  if (!project || !fs.statSync(project).isDirectory()) throw new Error('A valid --project directory is required.');
  const resolve = createRequire(path.join(project, '__web_change_proof_probe__.cjs'));
  const attempts = [];
  let resolved;
  for (const candidate of explicitModule ? [explicitModule] : ['playwright', '@playwright/test', 'playwright-core']) {
    try { resolved = resolve.resolve(candidate); break; }
    catch (error) { attempts.push({ candidate, code: error.code }); }
  }
  if (!resolved) {
    console.log(JSON.stringify({ status: 'blocked', kind: 'module-missing', project, attempts,
      next: 'Inspect host browser tools first. If none fit, offer a compatible project dev dependency and wait for installation approval.' }, null, 2));
    process.exitCode = 2; return;
  }
  const { chromium } = resolve(resolved);
  if (!chromium) throw new Error('Resolved module has no Chromium API. Inspect the project browser configuration.');
  const executable = chromium.executablePath();
  if (!fs.existsSync(executable)) {
    console.log(JSON.stringify({ status: 'blocked', kind: 'binary-missing', module: resolved, executable,
      next: 'Check other configured installed browsers. If none fit, offer the existing Playwright CLI install chromium and wait for approval.' }, null, 2));
    process.exitCode = 2; return;
  }
  let browser;
  try {
    browser = await chromium.launch();
    console.log(JSON.stringify({ status: 'available', module: resolved, executable, browser: 'Chromium', version: browser.version(),
      scope: 'Local launch only; no website flow or video checked.' }, null, 2));
  } catch (error) {
    console.log(JSON.stringify({ status: 'blocked', kind: 'launch-failed', module: resolved, executable, error: error.message,
      next: 'Diagnose the exact launch failure. Do not assume a missing package or install without approval.' }, null, 2));
    process.exitCode = 2;
  } finally { if (browser) await browser.close(); }
}
main().catch(error => { console.log(JSON.stringify({ status: 'blocked', kind: 'probe-error', error: error.message }, null, 2)); process.exitCode = 2; });
