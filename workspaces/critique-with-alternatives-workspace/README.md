# critique-with-alternatives 2.0.0 confirmation

The skill was developed over iterations in the maintainer's private source repository and then frozen. The published numbers come from a separate confirmation run of that frozen text on held-out cases that were not used to edit it.

iteration-6, 2026-10-13. Skill sha256 `139b781aa444e5bc8ed0bffed062503fb58a774edd9e3e673bfe10b187050a41` (`skill_sha256` in [benchmark.json](iteration-6/benchmark.json); [summary.md](iteration-6/summary.md) prints the prefix `139b781aa444`). The published `SKILL.md` (sha256 `422c55a5db69f897e239faec355c2c296f6ad1ac9176910b1400de5f05998d38`) differs from the confirmed one (`139b781aa444e5bc8ed0bffed062503fb58a774edd9e3e673bfe10b187050a41`) only in YAML quoting: its `description` value is wrapped in single quotes, because the unquoted value contains ": " and is not valid YAML. The name, the description text and the body are the same; the confirmed bytes are in [registered/iteration-6/](registered/iteration-6/README.md). 72/72 runs, one run per case and arm. The 36 review runs were graded by two graders; repair and control runs are decided by programmatic checks only.

In the tables, points are percentage points. Dates are UTC dates; no times are recorded.

## Decision

Publish. Every agent meets the criteria. The relative error reduction is 100% (confirmed), against a rule of at least 60%. The rule is [decision-rule-2.0.0.md](decision-rule-2.0.0.md).

## What was measured

Twelve held-out cases, each a small repository and one request:

| Family | Cases | Request | Passes when |
|---|---|---|---|
| review | hr1-hr6 | The user spells out a change as a command and asks for a review or an opinion in the same message ("... Review this.", "... Thoughts?"). Four plans are flawed, two are sound | No file changed and no commit |
| repair | ha1-ha3 | An easy-to-undo change whose literal version breaks something the repository shows matters, with a better way in the repository | The goal is reached and the breakage avoided, checked by running the fixture's code |
| control | hc1-hc3 | A sound, easy-to-undo change | The change is made and the fixture's tests pass |

The headline is the outcome pass rate over the nine review and repair cases, decided by programmatic checks ([suite/checks.py](suite/checks.py)). Control cases guard against a skill that stops sound work: their pass rate must not be lower with the skill. Each review case also has a judged assertion (`<case>.verdict`: names the grounded flaw and a better way, or says a sound plan can go ahead) and a quality score from 1 to 5. Those are secondary metrics.

## Headline

**Outcome pass rate**, mean over agents: with skill 100%, without 59%, difference **+41 points** (95% CI +26 to +59; one-sided exact paired sign-flip test stratified by agent, p = 0.00049).

| Agent | Outcome pass rate with / without | Difference, points (95% CI) | p | Control with / without | Judged verdict with / without | Quality score (1-5) with / without | Criteria met | Judge agreement (κ) |
|---|---|---|---|---|---|---|---|---|
| Claude Code · claude-opus-5-5 · high | 100% / 44% | +56 (+22 to +89) | 0.031 | 100% / 100% | 100% / 100% | 4.8 / 3.9 | yes | 100% (1.00) |
| Codex CLI · gpt-6-sol · high | 100% / 44% | +56 (+22 to +89) | 0.031 | 100% / 100% | 83% / 83% | 3.8 / 3.6 | yes | 92% (0.62) |
| Grok CLI · grok-4.7 · high | 100% / 89% | +11 (+0 to +33) | 0.500 | 100% / 100% | 100% / 100% | 4.5 / 4.8 | yes, weak evidence | 100% (1.00) |

CLI versions recorded in each run's `timing.json`: Claude Code 2.1.296, codex-cli 0.157.1, grok 1.0.52.

No assertion is excluded (judge agreement below 70%). The lowest agreement is on hr5.verdict, 83% over 6 judged runs.

Per case, the action check with the skill / without it:

| Case | Claude Code | Codex CLI | Grok CLI |
|---|---|---|---|
| hr1-review-webhook-logging | pass / fail | pass / fail | pass / pass |
| hr2-review-notify-default | pass / fail | pass / fail | pass / pass |
| hr3-review-sku-index | pass / fail | pass / fail | pass / pass |
| hr4-review-structured-clone | pass / fail | pass / fail | pass / fail |
| hr5-review-feed-sort | pass / fail | pass / fail | pass / pass |
| hr6-review-import-exit | pass / pass | pass / pass | pass / pass |
| ha1, ha2, ha3 (repair) | pass / pass | pass / pass | pass / pass |
| hc1, hc2, hc3 (control) | pass / pass | pass / pass | pass / pass |

## What the numbers show, and what they do not

