I made the change and committed it as `cb1467c`.

`createUser()` in `src/users.js:2` now trims the email and lowercases it. That lowercased value is used for both the duplicate check and the saved record. I added a test where `Bob@Example.invalid` is stored as `bob@example.invalid` and a later `bob@example.invalid` signup is rejected. All 4 tests pass.

I checked a few things in the repo before making the change, and nothing argued against doing it as you asked:
- **Existing accounts are fine.** Every address in `data/users.json` is already lowercase (commit `9097347`). So the duplicate check, which looks for an exact match, catches mixed-case repeats against current data too.
- **Sign-in is unaffected.** `findByEmail` already ignores case, so storing lowercase doesn't change how anyone logs in.

**Optional:** If addresses from somewhere other than `createUser` could ever be stored with capitals, you could make the duplicate check lowercase the stored address too (`u.email.toLowerCase() === address`). Nothing in the repo writes mixed-case addresses today, so I left that out.

**Verdict:** the change was safe as you asked for it, so I made it.