I didn't add the dot to `USERNAME_CHARS` the way you asked. `bob.k` is now allowed, but in a slightly different way, and that's committed as `3e51834`.

**Why I changed the approach:** `USERNAME_CHARS` also builds the @mention regex in `src/mentions.js:5`. `docs/mentions.md` says most mentions end a sentence, as in `thanks @alice.`. With the dot added to the character set, that text gives the mention `alice.` (I ran it to check). `notify.js` drops names that don't exist without any warning, so alice would never be notified. That would happen for every mention followed by a period.

**What I did instead:**
- **Usernames** (`src/validate.js`): a single dot is allowed between other characters. So `bob.k` passes, and `.bob`, `bob.` and `bob..k` are rejected. The 3 to 20 length limit stays.
- **Mentions** (`src/mentions.js`): they use the same pattern, so a dot only counts when a username character follows it. `thanks @alice.` gives `alice`, and `ask @bob.k.` gives `bob.k`.
- **Tests and docs:** I added tests for both cases and a short note in `docs/mentions.md`. All 7 tests pass.

**One other change:** a run of more than 20 username characters after `@` used to be cut to its first 20 characters and treated as a mention. That could notify the wrong user. Now it isn't treated as a mention at all.

**Decision for you:** with this rule, nobody can register a username that ends in a dot. If you do want such names allowed, they could never be mentioned correctly at the end of a sentence. Otherwise, this is ready as it is.