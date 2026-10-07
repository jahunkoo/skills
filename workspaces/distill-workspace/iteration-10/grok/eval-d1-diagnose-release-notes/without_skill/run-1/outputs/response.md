`prompts/release-notes/SKILL.md` is now just the current release-notes steps. History, duplicates, and contradictions are gone.

What it still tells the agent to do:

- Write English notes in `CHANGELOG.md`.
- Build entries from `scripts/collect-prs.sh`, using the PR title and the `feat`, `fix`, and `chore` labels from ADR-0007.
- Omit `skip-changelog`, and do not auto-summarize.
- For a security-patch release, write one line, "Security fixes", and add CVE details only after public disclosure.
- Use `## vX.Y.Z (YYYY-MM-DD)` headings, and do not bump the version by hand.
- Open a PR, get one approval, and merge the day before release.
- Let CI cut the tag. A locally pushed tag runs the release job twice.

Dropped as stale or conflicting:

- The Notion move, the old Spanish guide, and the "US customers" rationale.
- Sourcing entries from commit messages. ADR-0003 is superseded by ADR-0007.
- The "still verifying with the owner" note. ADR-0007 is accepted, and the changelog already follows it.
- The pointer to `docs/format-guide.md`, which is not in the repo. The format now follows `CHANGELOG.md`.
- The repeated `skip-changelog` line.
- Writing notes on release day after the tag. That conflicted with the day-before merge, the version check, and CI-only tags.
- The 2026-07 incident story. The rule itself stays: only CI cuts tags.