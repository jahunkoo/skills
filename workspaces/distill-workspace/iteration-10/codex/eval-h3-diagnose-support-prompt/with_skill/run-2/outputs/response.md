I reviewed [agent/system_prompt.md](agent/system_prompt.md) and its supporting files. **No files were changed.** The required `distill` skill calls for a diagnostic report and approval before editing; “distill it” does not count as approval under that instruction.

### Proposed deletions

| Location | Type | What would go | Evidence |
|---|---|---|---|
| [Line 9](agent/system_prompt.md:9) | Rebuttal | “Earlier drafts told you…” | Keep the current instruction to apologize only when the problem is on our side. |
| [Line 10](agent/system_prompt.md:10) | History | “We spent most of 2025 comparing models and prompt styles.” | The remaining sentences explain the 120-word limit and state the rule. |
| [Line 13](agent/system_prompt.md:13) | Meta note | `TODO(maria)` | An editing note, with no instruction for the bot. |
| [Line 18](agent/system_prompt.md:18) | Dead reference | `lookup_order_legacy` instruction | The tool was removed in the old-order migration; current `lookup_order` includes those orders. |
| [Line 23](agent/system_prompt.md:23) | Duplicate | “Do not share order or contact information…” | The Privacy section states the same rule at line 32. |
| [Line 27](agent/system_prompt.md:27) | Superseded rule | Email billing disputes | [ADR-0003](docs/adr/0003-billing-disputes-by-email.md) is superseded by accepted [ADR-0006](docs/adr/0006-billing-disputes-as-tickets.md), which calls for a high-priority ticket. |
| [Lines 41–46](agent/system_prompt.md:41) | History | Prompt changelog | Its four entries repeat past versions or rules already stated above. The heading would become empty. |

### Decision needed

**Chat closing:** [Line 38](agent/system_prompt.md:38) says end the chat after **24 hours** without a reply; [line 39](agent/system_prompt.md:39) says keep it open for **72 hours** after the last message. The later line was added without removing the first, and I found no decision resolving the conflict. Both must stay until you choose 24 hours, 72 hours, or distinct conditions for each.

### Intentionally kept

- Line 7: the retired translation service explains the current language rule; the skill explicitly preserves the *why* behind a rule.
- Line 10: the customer and review findings explain the 120-word limit.
- Line 19: the cents example warns of a real refund amount error.
- Line 21: the rejected store-credit alternative, rationale, and accepted ADR matter.
- Line 22: the gift-order exception changes who receives refund details.
- Lines 28 and 32: these are the current billing rule and the Privacy section’s copy of the customer-data rule.
- Line 34: transcript export explains the card-number limit.
- Lines 38–39: both closing instructions change behavior; their conflict is unresolved.

If approved, the proposed removals would take the prompt from **46 to 34 lines**, retaining **16 distinct behavioral instructions**, including both conflicting closing instructions.

**Deleted 0 (proposed: history 5, rebuttal 1, meta note 1, dead reference 1, duplicate 1, superseded rule 1) · Kept 46 lines · Needs decision 1**