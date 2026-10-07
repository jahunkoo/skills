Distilled [the release-notes skill](prompts/release-notes/SKILL.md) from 41 lines to 15. It now follows the accepted ADR’s PR-title rule and removes duplicate instructions, the missing format-guide link, and the conflicting instruction to write notes after tagging. It retains the security-release, review, and CI tagging rules.

`git diff --check` passes.