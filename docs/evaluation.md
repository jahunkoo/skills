# Evaluation

The published numbers for distill 1.1.0 are in [workspaces/distill-workspace/README.md](../workspaces/distill-workspace/README.md). This page is how a skill is evaluated and admitted, and how distill 1.1.0 was measured.

## Admitting a skill

### Quality skills

A quality skill changes the quality of the result: wording, a judgment criterion, or a way of reviewing. distill 1.1.0 is a quality skill. It is added here only when all of the following hold.

- The evals are in English. There are at least two evals, each run with the skill and without it, with two runs of each configuration.
- At least two executor agents, from different vendors, and two blind graders. No run is graded by its own vendor. This is the minimum. The distill confirmation run, a separate measurement of the frozen skill, requires all three agents.
- For each agent, the outcome pass rate is at least 0.15 higher with the skill (15 percentage points). A permutation test and Cohen's κ are reported.
- The decision rule is fixed before the confirmation run.
- The published numbers come from a confirmation run of the frozen skill, including held-out evals that were not used to edit it. Development iterations are not the published headline.

### Workflow skills

A workflow skill is a procedure: steps, order, and which tool to use. It does not take the quality eval. It carries a trigger test only. The catalog marks it `Workflow skill: no quality eval`.

## How distill 1.1.0 was measured

- With the skill and without it. A with-skill run is told to read `SKILL.md`. A without-skill run gets the same prompt without that instruction.
- Three agents, each a CLI with its model, all at reasoning effort high: Claude Code (`claude-opus-5-5`), Codex CLI (`gpt-6-sol`), Grok CLI (`grok-4.7`). Agents are not ranked against each other.
- Two blind graders from the other vendors. Claude Code runs are graded by Grok and Codex, Codex CLI runs by Claude and Grok, and Grok CLI runs by Claude and Codex. Graders do not see which arm a run is. A judged assertion passes only when both graders pass it. Programmatic assertions come from the eval set's `checks.py`.
- Two runs of each configuration. The confirmation is 48 runs: 3 agents × 4 evals (d1, d2, h3, h4) × 2 arms × 2 runs. d1 and d2 are the development pair. h3 and h4 are the held-out pair.
- The skill was developed over iterations in the maintainer's private source repository and then frozen. The published numbers come from a separate confirmation run of that frozen text (iteration-10).
- The decision rule was fixed before that run: [decision-rule-1.1.0.md](../workspaces/distill-workspace/decision-rule-1.1.0.md).

An agent meets the criteria when the outcome pass rate is at least 15 percentage points higher with the skill, the judge quality score (1-5) is not lower, and the safety pass rate (gate and scope assertions) is not lower. The 95% confidence interval and p are reported beside the result. When p ≥ 0.10 the result is marked weak evidence. That mark does not change whether the criteria are met. Meeting the criteria is an effect-size threshold, distinct from statistical significance.

Publishing also requires two further conditions. On the held-out evals alone, the relative error reduction is at least 60%: the skill removes at least 60% of the failures the baseline still makes. If the baseline leaves less than 10 percentage points of room, the held-out result is uninformative and the edition is not published. Every planned run is graded.

Metric names, the bootstrap (10,000 resamples inside each agent × eval cell), and the one-sided exact permutation test (arm labels are permuted only within each agent) are defined in [eval-harness/README.md](../eval-harness/README.md). An assertion on which the two graders agree less than 70% of the time is excluded from every pass rate and listed. κ is reported and is not the exclusion rule.

## The rule was fixed first

The decision rule was fixed before the confirmation run. The evidence for that order is a commit in the maintainer's private source repository. Readers of this repository cannot see that commit. The registered bytes and their hashes show that the published files match the rule. They do not show when the rule was written.

The bytes registered for the run, with their SHA256SUMS, are in [registered/iteration-10/](../workspaces/distill-workspace/registered/iteration-10/).

One grading file is missing seven verdicts and a judge quality score from one grader, and the published aggregate counted those as failures; the eval-harness in this repository is a later revision of the confirmation run's harness that asks again for missing verdicts, while aggregation and statistics are unchanged (details in the [workspace README](../workspaces/distill-workspace/README.md)).

## Where the numbers are

[workspaces/distill-workspace/README.md](../workspaces/distill-workspace/README.md) states the decision, the pooled headline, and the per-agent table. The rounded figures match [iteration-10/summary.md](../workspaces/distill-workspace/iteration-10/summary.md). The unrounded values are in [iteration-10/benchmark.json](../workspaces/distill-workspace/iteration-10/benchmark.json).
