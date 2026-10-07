I stripped the history and the repeated rule from `prompts/release-notes/SKILL.md` and left the conflicting or unsettled lines as they were.

**Removed**

- The Notion page and the 2026-05 meeting. The current location stays: `CHANGELOG.md` at the repo root.
- The older Spanish guide. The current rule stays: write the notes in English because the customers are in the US.
- The "rejected as alternative B" note on the auto-summarizing LLM. The rule stays: do not generate the note body that way.
- The 2026-07 incident framing. The current rule stays: pushing a `git tag` locally makes the CI release job run twice, so only CI cuts tags.
- The second `skip-changelog` line in the wrap-up. The same rule is already in "What to include".

**Left in place**

- **When the notes are written.** Section 4 says to merge them into main by the day before the release. The wrap-up says to write them on release day, after the tag has been created. The skill description also says "before a release." Those timings do not agree, so both instructions are unchanged.
- **Where entry text comes from.** One bullet says change entries come from commit messages (ADR-0003). The next says to classify them by PR label (ADR-0007). In `docs/adr/`, ADR-0007 supersedes ADR-0003 and rejects parsing commit messages, but the skill states both as current. I could not tell whether the commit-message line is leftover or still meant to apply, so both bullets are unchanged.
- **Whether the label rules are final.** The note that the classification criteria are still being verified, with a TODO to confirm with the owner, is still there.
- **The format pointer.** "Follow `docs/format-guide.md`" is still there. That file is not in the repo, so I could not tell whether the pointer is current.