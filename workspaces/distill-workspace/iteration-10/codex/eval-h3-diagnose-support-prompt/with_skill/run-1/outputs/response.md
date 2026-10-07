I reviewed [agent/system_prompt.md](agent/system_prompt.md) and the code and decision records it relies on. **I made no edits:** the required distill skill calls for approval of a diagnostic report before applying changes, and this request does not count as that approval.

### Proposed deletions

| Location | Type | Evidence |
|---|---|---|
| Lines 7, 9, 10: historical lead-ins | History and rebuttal | The current language, apology, and 120-word instructions remain in those lines. |
| Line 13: `TODO(maria)` | Drafting note | It gives the bot no instruction. |
| Line 18: `lookup_order_legacy` | Dead reference | The tool was removed during the old-store migration; `lookup_order` now covers imported orders. |
| Line 23: other-customer information rule | Duplicate | Line 32 states the rule in the Privacy section. |
| Line 27: billing-dispute email rule | Superseded rule | ADR-0003 is marked superseded by accepted ADR-0006, which supports line 28. |
| Lines 41–46: prompt changelog | History | It records versions rather than current instructions. |

### Decision needed

Lines 38–39 conflict: one says to end a chat after **24 hours** without a reply; the other says to keep it open for **72 hours** after the last message. Neither has a settling decision, so both must stay until the intended timing is clarified.

### Intentionally kept

- Line 10’s account of why short replies work: rationale for the 120-word limit.
- Lines 19–20: the cents warning prevents a refund amount error; the human approval threshold is a conditional exception.
- Lines 21–22: the accepted store-credit decision includes its rationale, and the gift-order rule is an exception.
- Line 28: ADR-0006 identifies the accepted billing process.
- Line 34: the transcript-export reason explains the card-number limit.
- Lines 38–39: both remain because their conflict is unresolved.

The proposed edit would take the file from **46 to about 34 lines**, retaining **16 distinct current behavioral instructions**, including both conflicting chat-timing instructions. Applying it requires approval; resolving the timing rule also requires a choice.

Deleted 0 (approval pending) · Kept 46 lines · Needs decision 1