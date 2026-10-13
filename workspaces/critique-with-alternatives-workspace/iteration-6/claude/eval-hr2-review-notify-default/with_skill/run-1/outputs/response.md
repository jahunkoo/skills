I'm reviewing your plan to change `DEFAULTS.notify` in `src/prefs.js:1` from `true` to `false` so that only new signups stop getting activity emails until they opt in.

**Short answer: no, not as a one-line change.** It would stop emails for existing users too, not just new signups.

**Checking the plan's assumptions against the code**

- **"Changing the default only affects new signups." False.** Stored records keep only the fields a user changed, and everything else is filled in from `DEFAULTS` on each read (`src/prefs.js:3-5`, `compact` at `:8-10`). No record in `data/prefs.json` has `notify: true`, because `true` is the current default and gets compacted away. I simulated the flipped default against the current data without writing anything:
  ```
  u1 now true after flip false
  u2 now true after flip false
  u3 now false after flip false
  u4 now true after flip false
  u5 now true after flip false
  ```
  So 4 of the 5 existing users would silently stop getting activity emails (`src/mailer.js:3` filters on `notify`). The repo has hit this before: commit `21826f4` says "changing a default changes it for every user who never touched the setting." That's why `digest` was backfilled before its default changed in `9a7a186`. Your plan skips that step.
- **"New signups get the default." True.** `onSignup` stores `{}` (`src/signup.js:3`), so a new user does pick up whatever `DEFAULTS` says.
- **"Nothing else depends on `notify` being true by default." False.** The test at `test/prefs.test.js:15-18` expects user `a: {}` to receive email. It passes now (3 of 3 pass) and would fail after the flip.

**Better way (replaces the one-line change)**

Leave `DEFAULTS` alone and set the opt-out at signup: in `src/signup.js:3`, change `store.set(userId, {})` to `store.set(userId, { notify: false })`. Since `false` differs from the default, `compact` keeps it in the stored record. New users start opted out, existing users keep their current behaviour, and no stored data changes. Opting in later stores `notify: true`, which `compact` then drops, and the result reads back as `true`. That's correct. The existing tests still pass. Add one test that `onSignup` produces a user that `recipients` excludes.

**Optional**

- If you want `DEFAULTS.notify` itself to read `false`, for example so the code says what new users get, follow the `digest` precedent instead. First write `notify: true` into every stored record that has no `notify`, the same way `scripts/backfill-digest.js` did for `digest`. Back up `data/prefs.json` before running it, because that write is the step you can't undo. Then flip the default, and update the test at `test/prefs.test.js:16` to `a: { notify: true }`. This also works, but it means a data migration, while the signup change doesn't need one.

**Verdict:** proceed with changes. Make the opt-out in `onSignup` (`src/signup.js:3`) rather than in `DEFAULTS`, or backfill `notify: true` before flipping the default.

I haven't changed anything in the repository. If you want me to go ahead, the question is: should I set `notify: false` in `onSignup`, leave `DEFAULTS` as it is, and add a test for it?