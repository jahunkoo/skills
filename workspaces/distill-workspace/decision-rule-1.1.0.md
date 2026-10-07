# Decision rule for distill 1.1.0 — fixed before the confirmation run

Fixed on 2026-10-01 (UTC). The confirmation run, `iteration-10`, is prepared at a commit that already contains this rule, and records that commit. No confirmation grade exists when this rule is fixed. Dates are UTC; no times are recorded.

Amended on 2026-10-01 before any grade existed. The first text of this rule ran all four development evals (72 runs) as `iteration-9`. At the user's request that run was stopped after 3 of 72 runs, before any check or grade and without reading any output, and the design was cut to the 1.0.0 size: one development pair and the new held-out pair (48 runs). In that attempt one held-out run finished (Codex CLI, h4, without skill) and two more were started (Grok CLI, h3, with skill); none was checked, graded or read. Nothing else changed. `iteration-9` is a ledger row marked stopped.

## What is evaluated

Paths are in the private source repository. At promotion the held-out evals are merged into `skills/distill/evals/evals.json`.

| Item | Path | sha256 |
| --- | --- | --- |
| Skill (distill 1.1.0 candidate) | `candidates/distill/SKILL.md` | `a5ecd0c50a19e203fcf4cb7f5e04836294b191e12ad0bc2f199e5f79b09806f8` |
| 2 development evals: d1, d2 (`"set": "dev"`; the file also holds h1, h2, which this run does not use) | `skills/distill/evals/evals.json` | `a172441dea9a15b837f73707162d97723f9618f0f90943fa088e0220fb88cd56` |
| 2 held-out evals: h3, h4 (`"set": "holdout"`; see the amendment note for the stopped attempt) | `candidates/distill-workspace/holdout/evals.json` | `5a7d7b27b2cebecce6469ccd437238431e1ef7b6ac9d0244a036e40a740a06c3` |
| Development fixture | `skills/distill/evals/files/release-notes.mbox` | `a4c481f8004d0ee5a0970ae60e9bfcd938229f19c5e90799a27f0e6c50e79468` |
| Held-out fixture | `candidates/distill-workspace/holdout/files/support-prompt.mbox` | `f9324ef696c230ef62d8aeb5a6d81667f6d3bdbc9937f3a3ea0845c738bf8d9d` |
| Answer keys | `workspaces/distill-workspace/answer-key.md` | `397417bee1e2d8f6379668d7a03b74fa38b2fd75a294e8d455265cc527cbc4b9` |
| | `candidates/distill-workspace/holdout/answer-key.md` | `75059230ca316122d12227aa8ec21e26b37b6b5348c22d2f32f4224c39e4f4ba` |
| Programmatic checks | `workspaces/distill-workspace/checks.py` | `d524f55722a0d0f8e120423f38d3121200f53404c4084cfab1d884654cd3417a` |
| | `candidates/distill-workspace/holdout/checks.py` | `1a65e40284cb0d18c9af5cab57cd662549b287f4a430c7b905b533317419464f` |
| Agents, efforts, grader assignment | `candidates/distill-workspace/eval-config.json` | `ee627e0ba29553cfcc4a5852c8711eaabaed4669a485c4c4e2d3974d9fb65194` |
| Harness, metrics and thresholds (`stats.RULE`) | `eval-harness/` at commit `f8b4534` | — |

The confirmation run records the repository commit it was prepared at; `git diff f8b4534 <that commit> -- eval-harness/` must be empty, and every file above must still match its hash.

How 1.1.0 came about: 1.0.0 passed its confirmation run (iteration-6). 1.1.0 was edited against the failures of the 1.0.0 runs (iterations 4 to 6) and developed in iterations 7 and 8 on d1, d2, h1 and h2. h1 and h2 were the 1.0.0 held-out evals; once used in iteration-6 they became development evals. The held-out evals h3 and h4 were written after 1.1.0 was frozen, and reviewed by Codex and Grok before this rule was fixed. Every iteration is a row in `workspaces/distill-workspace/ledger.json`.

## Design

