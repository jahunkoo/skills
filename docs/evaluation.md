# Evaluation

The published numbers are in [workspaces/distill-workspace/README.md](../workspaces/distill-workspace/README.md) (distill 1.1.0) and [workspaces/critique-with-alternatives-workspace/README.md](../workspaces/critique-with-alternatives-workspace/README.md) (critique-with-alternatives 2.0.0). This page is how a skill is evaluated and admitted, and how each was measured.

## Admitting a skill

### Quality skills

A quality skill changes the quality of the result: wording, a judgment criterion, or a way of reviewing. distill and critique-with-alternatives are quality skills. A quality skill is added here only when all of the following hold.

- The evals are in English. Since 2026-10-13 there are at least 12 distinct cases, each run once with the skill and once without; another case says more about other requests than another run of the same case does. distill 1.1.0 was admitted under the earlier rule: at least two evals, with two runs of each configuration.
- The headline comes from programmatic checks wherever the behaviour can be checked that way (what the agent did to the repository); judged assertions are then a secondary metric. Judged assertions are graded by two graders who are not told which arm a run is. No run is graded by its own vendor.
- At least two executor agents, from different vendors. This is the minimum; both confirmation runs published here require all three agents.
- For each agent, the outcome pass rate is at least 15 percentage points higher with the skill. A decision rule may instead require the smaller of 15 points and 60% of the agent's room (1 minus its without-skill pass rate), so a baseline near the ceiling does not make the criterion unreachable; less than 10 points of room is uninformative and fails. critique-with-alternatives 2.0.0 uses this form. A permutation test and judge agreement (Cohen's κ) are reported.
- Cases that should simply be carried out (a control family), when the eval has them, pass no less often with the skill, so a skill cannot score by stopping everything.
- The decision rule is fixed before the confirmation run.
- The published numbers come from a confirmation run of the frozen skill on held-out cases that were not used to edit it. Development iterations are not the published headline.

### Workflow skills

A workflow skill is a procedure: steps, order, and which tool to use. It does not take the quality eval. It carries a trigger test only. The catalog marks it `Workflow skill: no quality eval`.

## How distill 1.1.0 was measured

- With the skill and without it. A with-skill run is told to read `SKILL.md`. A without-skill run gets the same prompt without that instruction.
- Three agents, each a CLI with its model, all at reasoning effort high: Claude Code (`claude-opus-5-5`), Codex CLI (`gpt-6-sol`), Grok CLI (`grok-4.7`). Agents are not ranked against each other.
- Two graders from the other vendors. Claude Code runs are graded by Grok and Codex, Codex CLI runs by Claude and Grok, and Grok CLI runs by Claude and Codex. Graders are not told which arm a run is, and the grading packet does not name it. The agent's answer can still reveal it: in iteration-10, 5 of 24 with-skill answers say they follow the distill skill or that the skill requires approval (0 of 24 without), and 21 of 24 end with the skill's "Deleted N … Kept N" report line (2 of 24 without). Programmatic gate and scope checks do not read the answer; judged assertions and the quality score can. How much this affected the graders was not measured. In that run the graders also worked inside the run workspace, which held the file that maps runs to arms; the published files do not show whether any grader read it. The decision rule's sentence "Graders do not see the arm" is the text frozen before the run. A judged assertion passes only when both graders pass it. Programmatic assertions come from the eval set's `checks.py`.
- Two runs of each configuration. The confirmation is 48 runs: 3 agents × 4 evals (d1, d2, h3, h4) × 2 arms × 2 runs. d1 and d2 are the development pair. h3 and h4 are the held-out pair.
- The skill was developed over iterations in the maintainer's private source repository and then frozen. The published numbers come from a separate confirmation run of that frozen text (iteration-10).
- The decision rule was fixed before that run: [decision-rule-1.1.0.md](../workspaces/distill-workspace/decision-rule-1.1.0.md).

An agent meets the criteria when the outcome pass rate is at least 15 percentage points higher with the skill, the judge quality score (1-5) is not lower, and the safety pass rate (gate and scope assertions) is not lower. The 95% confidence interval and p are reported beside the result. When p ≥ 0.10 the result is marked weak evidence. That mark does not change whether the criteria are met. Meeting the criteria is an effect-size threshold, distinct from statistical significance.

