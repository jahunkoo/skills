# eval-harness

Measures whether a skill changes what an agent actually does. Each eval runs with and without the skill on several
agent CLIs, and graders from other vendors, who are not told which arm a run is, judge the results. Python 3 standard library only.

## Requirements

- The agent CLIs you run: `claude` (Claude Code), `codex` (Codex CLI), `grok` (Grok CLI), each logged in.
- Isolated Claude Code runs need a long-lived subscription token from `claude setup-token`, in
  `$CLAUDE_CODE_OAUTH_TOKEN` or the macOS keychain item `claude-eval-oauth`. It is not an API key.
  Tokens of further accounts go in `claude-eval-oauth-2`, `claude-eval-oauth-3`, ... (up to 9) and are used in that
  order: a run that stops at a usage limit before any tool call runs again with the next token, and the harness
  skips that token for the rest of the command. Each result records the slot it used (`auth_slot`), never the token.
  Without any token, pass `--claude-login` to use the normal login; those runs are recorded as `isolation: none`.
- Codex runs use the login in `$CODEX_HOME` when it is set (an account manager may point it at another account),
  else `~/.codex`.

## Isolation

- Every run gets a fresh temporary `HOME`. User-level settings, memory files, hooks and skills do not load.
  Only the CLI's credential file is linked in (codex, grok) or passed as a token (claude).
- Claude Code runs with `--disable-slash-commands`; Grok with `GROK_*_SKILLS_ENABLED=false`. Each run records the
  skills its CLI reported (`skills_seen`).
- A with-skill run is told to read a copy of `SKILL.md` alone; the copy has no `evals/`. The agents are not sandboxed to
  that copy or to the fixture: a run can reach other runs' folders in the same workspace, and the harness does not
  detect such reads.
- Graders work in a temporary folder outside the run workspace that holds only the grading packet. They still read
  the agent's answer, which can reveal the arm.
- Claude Code and Grok run with permission prompts off (`bypassPermissions`, `--always-approve`) and inherit the
  environment. Codex runs in its `workspace-write` sandbox with the fixture's `.git` added as a writable root, so it
  can commit as the other CLIs can (by default that sandbox keeps `.git` read-only). Run the harness in a disposable
  VM or container.
- Fixtures are git repositories replayed from a mbox with their original dates, so SHAs and `git blame` are stable.

## Usage

```sh
H=eval-harness/harness.py
python3 $H prepare --config <skill-workspace>/eval-config.json --sets dev --label iteration-6   # prints the workspace path (~/.cache/eval-harness/...)
python3 $H run       --ws <ws> --jobs 3
python3 $H check     --ws <ws>          # programmatic assertions and grader packets without the arm
python3 $H grade     --ws <ws> --jobs 3 # two graders per run, assigned in eval-config.json
python3 $H aggregate --ws <ws> --out <skill-workspace>/iteration-6 --ledger <skill-workspace>/ledger.json
python3 $H status    --ws <ws>
python3 $H room      --ws <ws> [--ws <ws2>] [--out FILE]  # room per family from programmatic results; works with one arm;
                                       # two workspaces (a pilot and a with-skill check) give a paired comparison
python3 -m unittest discover -s eval-harness/tests
```

For a targeted check after a SKILL.md change, `prepare --evals <names> --executors <agents> --arms with_skill
--replicates 1` makes only the runs that change touches; read their programmatic results after `check`. Such a
workspace has one arm and cannot be aggregated: compare it with the without-skill runs of the last full iteration,
which a SKILL.md change does not affect.

`eval-config.json` names the skill folder, the eval sets (`dev`, `holdout`), each agent's CLI, model and reasoning
effort, and which graders judge which agent. By default no run is graded by its own vendor. An agent is a CLI with
its model; results are reported per agent and pooled, never ranked across agents.

`grade` asks a grader again when a reply leaves out a verdict, gives one that is not true or false, or has no
holistic score. A confirmation aggregate (`prepare --kind confirm`) stops while any grade is still incomplete:
run `grade` again, or pass `--allow-incomplete` to count the missing verdicts as failures.

