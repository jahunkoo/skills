I've rewritten `prompts/release-notes/SKILL.md` and cut it from 41 lines to 25. I haven't committed it. Every rule an agent actually needs is still there, and four changes are judgement calls you should check.

**Removed:**
- **History that doesn't change what the agent does:** the move away from Notion in 2026-05, and the old guide that said to write in Spanish. The real rules (`CHANGELOG.md`, English, US customers) are kept in one line.
- **Repeated rule:** "leave out `skip-changelog` PRs" appeared in both §2 and §5. It's now in one place.
- **Broken link:** "For the detailed format, follow `docs/format-guide.md`" pointed to a file that doesn't exist in the repo.
- **Stale TODO:** "NB: the classification criteria above are still being verified (TODO: confirm with the owner)". ADR-0007 is marked accepted, and the note gave the agent nothing to act on.

**Contradictions I resolved (please check these):**
1. **Where entries come from.** The prompt pointed to ADR-0003 (entries from commit messages), but ADR-0003 is marked superseded by ADR-0007, which says to use PR titles. ADR-0007 also rejected commit messages because squash merges mangle them. The prompt now says to use PR titles and links only ADR-0007.
2. **When to write.** §4 said to merge the notes into main "by the day before the release". §5 said to write them "on release day, after the tag has been created". I kept the day-before rule and dropped the other. The tag script checks the `CHANGELOG.md` version against the tag, so the notes must exist before tagging, and only CI cuts tags anyway. If release day is actually correct, that rule needs a rethink.
3. **"Don't use an auto-summarizing LLM."** The agent reading this prompt is itself an LLM, so I reworded it as: use PR titles as the entry text and don't write your own summaries. This keeps the reason ADR-0007 gives (inaccurate entries).
4. **The 2026-07 incident rule.** I kept it as a firm rule: never create or push a tag yourself, only CI does. The short reason stays (a local tag makes the release job run twice and publishes the notes twice); the dated incident story is gone.

**Kept unchanged in substance:** the `collect-prs.sh` step, the security-patch exception, the version heading format, the rule against bumping versions by hand (with the tag-script reason), and the one-reviewer PR approval.

You may also want to either create `docs/format-guide.md` or confirm it was never meant to exist. If the classification TODO is in fact still open, it belongs in an issue rather than in the agent's instructions.