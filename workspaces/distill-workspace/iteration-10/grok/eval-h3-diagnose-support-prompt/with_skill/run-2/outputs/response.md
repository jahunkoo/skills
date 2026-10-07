`agent/system_prompt.md` is unchanged. Distill waits for approval before any edit. One conflict stays as written until you settle it.

Checked `agent/tools.py`, `agent/bot.py`, `README.md`, and `docs/adr/0003`, `0005`, and `0006`. This prompt is the only agent instruction file. The ADRs are the decision records it cites.

## Delete

1. **History** — line 7, the lead-in only. Excerpt: "Until March 2026 we answered in English only and ran every reply through a translation service; that service was retired, and now". The sentence says the old practice and the retirement itself. Commit `9aeb4b4` (2026-03-18) replaced "Answer in English" with this wrap. Keep: "You reply in the language the customer writes in."

2. **Rebuttal** — line 9, the lead-in only. Excerpt: "Earlier drafts told you to open every reply with an apology, but in fact". Same commit replaced "Open every reply with an apology for the inconvenience." Keep: "You apologize only when the problem is on our side."

3. **History** — line 10, the setup clause only. Excerpt: "We spent most of 2025 comparing models and prompt styles." That is the story of the comparison, and it adds no action. Keep the rest of the bullet (the reason, and the 120-word cap).

4. **Meta note** — line 13. Excerpt: `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->`. A drafting note. It does not change what the agent does.

5. **Dead reference** — line 18. Excerpt: "For orders placed before 2024, use `lookup_order_legacy` instead." `lookup_order_legacy` was removed from `agent/tools.py` in `e06d19b` (2026-06-09). It is not in `TOOLS`. `lookup_order` now covers orders imported from the old store. The name survives only on this line.

6. **Duplicate** — line 23. Excerpt: "Do not share order or contact information that belongs to another customer." Same rule as line 32, "Never reveal another customer's orders or contact details." One file, so keep one statement: the Privacy bullet.

7. **Superseded rule** — line 27. Excerpt: "Send billing disputes to billing@northwind.example by email (ADR-0003)." ADR-0003 is `superseded by ADR-0006 (2026-06-09)`. ADR-0006 is `accepted`: escalate with `create_ticket` at priority `high`, which line 28 already says.

8. **History** — lines 41–46, the whole Prompt changelog (heading and the v1–v4 bullets). Version notes only. The live rules are already in the sections above. The heading goes with the section.

## Decisions needed

**Closing a chat — two timeouts, nothing settles them.** Both stay.

- Line 38 (from `f6199b5`, 2025-11-03): "End the chat after 24 hours without a reply from the customer."
- Line 39 (added in `9aeb4b4`, 2026-03-18, without removing line 38): "Keep a chat open for 72 hours after the customer's last message, so they can come back to it."

No ADR covers chat lifetime. Options:

- 24 hours of customer silence ends the chat.
- The chat stays open for 72 hours after the customer's last message.
- Leave both until someone settles it.

## Intentionally kept

- "Long answers tested worst: customers skimmed them and opened a second ticket, and the December review showed that the shortest variant resolved the most chats." — reason for the 120-word cap.
- "Passing dollars refunds a hundredth of the amount." — trap on `issue_refund` units.
- "Do not offer store credit… ADR-0005 rejected it because EU customers are entitled to a refund to the original payment method." — rejected alternative, reason, and ADR link. ADR-0005 is `accepted`.
- "Exception: for orders marked `gift`, send refund details to the purchaser only, never to the recipient." — conditional exception.
- "Escalate billing disputes with `create_ticket` at priority `high` (ADR-0006)." — rationale link. ADR-0006 is `accepted`.
- "chat transcripts are exported to our analytics vendor every night." — reason for the last-four-digits rule.
- "so they can come back to it." — reason on the 72-hour rule, which stays while the timeout is unsettled.

## Effect

46 lines → 34 lines, 17 behavioral instructions kept:

1. Answer Northwind Outfitters customer questions in the chat widget.
2. Reply in the language the customer writes in.
3. Greet the customer by first name.
4. Apologize only when the problem is on our side.
5. Keep replies under 120 words.
6. Sign every reply "— Helpdesk".
7. Look up the order with `lookup_order` before answering.
8. Pass `issue_refund` amounts in cents.
9. Refunds above $100 go to `create_ticket` (priority `normal`, tag `refund-approval`), not `issue_refund`.
10. Do not offer store credit.
11. Gift orders: refund details to the purchaser only.
12. Never reveal another customer's orders or contact details.
13. Billing disputes: `create_ticket` at priority `high`.
14. Never ask for a password.
15. Never paste more than the last four digits of a card number.
16. End the chat after 24 hours without a customer reply (unresolved).
17. Keep the chat open for 72 hours after the customer's last message (unresolved).

Trimmed bullets, with tense markers and filler dropped and the wording otherwise left alone:

- "You reply in the language the customer writes in."
- "You apologize only when the problem is on our side."
- "Long answers tested worst: customers skimmed them and opened a second ticket, and the December review showed that the shortest variant resolved the most chats. Keep replies under 120 words."

Suggestion, not applied: the TODO asked for a tone rewrite of Language and tone. That is a style change, so it is outside this distill.

Say if I should apply the delete list. The 24-hour and 72-hour lines stay either way until you choose one.