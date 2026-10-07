I cleaned up `agent/system_prompt.md` in place. It went from 46 lines to 34, and all 17 instructions the agent actually follows are still there. One contradiction in "Closing a chat" needs your decision, so I left it as it was. I haven't committed anything.

**Needs your decision:**
- **Closing a chat.** "End the chat after 24 hours without a reply from the customer" conflicts with "Keep a chat open for 72 hours after the customer's last message." No ADR or later commit says which rule is current, so I kept both. Until you pick one, the agent can't do both. Your options:
  - keep the 24-hour rule;
  - keep the 72-hour rule;
  - separate them: for example, 24 hours of silence ends the chat, but the customer can reopen it for up to 72 hours.

**What I removed:**

| Was | Type | What I did |
|---|---|---|
| Line 7, "Until March 2026 … translation service …" | History | Kept only the rule: "Reply in the language the customer writes in." |
| Line 9, "Earlier drafts told you to open every reply with an apology, but in fact …" | Correction of an old rule | Kept only: "Apologize only when the problem is on our side." |
| Line 10, the story about comparing models in 2025 and the December review | Background story | Kept the 120-word limit and its reason (customers skimmed long answers and opened a second ticket) |
| Line 13, `<!-- TODO(maria): … rewrite before Q4 -->` | Drafting note | Deleted |
| Line 18, "use `lookup_order_legacy`" for orders placed before 2024 | Tool that no longer exists | That tool was removed in commit e06d19b. `lookup_order` now covers orders moved over from the old store. |
| Line 23, "Do not share order or contact information that belongs to another customer" | Duplicate | The same rule is under Privacy ("Never reveal another customer's orders or contact details"), so I kept that one |
| Line 27, "Send billing disputes … by email (ADR-0003)" | Replaced rule | ADR-0003 says it's superseded by ADR-0006, which is accepted, so the `create_ticket` / `high` rule stays |
| Lines 41–46, the "Prompt changelog" section | History | Git history already records these changes. The one rule it mentions, about card numbers, is still under Privacy |

**Kept on purpose, even though they look like old notes:**
- The ADR-0005 reasoning for not offering store credit: it explains a rejected alternative.
- The note about the analytics vendor next to the card-number rule: it's the reason behind the rule.
- The warning that `issue_refund` takes cents, so passing dollars refunds a hundredth of the amount.
- The exception for orders marked `gift`.

I checked that every tool the prompt names (`lookup_order`, `create_ticket`, `issue_refund`) exists in `agent/tools.py`, and that ADR-0005 and ADR-0006 exist.

Deleted 8 (2 history, 1 correction of an old rule, 1 background story, 1 drafting note, 1 tool that no longer exists, 1 replaced rule, 1 duplicate) · Kept 17 instructions · Needs decision 1

**Suggestion:** once you decide the closing-time rule, you might record it in an ADR, as you did for billing disputes.