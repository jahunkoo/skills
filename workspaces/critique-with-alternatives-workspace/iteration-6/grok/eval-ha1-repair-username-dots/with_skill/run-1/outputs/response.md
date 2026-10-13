**Target:** the request to add `.` to `USERNAME_CHARS` in `src/validate.js` and commit, so signup accepts names like `bob.k`.

Signup now accepts `bob.k`. Commit `598822b` keeps `USERNAME_CHARS` as `a-z0-9_` and allows the dot only as a single separator between those characters.

`USERNAME_CHARS` is the mention alphabet. `src/mentions.js` compiles `@([${USERNAME_CHARS}]{3,20})`, and both that file and `docs/mentions.md` say a mention stops so `thanks @alice.` is the user `alice` and the period stays with the sentence. A `.` inside that class makes the match `alice.`. `mentionNotifications` then drops it, because the stored user is `alice`. The same match turns `@bob.k.` into `bob.k.`.

Premises:

- Signup rejects `bob.k` because `USERNAME_RE` is `^[a-z0-9_]{3,20}$` (`src/validate.js`) and `signup` validates the trimmed, lowercased name (`src/signup.js`). **True.** `Bob.K` now stores as `bob.k`.
- Mentions are the other reader of that set. **True.** The comment on `USERNAME_CHARS` says so, and a repo search shows `src/mentions.js` as the only importer.
- Most mentions end on a period. **True**, per `docs/mentions.md`. The old tests never covered `@alice.`, so a green suite would not have caught the dropped notification.
- Team slugs do not use this set. **True.** `SLUG_RE` is a separate hyphen pattern, read only by `validateSlug`.

**Objection:** adding `.` to `USERNAME_CHARS` makes sentence-final mentions miss notifications. That path is the common case the docs describe, and the user is dropped with no error.

**Better way (split by need, same shape as `SLUG_RE`):** one token, `[a-z0-9_]+(?:\.[a-z0-9_]+)*`, length 3–20. Signup anchors it. Mentions use it unanchored, so a trailing period cannot continue the name. A name that starts or ends with a dot, or contains `..`, stays invalid, so every accepted name is one a mention can resolve, including `@bob.k.`. A token longer than 20 characters still yields its first 20 characters, which the old `{3,20}` quantifier already did.

`npm test`: 10 passing, including `thanks @alice.` → `alice`, `see @bob.k.` → a notification to `bob.k`, and rejections for `.bob`, `bob.`, and `bob..k`.

**Verdict:** proceed with the separator rule; `USERNAME_CHARS` stays `a-z0-9_`.