# eval-harness

Measures whether a skill changes what an agent actually does. Each eval runs with and without the skill on several
agent CLIs, and blind graders from other vendors judge the results. Python 3 standard library only.

## Requirements

- The agent CLIs you run: `claude` (Claude Code), `codex` (Codex CLI), `grok` (Grok CLI), each logged in.
- Isolated Claude Code runs need a long-lived subscription token from `claude setup-token`, in
  `$CLAUDE_CODE_OAUTH_TOKEN` or the macOS keychain item `claude-eval-oauth`. It is not an API key.
  Without it, pass `--claude-login` to use the normal login; those runs are recorded as `isolation: none`.

## Isolation

- Every run gets a fresh temporary `HOME`. User-level settings, memory files, hooks and skills do not load.
  Only the CLI's credential file is linked in (codex, grok) or passed as a token (claude).
- Claude Code runs with `--disable-slash-commands`; Grok with `GROK_*_SKILLS_ENABLED=false`. Each run records the
  skills its CLI reported (`skills_seen`).
- A with-skill run is told to read a copy of `SKILL.md` alone, so it cannot read the skill's `evals/`.
- Fixtures are git repositories replayed from a mbox with their original dates, so SHAs and `git blame` are stable.

## Usage

```sh
H=eval-harness/harness.py
python3 $H prepare --config <skill-workspace>/eval-config.json --sets dev --label iteration-6   # prints the workspace path
python3 $H run       --ws <ws> --jobs 3
python3 $H check     --ws <ws>          # programmatic assertions and blind grader packets
python3 $H grade     --ws <ws> --jobs 3 # two graders per run, assigned in eval-config.json
python3 $H aggregate --ws <ws> --out <skill-workspace>/iteration-6 --ledger <skill-workspace>/ledger.json
python3 $H status    --ws <ws>
python3 -m unittest discover -s eval-harness/tests
```

`eval-config.json` names the skill folder, the eval sets (`dev`, `holdout`), each agent's CLI, model and reasoning
effort, and which graders judge which agent. By default no run is graded by its own vendor. An agent is a CLI with
its model; results are reported per agent and pooled, never ranked across agents.

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
- **Outcome pass rate** (the headline): the same over outcome assertions only. Also reported: safety (gate and scope
  assertions), procedure, and the judge quality score (1–5, mean of the two graders).
- **Difference**: with − without, in percentage points, mean over agents. **95% CI**: percentile bootstrap,
  resampling runs within each agent × eval cell (10,000 resamples, fixed seed). **p**: one-sided exact permutation
  test that permutes arm labels only within each agent.
- **Judge agreement**: the share of judge verdicts on which the two graders agree, with Cohen's κ. An assertion on
  which they agree less than 70% of the time is excluded and listed. κ is not used for exclusion because it
  collapses when nearly every verdict is PASS.
- **Criteria met** (per agent): outcome pass rate at least 15 points higher, judge quality score not lower, and
  safety pass rate not lower with the skill. "Weak evidence" when p ≥ 0.10; "regression" when the outcome pass rate
  drops 15 points or more, the quality score drops 0.5 or more, or the safety pass rate drops.
- **Relative error reduction** (held-out evals): (with − without) / (1 − without), the share of the baseline's
  failures the skill removes. It must be at least 60%; if the baseline leaves less than 10 points of room, the
  held-out result is uninformative.

The thresholds live in `stats.RULE` and are fixed in each skill's decision rule before a confirmation run.
