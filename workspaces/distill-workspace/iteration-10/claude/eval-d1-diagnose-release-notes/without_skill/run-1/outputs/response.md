I rewrote `prompts/release-notes/SKILL.md`. It went from 41 lines to 29, and every working rule is still in it. I haven't committed the change.

**Removed or rewritten:**
- **Old history:** I dropped the Notion-to-repo move and the old Spanish-language guidance. What's left is the rule itself: write in English, in `CHANGELOG.md`.
- **Instructions that pointed to a replaced decision:** "entries are sourced from commit messages" cited ADR-0003, which has been replaced by ADR-0007. ADR-0007 says to use the PR title as the entry text, and the skill now says that.
- **A repeated rule:** the `skip-changelog` exclusion appeared in both §2 and §5. It's now stated once.
- **A link to a missing file:** `docs/format-guide.md` doesn't exist in the repo, so I removed the reference. The heading format rule stays.
- **Incident story:** I shortened the 2026-07 note to the rule plus a one-line reason. The skill now says never to create or push a `git tag`, because only CI cuts tags and a local tag makes the notes publish twice.
- **Rationale kept:** I kept the reasons that help the agent follow a rule: why LLM summaries are banned, and why not to bump versions by hand.
- **Structure:** five numbered sections became three: Content, Format and Process.

**Two decisions for you to check:**
1. **Conflicting timing rules.** §4 said "merge into main by the day before the release", but §5 said "write the notes on release day, after the tag has been created". I kept the day-before rule and removed the other. The tag script compares `CHANGELOG.md` with the tag, so the notes have to exist before tagging. If release-day writing is still a real practice, tell me and I'll put it back.
2. **The open TODO.** I removed "NB: the classification criteria above are still being verified (TODO: confirm with the owner)". It's a note for whoever maintains the skill, and the agent can't act on it. ADR-0007 is also marked as accepted. If the classification really is still unsettled, it's better tracked in an issue or in the ADR than in the prompt.

One more thing: the "tag script" the skill mentions isn't in this repo. I left the rule in because it describes a real limit on the release, but you may want to add where that script lives.