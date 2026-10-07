I cleaned up `prompts/release-notes/SKILL.md` and applied the changes directly, as you asked. It went from 41 lines to 35. I didn't commit anything. One pair of sentences contradicts each other, so I left both in for you to decide.

## Needs your decision

**1. When the release notes get written (contradiction, left unchanged).**
- §4, line 29: "Merge the release notes into main by the day before the release."
- §5, line 35: "Write the release notes on release day, after the tag has been created."

These can't both be followed: the notes can't be merged the day before release if they're only written on release day, after the tag exists. No ADR or later decision says which one is current. Until it's settled, the agent may write them at the wrong time. There are three options:
- Keep the day-before deadline and delete line 35.
- Write on release day after the tag and delete line 29.
- Treat them as two separate steps, a draft merged the day before and a final pass after the tag. The file would need rewording to say that.

**2. Was the label classification ever confirmed?** I deleted the note "NB: the classification criteria above are still being verified (TODO: confirm with the owner)". A drafting note like that doesn't change what the agent does, and ADR-0007 is `accepted`. If the owner never confirmed the `feat`/`fix`/`chore` criteria, that question is still open.

## Deleted
| Line | Type | Excerpt | Evidence |
|---|---|---|---|
| 10 | History | "used to be written directly on a Notion page… 2026-05 meeting…" | Kept only the conclusion: write in `CHANGELOG.md` |
| 12 | Rebuttal | "An older guide suggested… Spanish, but in fact…" | Now states plainly: English, with the reason (US customers) kept |
| 17 | Superseded rule | "entries are sourced from commit messages (ADR-0003)" | ADR-0003 is marked `superseded` by ADR-0007 |
| 23 | Meta note | "NB: … still being verified (TODO…)" | See decision 2 |
| 27 | Dead reference | "follow `docs/format-guide.md`" | That file doesn't exist; `docs/` only contains `adr/` |
| 40 | Duplicate | "Do not include PRs whose label is `skip-changelog`…" | Same rule as §2, line 18, which I kept |

## Kept even though they look like cruft
- **Line 30, the "2026-07 incident" sentence:** it warns that tagging locally makes CI publish the notes twice. Commit dd00c8d added it on purpose; the incident is the reason behind "Only CI cuts tags."
- **Line 12, "because all of our customers are in the US":** it's the reason for the English rule.
- **Line 19, the auto-summarizing LLM ban:** it records an alternative ADR-0007 rejected, so the agent shouldn't use it.
- **Line 20, the security-patch exception:** it's a real exception to the normal rules.
- **Line 25, "the tag script checks the version…":** it explains why version numbers must not be bumped by hand.

## Checks
- The remaining links and paths all point to real files (ADR-0007, `scripts/collect-prs.sh`, `CHANGELOG.md`).
- Every instruction the agent acts on is still there. The only things lost are the obsolete commit-message source and the reference to a file that doesn't exist.

Deleted 6 (1 history, 1 rebuttal, 1 superseded, 1 meta note, 1 dead reference, 1 duplicate) · Kept 13 · Needs decision 2

## Suggestions (not applied)
- ADR-0007 says the PR title is the entry text. With the old commit-message line gone, the file no longer says where entry text comes from. You might add a line saying it.
- If the format guide matters, either write `docs/format-guide.md` or put the format rules directly in §3.