---
name: release-notes
description: Write or update release notes in the repository changelog before a release.
---

# Release notes

Write release notes in English in the root `CHANGELOG.md`. Open a PR for the draft notes, obtain at least one reviewer's approval, and merge it by the day before the release.

- Collect merged PRs with `scripts/collect-prs.sh <previous-tag>`.
- Use each PR title as its entry text. Group entries by the `feat`, `fix`, and `chore` PR labels; omit PRs labeled `skip-changelog`. See [ADR-0007](../../docs/adr/0007-changelog-from-pr-labels.md).
- Do not generate entries from commit messages or LLM summaries.
- Use version headings in the form `## vX.Y.Z (YYYY-MM-DD)` and follow the existing changelog's section format. Use the planned release version; do not bump it independently.
- For a security-patch release, use a single entry, `Security fixes`. Add CVE details only after public disclosure.

Only CI creates release tags. Do not create or push a tag locally.
