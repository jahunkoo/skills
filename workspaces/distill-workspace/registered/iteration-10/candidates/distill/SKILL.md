---
name: distill
description: Distills agent instructions (AGENTS.md, SKILL.md, command definitions, system prompts) by stripping the history, legacy, and residue that pile up over time, keeping only the sentences that answer "what should the agent do now?". Works sentence by sentence, in the order judge → diagnostic report (approval gate) → apply → verify that behavior is preserved. Use for requests like "distill this prompt", "clean up AGENTS.md", "strip the history out of these instructions", or "clear the cruft that has built up in this prompt". Do not use for writing new rules, polishing style, or summarizing general documents.
license: MIT
metadata:
  version: "1.1.0"
---

# distill — prompt distillation

The goal is to strip the history and residue that pile up over time in the instructions an agent reads (AGENTS.md, SKILL.md, commands, system prompts), keeping only the sentences that answer: **"So what exactly should I do now, and how?"** Distill the file the user names; if none is named, ask which one — do not guess.

Only remove: add no rules or guidance and rewrite no style; put improvement ideas in the final report as suggestions.

## 1. Read

Before judging, read the whole target file and the files it layers on (root AGENTS.md ↔ app AGENTS.md ↔ SKILL.md), noting which file is the single source (SSoT) of each shared rule.

## 2. Judge each sentence

Ask: **if this sentence were deleted, would the agent behave differently?** Yes → a rule; keep it, however verbose or old. No → residue.

| Residue | Looks like | Handling |
|---|---|---|
| History | "previously X", "changed from A to B" | Keep only the conclusion |
| Rebuttal | "X was said, but actually Y" | Drop the rebuttal; state Y plainly |
| Meta note | "NB:", "TODO: confirm", "(being verified)", drafting notes | Delete: it does not change what the agent does, even when it says a rule is still being verified. If it raises a real open question, also ask it in the report |
| Dead reference | a path, command or script the reader is told to use that does not exist | Delete after confirming it is missing |
| Superseded rule | a rule backed by an ADR marked `superseded` | Delete. Before calling two sentences a contradiction, check the ADRs they cite: `superseded` makes one residue; `accepted` or `provisional` means current |
| Duplicate | the same rule stated more than once | In one file: keep one statement. Across files: keep it in the SSoT and replace each copy with a link to it — do not restate the rule beside the link, and do not delete a copy without leaving the link |
| Excess narrative | background burying the instruction | Keep the instruction; drop the story without turning it into new rules |
| Contradiction | two rules conflict and nothing (an ADR status, a later decision) settles which is current | **Keep both.** List it first under decisions needed: until it is settled, the agent is already going wrong |

Keep these, even though they mention the past:
- the WHY behind a rule, even when it names a tool this repository lacks (it may live in CI or another repository); do not offer to delete it
- trap and near-miss warnings ("doing A silently flips B")
- rationale links (ADR and issue numbers)
- rejected alternatives ("we don't use B")
- conditional exceptions, however verbose

History, rebuttals, meta notes and duplicates are evidenced by their own text. Dead references, ADR status and a sentence's age need a check (look for the file, read the ADR, `git log -L` or `git blame`; a sentence added recently and on purpose is unlikely to be residue). If a check is inconclusive, or you cannot tell whether a sentence still changes behavior, ask instead of deleting.

## 3. Diagnostic report — approval gate

Report before editing, and change no files in this step:
- **Delete:** location, type, excerpt, and the evidence (ADR status, missing file, where the SSoT is).
- **Decisions needed:** contradictions first, then inconclusive items, each with what conflicts with what and the options.
- **Intentionally kept:** every residue-looking sentence you kept, one line each with its own reason.
- **Effect:** N lines → M lines, K behavioral instructions kept.

Apply nothing until it is approved. An explicit request to apply without review counts as approval; a request to distill or clean up a file does not. Items that need a decision stay unchanged until the user decides them.

## 4. Apply

- Edit only approved items, only in the target file; report residue in other files instead.
- In kept sentences, drop tense markers and filler only; do not reword them.
- Keep the heading structure unless a section ends up empty.

## 5. Verify and report

- Check that links and paths resolve.
- Check that every behavioral instruction of the original survives; a missing one is loss, not compression.
- End with one line, `Deleted N (by type) · Kept M · Needs decision K`, then anything not applied and your suggestions.
