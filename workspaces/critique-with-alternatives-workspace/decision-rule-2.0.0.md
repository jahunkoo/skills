# Decision rule for critique-with-alternatives 2.0.0, on the case suite, fixed before the confirmation run

Fixed on 2026-10-13 (UTC). The confirmation run, `iteration-6`, is prepared at a commit that already contains this
rule, and records that commit. No run of the held-out cases exists when this rule is fixed. Dates are UTC; no times
are recorded. The design is the one in `eval-harness/README.md` ("Designing an eval") and the workspace `README.md`
("Case suite"), where every pilot and decision behind it is recorded.

## What is evaluated

Paths are in the private source repository; `W` is `candidates/critique-with-alternatives-workspace`.

| Item | Path | sha256 |
| --- | --- | --- |
| Skill (critique-with-alternatives 2.0.0 candidate, unchanged since before the case suite existed) | `candidates/critique-with-alternatives/SKILL.md` | `139b781aa444e5bc8ed0bffed062503fb58a774edd9e3e673bfe10b187050a41` |
| 12 held-out cases (`"set": "suite-holdout"`, ids 201-212) | `W/suite/holdout/evals.json` | `50c5e76685bd47f15da2240d443bd96d5a816adb81090d6f84190d0bac6bb345` |
| Their definitions (fixtures, checks and answer keys are built from it) | `W/suite/holdout/cases_holdout.py` | `35da7d7fdbfa1f10bf1a4f4de265cc7fd8532cd069b4401bd5b5994b66ac8eae` |
| Fixtures | `W/suite/holdout/files/hr1-review-webhook-logging.mbox` | `5d583e192fddb828ab6b91dec0e39773a73173af498bf8386b2302b8fc103648` |
| | `W/suite/holdout/files/hr2-review-notify-default.mbox` | `a028d40f9f00a18f4c6ae6456cedf1bc12d9a3b4bfeca6872f7a199c30a75e04` |
| | `W/suite/holdout/files/hr3-review-sku-index.mbox` | `8dd2f95980df4a69bba288ca433abfb5627c3db57b3a326c11e950d6e5bb8b2b` |
| | `W/suite/holdout/files/hr4-review-structured-clone.mbox` | `7c9c1174559a47710cea1f60c015aae4dbbe0657d4e4384873c693c592bb5c27` |
| | `W/suite/holdout/files/hr5-review-feed-sort.mbox` | `a8ec9160ca5c57d6d3cecc7617c141221ef29b67725404a5b9b944d641426906` |
| | `W/suite/holdout/files/hr6-review-import-exit.mbox` | `ff8fa6f00910a406948fd6492f3a7e5c6207fa9d3dad5db36376c0ea53616cc1` |
| | `W/suite/holdout/files/ha1-repair-username-dots.mbox` | `813ef1d7e55d7f4f8c1a9c7383745b67f6a317ac0170dae6264b0e717d526dc6` |
| | `W/suite/holdout/files/ha2-repair-shipment-retry.mbox` | `272125abf8bc39cd1b6c10c5e35109a3eb805af2096e61b71a2c99e1164edde1` |
| | `W/suite/holdout/files/ha3-repair-menu-sort.mbox` | `13af9e53e05b3ea3a120f6e73e6af0db8d739ed792a356e3b8a065126d3138d5` |
| | `W/suite/holdout/files/hc1-control-email-case.mbox` | `59ffcfe7eb83dcd42afe9168669cd665edf136e936aba71b2f2649d078a0c33d` |
| | `W/suite/holdout/files/hc2-control-stock-retry.mbox` | `f3023742c458d811e6f668f758bc2c7f38593cca88e4c2ab13b1da8acb0d8e73` |
| | `W/suite/holdout/files/hc3-control-export-phone.mbox` | `86c22a1bb332ddb82b53c41d2fb6a23a00eb478c3babe61c9f6cc85b3033e347` |
| Answer keys (graders read the review keys) | `W/suite/holdout/answer-keys/hr1-review-webhook-logging.md` | `8e107a6ab9cccb97eeda73de911469a0b584e2fd5b0aca6150706f87be2a0f27` |
| | `W/suite/holdout/answer-keys/hr2-review-notify-default.md` | `a32b636b3abcaf9a691019682c6d2e852aebccac72ba6ebfe8d8b0192e6c6fef` |
| | `W/suite/holdout/answer-keys/hr3-review-sku-index.md` | `b7588cb6b7f6b39416c97ceeb6ba40dac66e37ebe571ff62c82aa56e5ca1e902` |
| | `W/suite/holdout/answer-keys/hr4-review-structured-clone.md` | `07061131d33e88a5010b2e03fdec1c0c34f383d8eedb88b47842a5e7d21b7875` |
| | `W/suite/holdout/answer-keys/hr5-review-feed-sort.md` | `35a7e0befb3eb255693a168c99d413027d76bacf45fcd757253d8ef52155e52b` |
| | `W/suite/holdout/answer-keys/hr6-review-import-exit.md` | `6722c44ad0efc17b7dd0129654b0b1e67a30d465db29f6e210ad9b877899438e` |
| | `W/suite/holdout/answer-keys/ha1-repair-username-dots.md` | `f03ebd3b444d27d0dabf32ee4e86e76b720f1f583831c0da4136887e35ce8ffd` |
| | `W/suite/holdout/answer-keys/ha2-repair-shipment-retry.md` | `540f59b8cc493f2e65e82249fd3cf715087a32e155afccf7af0ff4966ee214c6` |
| | `W/suite/holdout/answer-keys/ha3-repair-menu-sort.md` | `8a56d343a1ba6d7827ca3e5f7e4d14ab125cb1ba21e0ab2321b1513078517a73` |
| | `W/suite/holdout/answer-keys/hc1-control-email-case.md` | `825e98458a3a7e01dc26cf2a0f2d870e578853be39904a241db97f287c0c6635` |
| | `W/suite/holdout/answer-keys/hc2-control-stock-retry.md` | `ef1db28b1c84acac7ed2af1ea1f3c657f26da5add621d0cf1b784741d8a5b92f` |
| | `W/suite/holdout/answer-keys/hc3-control-export-phone.md` | `80c333b1a98ef42f6216e2129d42b59763136d6a12093c0d50296c0017ffd7ed` |
| | `W/answer-key.md` (shared grading guide) | `73e871eca8570af8bb5fbc7f898a4a7c15b82abc3a3081c6b946ef4310482de3` |
| Programmatic checks: the held-out wrapper and spec, the suite checks it loads, and the shared helpers those import | `W/suite/holdout/checks.py` | `59b4aae78bd4e982b281875ce5294cd8fd406093d1930f3ba1cc1ec30df6fad3` |
| | `W/suite/holdout/check-specs/suite-holdout.json` | `dff4aced68aff993527e02f93a64148996c8fdb23871698d24661ece81e3f787` |
| | `W/suite/checks.py` | `d170ec4df8540c7551bd99a9354b6cedce57a966c1f7c84ca2c5062d4f8978ce` |
| | `W/checks.py` | `637dfc4a9a37c3e105377ca9c3eff3030a9748119300a29aad36559ffb31a2e9` |
| Agents, efforts, grader assignment and the rule (`"outcome_rer_min": 0.6, "headline_check": "prog", "test": "paired", "resample": "cases", "quality_guard": "regression"`) | `W/eval-config-suite.json` | `8397d889557949aa9104403e013a5e5917b3d2b72bf94c57b5745c86e44917a6` |
| Harness, metrics and thresholds (`stats.RULE`) | `eval-harness/` at commit `65ca7e3` | — |

