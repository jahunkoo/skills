**Target:** flipping `DEFAULTS.notify` in `src/prefs.js` from `true` to `false` so new signups get activity email only after they opt in.

That edit would also turn email off for the people already stored. Leave the default as it is.

**Goal:** new signups receive activity email only after they opt in.

## Premises

- **`notify` defaults to `true`.** True. `src/prefs.js:1` is `DEFAULTS = { notify: true, digest: 'weekly', theme: 'light' }`.
- **The default is applied only when someone signs up.** False. `readPrefs` merges `DEFAULTS` on every read (`src/prefs.js:3-5`). `onSignup` stores `{}` (`src/signup.js:2-3`). `compact` drops any field equal to the default (`src/prefs.js:8-9`), so an opted-in user is saved with no `notify` key at all.
- **Existing rows already record a notify choice.** False. In `data/prefs.json`, only `u3` has `"notify": false`. `u1`, `u2`, `u4`, and `u5` omit it. Resolving the file today gives those four `notify: true` and recipients `['u1', 'u2', 'u4', 'u5']`. Treating a missing key as off leaves recipients `[]`.
- **The mailer sends only when `notify` is on.** True. `recipients` keeps ids where `store.get(id).notify` is true (`src/mailer.js:3`), and `store.get` is `readPrefs` (`src/store.js:7`).
- **Tests lock “missing notify means on.”** True. `test/prefs.test.js:15-18` expects user `a` stored as `{}` to get mail and user `b` with `notify: false` to get none. After this flip, that assertion fails.
- **This repository has already been through this.** True. Commit `21826f4` says stored records leave out values equal to the default, so changing a default changes it for every user who never touched the setting. Digest was written into those rows first; `9a7a186` changed the digest default only after that.

## Objection

Changing `DEFAULTS.notify` changes the meaning of every saved row that left the key out. All four current recipients lose activity email, and the mailer test fails. A later `store.set` runs `compact` against the new default, so `notify: false` is then omitted and the old opt-in is gone from the file.

## Better way

**Keep the contract.** Replace the edit in `src/prefs.js` with one in `src/signup.js`: call `store.set(userId, { notify: false })`, and leave `DEFAULTS.notify` as `true`. Update the signup comment so it matches that write.

Checked against the repo:

- `onSignup` is the only `store.set` call, so this is the only new-user write.
- `store.set` compacts (`src/store.js:9`). With the default still `true`, `notify: false` is kept, and `readPrefs` returns off, so `recipients` skips that user.
- A later opt-in, `store.set(userId, { notify: true })`, matches the default, so `compact` drops the key and the next read is on. The mailer includes them again.
- `u1`, `u2`, `u4`, and `u5` still resolve to on. `u3` stays off. `test/prefs.test.js:15-18` still passes. `data/prefs.json` stays untouched.

The digest sequence (write the old value into raw rows that lack the key, then change the default, then update the empty-record test) is what a change to `DEFAULTS` itself requires. This goal is met without that migration.

**Optional:** add a test that `onSignup` stores `{ notify: false }` and that this user is absent from `recipients`.

**Verdict:** Stop. Leave `DEFAULTS.notify` true, and store `{ notify: false }` from `onSignup`.

Should I opt out new signups in `onSignup` and leave `DEFAULTS.notify` true?