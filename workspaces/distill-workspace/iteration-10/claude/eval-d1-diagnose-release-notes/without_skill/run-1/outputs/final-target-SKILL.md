---
name: release-notes
description: Use when writing or updating release notes before a release. Triggers on requests like "write the release notes" or "tidy up the changelog".
---

# release-notes — writing release notes

Write release notes in English, in `CHANGELOG.md` at the repo root. All customers are in the US.

## Content

Follows [ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md).

- Collect the merged PRs with `scripts/collect-prs.sh <previous tag>`.
- Use each PR's title as the entry text, grouped by PR label (`feat`, `fix`, `chore`).
- Leave out PRs labeled `skip-changelog`.
- Write the entries yourself from the PR titles; don't auto-summarize them. LLM summaries were rejected because they introduced inaccurate entries that cost more to review.
- Security-patch releases: the only entry is "Security fixes". Add CVE details only after the public disclosure date.

## Format

- Version heading: `## vX.Y.Z (YYYY-MM-DD)`.
- Don't bump version numbers by hand. The tag script compares the version in `CHANGELOG.md` with the tag and stops the release if they differ.

## Process

- Open the notes as a PR and get approval from one reviewer.
- Merge into main by the day before the release.
- Never create or push a `git tag`; only CI cuts tags. A locally pushed tag makes the CI release job run twice and publishes the notes twice.
