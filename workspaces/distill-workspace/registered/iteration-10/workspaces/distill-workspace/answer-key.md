# distill fixture answer key — prompts/release-notes/SKILL.md

## Residue (should be stripped)

| ID | Type | Location in the original | Correct handling |
| --- | --- | --- | --- |
| R1 | History | §1 "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting we decided to move them into the repo, so …" | Delete the backstory; keep only the conclusion "write them in `CHANGELOG.md`" |
| R2 | Rebuttal | §1 "An older guide suggested that release notes should be written in Spanish, but in fact …" | Delete the rebuttal; state "write them in English" as a plain sentence. Keeping "That is because all of our customers are in the US" is also correct, since it is a WHY |
| R3 | Meta note | End of §2 "NB: the classification criteria above are still being verified (TODO: confirm with the owner)" | Delete |
| R4 | Dead reference | §3 "For the detailed format, follow `docs/format-guide.md`." — the file does not exist | Delete after confirming |
| R5 | Stacked duplicate | §2 "Leave PRs labeled `skip-changelog` out of the notes." ↔ §5 "Do not include PRs whose label is `skip-changelog` in the list." | Keep one of them |
| R6 | Superseded ADR | §2 "Change entries are sourced from commit messages (ADR-0003)." — ADR-0003's status is superseded (replaced by ADR-0007) | Delete |
| R7 | Contradiction | §4 "Merge the release notes into main by the day before the release." ↔ §5 "Write the release notes on release day, after the tag has been created." | **Do not delete; ask the user** |

## Live rules (should be kept — proposing to delete them, or deleting them, is wrong)

| ID | Type | Original |
| --- | --- | --- |
| K1 | WHY | §3 "Do not bump version numbers by hand — the tag script checks the version in `CHANGELOG.md` against the tag and stops the release if they differ." (the WHY clause must remain too) |
| K2 | Near-miss warning | §4 "After the 2026-07 incident, we learned that pushing a `git tag` locally first makes the CI release job run twice, which publishes the notes twice. Only CI cuts tags." (It came in with the most recent commit. Trimming only the "After the … incident, we learned" backstory wording is allowed; deleting the rule or its reason is wrong) |
| K3 | Rationale link | §2 "Classify entries by PR label (rationale: ADR-0007)" — keep the link |
| K4 | Rejected alternative | §2 "Do not generate the note body with an auto-summarizing LLM — it was rejected as alternative B in the ADR-0007 review." |
| K5 | Conditional exception | §2 "Exception: for a security-patch release, write the entries as a single line, "Security fixes", and add CVE details only after the public disclosure date." |

## Other behavioral instructions (should remain)

- Collect the PR list with collect-prs.sh · version heading format `## vX.Y.Z (YYYY-MM-DD)` · open the draft notes as a PR and get approval from one reviewer
