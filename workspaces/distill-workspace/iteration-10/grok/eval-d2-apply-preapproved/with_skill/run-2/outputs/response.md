Distilled `prompts/release-notes/SKILL.md` (41 lines → 35). Current instructions are unchanged. Two timing rules conflict, and two other lines are hard to judge, so those stayed word for word.

**Deleted**

- **History** (§1): the Notion page and the 2026-05 meeting. Conclusion kept: release notes are written in `CHANGELOG.md` at the repo root.
- **Rebuttal** (§1): the older Spanish guide. Kept: release notes are written in English, because customers are in the US.
- **Superseded rule** (§2): "Change entries are sourced from commit messages" ([ADR-0003](docs/adr/0003-changelog-source.md) is `superseded` by accepted [ADR-0007](docs/adr/0007-changelog-from-pr-labels.md)).
- **Meta note** (§2): "NB: the classification criteria above are still being verified (TODO: confirm with the owner)".
- **Dead reference** (§3): `docs/format-guide.md` is not in the repo.
- **History** (§4): "After the 2026-07 incident, we learned that". The trap stays: a local `git tag` makes the CI release job run twice and publish the notes twice. Only CI cuts tags. That sentence was added on purpose in `dd00c8d` (2026-07-18).
- **Duplicate** (§5): "Do not include PRs whose label is `skip-changelog` in the list." The same rule remains in §2: leave those PRs out of the notes.

**Unclear — left as they are**

- **Conflict.** "Merge the release notes into main by the day before the release" versus "Write the release notes on release day, after the tag has been created." No ADR picks one.
- **Hard to judge.** "The tag script checks the version in `CHANGELOG.md` against the tag" only works if that version heading is already in the file when the tag is cut. That may conflict with writing the notes after the tag, depending on whether "release notes" includes the version heading. No tag script exists in this repo. The sentence stays, because it is the reason for "do not bump version numbers by hand."
- **Hard to judge.** The skill description says to use it when writing notes before a release. That reads as a trigger, and it may also be a schedule. It stays.

Open question from the deleted note: the `feat` / `fix` / `chore` criteria were still marked "being verified" (confirm with the owner). The rules stay; [ADR-0007](docs/adr/0007-changelog-from-pr-labels.md) is `accepted`.

**Intentionally kept**

- English because all customers are in the US (the reason for the rule).
- Do not generate the body with an auto-summarizing LLM — rejected as alternative B in the ADR-0007 review.
- Security-patch exception: one line, "Security fixes", and CVE details only after public disclosure.
- Do not bump versions by hand; the tag script checks `CHANGELOG.md` against the tag.
- Local `git tag` double-publishes; only CI cuts tags.
- ADR-0007 link on the label-classification rule.

**Check.** The ADR-0007 link resolves. `CHANGELOG.md` and `scripts/collect-prs.sh` are in the repo. Every current behavioral instruction is still there: where to write, English, collect PRs, classify by label, omit `skip-changelog`, no LLM summaries, the security exception, the version heading, no hand bumps, merge the day before, only CI tags, one reviewer, and write on release day. Nothing else in the repo restates these rules. `README.md` only points at this file.

Deleted 7 (history 2, rebuttal 1, superseded 1, meta 1, dead reference 1, duplicate 1) · Kept 5 · Needs decision 1

Not applied: the three items under "Unclear." Suggestion: ADR-0007 says the entry text is the PR title. This file never said that. The only sourcing sentence was the superseded commit-message rule, so the skill now does not say where entry text comes from. I did not add a rule. The version-heading line is the only format rule left after removing the missing format guide.