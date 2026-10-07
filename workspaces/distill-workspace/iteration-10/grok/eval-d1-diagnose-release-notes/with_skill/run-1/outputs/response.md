`prompts/release-notes/SKILL.md` is unchanged. Distill stops at the diagnostic until you approve the deletions. One timing conflict stays in the file until you decide it.

No root or app `AGENTS.md` exists. This skill is the only agent instruction file. `docs/adr/0007-changelog-from-pr-labels.md` (status **accepted**) is the decision record for classification, `skip-changelog`, and the rejected LLM summary. `docs/adr/0003-changelog-source.md` (status **superseded**, 2026-06-02) is the old commit-message decision.

## Delete

1. **Line 10, history.** "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting we decided to move them into the repo, so". The sentence itself is the evidence. The conclusion stays: "Release notes are written in `CHANGELOG.md` at the repo root."
2. **Line 12, rebuttal.** "An older guide suggested that release notes should be written in Spanish, but in fact". Stated plainly, the remainder stays: "They are written in English. That is because all of our customers are in the US."
3. **Line 17, superseded rule.** "Change entries are sourced from commit messages ([ADR-0003](../../docs/adr/0003-changelog-source.md))." ADR-0003 is `superseded` by ADR-0007. ADR-0007 rejects "Keep parsing commit messages."
4. **Line 23, meta note.** "NB: the classification criteria above are still being verified (TODO: confirm with the owner)". An NB/TODO does not change what the agent does. The classification rule stays because ADR-0007 is accepted.
5. **Line 27, dead reference.** "For the detailed format, follow `docs/format-guide.md`." `docs/` contains only `adr/`. The path is missing. The version-heading rule on line 29 stays.
6. **Line 40, duplicate.** "Do not include PRs whose label is `skip-changelog` in the list." Same rule as line 19, "Leave PRs labeled `skip-changelog` out of the notes." Both were added in `42e78f7` (2026-06-10). Line 19 stays with the other inclusion rules.

## Decisions needed

**When the notes are written.** Nothing settles it. Both lines come from `42e78f7`. No ADR covers timing. The later tag rule (`dd00c8d`, 2026-07-18) does not choose between them.

- Line 34: "Merge the release notes into main by the day before the release."
- Line 41: "Write the release notes on release day, after the tag has been created."

Both stay until you pick one: the day-before merge, the release-day write after the tag, or two distinct steps you define. The skill description ("before a release") only says when to use the skill.

Open question from the deleted NB: the file still says the classification criteria were awaiting the owner, while ADR-0007 has been accepted since 2026-06-02. That question does not hold the NB or the classification rule.

## Intentionally kept

- Line 12, "That is because all of our customers are in the US." The reason notes are in English.
- Line 18, classify by `feat`, `fix`, and `chore`, with the ADR-0007 link. Accepted decision, and the rationale link stays.
- Line 20, do not auto-summarize the body with an LLM. Rejected alternative B in ADR-0007.
- Line 21, security-patch exception (one line, "Security fixes"; CVE details only after public disclosure). Conditional exception.
- Line 30, do not bump versions by hand, because the tag script checks `CHANGELOG.md` against the tag. The reason stays. This repo has no tag script; it may live in CI or another repo.
- Line 35, the full 2026-07 tag warning. A local `git tag` makes the CI release job publish the notes twice, and only CI cuts tags. Trap warning, added on purpose in `dd00c8d`.

`scripts/collect-prs.sh` exists and takes the previous tag. Both ADR links resolve. `CHANGELOG.md` is at the repo root.

## Effect

41 lines → 35 lines. 14 behavioral instructions kept: skill trigger, `CHANGELOG.md` at the repo root, English, `scripts/collect-prs.sh`, PR-label classification, omit `skip-changelog`, no LLM body, security-patch exception, `## vX.Y.Z (YYYY-MM-DD)` headings, no hand-bumped versions, merge the day before release, only CI cuts tags, one approving reviewer, and write on release day after the tag.

Deleted 6 (history 1, rebuttal 1, superseded 1, meta note 1, dead reference 1, duplicate 1) · Kept 14 · Needs decision 1

Nothing applied. The timing pair is untouched. Suggestion: ADR-0007 also says the entry text is the PR title. This skill does not say that. Say if you want that sentence added after the superseded commit-message line is removed.