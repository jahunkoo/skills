---
name: release-notes
description: Use when writing or updating release notes before a release. Triggers on requests like "write the release notes" or "tidy up the changelog".
---

# release-notes — writing release notes

Release notes live in `CHANGELOG.md` at the repo root, written in English (all customers are in the US).

## Content

- Collect merged PRs with `scripts/collect-prs.sh <previous tag>`.
- Use each PR's title as the entry text, grouped under its label (`feat`, `fix`, `chore`). Don't write your own summaries — LLM-generated entries were rejected for inaccuracy ([ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md)).
- Leave out PRs labeled `skip-changelog`.
- Security-patch release: write a single entry, "Security fixes". Add CVE details only after the public disclosure date.

## Format

- Version heading: `## vX.Y.Z (YYYY-MM-DD)`.
- Don't bump version numbers by hand — the tag script stops the release if the `CHANGELOG.md` version doesn't match the tag.

## Process

- Open the notes as a PR, get one reviewer's approval, and merge into main by the day before the release.
- Never create or push a git tag yourself; only CI cuts tags. A locally pushed tag makes the release job run twice and publishes the notes twice.
