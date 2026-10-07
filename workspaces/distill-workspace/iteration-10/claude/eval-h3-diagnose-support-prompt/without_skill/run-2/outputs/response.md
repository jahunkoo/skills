I've rewritten `agent/system_prompt.md` from 403 words down to 254. Every rule the bot follows today is still there, except that two outdated instructions are gone, and I've left one contradiction for you to settle (below). I haven't committed anything.

**Two fixes to how the bot behaves:**
- **Old-order lookup tool:** the prompt told the bot to use `lookup_order_legacy` for orders placed before 2024. That tool was removed in the June migration (e06d19b), and `lookup_order` now finds old-store orders too. So the bot was being pointed at a tool that no longer exists. I removed that line.
- **Billing disputes:** the prompt said both "send them to billing@ by email" (ADR-0003) and "open a `high` priority ticket" (ADR-0006). ADR-0006 replaced ADR-0003, so I kept only the ticket rule.

**Clutter removed:**
- **History notes:** the translation-service and apology-opener backstory now reads as plain rules: "Reply in the language the customer writes in" and "Apologize only when the problem is on our side." I cut the 2025 testing story behind the 120-word limit down to one line of reasoning.
- **Changelog:** removed the "Prompt changelog" section. Git history already records it, and the bot gains nothing from reading it.
- **ADR numbers:** dropped them from the prompt, but kept the reasons the bot needs: the EU refund right behind "no store credit", and the nightly analytics export behind the card-digit rule.
- **Duplicate rule:** "Don't share another customer's order or contact info" appeared under Refunds and again under Privacy. It now appears only under Privacy.
- **Gift orders:** the gift-order rule started with "Exception:" but wasn't an exception to anything. It's now a plain rule.
- **TODO note:** I removed `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->`. `bot.py` sends the file to the model unedited, so the bot was reading this note. If Maria still needs the reminder, it belongs in your issue tracker.

**Decision needed: how long a chat stays open.** The "Closing a chat" section says both "end the chat after 24 hours without a reply" and "keep a chat open for 72 hours after the customer's last message." The 72-hour rule was added in March without removing the 24-hour one, and nothing in the repo says which is correct. I left both lines unchanged rather than guess. Tell me which one applies and I'll delete the other.