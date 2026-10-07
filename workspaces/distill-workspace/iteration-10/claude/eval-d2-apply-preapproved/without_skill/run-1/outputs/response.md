I cleaned up `prompts/release-notes/SKILL.md` without asking first, as you said. The changes are not committed.

**What I changed**
- **§1 Where to write:** I cut the history about Notion, the 2026-05 meeting and the old "write in Spanish" guide. It's now one line: write in `CHANGELOG.md` at the repo root, in English, with the reason (customers are all in the US).
- **§2, LLM rule:** I replaced "it was rejected as alternative B in the ADR-0007 review" with the actual reason from the ADR: it produced inaccurate entries that cost more to review.
- **§4, tag rule:** I dropped the "after the 2026-07 incident" story. It now reads as a direct rule: never push a `git tag` yourself, only CI cuts tags. I kept the reason, because it explains why the rule matters.
- **§5:** I removed "Do not include PRs whose label is `skip-changelog`", because §2 already says the same thing.

**Left as-is because they conflict or are hard to judge**
1. **Where entries come from (§2):** "Change entries are sourced from commit messages (ADR-0003)" conflicts with the next line, which classifies by PR label under ADR-0007. ADR-0003 is marked as superseded by ADR-0007, which says to use the PR title as the entry text. So that line looks out of date, but I left it because it's a conflict. If you agree, delete it, or replace it with "Use the PR title as the entry text."
2. **When to write (§4 vs §5):** "Merge the release notes into main by the day before the release" contradicts "Write the release notes on release day, after the tag has been created." I can't tell which one is current.
3. **"NB: the classification criteria above are still being verified (TODO: confirm with the owner)":** ADR-0007 is marked "accepted", so this may be stale. But it may also refer to an open question I can't see.
4. **"For the detailed format, follow `docs/format-guide.md`":** that file doesn't exist in the repo. Either the path is wrong or the guide was never added.