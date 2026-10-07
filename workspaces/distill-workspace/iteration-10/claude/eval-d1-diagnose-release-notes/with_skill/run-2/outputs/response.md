I've only produced the diagnostic report so far. The skill requires approval before any edit, so nothing is applied yet and `prompts/release-notes/SKILL.md` is unchanged.

## Diagnostic report: `prompts/release-notes/SKILL.md`

### Delete or rewrite

| Line | Type | Excerpt | Evidence / proposed result |
|---|---|---|---|
| 10 | History | "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting…" | Keep only the conclusion: "Write release notes in `CHANGELOG.md` at the repo root." |
| 12 | Rebuttal | "An older guide suggested … Spanish, but in fact they are written in English." | Drop the rebuttal and keep the reason: "Write release notes in English, because all of our customers are in the US." |
| 17 | Superseded rule | "Change entries are sourced from commit messages (ADR-0003)" | `docs/adr/0003-changelog-source.md` is marked `superseded` and was replaced by ADR-0007, which is `accepted`. Line 18 already states the current rule. |
| 23 | Meta note | "NB: the classification criteria above are still being verified (TODO: confirm with the owner)" | Doesn't change what the agent does. The criteria come from ADR-0007, which is `accepted`, so no real open question remains. |
| 27 | Dead reference | "For the detailed format, follow `docs/format-guide.md`." | The file doesn't exist; `docs/` only contains `adr/`. |
| 40 | Duplicate | "Do not include PRs whose label is `skip-changelog` in the list." | Line 19 says the same thing. I'd keep line 19, which is in "What to include". |

### Decisions needed

1. **Contradiction about timing: line 34 vs. line 41.**
   - Line 34: "Merge the release notes into main by the day before the release."
   - Line 41: "Write the release notes on release day, after the tag has been created."

   Nothing in the repo settles which one is current, so I'm keeping both until you decide. Line 30 is a hint: the tag script checks the version in `CHANGELOG.md` against the tag, so the notes have to exist before the tag. That fits line 34. Line 35 adds that only CI cuts tags.
   - **Option A:** keep line 34 and delete line 41.
   - **Option B:** keep line 41 and change the release flow to match it.

   Until this is settled, an agent following the file can get the timing wrong.

### Intentionally kept

- **Line 12, the reason "all of our customers are in the US":** it's the reason behind a rule.
- **Line 18, the ADR-0007 link:** it's the source of the rule.
- **Line 20, no auto-summarizing LLM:** it's an alternative the team rejected (option B in ADR-0007).
- **Line 21, security-patch exception:** it's a conditional exception.
- **Line 30, don't bump versions by hand:** it warns about a trap (a mismatch stops the release).
- **Line 35, the 2026-07 incident and "only CI cuts tags":**
  - It warns about a trap: tagging locally runs the CI release job twice, which publishes the notes twice.
  - It was added on purpose recently (`dd00c8d`, 2026-07-18).
  - I'd leave its wording unchanged, including "After the 2026-07 incident".
- **Line 41:** kept while the contradiction above is open.

### Effect

The file would go from 41 lines to 35. All 13 rules would stay (lines 10, 12, 16, 18, 19, 20, 21, 29, 30, 34, 35, 39, 41). Each section heading would still have content.

---

`Deleted 6 (history 1, rebuttal 1, superseded 1, meta note 1, dead reference 1, duplicate 1) · Kept 13 · Needs decision 1`

**Not applied:** all of the above. Reply "apply" to make the edits, and say whether you want option A or B for the timing conflict.

**Suggestions (none of these are in the plan):**
- Once line 17 is gone, the file no longer says what text to use for each entry. ADR-0007 says to use the PR title; you could add "Use the PR title as the entry text" to section 2.
- If a format guide exists somewhere else, such as in another repo, link to it instead of the missing `docs/format-guide.md`.