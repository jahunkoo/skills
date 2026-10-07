I cleaned up `prompts/release-notes/SKILL.md` and applied the changes directly, as you asked. It went from 41 to 35 lines. Nothing is committed.

## Deleted

| Line (orig.) | Type | Excerpt | Evidence |
|---|---|---|---|
| L10 | History | "used to be written directly on a Notion page … at a 2026-05 meeting …" | Kept only the conclusion: "Write release notes in `CHANGELOG.md` at the repo root." |
| L12 | Rebuttal | "An older guide suggested … Spanish, but in fact …" | Now states the rule plainly and keeps the reason: "Write release notes in English, because all of our customers are in the US." |
| L17 | Superseded rule | "Change entries are sourced from commit messages (ADR-0003)" | `docs/adr/0003` is marked `superseded`, replaced by ADR-0007 (`accepted`). |
| L23 | Meta note | "NB: … still being verified (TODO: confirm with the owner)" | It doesn't change what the agent does. The criteria it refers to are already backed by the accepted ADR-0007. |
| L27 | Dead reference | "follow `docs/format-guide.md`" | `docs/` contains only `adr/`, so that file doesn't exist. |
| L40 | Duplicate | "Do not include PRs whose label is `skip-changelog`…" | Same rule as §2 L19, which I kept. |

## Unclear: left unchanged
1. **Contradiction about when to write the notes. Please decide this first.** §4 says "Merge the release notes into main by the day before the release." §5 says "Write the release notes on release day, after the tag has been created." Both can't be true. No ADR or later decision says which one is current, so I kept both. Until one is chosen, an agent will follow one of them and break the other. Your options:
   - (a) keep the day-before merge and delete the §5 line;
   - (b) keep writing after the tag on release day and delete the §4 line;
   - (c) clarify that they are separate steps, for example a draft before release and a final version after the tag.

   Related: §3 says the tag script checks `CHANGELOG.md` against the tag. That suggests the notes must exist before the tag, which leans towards (a). This is only my inference.
2. **"the tag script" (§3 L25)** gives no path, and there's no such script in this repo. It isn't a path the agent is told to use, and it may live in CI, so I kept it.

## Kept on purpose (even though they look like residue)
- §2 "Do not generate … with an auto-summarizing LLM — rejected as alternative B": this is a rejected alternative, and ADR-0007 confirms it.
- §2 "Exception: for a security-patch release…": a conditional exception.
- §2 the ADR-0007 link: a rationale link. It resolves correctly from the file's location.
- §4 "After the 2026-07 incident … Only CI cuts tags.": a warning about a known trap (running the release job twice), added on purpose in the latest commit (dd00c8d). I left the wording as is.
- §1 "because all of our customers are in the US": the reason behind the language rule.

## Verification
- The ADR-0007 link and `scripts/collect-prs.sh` both resolve.
- All 13 instructions from the original are still there (counting the conflicting pair as two). The deleted lines were either duplicates, superseded, a dead reference, or not instructions at all.

Deleted 6 (2 history/rebuttal · 1 superseded · 1 meta note · 1 dead reference · 1 duplicate) · Kept 13 · Needs decision 1

**Suggestion:** if a format guide is still needed, either add a real `docs/format-guide.md` or put the format rules directly in §3. I didn't add any new rules myself.