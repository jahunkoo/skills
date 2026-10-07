---
name: release-notes
description: Use when writing or updating release notes before a release. Triggers on requests like "write the release notes" or "tidy up the changelog".
---

# release-notes

## Where to write

Write release notes in `CHANGELOG.md` at the repo root.

Write release notes in English.

## What to include

- Collect the PR list with `scripts/collect-prs.sh <previous tag>`.
- Change entries are sourced from commit messages ([ADR-0003](../../docs/adr/0003-changelog-source.md)).
- Classify entries by PR label (`feat`, `fix`, `chore`) (rationale: [ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md)).
- Leave PRs labeled `skip-changelog` out of the notes.
- Do not generate the note body with an auto-summarizing LLM.
- Exception: for a security-patch release, write the entries as a single line, "Security fixes", and add CVE details only after the public disclosure date.

NB: the classification criteria above are still being verified (TODO: confirm with the owner)

## Format

For the detailed format, follow `docs/format-guide.md`.

- Write version headings as `## vX.Y.Z (YYYY-MM-DD)`.
- Do not bump version numbers by hand — the tag script checks the version in `CHANGELOG.md` against the tag and stops the release if they differ.

## When to write

- Merge the release notes into main by the day before the release.
- Only CI cuts tags.

## Wrap-up

- Open the draft notes as a PR and get approval from one reviewer.
- Write the release notes on release day, after the tag has been created.
