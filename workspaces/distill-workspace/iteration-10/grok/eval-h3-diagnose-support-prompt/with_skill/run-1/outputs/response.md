`agent/system_prompt.md` is judged and unchanged. Approving the delete list below is what allows an edit. The chat-timeout pair stays either way until you pick one.

**Effect:** 46 lines → 34 lines, 17 behavioral instructions kept.

## Delete

1. **Line 7, history.** "Until March 2026 we answered in English only and ran every reply through a translation service; that service was retired, and now". The sentence records the old English-only path and the retired translation service. Kept conclusion: "You reply in the language the customer writes in." (`9aeb4b4`, 2026-03-18, replacing "Answer in English.")

2. **Line 9, rebuttal.** "Earlier drafts told you to open every reply with an apology, but in fact". Kept rule, stated plainly: "You apologize only when the problem is on our side." (same commit, replacing "Open every reply with an apology for the inconvenience.")

3. **Line 10, excess narrative.** "We spent most of 2025 comparing models and prompt styles." Process story around the length rule. Kept: "Long answers tested worst: customers skimmed them and opened a second ticket, and the December review showed that the shortest variant resolved the most chats. Keep replies under 120 words."

4. **Line 13, meta note.** `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->` Drafting note. It does not change what the agent does (`9aeb4b4`, 2026-03-18).

5. **Line 18, dead reference.** "For orders placed before 2024, use `lookup_order_legacy` instead." `lookup_order_legacy` was removed from `agent/tools.py` in `e06d19b` (2026-06-09, "old-store orders migrated"). `lookup_order` now covers orders imported from the old store. Registered tools are `lookup_order`, `create_ticket`, and `issue_refund`.

6. **Line 23, duplicate.** "Do not share order or contact information that belongs to another customer." Same rule as line 32, "Never reveal another customer's orders or contact details." Both are from `f6199b5` (2025-11-03). The single statement stays on line 32 under Privacy.

7. **Line 27, superseded rule.** "Send billing disputes to billing@northwind.example by email (ADR-0003)." `docs/adr/0003-billing-disputes-by-email.md` is **superseded by ADR-0006 (2026-06-09)**. ADR-0006 is **accepted** and supersedes ADR-0003. The current rule is line 28.

8. **Lines 41–46, history.** The Prompt changelog (v1 English-only, v2 language and apology, v3 tickets / ADR-0006, v4 card-number rule). Each conclusion already stands in the current rules (language, apology, line 28, line 34). The ADR-0006 link stays on line 28. The empty section heading goes with it. v4 was added on purpose in `e1d8d23` (2026-08-20) next to the card rule; the changelog line is the history of that edit, and the rule itself stays.

## Decisions needed

**Closing a chat, lines 38 and 39.** Nothing settles which rule is current.

- Line 38 (`f6199b5`, 2025-11-03): "End the chat after 24 hours without a reply from the customer."
- Line 39 (`9aeb4b4`, 2026-03-18): "Keep a chat open for 72 hours after the customer's last message, so they can come back to it."

No ADR covers this. The March commit message only mentions language, and it left the 24-hour rule in place. After a customer message, one rule closes the chat at 24 hours of silence and the other holds it open for 72 hours.

Options:

- A. 24-hour close only.
- B. 72-hour window only.
- C. You specify how the two timers combine.

Both lines stay until you choose. No other item was inconclusive.

## Intentionally kept

- Line 10, "Long answers tested worst: customers skimmed them and opened a second ticket, and the December review showed that the shortest variant resolved the most chats." Why the 120-word cap exists.
- Line 19, "Passing dollars refunds a hundredth of the amount." Trap warning on `issue_refund`. The cents example matches the `issue_refund` docstring in `agent/tools.py`; the prompt keeps it because that sentence also carries the trap.
- Line 21, "Do not offer store credit in place of a refund — ADR-0005 rejected it because EU customers are entitled to a refund to the original payment method." Rejected alternative, why, and rationale link. ADR-0005 is **accepted**.
- Line 22, "Exception: for orders marked `gift`, send refund details to the purchaser only, never to the recipient." Conditional exception.
- Line 28, "`create_ticket` at priority `high` (ADR-0006)." Current escalation rule and rationale link. ADR-0006 is **accepted**.
- Line 34, "chat transcripts are exported to our analytics vendor every night." Why card numbers stop at the last four digits (`e1d8d23`, 2026-08-20).
- Lines 38 and 39, both timeout rules, including "so they can come back to it." Unsettled contradiction, so neither side is residue.

Seventeen behavioral instructions survive: role, customer language, first-name greeting, apology only when the problem is ours, replies under 120 words, "— Helpdesk" sign-off, `lookup_order` before answering about an order, refunds in cents, human approval above $100 (`create_ticket`, priority `normal`, tag `refund-approval`), no store credit, gift-order refund details to the purchaser only, no other customer's orders or contact details, no passwords, last four card digits only, billing disputes as high-priority tickets, and both chat timers.

No other file needs an edit. ADR-0003 stays as the superseded decision record. `agent/tools.py` matches the migration.

## Suggestions

The line 13 TODO asks for a less robotic rewrite of Language and tone before Q4 2026. That is a style rewrite, separate from distillation.

Reply with approval of the delete list, and with A, B, or C for the chat timers, and I will edit only `agent/system_prompt.md`.