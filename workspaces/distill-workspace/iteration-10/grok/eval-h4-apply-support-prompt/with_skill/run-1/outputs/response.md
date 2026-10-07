`agent/system_prompt.md` is distilled from 46 lines to 34. One contradiction is untouched.

**Decisions needed**

Closing a chat still has both rules. Nothing settles them: there is no ADR, and the 72-hour line was added on 2026-03-18 in `9aeb4b4` without retiring the 24-hour line from 2025-11-03.

- End the chat after 24 hours without a reply from the customer.
- Keep a chat open for 72 hours after the customer's last message, so they can come back to it.

Those two clocks overlap, so the agent can both close a chat and keep it open. Say which window is current and I will drop the other.

**Deleted**

- History, language bullet: dropped the English-only period and the retired translation service. Kept "You reply in the language the customer writes in."
- Rebuttal, apology bullet: dropped the earlier-draft apology opener. Kept "You apologize only when the problem is on our side."
- Excess narrative: dropped "We spent most of 2025 comparing models and prompt styles."
- Meta note: removed `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->`. It does not change what the agent does.
- Dead reference: removed `lookup_order_legacy` for pre-2024 orders. `e06d19b` (2026-06-09) deleted that function and registered only `lookup_order`, whose docstring covers orders imported from the old store. `lookup_order` is still required before any order answer.
- Duplicate: removed "Do not share order or contact information that belongs to another customer." The same rule remains under Privacy: "Never reveal another customer's orders or contact details."
- Superseded: removed "Send billing disputes to billing@northwind.example by email (ADR-0003)." ADR-0003 is `superseded by ADR-0006`. The accepted rule stays: `create_ticket` at priority `high`.
- History: removed the Prompt changelog (v1–v4). Each entry only restates a rule already in the prompt. The empty heading went with it.

**Intentionally kept**

- Long answers caused skimming and a second ticket, and the shortest variant resolved the most chats — the reason for the 120-word cap.
- `issue_refund` is in cents (`4999` = $49.99); passing dollars refunds a hundredth — a trap.
- No store credit, with ADR-0005 (status `accepted`) and the EU original-payment-method reason — a rejected alternative.
- Gift orders: refund details go to the purchaser only — a conditional exception.
- No more than the last four card digits, because transcripts are exported to the analytics vendor every night — the reason for the limit.
- Both closing-chat timers — unsettled, so left verbatim.

Cited tools `lookup_order`, `issue_refund`, and `create_ticket` are registered in `agent/tools.py`. ADR-0005 and ADR-0006 both exist and are `accepted`. No other instruction file layers on this prompt. ADR-0003 was left as the superseded decision record.

The removed TODO asked for a less robotic tone. Wording of kept sentences was not restyled.

Deleted 11 (history 5, rebuttal 1, excess narrative 1, meta note 1, dead reference 1, duplicate 1, superseded 1) · Kept 17 · Needs decision 1