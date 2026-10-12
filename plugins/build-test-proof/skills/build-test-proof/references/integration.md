# Installation and invocation checks

Use the current host's documented plugin flow. A local marketplace is an authoring source, not a public listing. Plugin installation does not supply a browser, access account sessions or grant permission for project changes.

For an installation test, record these independently:

1. Package installed/enabled and installed files match the requested version.
2. A **fresh** chat/session's skill catalog contains BuildTestProof and its real qualified name/path.
3. Explicit invocation selects that catalog entry and reads its instructions.
4. An ordinary website-change request selects it implicitly, if the client supports that behavior. A successful explicit invocation does not prove implicit routing.

Use the real catalog name. Some hosts namespace the skill as `build-test-proof:build-test-proof`; others expose the bare name. Do not manufacture a namespaced command. If the catalog entry is absent, report discovery unavailable. Reading a packaged SKILL.md directly is a useful manual fallback for ordinary work, but it is **manual_file**, not a successful discovery test. A file found by disk search is not proof that the client loaded it.

After local package updates, refresh/reinstall with the host's supported command and create a fresh session. If the host documents a restart requirement, report that limitation rather than restarting an active user session or interrupting unrelated chats without need.

For agent/project setup, use the included [AGENT_GUIDE.md](../../../AGENT_GUIDE.md). Explicit project instructions may request this workflow for affected website changes while preserving the project's own test/deploy rules. Do not edit every project's AGENTS.md or user-wide settings automatically.

Current OpenAI packaging: root plugin.json + skills/, local marketplace discovery and installation. [Official documentation](https://developers.openai.com/plugins/build/plugins). Public distribution requires separate dashboard validation and publisher metadata: [submission documentation](https://developers.openai.com/plugins/deploy/submission). Other coding agents may support portable skills but their plugin installation/discovery remains host-specific and must be tested rather than promised.
