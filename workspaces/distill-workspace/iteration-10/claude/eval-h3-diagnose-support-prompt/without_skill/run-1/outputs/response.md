I've rewritten `agent/system_prompt.md`. It went from 46 lines to 33, and every rule that's still in force is still there. The bot now gets only current instructions, with a short reason kept where it helps the bot handle edge cases. I haven't committed the change.

**Decision for you: when to close a chat.** The old prompt told the bot to end a chat after 24 hours without a reply, and also to keep it open for 72 hours after the customer's last message. The 72-hour rule was added in March 2026 but the 24-hour rule was never removed, so the bot had conflicting instructions. I kept the newer 72-hour rule. If 24 hours is what you want, swap that line back.

**Removed because they were wrong or out of date:**
- **The instruction to use `lookup_order_legacy` for orders placed before 2024.** That tool was removed in commit e06d19b, and `lookup_order` now covers orders moved over from the old store. The bot was being told to call a tool that doesn't exist.
- **Emailing billing disputes to billing@northwind.example.** That rule came from ADR-0003, which ADR-0006 replaced. The prompt still had both rules, so disputes could have gone to the old inbox. Only the high-priority ticket rule remains.

**Removed because they were noise:**
- History the bot doesn't need: the old translation service, the dropped apology opener, and the 2025 testing story. Each is now just its current rule, with a one-line reason for the 120-word limit.
- The prompt changelog and ADR numbers. That history is already in git and `docs/adr/`.
- A duplicate "don't share another customer's info" line (it's kept under Privacy).
- The "Exception:" label on the gift-order rule. It isn't an exception to anything, so it's now a plain rule.
- The `<!-- TODO(maria): … rewrite before Q4 -->` comment. An HTML comment isn't hidden from the bot; it reads it with every message. If Maria still plans that rewrite, it belongs in your issue tracker. I didn't rewrite the tone section myself.

I also renamed the "Escalation" section to "Billing disputes", since that's the only thing left in it.