# Harness integration

One SKILL.md is shared across hosts. Select the host's actual browser tooling at runtime; this skill does not add a browser. OpenAI's `agents/openai.yaml` affects OpenAI hosts only. Portable installs omit it and retain automatic discovery through the name/description defaults.

| Host | Personal skill location | Project skill location | Explicit invocation |
| --- | --- | --- | --- |
| Cursor | `~/.cursor/skills/build-test-proof/` | `.cursor/skills/build-test-proof/` | `/build-test-proof` |
| Claude Code | `~/.claude/skills/build-test-proof/` | `.claude/skills/build-test-proof/` | `/build-test-proof` standalone; `/build-test-proof:build-test-proof` plugin |
| GitHub Copilot | `~/.copilot/skills/build-test-proof/` | `.github/skills/build-test-proof/` | Ask to use the named skill; check the host's current picker/tool |
| OpenCode | `~/.config/opencode/skills/build-test-proof/` | `.opencode/skills/build-test-proof/` | Ask to load `build-test-proof` through its skill tool |

These are documented default locations; customized config roots and remote sessions require their own setup. Do not install duplicate copies in several search roots. Choose standalone skill OR Claude plugin, not both. A standalone folder's INSTALLATION.json records its version; do not require plugin.json outside that folder to confirm installation.

Cursor/Claude/Copilot select relevant skills using their descriptions. OpenCode exposes skill names/descriptions through its skill tool. Neither a folder's existence nor a successful explicit call proves implicit activation. For an installation test, check the real fresh-session catalog, explicit use, and an ordinary relevant request separately. Label unavailable host tests honestly. A backend-only request with no affected website flow is a useful negative routing case.

## Persistent routing

Use a short impact-based instruction in the host's documented persistent instructions: Cursor User Rules or project rules/AGENTS.md; Claude Code CLAUDE.md; Copilot repository custom instructions; OpenCode AGENTS.md. Preserve existing content and permission gates. Never assume Codex's global AGENTS.md is read by all these hosts.

> For visible website UI or backend changes affecting a user-facing website flow, use the installed BuildTestProof skill when available. Test the affected flow and actual saved/generated result. Show fresh screenshots for meaningful visual changes and actual video for longer flows. For internal backend-only work without website behavior changes, use the appropriate technical tests. If the skill or browser is unavailable, disclose the gap. Existing project instructions and approval gates remain in effect.

Do not insert a hook that forces browser capture on every edit, or auto-install browser packages. If the host supports screenshots but not actual recording, use an already-installed recorder for the same safe flow, disclosing the switch; otherwise mark video blocked. Use the host's native artifact display when supported; fallback to usable file links. Do not claim cross-host chat rendering parity.

## Remote and cloud sessions

Local personal skills are not automatically present in every cloud/remote session. Cursor documents separate personal-skill sync; Claude Code cloud sessions can read committed project skills but not your local home folder. Use project scope when the execution environment needs repository-carried instructions, and explicitly inspect the remote session's skill catalog and browser availability. Installing a local folder does not authorize cloud sync or production access.

## Sources (checked 2026-10-13)

- [Cursor skills and discovery](https://cursor.com/docs/skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code plugins](https://code.claude.com/docs/en/plugins-reference)
- [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Copilot skill directories and activation](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [OpenCode skills](https://opencode.ai/docs/skills/)
