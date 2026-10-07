The distill skill requires a diagnostic report and approval before editing. I made no changes to [SKILL.md](prompts/release-notes/SKILL.md).

### Decision needed

- **Timing conflict, lines 34 and 41:** one rule says to merge the notes by the day before release; another says to write them on release day after the tag is created. Both must stay until the intended schedule is chosen.

### Proposed deletions

| Location | Type | Evidence |
|---|---|---|
| Line 10, “used to be written directly on a Notion page…” | History | Keep the instruction to write in root `CHANGELOG.md`; the former location does not affect it. |
| Line 12, “An older guide suggested…Spanish…” | Rebuttal | Keep the English instruction and its customer rationale. |
| Line 17, commit-message source | Superseded rule | [ADR-0003](docs/adr/0003-changelog-source.md) is marked superseded by accepted [ADR-0007](docs/adr/0007-changelog-from-pr-labels.md). |
| Line 23, “NB…still being verified (TODO…)” | Meta note | ADR-0007 records the classification decision as accepted. |
| Line 27, `docs/format-guide.md` | Dead reference | The file is absent from the repository. |
| Line 40, `skip-changelog` instruction | Duplicate | Line 19 already states the same rule. |

### Intentionally kept

- Line 12’s US customer explanation gives the reason for English.
- Line 18’s ADR-0007 link documents the current classification decision.
- Line 20 records a rejected LLM alternative.
- Line 21 contains a security-release exception and a disclosure condition.
- Line 30 explains why version numbers must not be bumped by hand; the cited tag script may run outside this repository.
- Line 35 warns of a duplicate-publish trap. It was also added deliberately after the incident, according to git history.
- Lines 34 and 41 remain together pending the timing decision.

**Proposed effect:** 41 → 35 lines, preserving 13 current or unresolved instruction-bearing lines. One possible later improvement is to state ADR-0007’s PR-title source explicitly; that would add guidance, so it is outside this deletion-only pass.

Deleted 0 (6 proposed: history 1, rebuttal 1, superseded rule 1, meta note 1, dead reference 1, duplicate 1) · Kept 13 instruction-bearing lines · Needs decision 1