## Designing an eval (decided 2026-10-13)

The design follows the evaluation pipeline of Chip Huyen, *AI Engineering* (O'Reilly, 2025), chapter 4: evaluate
each component, write down what a good and a bad result is, then choose methods and data and evaluate the pipeline
itself. What earlier rounds taught: two evals at two runs each detected only very large effects, and evals that were
written, run and graded before anyone checked the baseline turned out to have no room.

- **Components.** A skill is measured in parts: whether it loads (`triggers.py`), what the agent does to the
  repository (programmatic checks), and what it says (graders). A public claim names the part it rests on.
- **Programmatic headline.** With `"rule": {"headline_check": "prog"}` the outcome pass rate counts programmatic
  outcome assertions only. Judged outcome assertions are a secondary metric (`judge_outcome_pass_rate`), graded by
  two blind graders with judge agreement, on the cases that need them: an eval with no judge assertion is not
  graded and has no quality score. `room` on a workspace with both arms reports the programmatic part of the criteria
  and the pooled relative error reduction, so a staged confirmation can grade only after the programmatic criteria hold.
- **Cases over replicates.** At least 12 distinct cases × with/without × 1 run per agent. Another run of the same case
  says little about other requests; another case does. Rule `"test": "paired"` compares each case's two arms with an
  exact sign-flip test, stratified by agent, and `"resample": "cases"` bootstraps over cases. The chance of detecting
  a real difference at p < 0.05 (one-sided, per agent, from the pass rates of the two arms):

  | Without skill | With skill | 4 cases | 8 | 12 | 40 |
  |---|---|---|---|---|---|
  | 30% | 90% | 16% | 66% | 92% | 100% |
  | 50% | 90% | 4% | 33% | 60% | 99% |
  | 70% | 85% | 0% | 6% | 12% | 40% |

  So a headline belongs where the effect is large; a 15-point effect needs far more cases than a run can afford.
- **Families and controls.** Cases come in families, one per behaviour the skill claims (`"family"` in evals.json).
  A control family (`[control·prog]` assertions) holds sound requests the agent should simply carry out; its pass rate
  must not be lower with the skill, so a skill cannot score by stopping everything.
- **Sets.** `dev` cases are seen and used while editing the skill. A held-out set is used for one decision and then
  becomes dev; its replacement comes from a builder who has not read the skill. Cases are generated from definitions
  (a cases module and a build script), so a new set costs a builder, not hand-written fixtures.

### Checking the eval itself

| Check | Question | How |
|---|---|---|
| Room | Can this family still show a difference? | `room` on a without-skill pilot: 1 − the without-skill pass rate; below 10 points is saturated |
| Validity | Does the check pass good results and fail bad ones? | Each case ships end states that must pass and must fail, run by the set's `validate.py` |
| Sensitivity | Does the eval catch a known-bad skill? | Once per suite, a skill with a key section removed on dev; its pass rate must drop |
| Discrimination | Does an assertion separate the arms? | `room` flags cases where both arms score the same |
| Reliability | Do repeated runs agree? | `room` flags configurations whose runs disagree; the CI width |
| Judge agreement | Can the graders be trusted? | Agreement and κ; low-agreement assertions are excluded |
| Correlation | Does grading add information? | If judged outcomes move with the programmatic ones, grade fewer cases |
| Contamination | Was a case seen while editing? | Record who read what; seen cases are dev |
| Cost | What does a decision cost? | Tokens and time per run (`timing.json`) |

### When the agent's model changes

1. Run the without-skill arm of the dev cases once on the new model (`prepare --arms without_skill --replicates 1`,
   then `run`, `check`, `room`). No grading.
2. A family with no room left means the new model no longer needs that part of the skill: compare a skill without
   that part against the current one (shorter skills cost fewer tokens).
3. Where room remains, run the with-skill arm. If the difference holds, keep the skill; if it dropped, edit on dev
   and confirm on a fresh held-out set.

Every result goes into the ledger with the model, the skill's sha256 and the evals' sha256, so differences can be
traced to a model, a skill version or a case set.

## Trigger test

`triggers.py` checks whether the skill's description makes an agent load it, with no instruction to do so.
Each session gets a fresh HOME with only this skill installed at user level and an empty project; it counts as
triggered when the agent reads the skill's `SKILL.md` or calls `Skill(<name>)`. Sessions stop at the first trigger
or after 4 tool calls, so a skill loaded later than that is missed. Project-level installs are not used: headless
Grok does not load skills from an untrusted project folder.

```sh
python3 eval-harness/triggers.py --config <skill-workspace>/eval-config.json --queries <skill>/evals/triggers.json \
  --label iteration-6 --out <skill-workspace>/iteration-6/triggers.json --runs 2
```

## What is kept

`aggregate` follows the [agentskills.io](https://agentskills.io/skill-creation/evaluating-skills) workspace layout,
with one extra level for the agent:

```
<skill>-workspace/
├── ledger.json                      # one row per iteration, development and confirmation
└── iteration-N/
    ├── benchmark.json               # run_summary per the spec, plus the fields below
    ├── summary.md
    └── <agent>/eval-<name>/<with_skill|without_skill>/run-K/
        ├── outputs/                 # response.md, and the edited target file if the run changed it
        ├── grading.json             # assertion_results (text, passed, evidence) and summary (pass_rate)
        └── timing.json              # total_tokens, duration_ms
```

Additions to the spec files: each assertion's id, kind, check (prog or judge), both graders' votes and whether it
was excluded; the judge quality score; tool calls, turns, CLI version, requested and reported model, effort,
isolation and the skills the CLI reported. Token counts are what each CLI reports and are not comparable across
agents. Dates are UTC; no times of day, session ids or local paths are kept. The raw CLI output stays in the
workspace.

## Metrics

- **Pass rate**: the share of a run's assertions that pass (spec `pass_rate`), then mean ± stddev over runs. A judge
  assertion passes only if both graders pass it; prog assertions come from the eval set's `checks.py`.
- **Outcome pass rate** (the headline): the same over outcome assertions only, or over programmatic outcome
  assertions only when the rule says `"headline_check": "prog"` (then judged outcome assertions are reported as a
  secondary metric). Also reported: safety (gate and scope assertions), control (control assertions), procedure, and
  the judge quality score (1–5, mean of the two graders).
- **Difference**: with − without, in percentage points, mean over agents. **95% CI**: percentile bootstrap,
  resampling runs within each agent × eval cell (10,000 resamples, fixed seed), or cases within each agent with
  `"resample": "cases"`. **p**: one-sided permutation test that permutes arm labels only within each agent: exact
  when each agent has at most 200,000 relabelings (8 vs 8 has 12,870), else estimated from 20,000 random relabelings
  with a fixed seed; with `"test": "paired"`, an exact sign-flip test on each case's difference. The summary says which.
- **Judge agreement**: the share of judge verdicts on which the two graders agree, with Cohen's κ. An assertion on
  which they agree less than 70% of the time is excluded and listed. κ is not used for exclusion because it
  collapses when nearly every verdict is PASS.
- **Criteria met** (per agent): outcome pass rate at least 15 points higher, judge quality score not lower (with
  `"quality_guard": "regression"`, not 0.5 or more lower), and safety and control pass rates not lower with the skill. "Weak evidence" when p ≥ 0.10; "regression" when the outcome pass rate
  drops 15 points or more, the quality score drops 0.5 or more, or the safety or control pass rate drops.
- **Relative error reduction** (held-out evals): (with − without) / (1 − without), the share of the baseline's
  failures the skill removes. It must be at least 60%; if the baseline leaves less than 10 points of room, the
  held-out result is uninformative.

The thresholds live in `stats.RULE` and are fixed in each skill's decision rule before a confirmation run.
