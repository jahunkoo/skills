I've read the prompt, the files it depends on (`agent/tools.py`, `agent/bot.py`) and the ADRs, and checked git history. I haven't changed any files yet: the distill process requires you to approve this report first.

## Proposed deletions

| Line | Type | Excerpt | Evidence / result |
|---|---|---|---|
| 7 | History | "Until March 2026 we answered in English only… translation service was retired…" | Only the outcome stays: **"Reply in the language the customer writes in."** |
| 9 | Rebuttal | "Earlier drafts told you to open every reply with an apology, but in fact…" | Becomes: **"Apologize only when the problem is on our side."** |
| 10 | Too much backstory | "We spent most of 2025 comparing models… the December review showed…" | Drop the story of the 2025 tests, keep the rule and its reason: **"Keep replies under 120 words: long answers tested worst — customers skimmed them and opened a second ticket."** |
| 13 | Note to editors | `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->` | It doesn't change what the bot does. `bot.py` sends the raw file, so the model sees this comment today. If Maria still wants the rewrite, it belongs in your issue tracker. |
| 18 | Tool that no longer exists | "For orders placed before 2024, use `lookup_order_legacy` instead." | Commit e06d19b removed `lookup_order_legacy` from `tools.py`. `lookup_order` now finds old-store orders too, since they were moved over in the 2026 migration. |
| 23 | Duplicate | "Do not share order or contact information that belongs to another customer." | Same rule as line 32 ("Never reveal another customer's orders or contact details"). I'd keep the one in Privacy. |
| 27 | Replaced by a newer decision | "Send billing disputes to billing@northwind.example by email (ADR-0003)." | ADR-0003 is marked "superseded by ADR-0006". Line 28, which follows ADR-0006 (accepted), stays. |
| 41–46 | History | The whole "Prompt changelog" section (v1–v4) | Git history already records this. Every rule it mentions still appears in the body (the card rule is line 34). The heading goes too, since the section would be empty. |

## Decision needed

1. **Conflicting rules for closing a chat (lines 38 and 39).**
   - Line 38: "End the chat after 24 hours without a reply from the customer." (in the original prompt, 2025-11)
   - Line 39: "Keep a chat open for 72 hours after the customer's last message…" (added 2026-03 in 9aeb4b4)
   - No ADR or later decision says which one wins, and between hour 24 and hour 72 they give opposite instructions. The bot can already get this wrong.
   - Your options: (a) 72 hours is current, so delete line 38; (b) 24 hours is current, so delete line 39; (c) both are meant to apply, for example closing at 24h but allowing a reopen within 72h, and the wording needs fixing.

   Until you decide, I'll leave both lines as they are.

## Kept on purpose (they look like leftovers but aren't)

- **Line 19:** "Passing dollars refunds a hundredth of the amount." This warns against a real, easy mistake.
- **Line 21:** "ADR-0005 rejected it because EU customers are entitled to a refund…" ADR-0005 is accepted, and the line records both the rejected option and the reason.
- **Line 22:** the `gift` exception is a conditional rule.
- **Line 28:** "(ADR-0006)" links to the decision behind the rule.
- **Line 34:** "chat transcripts are exported to our analytics vendor every night" is the reason for the card rule, and it was added recently (e1d8d23) on purpose.
- **Line 10:** "customers skimmed them and opened a second ticket" stays as the reason for the 120-word limit.

## Effect

46 lines → 34 lines. All 16 of the bot's instructions are kept; none are lost.

`Deleted 8 items (history 2 [line 7, changelog section], rebuttal 1, backstory 1, editor note 1, missing tool 1, duplicate 1, superseded 1) · Kept 16 instructions · Needs decision 1`

**Next step:** reply "apply" to approve the deletions above, or tell me which ones to leave out. Please also pick (a), (b) or (c) for the closing rules. I'll only edit `agent/system_prompt.md`.

**Suggestions (I won't apply these as part of distilling):** Once the closing rule is settled, an ADR for it would stop the conflict from coming back. A short comment in `tools.py` that `lookup_order` covers pre-2024 orders would also stop someone re-adding the legacy-tool line.