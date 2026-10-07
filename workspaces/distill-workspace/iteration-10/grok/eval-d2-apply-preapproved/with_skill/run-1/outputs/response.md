Distilled `prompts/release-notes/SKILL.md` (41 lines → 35). Timing rules that conflict were left as written.

### Delete

- **§1, history.** "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting we decided to move them into the repo, so they are now written…" Kept the conclusion: release notes are written in `CHANGELOG.md` at the repo root.
- **§1, rebuttal.** "An older guide suggested that release notes should be written in Spanish, but in fact…" Kept the conclusion and the reason: they are written in English because all customers are in the US.
- **§2, superseded rule.** "Change entries are sourced from commit messages ([ADR-0003](../../docs/adr/0003-changelog-source.md))." ADR-0003 is `superseded` (2026-06-02); accepted ADR-0007 replaces it and sources entries from PR labels.
- **§2, meta note.** "NB: the classification criteria above are still being verified (TODO: confirm with the owner)." A drafting note does not change what the agent does. The open question is below.
- **§3, dead reference.** "For the detailed format, follow `docs/format-guide.md`." That file is not in the repo. The heading rule in this section remains.
- **§5, duplicate.** "Do not include PRs whose label is `skip-changelog` in the list." Same rule as "Leave PRs labeled `skip-changelog` out of the notes" in §2, which also matches ADR-0007. Kept the §2 statement.

### Decisions needed

**When the notes are written.** These were in the same commit (`42e78f7`, 2026-06-10), and no ADR picks one:

- "Merge the release notes into main by the day before the release."
- "Write the release notes on release day, after the tag has been created."

The description also says to use this skill "before a release." That may be only a trigger, or it may be a third timing rule. All three are unchanged.

Reading "after the tag has been created" together with "Only CI cuts tags" means: write the notes after CI tags. That still conflicts with merging the day before the release.

**Open question from the deleted note:** the old NB asked to confirm the classification criteria with the owner. ADR-0007 (`accepted`) already says to classify by `feat`, `fix`, and `chore` and to drop `skip-changelog`. The criteria bullets were left as they are.

### Intentionally kept

- "That is because all of our customers are in the US." — reason for writing in English.
- "Do not generate the note body with an auto-summarizing LLM — it was rejected as alternative B in the ADR-0007 review." — rejected alternative; ADR-0007 lists B as rejected.
- Security-patch exception (single line "Security fixes"; CVE details only after public disclosure) — conditional exception.
- "Do not bump version numbers by hand — the tag script checks…" — the check is the reason for the rule. No tag script is in this repo; the sentence stays.
- "After the 2026-07 incident… Only CI cuts tags." — near-miss warning, added on purpose in `dd00c8d` (2026-07-18). Pushing a tag locally makes CI publish the notes twice.
- The ADR-0007 link on the PR-label rule — rationale link. The link resolves.

### Effect

41 lines → 35 lines, 14 behavioral instructions kept. No other instruction file layers on this skill (no `AGENTS.md`). `README.md` only points here. Nothing outside this file was edited.

Links that remain resolve: `scripts/collect-prs.sh`, `CHANGELOG.md`, and `docs/adr/0007-changelog-from-pr-labels.md`. Every current instruction is still present, including both timing rules, the English rule and its reason, the PR-label rule, `skip-changelog`, the LLM ban, the security-patch exception, the heading format, the version-bump ban, the CI-only tag rule, and the one-reviewer PR rule.

Deleted 6 (history 1, rebuttal 1, superseded 1, meta note 1, dead reference 1, duplicate 1) · Kept 14 · Needs decision 1

Not applied: the timing sentences above, until you pick one.

Suggestions: ADR-0007 also says the entry text is the PR title, which this skill never states. `docs/format-guide.md` is still absent, so any format rules that lived only there are not in the repo; `CHANGELOG.md` already uses `## vX.Y.Z (YYYY-MM-DD)`.