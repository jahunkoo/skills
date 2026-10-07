Cleaned [agent/system_prompt.md](agent/system_prompt.md) directly. I removed the changelog, drafting note, old lead-ins, duplicate privacy rule, missing `lookup_order_legacy` instruction, and email escalation rule superseded by ADR-0006. I kept the refund and card-number warnings and the rationale for short replies. `git diff --check` passes.

**Decision needed:** The instructions to close a chat after 24 hours and keep it open for 72 hours conflict. I left both unchanged.

Deleted 12 lines (5 changelog, 1 TODO, 1 dead reference, 1 duplicate, 1 superseded rule, 3 blank lines) · Kept 34 lines · Needs decision 1