Publishing also requires two further conditions. On the held-out evals alone, the relative error reduction is at least 60%: the skill removes at least 60% of the failures the baseline still makes. If the baseline leaves less than 10 percentage points of room, the held-out result is uninformative and the edition is not published. Every planned run has an executor result and programmatic checks and enters the aggregate ("graded" in the tables). That does not mean both graders returned every verdict; see the workspace README.

Metric names, the bootstrap (10,000 resamples inside each agent × eval cell), and the one-sided exact permutation test (arm labels are permuted only within each agent) are defined in [eval-harness/README.md](../eval-harness/README.md). An assertion on which the two graders agree less than 70% of the time is excluded from every pass rate and listed. κ is reported and is not the exclusion rule.

## How critique-with-alternatives 2.0.0 was measured

The design follows the evaluation pipeline in Chip Huyen's *AI Engineering* (O'Reilly, 2025), chapter 4, as set out in [eval-harness/README.md](../eval-harness/README.md) ("Designing an eval"): evaluate each part of the skill, decide what a good and a bad result is before measuring, and check the evaluation itself.

- Twelve held-out cases in three families: review 6 (a change spelled out as a command, with a request for a review or an opinion), repair 3 (an easy-to-undo change whose literal version breaks something the repository shows matters) and control 3 (sound requests). Each case is a small repository built from a case definition, and each family has a programmatic check: no change for review, the goal reached with the breakage avoided for repair, the change made for control.
- The headline is the share of the nine review and repair cases whose check passes. Control cases must not pass less often with the skill. The review cases' judged verdict and the quality score (1-5) are secondary; the quality score fails an agent only when it drops by 0.5 or more.
- Three agents, the same as for distill, each with and without the skill, one run per case and arm: 72 runs. Two graders from the other vendors grade the 36 review runs.
- The held-out composition was chosen by family from without-skill pilots on twelve development cases: a pressure family (a harmful step that is hard to undo, with the user pushing) had no room for any agent and was left out. The held-out cases were written by an agent that read neither the skill nor any result.
- p is a one-sided exact sign-flip test on each case's difference, stratified by agent; the 95% interval is a bootstrap over cases within each agent.
- The run went in stages that could only stop it, never favour publishing: Grok CLI's baseline first (stop if its room was under 10 points), then the rest, then grading only after the programmatic criteria held.
- The decision rule: [decision-rule-2.0.0.md](../workspaces/critique-with-alternatives-workspace/decision-rule-2.0.0.md). The registered bytes: [registered/iteration-6/](../workspaces/critique-with-alternatives-workspace/registered/iteration-6/README.md).

## The rule was fixed first

For each skill, the decision rule was fixed before the confirmation run. The evidence for that order is a commit in the maintainer's private source repository. Readers of this repository cannot see that commit. The registered bytes and their hashes show that the published files match the rule. They do not show when the rule was written.

The bytes registered for each run, with their SHA256SUMS, are in [registered/iteration-10/](../workspaces/distill-workspace/registered/iteration-10/) (distill) and [registered/iteration-6/](../workspaces/critique-with-alternatives-workspace/registered/iteration-6/README.md) (critique-with-alternatives).

For distill, one grading file is missing seven verdicts and a judge quality score from one grader, and the published aggregate counted those as failures; the eval-harness in this repository is a later revision of the confirmation run's harness: it asks a grader again for missing verdicts, runs graders outside the run workspace, and refuses to aggregate a confirmation run with incomplete grades unless `--allow-incomplete` is passed. The statistics are unchanged (details in the [workspace README](../workspaces/distill-workspace/README.md)).

## Where the numbers are

Each workspace README states the decision, the pooled headline, and the per-agent table: [distill](../workspaces/distill-workspace/README.md) and [critique-with-alternatives](../workspaces/critique-with-alternatives-workspace/README.md). The rounded figures match each confirmation run's `summary.md` ([iteration-10](../workspaces/distill-workspace/iteration-10/summary.md), [iteration-6](../workspaces/critique-with-alternatives-workspace/iteration-6/summary.md)); the unrounded values are in its `benchmark.json`.
