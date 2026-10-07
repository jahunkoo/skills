I left `prompts/release-notes/SKILL.md` unchanged. Six sentences are residue and can come out once you approve. Two timing rules conflict, and nothing in the repo settles which one is current, so both stay until you choose.

## Delete

| Location | Type | Excerpt | Evidence |
|---|---|---|---|
| §1, line 10 | History | "Release notes used to be written directly on a Notion page, but at a 2026-05 meeting…" | Keep only the conclusion: write them in `CHANGELOG.md` at the repo root. |
| §1, line 12 | Rebuttal | "An older guide suggested that release notes should be written in Spanish, but in fact…" | State the rule plainly: write them in English. Keep the reason, "all of our customers are in the US." |
| §2, line 17 | Superseded rule | "Change entries are sourced from commit messages ([ADR-0003](docs/adr/0003-changelog-source.md))." | ADR-0003 is marked superseded, replaced by ADR-0007 on 2026-06-02. ADR-0007 uses the PR title and the PR label. |
| §2, line 23 | Meta note | "NB: the classification criteria above are still being verified (TODO: confirm with the owner)" | It does not tell the agent what to write. ADR-0007, which sets those criteria, is accepted. |
| §3, line 27 | Dead reference | "For the detailed format, follow `docs/format-guide.md`." | That file is not in the repo. `docs/` contains only `adr/`, and git history has no `docs/format-guide.md`. |
| §5, line 40 | Duplicate | "Do not include PRs whose label is `skip-changelog` in the list." | Line 19 already says to leave `skip-changelog` PRs out. Keep line 19, under "What to include." |

Removing those six items, and the blank lines that only separated them, takes the file from **41 lines to 35**. **16 behavioral instructions** stay.

## Decisions needed

1. **When the notes are written.** Line 34 says merge them into main by the day before the release. Line 41 says write them on release day, after the tag has been created. No ADR picks one. Line 35 (only CI cuts tags) does not settle the order either. Both lines stay until you choose.
2. **Owner confirmation.** Line 23 says the label criteria are still unverified. ADR-0007 marks that decision accepted. The note itself can go. Say if someone still needs to confirm it.

## Intentionally kept

- **Line 12, US customers.** That is the reason the notes are in English.
- **Line 18, ADR-0007 link.** The label rule (`feat`, `fix`, `chore`) keeps its rationale link.
- **Line 20, no auto-summarizing LLM.** That is a rejected alternative (ADR-0007 alternative B), with the reason it was rejected.
- **Line 21, security-patch exception.** A security-patch release is one line, "Security fixes", and CVE details wait until the public disclosure date.
- **Line 30, tag-script check.** Do not bump the version by hand. The tag script compares `CHANGELOG.md` with the tag and stops the release if they differ. That script is not in this repo. The warning still stands.
- **Line 35, local tags.** Pushing a `git tag` locally first makes the CI release job run twice and publish the notes twice. Only CI cuts tags. This is the newest commit (`dd00c8d`, 2026-07-18), added on purpose. The incident lead-in can be shortened later. The warning and the reason stay.
- **Lines 34 and 41.** Both timing rules stay because the conflict is unresolved.

Also unchanged: collect PRs with `scripts/collect-prs.sh <previous tag>` (the script is in the repo), version headings as `## vX.Y.Z (YYYY-MM-DD)`, and open the draft as a PR for one reviewer.

Suggestion, not part of this cleanup: after line 17 is removed, the skill no longer says what the entry text is. ADR-0007 says to use the PR title. That would be a new sentence, so I did not add it.

Deleted 6 (history 1, rebuttal 1, superseded rule 1, meta note 1, dead reference 1, duplicate 1) · Kept 16 · Needs decision 2

Approve the six removals, and choose which timing rule stands, if you want this applied.