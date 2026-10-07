Nothing is edited yet. The distill process requires your approval before any change, so below is the report and what I propose to change.

## Proposed deletions (`agent/system_prompt.md`)

| Line | Type | Excerpt | Evidence / result |
|---|---|---|---|
| 7 | History | "Until March 2026 we answered in English only… that service was retired, and now you…" | Keeps only the current rule: **"Reply in the language the customer writes in."** |
| 9 | Rebuttal | "Earlier drafts told you to open every reply with an apology, but in fact…" | Keeps only the rule: **"Apologize only when the problem is on our side."** |
| 10 | Too much backstory | "We spent most of 2025 comparing models and prompt styles." and "…and the December review showed that the shortest variant resolved the most chats" | Keeps the reason and the rule: **"Long answers tested worst: customers skimmed them and opened a second ticket. So keep replies under 120 words."** |
| 13 | Note to the team | `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->` | Doesn't change what the bot does. `bot.py` sends the file as-is, so the model currently sees this comment too. |
| 18 | Dead reference | "For orders placed before 2024, use `lookup_order_legacy` instead." | That tool was removed from `agent/tools.py` in e06d19b. `lookup_order` now finds old-store orders imported in the 2026 migration. |
| 23 | Duplicate | "Do not share order or contact information that belongs to another customer." | Same rule as line 32 under Privacy, which I'd keep. |
| 27 | Superseded rule | "Send billing disputes to billing@northwind.example by email (ADR-0003)." | ADR-0003 says "superseded by ADR-0006". Line 28 (tickets at `high`, ADR-0006, accepted) is the current rule. |
| 41–46 | History | The whole `## Prompt changelog` section | Doesn't change behavior. Git log already records it. "v1: English only" could even mislead the model. The section would be empty, so the heading goes too. |

## Decisions needed

1. **Contradiction about when to close a chat (lines 38–39):**
   - Line 38: "End the chat after 24 hours without a reply from the customer." (from 2025-11)
   - Line 39: "Keep a chat open for 72 hours after the customer's last message, so they can come back to it." (added deliberately in 9aeb4b4, 2026-03)

   If a customer goes quiet, line 38 closes the chat at about 24 hours, but line 39 says it stays open until 72 hours. No ADR or later decision settles which one applies. Until you decide, the bot follows conflicting instructions. Options:
   - (a) Keep 72 hours and delete line 38.
   - (b) Keep 24 hours and delete line 39.
   - (c) Keep both and scope them differently, e.g. "close" means stop prompting the customer while the chat stays reopenable for 72 hours. That would add wording, so you'd need to write it.

   Both lines stay unchanged until you choose.

## Intentionally kept

- **Line 10's reason** ("customers skimmed them and opened a second ticket"): it explains the 120-word limit.
- **Line 19's warning** ("Passing dollars refunds a hundredth of the amount"): it warns about an easy, costly mistake.
- **Line 21** (no store credit, ADR-0005): a rejected alternative with its reason and an ADR link. ADR-0005 is still accepted.
- **Line 22** (gift orders): a conditional exception.
- **Line 28** (ADR-0006): the current rule. The ADR is accepted.
- **Line 34's reason** (transcripts are exported to the analytics vendor every night): it explains the card-number rule.

## Effect

46 lines → 34 lines, with all 16 behavioral rules and the one-line role statement kept.

`Deleted 8 (history 2, rebuttal 1, backstory 1, team note 1, dead reference 1, superseded 1, duplicate 1) · Kept 16 rules + role · Needs decision 1`

## Suggestions (not part of this change)

- Move Maria's TODO into your issue tracker so it isn't lost when the comment is removed.
- If you want a prompt changelog, keep it outside `system_prompt.md` (e.g. in git history or a separate `CHANGELOG.md`). `bot.py` sends this file to the model on every request.

Reply "apply" (and pick an option for the close-chat conflict, if you like) and I'll make the edits and check that every rule survives.