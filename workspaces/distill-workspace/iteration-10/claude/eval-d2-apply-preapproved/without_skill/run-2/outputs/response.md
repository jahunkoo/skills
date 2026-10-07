I cleaned up `prompts/release-notes/SKILL.md` without asking first, as you said. The changes are not committed.

**What I changed**
- **Lines 10–12 (Where to write):** I removed the history about Notion and the 2026-05 meeting, and the "older guide said Spanish" story. What's left is the rule and its reason: write release notes in `CHANGELOG.md` at the repo root, in English, because all customers are in the US.
- **LLM auto-summary rule:** I replaced "rejected as alternative B in the ADR-0007 review" with the actual reason given in ADR-0007: it produces inaccurate entries that cost more to review.
- **Tag rule:** I removed the "After the 2026-07 incident, we learned…" story but kept the instruction and its reason. It now says to never push a `git tag` locally, because only CI cuts tags and a local tag makes the release job run twice.
- **Wrap-up:** I deleted the `skip-changelog` line, because the same rule already appears in section 2.

**Left as is, because they conflict or were hard to judge**
1. **Release timing (line 32 vs line 38):** One line says to merge the notes into main the day before the release. The other says to write them on release day, after the tag exists. These can't both be true.
2. **Where entries come from (line 15):** It says entries come from commit messages and links ADR-0003. But ADR-0003 is marked as superseded by ADR-0007, which says to use the PR title as the entry text. Line 16 already follows ADR-0007, so line 15 is probably out of date. I left it because deleting it changes what the agent does.
3. **`docs/format-guide.md` (line 25):** This file doesn't exist in the repo. Either the link is dead or the guide hasn't been written yet.
4. **"NB: … still being verified (TODO: confirm with the owner)" (line 21):** I can't tell whether that check is still pending, so I kept the note.

If you tell me how to settle these four, I'll apply the fixes.