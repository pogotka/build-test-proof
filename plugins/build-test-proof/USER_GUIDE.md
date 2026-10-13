# BuildTestProof user guide

BuildTestProof helps an agent verify affected website flows, reproduce bugs, rerun after fixes and associate results with fresh screenshots or actual videos. It supplies a skill and optional helpers; the host/project supplies the browser and account session.

## Choose an installation

- Codex/OpenAI: use the repository marketplace and plugin installation in the [README](https://github.com/pogotka/build-test-proof#install).
- Cursor, Claude Code, Copilot and OpenCode: use the [cross-harness installer guide](https://github.com/pogotka/build-test-proof/blob/main/HARNESSES.md).
- Claude Code can alternatively install the native plugin from the included marketplace.

Choose one installation source per host to avoid duplicate skill entries. After updating, follow the host's documented refresh/new-session flow. Installed files alone do not prove discovery in an already-open chat. A standalone copy has INSTALLATION.json; a plugin has its native manifest.

## First use

Check that BuildTestProof is present in the actual session catalog/picker. Select that entry explicitly for your first safe verification. Use the host's actual qualified name; Claude/Cursor standalone skills use `/build-test-proof`, while the Claude plugin is namespaced.

Then try an ordinary request without a skill mention:

> Fix the layout of this local website form. Verify submission and the actual saved record. Show screenshots beside meaningful visual changes; record the full flow only if it spans several steps. Do not change production.

Provide the project path/URL, affected page, expected result and permission to fix code. Log in to a safe test account yourself; do not paste secrets. Missing dependencies require an exact setup offer and approval before installation.

## Automatic use and scope

The skill description supports relevant-task selection. For persistent defaults, use the [automatic-use rule](AUTO_USE.md) in the correct host's instructions; [harness integration](skills/build-test-proof/references/harnesses.md) explains the differences. Local personal installation does not automatically cover remote/cloud sessions.

Use for visual changes or backend behavior affecting website flows, such as saved forms, authentication, exports or generated media. Internal backend work with no website behavior change needs appropriate technical tests, without mandatory browser captures.

## What a report should show

Each change and its actual verification; fresh screenshots beside visual results; actual recordings for long flows; problems, fix/rerun, unresolved issues and unchecked behavior. Generated media must be checked as completed output, not only a client preview or accepted job. Screenshots and static outputs have limits that must be disclosed.

Browser tests cover selected scenarios rather than all routes or all devices. A narrow desktop viewport is not a physical mobile device test. See the public README for a real safe demo.

## Dependencies and license

The portable instructions require no service. Optional Node helpers inspect Playwright or stable geometry; the optional evidence-index validator requires Python 3.9+. The installer/package builder also uses Python 3.9+ and does not fetch dependencies. MIT, npdev; [npdev.ru](https://npdev.ru).
