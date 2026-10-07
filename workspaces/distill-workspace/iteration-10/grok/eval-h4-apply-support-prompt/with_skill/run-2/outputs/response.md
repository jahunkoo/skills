`agent/system_prompt.md` is distilled from 46 lines to 34. Every current behavioral instruction is still there. One conflict is untouched.

**Needs decision.** Closing a chat still says both of these, and nothing settles which one is current:

- End the chat after 24 hours without a reply from the customer.
- Keep a chat open for 72 hours after the customer's last message, so they can come back to it.

**Deleted**

- History: the English-only and translation-service backstory. The conclusion is still "You reply in the language the customer writes in."
- Rebuttal: "earlier drafts told you to open every reply with an apology." The rule is still "You apologize only when the problem is on our side."
- Excess narrative: "We spent most of 2025 comparing models and prompt styles."
- Meta note: the `TODO(maria)` comment about a less robotic tone.
- Dead reference: `lookup_order_legacy`. That function was removed when old-store orders moved into `lookup_order` (`e06d19b`).
- Superseded rule: email billing disputes to `billing@northwind.example` (ADR-0003, status superseded). The current rule remains: `create_ticket` at priority `high` (ADR-0006, accepted).
- Duplicate: "Do not share order or contact information that belongs to another customer." The same rule stays under Privacy.
- History: the Prompt changelog (v1–v4). Those conclusions are already in the rules above.

**Intentionally kept**

- The long-answer warning (customers skim them and open a second ticket; the shortest variant resolved the most chats), because it is why replies stay under 120 words.
- "Passing dollars refunds a hundredth of the amount," because it is a trap.
- The store-credit ban with ADR-0005, because that ADR is accepted and records a rejected alternative.
- The `gift` order exception.
- The nightly analytics export, because it is why card numbers stop at the last four digits.
- Both closing-a-chat timers, because they conflict.

`lookup_order`, `issue_refund`, `create_ticket`, ADR-0005, and ADR-0006 all still resolve. No other files were edited.

Suggestion: the removed TODO asked for a tone rewrite before Q4. That is style work, so it was not done here.

Deleted 8 (history 2, rebuttal 1, excess narrative 1, meta note 1, dead reference 1, superseded 1, duplicate 1) · Kept 17 · Needs decision 1