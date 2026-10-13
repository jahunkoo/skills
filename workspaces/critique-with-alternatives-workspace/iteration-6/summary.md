# critique-with-alternatives — iteration-6 (confirmation)

2026-10-13 UTC · skill sha256 `139b781aa444` · harness `69dd2d9` · 72/72 runs graded · 1 runs per configuration · staged confirmation of 2.0.0 on suite-holdout: Grok baseline first, grading after the programmatic criteria held; aggregated after fixing the harness's assumption that a confirmation set is named holdout

**Outcome pass rate**, mean over agents: with skill 100%, without 59%, difference **+41 points** (95% CI +26 to +59; one-sided exact paired sign-flip permutation test stratified by agent, p = 0.00049). The outcome pass rate counts programmatic assertions only; judged outcome assertions are a secondary metric.

| Agent | Outcome pass rate with / without | Difference, points (95% CI) | p | All assertions with / without | Judge quality score (1–5) with / without | Safety with / without | Control with / without | Judged outcome with / without | Criteria met | Judge agreement (κ) | Mean time with / without | Mean tokens with / without |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Code · claude-opus-5-5 · high | 100% / 44% | +56 (+22 to +89) | 0.031 | 100% / 79% | 4.8 / 3.9 | — / — | 100% / 100% | 100% / 100% | yes | 100% (1.00) | 30s / 28s | 122k / 111k |
| Codex CLI · gpt-6-sol · high | 100% / 44% | +56 (+22 to +89) | 0.031 | 96% / 75% | 3.8 / 3.6 | — / — | 100% / 100% | 83% / 83% | yes | 92% (0.62) | 81s / 95s | 139k / 134k |
| Grok CLI · grok-4.7 · high | 100% / 89% | +11 (+0 to +33) | 0.500 | 100% / 96% | 4.5 / 4.8 | — / — | 100% / 100% | 100% / 100% | yes, weak evidence | 100% (1.00) | 248s / 108s | 327k / 172k |

Excluded assertions (judge agreement below 70%): none.

| Eval set | Evals | Outcome pass rate with / without | Difference, points (95% CI) | p | Relative error reduction |
|---|---|---|---|---|---|
| suite-holdout | ha1-repair-username-dots, ha2-repair-shipment-retry, ha3-repair-menu-sort, hc1-control-email-case, hc2-control-stock-retry, hc3-control-export-phone, hr1-review-webhook-logging, hr2-review-notify-default, hr3-review-sku-index, hr4-review-structured-clone, hr5-review-feed-sort, hr6-review-import-exit | 100% / 59% | +41 (+26 to +59) | 0.00049 | 100% (confirmed) |

Decision: publish.
