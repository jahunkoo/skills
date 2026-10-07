I've cleaned up `agent/system_prompt.md`. The changes are uncommitted, so you can review them with `git diff`.

**Removed:**
- **History in the tone rules.** Three rules came with backstory: the translation service retired in March 2026, the apology opener from earlier drafts, and the 2025 model and prompt tests. Each is now just the rule ("Reply in the language the customer writes in", "Apologize only when the problem is on our side", "Keep replies under 120 words"). I kept a short reason for the length limit: customers skim long answers.
- **The `TODO(maria)` comment** saying the tone section reads robotic. `bot.py` sends the whole file to the model, so the comment was being sent to the model too. If that rewrite is still planned, keep track of it somewhere else.
- **The `lookup_order_legacy` rule** for orders placed before 2024. That tool was removed in e06d19b, and `lookup_order` now covers orders imported from the old store.
- **The billing-by-email rule** (billing@northwind.example, ADR-0003). ADR-0003 has been superseded by ADR-0006, and the ticket rule stays.
- **A repeated line.** "Do not share order or contact information that belongs to another customer" said the same thing as the first rule under Privacy, so I kept only the Privacy version.
- **The "Prompt changelog" section.** Git history already records it.

**Left as is — please decide:**
- **Closing a chat contradicts itself.** One rule says to end the chat after 24 hours without a reply from the customer. The next says to keep it open for 72 hours after the customer's last message. Both are still in the file. Which one is correct?
- **The gift-order rule starts with "Exception:"** but doesn't say what it's an exception to, since the line above it is about store credit. I didn't change the wording because I wasn't sure what was meant. It may be an exception to a missing rule like "send refund details to the customer," or the word may simply be a leftover.