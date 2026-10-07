I distilled `prompts/release-notes/SKILL.md` and applied the edits.

**Unclear, left as written.** When to write the notes is unsettled. "Merge the release notes into main by the day before the release." and "Write the release notes on release day, after the tag has been created." conflict, and no ADR picks one. Both sentences are still in the file.

The removed NB is a separate open question: it said the `feat` / `fix` / `chore` classification was still being verified and to confirm with the owner. ADR-0007 is accepted, so that classification stays the rule. Confirm with the owner if it is still provisional.

**Removed**

- History: the Notion page and the 2026-05 meeting. The current location remains `CHANGELOG.md`.
- Rebuttal: the older Spanish guide. The current rule remains English.
- Superseded rule: source entries from commit messages. ADR-0003 is marked superseded by ADR-0007.
- Meta note: `NB: … (TODO: confirm with the owner)`.
- Dead reference: `docs/format-guide.md` is not in the repo.
- Duplicate: the wrap-up `skip-changelog` line. The same rule remains under "What to include" ("out of the notes").
- Excess narrative: "After the 2026-07 incident, we learned that". The double-publish warning and "Only CI cuts tags." remain.

**Kept on purpose**

- English because customers are in the US.
- The rejected LLM auto-summary, including the ADR-0007 alternative B clause.
- The security-patch exception.
- The tag-script reason for not bumping versions by hand. That script is not in this repo; the reason stays.
- The ADR-0007 link on label classification.
- Both timing sentences above.

Links that remain resolve: `scripts/collect-prs.sh`, `CHANGELOG.md`, and ADR-0007. 41 lines → 35 lines, 13 behavioral instructions kept.

Deleted 7 (history 1, rebuttal 1, superseded 1, meta 1, dead reference 1, duplicate 1, excess narrative 1) · Kept 13 · Needs decision 1

Suggestion: settle the day-before versus release-day timing, then the skill trigger ("before a release") can be aligned with that choice. If a format guide lives outside this repo, the pointer can be restored.