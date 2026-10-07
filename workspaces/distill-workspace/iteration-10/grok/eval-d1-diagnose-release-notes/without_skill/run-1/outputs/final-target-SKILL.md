---
name: release-notes
description: Use when writing or updating release notes before a release. Triggers on requests like "write the release notes" or "tidy up the changelog".
---

# release-notes — writing release notes

Write release notes in English in `CHANGELOG.md` at the repo root.

## What to include

- Collect the PR list with `scripts/collect-prs.sh <previous tag>`.
- Use the PR title as the entry text. Classify entries by PR label (`feat`, `fix`, `chore`) ([ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md)).
- Leave out PRs labeled `skip-changelog`.
- Do not auto-summarize entry text.
- For a security-patch release, write the entries as a single line, "Security fixes", and add CVE details only after the public disclosure date.

## Format

Follow the structure in `CHANGELOG.md`.

- Write version headings as `## vX.Y.Z (YYYY-MM-DD)`.
- Do not bump version numbers by hand — the tag script checks the version in `CHANGELOG.md` against the tag and stops the release if they differ.

## When to write

- Open the draft notes as a PR and get approval from one reviewer.
- Merge the release notes into main by the day before the release.
- Do not push a `git tag` locally. Only CI cuts tags. A locally pushed tag makes the CI release job run twice and publish the notes twice.
