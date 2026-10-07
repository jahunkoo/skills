I've read the target file and everything it points to: `README.md`, `CHANGELOG.md`, both ADRs and `scripts/collect-prs.sh`. I also checked git history. This is the diagnostic report for your review. I haven't changed any files yet.

## Distillation report: `prompts/release-notes/SKILL.md`

### Decisions needed

1. **The two "when to write" rules contradict each other.**
   - L34: "Merge the release notes into main by the day before the release."
   - L41: "Write the release notes on release day, after the tag has been created."

   Nothing settles which one is current. Both came in with the first commit (42e78f7), and no ADR covers timing. L30 points toward L34: the tag script stops the release if the version in `CHANGELOG.md` doesn't match the tag, so the notes probably need to exist before the tag. That's an inference, though, not a decision. Until this is settled, the agent gets two conflicting instructions.
   - **Options:** (a) keep L34 and delete L41; (b) keep L41 and delete L34; (c) keep both and say when each applies.
   - I'm leaving both lines unchanged until you decide.

2. **Optional question from the TODO on L23.** The note says the classification criteria are "still being verified (TODO: confirm with the owner)". ADR-0007 is `accepted` and already defines those criteria (`feat`/`fix`/`chore`, plus `skip-changelog`), so I think this question is already answered. If the owner really is still reviewing them, that should be recorded in the ADR, not in the prompt. Either way, I'll delete the note (see below).

### Delete

| Line | Type | Excerpt | Evidence / result |
|---|---|---|---|
| L10 | History | "used to be written directly on a Notion page, but at a 2026-05 meeting we decided…" | Keep only the conclusion: "Release notes are written in `CHANGELOG.md` at the repo root." |
| L12 | Rebuttal | "An older guide suggested… Spanish, but in fact…" | Remove the rebuttal and keep the rule and its reason: "Release notes are written in English, because all of our customers are in the US." |
| L17 | Superseded rule | "Change entries are sourced from commit messages (ADR-0003)" | ADR-0003 is `superseded` by ADR-0007, which is accepted and uses PR titles and labels. |
| L23 | Meta note | "NB: … still being verified (TODO: confirm with the owner)" | Doesn't change what the agent does. The open question is raised above. |
| L27 | Dead reference | "follow `docs/format-guide.md`" | The file doesn't exist and never appears in git history (`docs/` only has `adr/`). |
| L35 (lead-in only) | Excess narrative | "After the 2026-07 incident, we learned that" | Remove only this lead-in. Keep the warning: "Pushing a `git tag` locally first makes the CI release job run twice, which publishes the notes twice. Only CI cuts tags." |
| L40 | Duplicate | "Do not include PRs whose label is `skip-changelog` in the list." | Same rule as L19. Keep L19, which sits next to the ADR-0007 classification rule. |

### Intentionally kept

- **L12, "because all of our customers are in the US":** this is the reason for the English rule.
- **L20, no LLM auto-summaries ("rejected as alternative B"):** this is a rejected alternative, and ADR-0007 backs it up.
- **L21, the security-patch exception:** a conditional exception.
- **L30, "the tag script checks… and stops the release":** a trap warning that explains why not to bump versions by hand.
- **L35, the double-publish warning:** a trap warning that was added on purpose recently (dd00c8d, 2026-07-18). Only the narrative lead-in goes.
- **L34 and L41:** both stay until you resolve the contradiction.

### Effect

41 lines → 35 lines, with 13 behavioral instructions kept (one of them is the contradicting L34/L41 pair).

### Suggestions (not part of this distillation)

- Once L17 is gone, nothing tells the agent that entry text comes from the PR title (ADR-0007). You may want to add a line pointing to ADR-0007 for that.
- If a format guide is planned, add the link back once the file exists.

**To apply:** approve the Delete table (all of it, or name which items), and pick option (a), (b) or (c) for the L34/L41 contradiction. I'll then edit only `prompts/release-notes/SKILL.md` and check that every link resolves and every instruction is still there.