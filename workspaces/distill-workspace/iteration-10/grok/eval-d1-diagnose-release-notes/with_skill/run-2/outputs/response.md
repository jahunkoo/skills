No edits yet. Distillation stops at the diagnostic until you approve it. `prompts/release-notes/SKILL.md` is the only agent instruction file (no `AGENTS.md`). The two ADRs are decision records, not a second copy of the prompt.

## Delete

1. **Line 10, history** (clause only). Excerpt: "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting we decided to move them into the repo, so". The sentence itself is the history. Keep the conclusion, with the tense marker dropped: "They are written in `CHANGELOG.md` at the repo root."

2. **Line 12, rebuttal** (clause only). Excerpt: "An older guide suggested that release notes should be written in Spanish, but in fact". Keep: "They are written in English. That is because all of our customers are in the US."

3. **Line 17, superseded rule.** Excerpt: "Change entries are sourced from commit messages ([ADR-0003](../../docs/adr/0003-changelog-source.md))." [ADR-0003](docs/adr/0003-changelog-source.md) is `superseded` (replaced by ADR-0007 on 2026-06-02). [ADR-0007](docs/adr/0007-changelog-from-pr-labels.md) is `accepted` and lists "keep parsing commit messages" as rejected alternative A.

4. **Line 23, meta note.** Excerpt: "NB: the classification criteria above are still being verified (TODO: confirm with the owner)". A verification note does not change what the agent does. The open question is under Decisions needed.

5. **Line 27, dead reference.** Excerpt: "For the detailed format, follow `docs/format-guide.md`." That path is not in the tree, and it has no git history.

6. **Line 40, duplicate.** Excerpt: "Do not include PRs whose label is `skip-changelog` in the list." Same rule as line 19, "Leave PRs labeled `skip-changelog` out of the notes." Keep line 19. It sits under "What to include" and matches ADR-0007.

## Decisions needed

**Timing contradiction. Both lines stay until you choose.** Both were added in `42e78f7` (2026-06-10). No ADR covers them. The 2026-07-18 commit did not touch them.

- Line 34: "Merge the release notes into main by the day before the release."
- Line 41: "Write the release notes on release day, after the tag has been created."

Options: keep the day-before merge and remove the release-day write; keep the release-day write and remove the day-before merge; or say they are two steps and give the wording. Line 35 (only CI cuts tags) and line 39 (PR plus one reviewer) stay either way.

**Classification confirmation.** The line 23 note asks whether `feat` / `fix` / `chore` and omitting `skip-changelog` are confirmed. ADR-0007 (accepted, 2026-06-02) already records that decision. The note is still proposed for deletion. If the criteria are not confirmed, say what should replace them. Those bullets stay until you do.

## Intentionally kept

- Line 12, "That is because all of our customers are in the US." The reason for writing in English.
- Line 20, the ban on an auto-summarizing LLM. ADR-0007 rejected alternative B is "Generate the body with LLM auto-summaries."
- Line 21, the security-patch exception: one line, "Security fixes", and CVE details only after the public disclosure date. It changes that release type.
- Line 30, the tag-script check against `CHANGELOG.md`. No tag script is in this repo. The reason for not bumping versions by hand stays. The checker may live in CI.
- Line 35, the 2026-07 warning: a local `git tag` makes the CI release job publish the notes twice, and only CI cuts tags. Added on purpose in `dd00c8d` (2026-07-18).

`scripts/collect-prs.sh` exists. Both ADR links resolve. The heading rule matches `CHANGELOG.md`.

## Effect

41 lines → 35 lines, 14 behavioral instructions kept.

Deleted 6 (history 1, rebuttal 1, superseded 1, meta 1, dead reference 1, duplicate 1) · Kept 14 · Needs decision 2

Nothing is applied. The two decisions above are unanswered, so those lines are unchanged even after approval. One suggestion, not applied: ADR-0007 also says the entry text is the PR title, and this skill never says that. Say if you want that sentence added.