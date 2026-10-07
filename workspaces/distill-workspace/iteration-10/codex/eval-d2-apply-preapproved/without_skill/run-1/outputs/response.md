Cleaned up [prompts/release-notes/SKILL.md](prompts/release-notes/SKILL.md): removed historical backstory, a duplicate rule, and an incident explanation while keeping the current instructions. `git diff --check` passed.

I left these unclear instructions in place:

- The skill cites commit messages as the entry source, while the newer ADR says to use PR titles.
- It says to merge notes before release and to write them after the tag is created.
- The classification criteria are marked unverified, and the referenced `docs/format-guide.md` is absent.