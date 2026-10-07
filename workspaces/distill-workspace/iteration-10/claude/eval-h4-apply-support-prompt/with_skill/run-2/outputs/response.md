I cleaned up `agent/system_prompt.md` directly. It's now 34 lines instead of 46 and still has all 18 instructions the agent actually acts on. I checked that the ADRs it cites (0005, 0006) and the tools it names all exist. Nothing was committed.

**Needs your decision: these contradict each other, so I left both in**
- **Closing a chat** (`agent/system_prompt.md:33-34`): "End the chat after 24 hours without a reply" conflicts with "Keep a chat open for 72 hours after the customer's last message." No ADR settles it. The 72-hour line was added in March 2026 (commit 9aeb4b4), but the 24-hour line was never removed, so it could be an oversight or deliberate. Until you pick one, the agent may close chats at 24 hours that customers expect to reopen. Tell me which rule wins and I'll delete the other.

**Removed**
- **Old history, now just the current rule:** the March 2026 translation-service story (now just "Reply in the language the customer writes in"). Also the 2025 testing and December review story, though I kept the reason behind the 120-word limit: customers skimmed long answers and opened a second ticket.
- **Correction of an earlier draft:** "Earlier drafts told you to open every reply with an apology…" is now just "Apologize only when the problem is on our side."
- **Drafting note:** `<!-- TODO(maria): this section still reads robotic… -->`.
- **Tool that no longer exists:** "For orders placed before 2024, use `lookup_order_legacy`". That tool was removed in e06d19b, and `lookup_order` now finds old-store orders too.
- **Replaced rule:** "Send billing disputes to billing@northwind.example by email (ADR-0003)". ADR-0003 is marked as replaced by ADR-0006, and the rule from ADR-0006 (open a high-priority ticket with `create_ticket`) is still there.
- **Duplicate:** "Do not share order or contact information that belongs to another customer" under Orders and refunds repeated the Privacy rule. I kept the Privacy version.
- **Changelog section:** "Prompt changelog" (v1–v4) was only history. Git log has the same information.

**Kept on purpose, even though they look like leftovers**
- The no-store-credit rule with its ADR-0005 reason (EU refund entitlement). It records an option that was turned down.
- The warning that passing dollars to `issue_refund` refunds a hundredth of the amount.
- The `gift` exception: refund details go to the purchaser only.
- The reason for the card-number rule: transcripts are exported to the analytics vendor every night.

Deleted 8 (2 old history, 1 draft correction, 1 drafting note, 1 dead tool, 1 replaced rule, 1 duplicate, 1 changelog) · Kept 18 · Needs decision 1

**Suggestion (not applied):** "Greet the customer by first name" doesn't say what to do when the name isn't known. You may want to add a fallback.