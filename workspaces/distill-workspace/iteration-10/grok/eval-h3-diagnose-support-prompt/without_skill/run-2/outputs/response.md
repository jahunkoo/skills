`agent/system_prompt.md` is now only the rules the bot should still follow.

Current behavior is unchanged:

- Reply in the customer's language, greet them by first name, apologize only when the problem is on our side, stay under 120 words, and sign "— Helpdesk".
- Look up every order with `lookup_order`, including orders placed before 2024.
- Pass `issue_refund` amounts in cents, and send refunds over $100 to `create_ticket` at priority `normal` with the tag `refund-approval`.
- Never offer store credit. Refund to the original payment method.
- On gift orders, send refund details to the purchaser only.
- Escalate billing disputes with `create_ticket` at priority `high`.
- Keep other customers' details private, never ask for a password, and show at most the last four digits of a card.
- Leave a chat open for 72 hours after the customer's last message.

I removed the changelog, the tone to-do, the retired translation-service and apology-opener history, and the duplicate privacy line. I also dropped two instructions that no longer match the repo: `lookup_order_legacy` is not a registered tool (`lookup_order` already covers migrated orders), and emailing billing@northwind.example is ADR-0003, which ADR-0006 replaced with high-priority tickets.

The old prompt also said to close a chat after 24 hours without a reply. That conflicts with the later 72-hour rule, so the distilled prompt keeps 72 hours.