| | |
| --- | --- |
| Agents | An agent is a CLI with its model: Claude Code (`claude-opus-5-5`), Codex CLI (`gpt-6-sol`), Grok CLI (`grok-4.7`). All agents and graders run at reasoning effort `high`. CLI versions are recorded per run |
| Runs | Per agent: 4 evals (d1, d2, h3, h4) × with/without skill × 2 runs = 16 runs; 48 runs in total (`--sets dev,holdout`) |
| Arms | A with_skill run is told to read the full `SKILL.md` (a copy of that file alone) before starting. A without_skill run gets the same prompt without that line. Every run starts in a fresh temporary home and a fresh fixture |
| Graders | Two graders per run, from vendors other than the agent's: Claude Code runs are graded by Grok and Codex, Codex CLI runs by Claude and Grok, Grok CLI runs by Claude and Codex. Graders do not see the arm. A judge assertion passes only when both graders pass it. Programmatic assertions are decided by `checks.py` |
| Missing runs | A run that ends without an answer is retried once from a fresh fixture. If it is still missing, that agent is incomplete |
| Output | The [agentskills.io](https://agentskills.io/skill-creation/evaluating-skills) layout with one level for the agent: `iteration-10/<agent>/eval-<name>/<with_skill\|without_skill>/run-K/` with `outputs/`, `grading.json` and `timing.json`, and `iteration-10/benchmark.json` |

## Metrics

| Metric | Definition |
| --- | --- |
| Pass rate | The share of a run's assertions that pass, then mean ± stddev over runs (the spec's `pass_rate`) |
| Outcome pass rate | The same over outcome assertions only. This is the headline and the main criterion |
| Safety pass rate | The same over gate and scope assertions |
| Judge quality score | Each grader's holistic score from 1 to 5; the mean of the two |
| Difference | With − without, in percentage points. Pooled over agents, the mean of the per-agent differences |
| 95% CI | Percentile bootstrap of the difference: 10,000 resamples with seed 20260930, resampling runs within each agent × eval cell |
| p | One-sided exact permutation test on per-run outcome pass rates (with > without). Per agent; pooled, arm labels are permuted only within each agent |
| Judge agreement | The share of judge verdicts on which the two graders agree, with Cohen's κ. An assertion on which they agree less than 70% of the time over the whole run is excluded from every pass rate and listed |
| Relative error reduction | (with − without) / (1 − without) on the outcome pass rate, pooled over agents, on the held-out evals: the share of the baseline's failures the skill removes |
| Cost | Mean time and tokens per run, with and without. Tokens are what each CLI reports and are not comparable across agents |

## Criteria (per agent)

An agent meets the criteria when all three hold:

1. The outcome pass rate is at least **15 percentage points** higher with the skill.
2. The judge quality score is not lower with the skill.
3. The safety pass rate is not lower with the skill.

The 95% CI and p are shown next to the result. When p ≥ 0.10 the result is marked "weak evidence"; this does not change whether the criteria are met. Meeting the criteria is an effect-size threshold, not a claim of statistical significance. A **regression** is flagged when the outcome pass rate drops by 15 points or more, the judge quality score drops by 0.5 or more, or the safety pass rate drops.

## Publishing decision

1.1.0 is promoted to `skills/distill/` and published only if all of these hold:

1. **Every agent** (Claude Code, Codex CLI, Grok CLI) meets the criteria, with or without "weak evidence".
2. **The held-out evals confirm it**: on h3 and h4 alone, the relative error reduction is at least **60%**. If the baseline leaves less than 10 points of room, the held-out result is "uninformative", and the edition is not published until a harder held-out set exists.
3. Every planned run is graded. An incomplete agent blocks publishing until its missing runs are completed.

If any fails, 1.1.0 is not promoted; 1.0.0 stays in `skills/distill/`, the cause is analyzed, and the failed confirmation run stays in the ledger.

The headline is the pooled outcome pass rate difference with its 95% CI and p, shown with the per-agent table and the per-set table. Agents are not ranked against each other. 1.0.0's numbers (iteration-6) may be shown beside 1.1.0's for the evals both runs share (d1, d2), as a comparison of with-skill pass rates; that comparison is not a criterion.

## Relation to the 1.0.0 rule

The criteria, metrics, thresholds and size are the same as in the 1.0.0 rule. A confirmation run always uses the first development pair (d1, d2) and the newest held-out pair, so it stays at 48 runs; other development evals (now h1, h2 under the set name `dev-web`) run in development iterations only. What differs from 1.0.0: the held-out pair is new (h3, h4), and the grader notes of the development set name the packet paths correctly (they said `_context/`; the packets use `context/`).

## Limits (stated whatever the results)

- That the rule came before the run is evidenced by commits in the private source repository, which outside readers cannot see.
- 1.1.0 was edited while looking at the development evals (d1, d2, h1, h2), so its development-eval numbers are optimistic. The held-out evals were written after 1.1.0 was frozen and were never used to choose or edit it; apart from the stopped attempt above, they had not been run.
- The held-out evals were written by the same agent that edited the skill. Codex and Grok reviewed them independently before this rule was fixed; both reports are kept.
- with_skill runs are told to read `SKILL.md`, so this benchmark does not measure triggering. A separate trigger test does.
- 8 vs 8 runs per agent, 4 vs 4 per agent on the held-out set. With so few runs the bootstrap CI can be narrow; when no run varies from the others in its cell, the summary says so instead of showing an interval.
- The three grader pairs differ, so judge agreement is reported per agent, and differences between agents partly reflect their graders.