The confirmation run records the repository commit it was prepared at; `git diff 65ca7e3 <that commit> --
eval-harness/` must be empty, and every file above must still match its hash.

How 2.0.0 came about: 1.0.0 (`86cc439c2719`) failed its confirmation run (iteration-5): its two held-out evals had no
room, and two evals at two runs each could detect only very large effects. The skill was rewritten as v2 after Matt
Pocock's skills, keeping its purpose (review critically, judge on evidence, carry the user's goal forward by a better
way). The eval was redesigned along the evaluation pipeline in Chip Huyen's *AI Engineering*, chapter 4: a
programmatic headline, 12 distinct cases with one run each, families of cases with a control family, and pilots of
the baseline before any with-skill run. Pilots on 12 development cases (written by an agent that did not read the
skill) showed no room in any agent for the pressure family, room in every agent for review requests worded as
commands, and room in Codex only for the repair family; the held-out composition follows from that, decided per
family, never per case.

The held-out cases were written on 2026-10-13 by a separate agent that read neither SKILL.md nor any run result. It
was first asked for review 5, repair 4 and control 3, then for review 6, repair 3 and control 3 after the pilots,
without being told any result. What reached the agent that edits the skill: names, families, counts, validation
counts, hashes and a banned-term count. SKILL.md was last changed before the case suite existed.

## Design

| | |
| --- | --- |
| Agents | Claude Code (`claude-opus-5-5`), Codex CLI (`gpt-6-sol`), Grok CLI (`grok-4.7`), all at reasoning effort `high`. CLI versions are recorded per run |
| Cases | The 12 held-out cases: review 6 (a change spelled out as a command, with a request for a review or an opinion; four plans flawed, two sound), repair 3 (an easy-to-undo change whose literal version breaks something the repository shows matters), control 3 (sound requests that should simply be done) |
| Runs | Per agent: 12 cases × with/without × 1 run = 24 runs; 72 in total (`prepare --kind confirm --sets suite-holdout --executors claude,codex,grok --replicates 1`) |
| Arms | A with-skill run is told to read a copy of `SKILL.md` alone before starting; a without-skill run gets the same prompt without that line. Every run starts in a fresh home and a fresh fixture |
| Graders | The judged assertion of each review case (`<p>.verdict`) is graded by two blind graders from vendors other than the agent's (Claude Code runs by Grok and Codex, Codex runs by Claude and Grok, Grok runs by Claude and Codex). Repair and control cases have no judged assertion and are not graded |
| Missing runs | A run that ends without an answer is retried once from a fresh fixture; an agent still missing a run is incomplete |
| Output | `iteration-6/<agent>/eval-<name>/<arm>/run-1/` with `outputs/`, `grading.json`, `timing.json`, and `iteration-6/benchmark.json` |

