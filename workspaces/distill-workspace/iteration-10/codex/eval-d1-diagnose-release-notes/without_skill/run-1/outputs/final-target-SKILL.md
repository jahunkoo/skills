---
name: release-notes
description: Write or update release notes before a release, including changelog cleanup.
---

# Release notes

Write release notes in English in the repository root `CHANGELOG.md`.

- Run `scripts/collect-prs.sh <previous tag>` to list merged PRs and their labels.
- Use each PR title as its entry text. Group entries by PR label (`feat`, `fix`, `chore`); omit PRs labeled `skip-changelog`. Do not generate entries with LLM summaries. See [ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md).
- For a security-patch release, use a single `Security fixes` entry. Add CVE details only after public disclosure.
- Use a version heading in the form `## vX.Y.Z (YYYY-MM-DD)`. Use the planned release version rather than bumping it by hand; the heading must match the release tag.
- Open the draft notes as a PR, get approval from one reviewer, and merge them into main by the day before release.
- Only CI creates release tags; pushing one yourself can publish the notes twice.