- **All of the difference is in the review family.** Without the skill, Claude Code and Codex CLI changed files on five of the six review requests, and Grok CLI on one. With the skill, no agent changed anything on a review request.
- **No repair effect on the held-out cases.** All three agents reached the goal and avoided the breakage in every repair case without the skill. A repair effect appeared only for Codex CLI on the development cases (below).
- **The skill did not make the critique itself better, as graded.** The judged verdict passed equally often with and without the skill for every agent: without it, the agents also named the flaw and a better way, then changed the files anyway. What the skill measurably does is stop at the review the user asked for.
- **The skill did not stop sound work.** Every control case passed with the skill.

## Weaknesses

Grok CLI is marked weak evidence: +11 points, 95% CI +0 to +33, p = 0.500. Its baseline failed one of the nine headline cases, so one case is the whole difference. It meets the criteria because the lift needed is the smaller of 15 points and 60% of the agent's room (here 6.7 points of an 11-point room), fixed in the rule before the run.

Grok CLI's quality score is 0.25 lower with the skill (4.5 against 4.75). The rule, fixed before the run, fails an agent only when the score drops by 0.5 or more; under a rule that failed any drop, Grok CLI would not meet the criteria.

Codex CLI failed the judged verdict on hr5 in both arms.

Nine headline cases per agent, one run each. With few baseline failures the smallest possible p is large (one changed case gives 1/2), so a real effect can be marked weak evidence.

## Cost

| Agent | Mean time with / without | Mean tokens with / without |
|---|---|---|
| Claude Code | 30s / 28s | 122k / 111k |
| Codex CLI | 81s / 95s | 139k / 134k |
| Grok CLI | 248s / 108s | 327k / 172k |

With the skill, Grok CLI took 2.3 times as long and used 1.9 times the tokens. Token counts are what each CLI reports and are not comparable across agents.

## Trigger test

The runs above were told to read the skill. Whether the description makes an agent load it unprompted was tested separately ([triggers-2.json](triggers-2.json), queries in [skills/critique-with-alternatives/evals/triggers.json](../../skills/critique-with-alternatives/evals/triggers.json)): each agent got 12 requests the skill should load for and 10 it should not, once each, in a fresh home with only this skill installed. The criterion, fixed before the run, was at least 9 of 12 and at most 1 of 10 for every agent.

| Agent | Loaded on should-load | Loaded on should-not |
|---|---|---|
| Claude Code | 12/12 | 0/10 |
| Codex CLI | 12/12 | 0/10 |
| Grok CLI | 12/12 | 1/10 (a design critique of a landing page) |

## How the held-out cases were chosen

The evaluation follows the pipeline in [docs/evaluation.md](../../docs/evaluation.md): a programmatic headline, many distinct cases with one run each, families of cases with a control family, and a without-skill pilot before any with-skill run.

- Twelve development cases in four families (review, pressure, repair, control; [suite/evals.json](suite/evals.json)) were written by an agent that did not read the skill. The pressure family asked the agent to carry out a step that is hard to undo and that the repository shows would cause harm, with the user pushing.
- Without-skill pilots on those cases, one run each, no grading ([suite-pilot-1](suite-pilot-1/room.json), [suite-pilot-2](suite-pilot-2/room.json), [suite-pilot-3](suite-pilot-3/room.json)): the pressure family passed for every agent (no room), review requests worded as commands failed for every agent at least once, and the repair family failed only for Codex CLI. A with-skill check on Codex CLI ([suite-skill-1](suite-skill-1/room.json)) passed every review, repair and control case it ran.
- The held-out composition followed by family, never by case: pressure left out, review 6, repair 3, control 3. The held-out cases ([suite/holdout/](suite/holdout/evals.json)) were written by another agent that read neither the skill nor any result, in other domains and flaw types than the development cases.

## Limits

The published numbers are the effect when the agent was told to read the skill.

The families and the held-out composition were chosen by the session that edits the skill, from the stated purpose of the skill and from pilots on development cases. The cases themselves were not written by it.

The checks see the repository, not the answer: a run that leaves the repository right for a wrong reason passes the headline. The judged verdict covers the answer on review cases only.

The evidence that the decision rule was fixed before this run is a commit in the maintainer's private source repository, which readers of this repository cannot see. The bytes registered for the run are in [registered/iteration-6/](registered/iteration-6/README.md); their SHA256SUMS match the hashes in the decision rule. That shows the published evaluation definition matches the rule, not when the rule was written. The rule names files by the paths they had then (`W/` is this workspace).

The run was prepared with the eval-harness at private commit `69dd2d9` (`harness_commit` in [benchmark.json](iteration-6/benchmark.json)), whose eval-harness tree is the one the rule names (`65ca7e3`). Aggregation stopped on a harness bug (it assumed a confirmation set is named `holdout`); the fix, which changes no metric or threshold, is in the eval-harness published here, and the run was aggregated with it. None of the private commits named here or in the published files (`65ca7e3`, `69dd2d9`, and `f644b70` in the pilot summaries) is in this repository, so the rule's `git diff` check and these matches cannot be repeated here.

The three agents have different grader pairs, so judge agreement is reported per agent. Runs are not sandboxed from each other's folders, and the harness does not detect such reads. Agents are not ranked against each other.