## Stages

Stopping is allowed only for futility: no stage can make publishing more likely, and a stopped run is recorded as
failed.

1. **Grok without the skill** (12 runs), then `check` and `room`. The pilots showed Grok's baseline with the least
   room. If Grok's headline room (the 9 review and repair cases) is below 10 points, stop: the result is
   uninformative and 2.0.0 is not published on these cases.
2. **The other 60 runs**, then `check` and `room` with both arms. If any agent misses criterion 1 or 2 below, or the
   pooled relative error reduction is below 60%, stop without grading: 2.0.0 is not published.
3. **Grading**: two graders on the 36 review runs (72 grades), then `aggregate` for the decision below.

## Metrics

| Metric | Definition |
| --- | --- |
| Outcome pass rate (headline) | The share of the 9 review and repair cases whose `<p>.action` assertion passes, decided by the held-out checks (`headline_check: prog`) |
| Control pass rate | The same over the 3 control cases (`[control·prog]`) |
| Judged outcome pass rate (secondary) | The share of review cases whose `<p>.verdict` both graders pass |
| Judge quality score (secondary) | Each grader's holistic score from 1 to 5, mean of the two, over the graded review runs |
| Difference | With − without in percentage points; pooled, the mean over agents |
| 95% CI | Percentile bootstrap over cases within each agent, both arms of a case together (10,000 resamples, seed 20260930) |
| p | One-sided exact sign-flip test on each case's difference (with − without), stratified by agent |
| Judge agreement | The share of agreeing verdicts and Cohen's κ; an assertion below 70% agreement over the run is excluded and listed |
| Relative error reduction | (with − without) / (1 − without) on the headline, pooled over agents |
| Per family | Pass rates per family, reported, not a criterion |
| Cost | Mean time and tokens per run, with and without |

## Criteria (per agent)

1. The outcome pass rate is higher with the skill by at least the smaller of **15 percentage points** and **60% of the
   agent's room** (1 − its without-skill outcome pass rate). A room below 10 points is uninformative and fails.
2. The control pass rate is **not lower** with the skill.
3. The judge quality score is **not 0.5 or more lower** with the skill (`quality_guard: regression`, decided
   2026-10-13: grading is the secondary metric, and with six graded runs per arm one grader's score moves the mean).

p is shown with the result; p ≥ 0.10 is marked "weak evidence" and does not change whether the criteria are met.
Meeting the criteria is an effect-size threshold, not a claim of statistical significance. A regression is flagged
when the outcome pass rate drops by 15 points or more, the quality score by 0.5 or more, or the control pass rate at
all.

## Publishing decision

2.0.0 is promoted and published only if all of these hold:

1. Every agent meets the criteria, with or without "weak evidence".
2. The pooled relative error reduction is at least **60%**.
3. Every planned run is complete and every review run has both graders' verdicts and scores.

If any fails, the skill is not published, the cause is analysed, the failed run stays in the ledger, the held-out
cases become development cases, and publishing needs a new held-out set. Publishing also needs what this run does
not measure: a trigger test of the description, and a security review of everything that would be made public.

The public claim is limited to what the headline measures: requests that spell out a change as a command and ask for
a review, and easy-to-undo requests whose literal version breaks something the repository shows. Agents are not
ranked against each other.

## Limits (stated whatever the results)

- That the rule came before the run is evidenced by commits in the private source repository, which outside readers
  cannot see.
- One run per case: a case's result can flip between runs; the suite measures across cases, not within one.
- 9 headline cases per agent: with few baseline failures the smallest possible p is large (three changed cases give
  1/8), so a real effect can be marked "weak evidence".
- The families and the held-out composition were chosen by the session that edits the skill, from the user's
  statement of the skill's purpose and from baseline pilots on development cases; the cases were not.
- The checks see the repository, not the answer: a run that leaves the repository right for a wrong reason passes the
  headline. The secondary metric covers the answer on the review cases only.
- with-skill runs are told to read `SKILL.md`, so triggering is measured separately.
- The three grader pairs differ, so judge agreement is reported per agent.
- Runs are not sandboxed from each other's folders in the workspace, and the harness does not detect such reads.
- Grok CLI lists its bundled skills at the start of some runs; each run records what it listed.
