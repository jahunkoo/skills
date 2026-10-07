---
name: release-notes
description: Use when writing or updating release notes before a release. Triggers on requests like "write the release notes" or "tidy up the changelog".
---

# release-notes — writing release notes

## 1. Where to write

Release notes are written in `CHANGELOG.md` at the repo root.

Release notes are written in English, because all of our customers are in the US.

## 2. What to include

- Collect the PR list with `scripts/collect-prs.sh <previous tag>`.
- Classify entries by PR label (`feat`, `fix`, `chore`) (rationale: [ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md)).
- Leave PRs labeled `skip-changelog` out of the notes.
- Do not generate the note body with an auto-summarizing LLM — it was rejected as alternative B in the ADR-0007 review.
- Exception: for a security-patch release, write the entries as a single line, "Security fixes", and add CVE details only after the public disclosure date.

## 3. Format

- Write version headings as `## vX.Y.Z (YYYY-MM-DD)`.
- Do not bump version numbers by hand — the tag script checks the version in `CHANGELOG.md` against the tag and stops the release if they differ.

## 4. When to write

- Merge the release notes into main by the day before the release.
- After the 2026-07 incident, we learned that pushing a `git tag` locally first makes the CI release job run twice, which publishes the notes twice. Only CI cuts tags.

## 5. Wrap-up

- Open the draft notes as a PR and get approval from one reviewer.
- Write the release notes on release day, after the tag has been created.