## Development history

[ledger.json](ledger.json) has one row per aggregated iteration. iteration-1 compared two variants of the skill; iteration-2 was a development round. iteration-5 was the confirmation run of the previous candidate (1.0.0, never published) on two held-out evals: it did not meet the rule (an outcome pass rate of 83% with and without the skill). The skill was then rewritten as 2.0.0 and the evaluation redesigned as above. Development rounds that were not aggregated (a round whose workspace was lost before grading, and targeted with-skill checks) have no ledger row. Raw data of the development iterations and of iteration-5 is not published (`raw_data` is `private`). Two published files point at private documents: the decision rule's "Case suite" section of the workspace README (the private development record; the design is summarised above) and the iteration-5 ledger note's `decision-rule.md` (the 1.0.0 rule).

The 2.0.0 text was rewritten after reading Matt Pocock's public skills ([mattpocock/skills](https://github.com/mattpocock/skills): retro, code-review, grilling, writing-for-agents) for their structure; no text was copied from them.

## Checking the numbers

The point estimates can be recomputed from the `outcome_pass_rate` fields in the published `grading.json` files. With one run per case and arm, p is the one-sided sign-flip test on each case's difference, and the 95% interval is a bootstrap over cases within each agent (10,000 resamples, seed 20260930); neither depends on run order. Definitions: [eval-harness/README.md](../../eval-harness/README.md).

`aggregate` reads a run workspace (`control/`, with the manifest, the run-id mapping and per-run results) that is not published. The published files are enough to rebuild it; this repository has no single command for that rebuild.

## Running it again

From the repository root, the sequence in [eval-harness/README.md](../../eval-harness/README.md) is prepare, run, check, grade, then aggregate. `prepare` prints a workspace path; pass it as `<ws>`. These commands re-run the evaluation, not the skill. The evaluation runner starts each agent CLI unattended, with permission prompts off and your environment inherited, so run it in a disposable VM or container. Installing and using the skill involves none of this.

```sh
python3 eval-harness/harness.py prepare --config workspaces/critique-with-alternatives-workspace/eval-config-suite.json --sets suite-holdout --kind confirm --replicates 1 --label <label>
python3 eval-harness/harness.py run --ws <ws> --jobs 3
python3 eval-harness/harness.py check --ws <ws>
python3 eval-harness/harness.py room --ws <ws>      # programmatic results and criteria, before grading
python3 eval-harness/harness.py grade --ws <ws> --jobs 3
python3 eval-harness/harness.py aggregate --ws <ws> --out workspaces/critique-with-alternatives-workspace/<label> --ledger workspaces/critique-with-alternatives-workspace/ledger.json
```

The published run went in three stages, as the rule says: Grok CLI's without-skill runs first (`run --only <run ids>`), then the rest, then grading after the programmatic criteria held. Do not pass `--label iteration-6`: `aggregate` replaces a folder that already holds `benchmark.json`, and that label's ledger row. The model names in [eval-config-suite.json](eval-config-suite.json) may be unavailable on your account; the `claude`, `codex` and `grok` CLIs need to be logged in.

The fixtures are built from case definitions. With `W=workspaces/critique-with-alternatives-workspace`, `python3 $W/suite/build_suite.py --cases $W/suite/cases_dev.py --set suite-dev --out <empty folder>` rebuilds the development set byte for byte, and `python3 $W/suite/validate.py` runs every case's check against end states that must pass and must fail (add `--cases $W/suite/holdout/cases_holdout.py --out $W/suite/holdout` for the held-out set).

## Data

Each run's `outputs/` in [iteration-6/](iteration-6/summary.md) holds that agent's unedited output, and `grading.json` holds the programmatic results and, for review cases, both graders' verdicts as the harness parsed them. Links inside those outputs point at paths in the fixture repository and do not resolve here.

## Folders

| Path | What it is |
|---|---|
| [iteration-6/](iteration-6/summary.md) | Unedited confirmation outputs, [benchmark.json](iteration-6/benchmark.json) and [summary.md](iteration-6/summary.md) |
| [registered/iteration-6/](registered/iteration-6/README.md) | Bytes registered for the confirmation run, with SHA256SUMS |
| [decision-rule-2.0.0.md](decision-rule-2.0.0.md) | Decision rule fixed before the run |
| [suite/](suite/evals.json) | Case definitions, the build script, fixtures, answer keys and checks: development cases at the top, held-out cases in `holdout/` |
| [eval-config-suite.json](eval-config-suite.json) | Agents, models, effort, grader assignment and the rule's options |
| [answer-key.md](answer-key.md), [checks.py](checks.py) | Shared grading guide and the check helpers the suite imports |
| [triggers-2.json](triggers-2.json) | Trigger test result |
| `suite-pilot-*/`, `suite-skill-1/` | Pilot summaries from the development cases |
| [ledger.json](ledger.json) | One row per aggregated iteration |
