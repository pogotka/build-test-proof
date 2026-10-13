# Automatic use

`policy.allow_implicit_invocation: true` permits the host to select this skill from its description. It is not an always-on hook and does not guarantee selection in every chat. The plugin must be installed, enabled and visible in the current session catalog. Start a fresh chat after installation when discovery is stale.

For a persistent working agreement, add the following block to a selected project's `AGENTS.md`, or to `~/.codex/AGENTS.md` for personal defaults across projects. Preserve existing instructions. An existing non-empty `AGENTS.override.md` takes precedence at the same level. Project instructions can override global defaults.

```md
## BuildTestProof: automatic website verification

When a task changes visible website UI, layout or interactions, or backend behavior affecting a user-facing website flow (forms, authentication, saved records, exports, generated output), use the installed BuildTestProof skill from the current session catalog, if available. Read its SKILL.md and verify the affected flow with real browser evidence within the authorized scope. For backend changes, also run appropriate API/integration checks and verify the actual saved/generated result. Put fresh screenshots beside meaningful visual changes; record actual video only for longer multi-step flows.

For backend-only refactors, database indexes/migrations, infrastructure or non-web jobs with no affected website behavior, use relevant technical tests; browser captures are not mandatory. Do not infer applicability from file extensions alone. Project-specific instructions and existing permission/deployment gates remain in effect. If the skill or browser is unavailable, disclose the gap; do not silently install dependencies or claim browser verification.
```

This adds a routing instruction, not a browser capability or permission to deploy. Avoid installing a second standalone copy of the same skill when the plugin already exposes it.

Official references: [skill discovery](https://learn.chatgpt.com/docs/build-skills), [AGENTS.md precedence](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

For other hosts, use [harness-specific routing instructions](skills/build-test-proof/references/harnesses.md). The OpenAI YAML policy is not a cross-host setting.
