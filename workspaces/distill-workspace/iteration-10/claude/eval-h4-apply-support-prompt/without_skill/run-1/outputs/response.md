I cleaned up `agent/system_prompt.md` and left the change uncommitted.

**Removed or reworded:**
- **Language:** the story about answering in English and the old translation service is gone. The rule now just says: "Reply in the language the customer writes in."
- **Apologies:** the line about earlier drafts is gone. The rule now says: "Apologize only when the problem is on our side."
- **Reply length:** I dropped the 2025 model-comparison story. I kept the 120-word limit and a one-line reason (customers skim long answers and open a second ticket).
- **`TODO(maria)` comment:** removed. `bot.py` sends the whole file to the model, so the model was reading this note. If Maria still plans to rewrite the "Language and tone" section before Q4, that needs to be tracked somewhere else now.
- **`lookup_order_legacy` instruction:** removed. That tool was deleted from `tools.py` in e06d19b, and `lookup_order` now finds orders brought over from the old store.
- **Duplicate privacy rule:** "Do not share order or contact information that belongs to another customer" in the Orders section said the same thing as the first Privacy rule. I kept the Privacy version.
- **Billing disputes by email (ADR-0003):** removed. Strictly, this one contradicted the ticket rule, but it wasn't a judgement call: ADR-0003 is marked "superseded by ADR-0006", and ADR-0006 says emailed disputes were getting lost. Only the `create_ticket` / priority `high` rule is left. If you'd rather I hadn't touched it, it's in the diff.
- **"Prompt changelog" section:** removed. Git already records that history, and the model was reading lines like "v1: English only".

**Left as is, needs your decision:**
- **Closing a chat:** "End the chat after 24 hours without a reply from the customer" conflicts with "Keep a chat open for 72 hours after the customer's last message." No ADR or code settles which one is right, so both are still there.
- **Gift orders:** the line starts with "Exception:", but it isn't clear what it's an exception to. It may be meant as an exception to the privacy rule, or it may be left over from a rule that no longer exists. I didn't change the wording.