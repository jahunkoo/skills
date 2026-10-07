# jahunkoo/skills

Agent skills for Claude Code, Codex, Grok, and others, each published with its evaluation. Skills follow the [Agent Skills](https://agentskills.io) format.

distill cleans agent instructions such as AGENTS.md, SKILL.md, command definitions, and system prompts: it removes outdated history and keeps what the agent should do now, and it edits a file only after you approve its diagnostic report.

```sh
npx skills add jahunkoo/skills --skill distill
```

It needs Node.js.

## Catalog

<!-- catalog:start -->
| Skill | Version | Description | With skill | Without skill | Difference | Confirmation |
| --- | --- | --- | --- | --- | --- | --- |
| [distill](skills/distill/SKILL.md) | 1.1.0 | Removes outdated history from agent instructions, keeping only what the agent should do now. Reports first and edits only after you approve. | 96% | 66% | +30 points | [iteration-10](workspaces/distill-workspace/iteration-10/) |
<!-- catalog:end -->

Outcome pass rate is the share of outcome assertions that pass in a run, averaged over runs. A judged assertion passes only when both graders pass it. Graders are not told which arm a run is, though an answer can reveal it ([docs/evaluation.md](docs/evaluation.md)). The runs were told to read the skill, so the numbers measure what the skill does once it is in use, not how often it is picked automatically. Per-agent results: [workspaces/distill-workspace/README.md](workspaces/distill-workspace/README.md). How skills are evaluated and admitted: [docs/evaluation.md](docs/evaluation.md).

## Use distill

Ask your agent to distill a file, for example "distill AGENTS.md". The [skill](skills/distill/SKILL.md) reads the file and reports, sentence by sentence, what it would remove and why, what it keeps, and anything you need to decide. It does not edit the file until you approve the report.

An excerpt from a [confirmation run](workspaces/distill-workspace/iteration-10/codex/eval-d1-diagnose-release-notes/with_skill/run-1/outputs/response.md) on a release-notes SKILL.md (Codex CLI):

> | Location | Type | Evidence |
> |---|---|---|
> | Line 10, "used to be written directly on a Notion page…" | History | Keep the instruction to write in root `CHANGELOG.md`; the former location does not affect it. |
> | Line 27, `docs/format-guide.md` | Dead reference | The file is absent from the repository. |
> | Line 40, `skip-changelog` instruction | Duplicate | Line 19 already states the same rule. |
>
> Deleted 0 (6 proposed: history 1, rebuttal 1, superseded rule 1, meta note 1, dead reference 1, duplicate 1) · Kept 13 instruction-bearing lines · Needs decision 1

Other published skills are also named `distill` and do different things. `npx skills` installs a skill into a folder named after it, so installing another `distill` replaces this one. Install this one from `jahunkoo/skills` as shown here.

## Install

The command at the top installs distill for your agents. To install it as a plugin from this repository's marketplace instead:

Claude Code

```sh
claude plugin marketplace add jahunkoo/skills
claude plugin install distill@jahunkoo-skills
```

Codex CLI

```sh
codex plugin marketplace add jahunkoo/skills
codex plugin add distill@jahunkoo-skills
```

Grok

```sh
grok plugin marketplace add jahunkoo/skills
grok plugin install distill --trust
```

Copilot CLI, Cursor, and Gemini CLI, invocation names, update, removal, and pinning to a release tag: [docs/install.md](docs/install.md).

## Layout

| Path | What it is |
| --- | --- |
| `skills/<name>/` | The skill itself. `npx skills` and Gemini CLI install from here. |
| `plugins/<name>/` | A generated copy of the skill with a `plugin.json`, for plugin marketplaces. Do not edit it. |
| `.claude-plugin/`, `.agents/plugins/`, `.grok-plugin/` | Marketplace files for Claude Code, Codex CLI, and Grok. Each lists `plugins/<name>/`. |
| `workspaces/<name>-workspace/` | Evaluation evidence: decision rule, answer keys, ledger, and the confirmation run's raw outputs. `registered/` holds the exact files registered for that run; it is not an install target. |
| `eval-harness/` | The evaluation runner. |
| `docs/` | Installation and evaluation guides. |

## Issues

Report problems as issues. Pull requests are not accepted. Changes are made in the maintainer's private source repository and exported here.

## License

[MIT](LICENSE). Each skill folder carries the same license as `LICENSE.txt`, so a copied skill keeps it.
