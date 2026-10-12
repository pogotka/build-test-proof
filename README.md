![BuildTestProof](assets/banner.svg)

<p align="center">
  <a href="https://github.com/pogotka/build-test-proof/releases"><img alt="Release" src="https://img.shields.io/github/v/release/pogotka/build-test-proof?color=0e766e"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-0e766e"></a>
  <img alt="Skills only" src="https://img.shields.io/badge/plugin-skills_only-174346">
</p>

**Build → test → proof.** A skills-only plugin that helps coding agents verify website changes in a real browser and show what actually worked.

[Install](#install) · [Automatic use](#automatic-use) · [When to use it](#when-to-use-it) · [Русский](#по-русски)

## What you get

- Fresh screenshots beside each meaningful visual change.
- Actual browser recordings for longer, multi-step flows.
- Bug reproduction, scoped fixes and reruns with the same input.
- Checks of saved records and generated output, beyond a successful request or client preview.
- Clear **passed / failed / blocked / not checked** outcomes.

The plugin supplies instructions and optional helpers. Your host or project supplies the browser. Missing dependencies are reported before installation; no silent browser downloads.

## Install

With a Codex client supporting plugin marketplaces:

```sh
codex plugin marketplace add pogotka/build-test-proof --ref main
codex plugin add build-test-proof@build-test-proof --json
codex plugin list --marketplace build-test-proof --json
```

Open a fresh chat and check that **BuildTestProof** appears in the skill catalog. If the client needs a refresh or restart, save your work first. Installation alone does not prove that an already-open chat has loaded the skill.

For a deliberate first check, select the skill in the picker or use its actual catalog name. The tested Codex name is:

```text
Use $build-test-proof:build-test-proof to verify this website change.
Show fresh evidence beside each result.
```

Already using the local installation? Keep it; do not install a duplicate just to use this repository. Choose one update source. [User guide](plugins/build-test-proof/USER_GUIDE.md) · [Release ZIP](https://github.com/pogotka/build-test-proof/releases/latest).

## Automatic use

The skill allows implicit invocation and describes the relevant work. The agent can select it without a skill mention when the task matches. This is task routing, not an always-on event hook, and selection is not guaranteed in every chat.

For consistent personal defaults, put the block from [AUTO_USE.md](plugins/build-test-proof/AUTO_USE.md) in `~/.codex/AGENTS.md`. For one project, put it in that project's `AGENTS.md`. Preserve existing instructions and check for `AGENTS.override.md` precedence.

Then an ordinary request is enough:

> Fix the mobile dialog layout and verify that submitting the form saves the record correctly.

The skill should apply because the task changes a website flow. It does not grant permission to deploy, use production accounts or install packages. [Agent/project guide](plugins/build-test-proof/AGENT_GUIDE.md).

## When to use it

| Change | Verification |
| --- | --- |
| Layout, copy, responsive UI | Browser interaction + fresh screenshot |
| Dialog, drag/resize, navigation | Actual affected actions; wait for stable geometry |
| Authentication, form save, web export, generated media | Browser → API → actual saved/generated result, plus relevant integration checks |
| Long journey across screens | Concise actual flow video |
| Internal backend refactor, DB index, infrastructure, non-web job | Appropriate technical tests; no mandatory browser captures |

Scope follows the **affected behavior**, not the filename or whether a repository happens to have a frontend. A backend bug can need browser proof; a backend-only change can be fully verified without screenshots.

## Evidence you can trust

A screenshot proves a visible state, not every server assertion. A client preview is not proof of the encoded export. A trace or screenshot montage is not a flow recording. Reports disclose these limits.

For a multi-run handoff, an optional `FINAL_INDEX.json` selects the final run, revision, environment and scenario coverage. The included validator checks references and declared consistency; it cannot prove that tests were performed. Evidence stays outside the application's source tree and is not committed by default.

## Tested behavior

The preceding 0.2.0 implementation was exercised in fresh chats: explicit catalog use and ordinary-prompt implicit use; desktop and narrow browser flows; an observed output bug followed by fix and rerun; screenshots and decoded actual videos. Optional helper tests covered 6 geometry cases and 18 evidence-index invariants. That does not establish universal automatic selection or full-site coverage.

0.2.1 clarifies routing for website-facing backend changes and adds distribution/automatic-use documentation. It retains the tested helpers. Real-project evidence is intentionally kept outside this public repository.

## Package and resources

```text
.agents/plugins/marketplace.json   GitHub marketplace
plugins/build-test-proof/
  plugin.json                     Portable plugin manifest
  skills/build-test-proof/         Skill, references and optional helpers
  AUTO_USE.md                     Persistent routing rule
  USER_GUIDE.md                    Installation and everyday use
  AGENT_GUIDE.md                   Project instructions
scripts/package.py                Build a clean plugin ZIP
```

```sh
python3 scripts/package.py
```

The ZIP contains the plugin only. Optional helpers need Node.js (browser probe/geometry) or Python 3.9+ (index validator); no runtime dependency installation is bundled.

## По-русски

**BuildTestProof проверяет результат веб-правок и показывает доказательства.** Для визуальных изменений — свежие скриншоты рядом с пунктами отчёта. Для длинного пути — настоящее видео. Для серверного результата — проверка сохранённой записи или фактически созданного файла.

Чтобы не писать название скилла каждый раз, установи и включи плагин, затем добавь правило из [AUTO_USE.md](plugins/build-test-proof/AUTO_USE.md) в общие инструкции Codex или `AGENTS.md` проекта. В новых чатах агент сможет применять его по задаче. Для внутренних backend-правок без влияния на веб-сценарий обязательного браузерного теста нет.

[Инструкция пользователю](plugins/build-test-proof/USER_GUIDE.md) · [Инструкция агентам](plugins/build-test-proof/AGENT_GUIDE.md).

## License and author

[MIT](LICENSE) · **npdev** · [npdev.ru](https://npdev.ru)

GitHub distribution is independent of OpenAI public-directory review. This repository does not imply an approved directory listing.
