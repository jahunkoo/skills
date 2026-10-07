# distill 1.1.0 confirmation

The skill was developed over iterations in the maintainer's private source repository and then frozen. The published numbers come from a separate confirmation run of that frozen text. A confirmation run is a measurement of the frozen skill, not a run used to edit it.

iteration-10, 2026-10-01. Skill sha256 `a5ecd0c50a19e203fcf4cb7f5e04836294b191e12ad0bc2f199e5f79b09806f8` (`skill_sha256` in [benchmark.json](iteration-10/benchmark.json); [summary.md](iteration-10/summary.md) prints the prefix `a5ecd0c50a19`). Harness `4828121` (a commit in the maintainer's private source repository; see Limits). 48/48 runs graded, 2 runs per configuration. The tables below are the summary. The same results, unrounded, are in the benchmark file.

In the tables, points are percentage points. Dates are UTC dates; no times are recorded.

## Decision

Publish. Every agent meets the criteria. On the held-out evals the relative error reduction is 78% (confirmed), against a rule of at least 60%. The rule is [decision-rule-1.1.0.md](decision-rule-1.1.0.md).

## Headline

**Outcome pass rate**, mean over agents: with skill 96%, without 66%, difference **+30 points** (95% CI +23 to +37; one-sided exact permutation test stratified by agent, p = 8.5e-06).

| Agent | Outcome pass rate with / without | Difference, points (95% CI) | p | All assertions with / without | Judge quality score (1–5) with / without | Safety with / without | Criteria met | Judge agreement (κ) | Mean time with / without | Mean tokens with / without |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Code · claude-opus-5-5 · high | 100% / 82% | +18 (+15 to +21) | 0.013 | 98% / 67% | 4.9 / 3.5 | 100% / 62% | yes | 95% (0.82) | 39s / 33s | 122k / 111k |
| Codex CLI · gpt-6-sol · high | 100% / 45% | +55 (+49 to +60) | 7.8e-05 | 98% / 43% | 4.6 / 2.4 | 100% / 62% | yes | 89% (0.73) | 132s / 95s | 125k / 150k |
| Grok CLI · grok-4.7 · high | 89% / 72% | +17 (-3 to +36) | 0.134 | 90% / 66% | 4.8 / 3.3 | 100% / 75% | yes, weak evidence | 95% (0.82) | 310s / 181s | 218k / 265k |

CLI versions recorded in each run's `timing.json`: Claude Code 2.1.286, codex-cli 0.157.1, grok 1.0.46.

Excluded assertions (judge agreement below 70%): h3.deadref, h3.keep.

| Eval set | Evals | Outcome pass rate with / without | Difference, points (95% CI) | p | Relative error reduction |
|---|---|---|---|---|---|
| dev | d1-diagnose-release-notes, d2-apply-preapproved | 100% / 65% | +35 (+28 to +42) | 4.4e-05 | 100% |
| holdout | h3-diagnose-support-prompt, h4-apply-support-prompt | 93% / 68% | +25 (+13 to +37) | 0.025 | 78% (confirmed) |

## Weaknesses

Grok CLI is marked weak evidence. The outcome difference is +17 points, the 95% CI is -3 to +36, and p = 0.134. The interval includes zero. The agent still meets the effect-size criteria: at least +15 points on the outcome pass rate, with judge quality and safety not lower. Meeting the criteria is that threshold. It is distinct from statistical significance.

One grading file is incomplete. In [iteration-10/grok/eval-h4-apply-support-prompt/with_skill/run-2/grading.json](iteration-10/grok/eval-h4-apply-support-prompt/with_skill/run-2/grading.json), the Claude grader's verdict is null on seven assertions (six outcome, one procedure), and `quality_score.by_grader` has no `claude` entry. A judged assertion passes only when both graders pass it, so the aggregate counted those seven as failures. The other grader's verdicts on those seven assertions are passes in that file. The published Grok row is the conservative figure.

Filling each missing verdict with the other grader's recorded verdict, in the published run order (`prepare` seed 20260930), changes the Grok row to 100% / 72%, +28 points (95% CI +15 to +41, p = 0.0035). In that same order the pooled difference changes from +30 points to +34 points (95% CI +29 to +39). The held-out with-skill outcome pass rate changes from 93% to 100%, and the held-out relative error reduction changes from 78% to 100%. Under that fill-in the Grok row would not be marked weak evidence. The decision stays publish either way. The tables above are the published count, not the fill-in. Only the parsed fields in that file are the basis for this note.

Two judged assertions, h3.deadref and h3.keep, are excluded because grader agreement on them is below 70%. They are in neither pass rate.

## Cost

Mean time and mean tokens per run, with the skill and without, from the table above.

| Agent | Mean time with / without | Mean tokens with / without |
|---|---|---|
| Claude Code | 39s / 33s | 122k / 111k |
| Codex CLI | 132s / 95s | 125k / 150k |
| Grok CLI | 310s / 181s | 218k / 265k |

With the skill, the runs take longer on every agent. Token counts are what each CLI reports. They are not comparable across agents.

## Limits

The published numbers are the effect when the agent was told to read the skill.

The skill was edited against the development evals, so the development-set difference (+35 points, relative error reduction 100%) is the optimistic side. The held-out evals were written after the skill was frozen and were not used to edit it. Their difference is +25 points, and their relative error reduction is 78%.

The evidence that the decision rule was fixed before this run is a commit in the maintainer's private source repository. Readers of this repository cannot see that commit. The bytes registered for the run are in [registered/iteration-10/](registered/iteration-10/). Their SHA256SUMS match the hashes in the decision rule, which shows that the published evaluation definition matches that table. The hashes do not show when the rule was written.

The confirmation run used the eval-harness at private commit `4828121` (`harness_commit` in [benchmark.json](iteration-10/benchmark.json) and in [summary.md](iteration-10/summary.md)). In the maintainer's private source repository, that eval-harness tree matches commit `f8b4534`, the harness named in the decision rule. This repository does not contain those commits, so the match cannot be checked here. The eval-harness published here is a later revision: when a grader's reply omits assertions, grade asks that grader again. The aggregation and statistics code are the same as in the private tree that ran iteration-10. That comparison was made in the private source repository; this repository cannot show the older tree.

Each agent has 8 runs with the skill and 8 without, and 4 and 4 of those are the held-out pair. The three agents have different grader pairs, so judge agreement is reported per agent. Agents are not ranked against each other.

Admission and the metric definitions: [docs/evaluation.md](../../docs/evaluation.md) and [eval-harness/README.md](../../eval-harness/README.md).

## Checking the numbers

The published point estimates and permutation p-values can be recomputed from the `outcome_pass_rate` fields in the published `grading.json` files. They do not depend on run order, apart from a fourth-decimal float difference that does not change the published table.

`aggregate` does not read this folder directly. It reads a run workspace (`control/`, with the manifest, the run-id mapping, and per-run results) that is not published. The published files are enough to rebuild that workspace, and the rebuilt aggregate matches these tables, including the run files.

The 95% confidence intervals depend on run order. The published intervals match `prepare --sets dev,holdout` with its default seed `20260930`. In folder order the Grok interval is -2 to +37, against the published -3 to +36, and the held-out interval is +12 to +38, against the published +13 to +37.

## Running it again

From the repository root, the sequence in [eval-harness/README.md](../../eval-harness/README.md) is prepare, run, check, grade, then aggregate. `prepare` prints a workspace path; pass that path as `<ws>`.

```sh
python3 eval-harness/harness.py prepare --config workspaces/distill-workspace/eval-config.json --sets dev,holdout --kind confirm --label <label>
python3 eval-harness/harness.py run --ws <ws> --jobs 3
python3 eval-harness/harness.py check --ws <ws>
python3 eval-harness/harness.py grade --ws <ws> --jobs 3
python3 eval-harness/harness.py aggregate --ws <ws> --out workspaces/distill-workspace/<label> --ledger workspaces/distill-workspace/ledger.json
```

`--sets dev,holdout` is this confirmation: d1, d2, h3, and h4. `--kind confirm` records a confirmation run. The default kind is a development iteration and does not apply the publishing rule. The published run is `iteration-10`. Do not pass `--label iteration-10`: `aggregate` deletes a folder that already contains `benchmark.json`, and it replaces that label's ledger row. Use a new label, such as `rerun-1`.

A new run uses the eval-harness in this repository, described under Limits, not the harness that produced iteration-10. The model names in [eval-config.json](eval-config.json) (`claude-opus-5-5`, `gpt-6-sol`, `grok-4.7`) may be unavailable on your account. The `claude`, `codex`, and `grok` CLIs need to be logged in. Requirements are in the harness README.

## Data

Each `iteration-N/` directory holds the unedited outputs of the agents named in that iteration's ledger row. For iteration-10, each run's `outputs/` holds that agent's unedited output, and `grading.json` holds both graders' verdicts as the harness parsed them.

Links inside those outputs, including `response.md`, point at paths in the fixture repository. They do not resolve in this repository.

[ledger.json](ledger.json) has one row per iteration. `raw_data` is `public` when this repository contains that run's raw data, and `private` when the raw data is not published. The iteration-6 row is the distill 1.0.0 confirmation run (`publish` true). This repository does not include the 1.0.0 skill or that run's raw data. `none` means the run has no raw data.

## Folders

| Path | What it is |
|---|---|
| [registered/iteration-10/](registered/iteration-10/) | Bytes registered for the confirmation run, with SHA256SUMS |
| [web-agents/](web-agents/README.md) | Answer key and programmatic checks for the web-agents evals |
| [support-prompt/](support-prompt/README.md) | Answer key, programmatic checks, and the fixture builder for the support-prompt evals |
| [ledger.json](ledger.json) | One row per iteration, development and confirmation |
| [iteration-10/](iteration-10/summary.md) | Unedited confirmation outputs, [benchmark.json](iteration-10/benchmark.json), and [summary.md](iteration-10/summary.md) |
| [decision-rule-1.1.0.md](decision-rule-1.1.0.md) | Decision rule fixed before the run |
| [eval-config.json](eval-config.json) | Agents, models, effort, and which graders judge which agent |
| [answer-key.md](answer-key.md), [checks.py](checks.py) | Answer key and programmatic checks for the development pair d1 and d2 |
