The requested distill skill requires a diagnostic report and approval before editing. I left [prompts/release-notes/SKILL.md](prompts/release-notes/SKILL.md) unchanged.

| Delete or trim | Type | Evidence |
|---|---|---|
| Line 10: former Notion workflow and meeting history; keep the `CHANGELOG.md` instruction | History | The current destination is stated in the same sentence. |
| Line 12: older Spanish guidance; keep English and its US-customer rationale | Rebuttal | The sentence states the current language. |
| Line 17: commit-message source | Superseded rule | [ADR-0003](docs/adr/0003-changelog-source.md) is superseded by accepted ADR-0007. |
| Line 23: “still being verified” TODO | Meta note | [ADR-0007](docs/adr/0007-changelog-from-pr-labels.md) is accepted. |
| Line 27: `docs/format-guide.md` instruction | Dead reference | The file does not exist in the repository. |
| Line 40: `skip-changelog` instruction | Duplicate | Line 19 already states it. |

**Decision needed:** Lines 34 and 41 conflict: merge the notes by the day before release, or write them on release day after the tag. Both should remain until you choose the intended timing.

**Intentionally kept:** Line 18’s ADR rationale; line 20’s rejected LLM alternative; line 21’s security exception; line 30’s tag-script rationale; and line 35’s incident warning, which was added deliberately after the incident. The current `CHANGELOG.md` location and English-language rationale also survive the proposed trims.

If approved, the file would go from 41 to approximately 35 lines, with all 16 identified behavioral instructions retained, including the unresolved pair. No changes were applied because the skill’s approval gate says a request to “distill” alone is not approval to edit.

Deleted 0 (approval pending) · Kept 41 lines · Needs decision 1