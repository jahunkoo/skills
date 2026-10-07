# distill — iteration-10 (confirmation)

2026-10-01 UTC · skill sha256 `a5ecd0c50a19` · harness `4828121` · 48/48 runs graded · 2 runs per configuration · 1.1.0 confirmation run under the amended rule (d1, d2, h3, h4)

**Outcome pass rate**, mean over agents: with skill 96%, without 66%, difference **+30 points** (95% CI +23 to +37; one-sided exact permutation test stratified by agent, p = 8.5e-06).

| Agent | Outcome pass rate with / without | Difference, points (95% CI) | p | All assertions with / without | Judge quality score (1–5) with / without | Safety with / without | Criteria met | Judge agreement (κ) | Mean time with / without | Mean tokens with / without |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Code · claude-opus-5-5 · high | 100% / 82% | +18 (+15 to +21) | 0.013 | 98% / 67% | 4.9 / 3.5 | 100% / 62% | yes | 95% (0.82) | 39s / 33s | 122k / 111k |
| Codex CLI · gpt-6-sol · high | 100% / 45% | +55 (+49 to +60) | 7.8e-05 | 98% / 43% | 4.6 / 2.4 | 100% / 62% | yes | 89% (0.73) | 132s / 95s | 125k / 150k |
| Grok CLI · grok-4.7 · high | 89% / 72% | +17 (-3 to +36) | 0.134 | 90% / 66% | 4.8 / 3.3 | 100% / 75% | yes, weak evidence | 95% (0.82) | 310s / 181s | 218k / 265k |

Excluded assertions (judge agreement below 70%): h3.deadref, h3.keep.

| Eval set | Evals | Outcome pass rate with / without | Difference, points (95% CI) | p | Relative error reduction |
|---|---|---|---|---|---|
| dev | d1-diagnose-release-notes, d2-apply-preapproved | 100% / 65% | +35 (+28 to +42) | 4.4e-05 | 100% |
| holdout | h3-diagnose-support-prompt, h4-apply-support-prompt | 93% / 68% | +25 (+13 to +37) | 0.025 | 78% (confirmed) |

Decision: publish.
