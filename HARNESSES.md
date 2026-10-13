# Use BuildTestProof in other coding agents

One portable skill, several installation formats. Browsers and runtimes remain host/project dependencies. The repository ships an OpenAI-compatible plugin, a Claude Code plugin manifest/marketplace, and a standalone skill ZIP for supported hosts.

## Cursor, Claude Code, Copilot and OpenCode

Clone and inspect this repository, then run the installer from the clone:

```sh
git clone https://github.com/pogotka/build-test-proof.git
cd build-test-proof
python3 scripts/install_skill.py --host cursor --scope user --dry-run
python3 scripts/install_skill.py --host cursor --scope user
```

Replace `cursor` with `claude`, `copilot` or `opencode`. Requires existing Python 3.9+. The installer only copies bundled files; it does not fetch packages, install an IDE, start a model, change rules or upload anything.

For one project (including repository-carried skills for remote work):

```sh
python3 scripts/install_skill.py --host claude --scope project --project /absolute/path/to/project --dry-run
python3 scripts/install_skill.py --host claude --scope project --project /absolute/path/to/project
```

Identical installs are idempotent. If an existing skill differs, installation stops without overwriting it. For an update, review and back up/move that exact skill folder first, then install the new version. Do not install duplicate copies into different discovery roots.

You can instead extract `build-test-proof-skill-VERSION.zip` from [Releases](https://github.com/pogotka/build-test-proof/releases/latest) and move the complete `build-test-proof/` directory into a documented skills root. Keep its references, scripts, LICENSE and INSTALLATION.json with it.

| Agent | Personal install | Project install | First explicit check |
| --- | --- | --- | --- |
| Cursor | `~/.cursor/skills/build-test-proof/` | `.cursor/skills/build-test-proof/` | `/build-test-proof` |
| Claude Code | `~/.claude/skills/build-test-proof/` | `.claude/skills/build-test-proof/` | `/build-test-proof` |
| Copilot | `~/.copilot/skills/build-test-proof/` | `.github/skills/build-test-proof/` | Ask to use BuildTestProof and inspect selected skill |
| OpenCode | `~/.config/opencode/skills/build-test-proof/` | `.opencode/skills/build-test-proof/` | Ask to load BuildTestProof via the skill tool |

For customized config roots, inspect the host's documentation rather than assuming these defaults. Cloud/remote sessions need their own discovery check; a personal local installation does not imply cloud availability.

## Claude Code plugin alternative

Inside Claude Code:

```text
/plugin marketplace add pogotka/build-test-proof
/plugin install build-test-proof@build-test-proof
```

After the host's documented reload/new-session flow, invoke the plugin skill as:

```text
/build-test-proof:build-test-proof
```

For a local clone, an existing Claude Code CLI can load the plugin for a test session:

```sh
claude --plugin-dir ./plugins/build-test-proof
```

Use either the plugin or standalone skill, not both. Claude's native manifest lives in `.claude-plugin/plugin.json`; OpenAI's portable manifest remains `plugin.json`. They share the exact same `skills/` directory. No MCP server or event hooks are included.

## Automatic use

After installation, open a fresh session and confirm the skill is actually discoverable. Cursor and Claude Code permit automatic skill selection by default; this skill does not disable it. Copilot also matches the description; OpenCode exposes it through its skill tool. Automatic selection remains a host/model decision.

For a persistent working agreement, copy the routing paragraph from [harness integration](plugins/build-test-proof/skills/build-test-proof/references/harnesses.md#persistent-routing) into the appropriate instructions:

- Cursor: User Rules for personal defaults, or the project's documented rules/AGENTS.md.
- Claude Code: `~/.claude/CLAUDE.md` or project `CLAUDE.md`.
- Copilot: repository `.github/copilot-instructions.md` (or that client's documented personal instructions).
- OpenCode: project `AGENTS.md` (or that client's documented global instructions).

The installer deliberately does not edit these files. Codex's `~/.codex/AGENTS.md` is not a universal cross-agent setting.

## Verify in your actual harness

1. Check the fresh session catalog/picker: BuildTestProof should be listed.
2. Explicitly select it for a safe one-screen website change; check that the instructions are read and actual screenshot evidence is produced.
3. In a separate fresh session, ask an ordinary visual-fix request without naming the skill. Inspect whether it activates implicitly.
4. Ask about an internal backend refactor with no website behavior change. Browser captures should not be forced.
5. Test a longer safe flow only if a recorder already exists; inspect the resulting actual video. Missing dependencies require a specific offer and approval before installation.

## Compatibility status

**Verified:** portable file layout and relative references; installer paths for four hosts in isolated user/project directories; idempotency, dry-run and conflict preservation; archive integrity; existing helper tests. The shared browser workflow has preceding Chromium evidence in Codex.

**Documented, not runtime verified here:** native discovery, implicit activation and browser/video behavior inside Cursor, Claude Code, Copilot and OpenCode. Their CLIs were not available in the authoring session. No new IDE/CLI or browser was installed. Claude marketplace/manifests were structurally checked against the documented fields, not validated by a running Claude CLI.

[Official source links](plugins/build-test-proof/skills/build-test-proof/references/harnesses.md#sources-checked-2026-10-13). Documentation checked on 2026-10-13; installed client versions and organization policies can differ.
