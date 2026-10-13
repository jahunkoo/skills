Not quite. Flipping only the default would also turn off activity emails for existing users, not just new signups. I made the change together with a backfill, and all 4 tests pass.

**Why the one-line change isn't enough:** stored records only keep the fields a user changed (`compact` in `src/prefs.js`). Everything else is read from `DEFAULTS` at read time. So `u1`, `u2`, `u4` and `u5` have no `notify` field in `data/prefs.json`; they get `true` only because that's the default. Change the default to `false` and those four silently stop getting activity emails (`src/mailer.js` filters on `notify`). Only `u3`, who already opted out, would be unaffected. The repo has already dealt with this once: commit `21826f4` backfilled `digest` before `9a7a186` changed its default.

**What I changed (not committed):**
- `scripts/backfill-notify.js`: a one-off script modelled on `backfill-digest.js`. It writes `notify: true` into every stored record that doesn't have it.
- `data/prefs.json`: I ran the script on it. u1, u2, u4 and u5 now have `notify: true` saved, and u3 keeps `false`.
- `src/prefs.js`: the default is now `notify: false`.
- `test/prefs.test.js`: the existing "notify off" test assumed an empty record means notify is on, so I made `notify: true` explicit there. I also added a test that a new signup (empty record) gets no activity email.

After the flip, a saved `notify: true` is kept, because `compact` only drops values that equal the new default (`false`). So the backfilled users keep their emails even after they change other settings.

**Before you ship:**
- The backfill must run against the real data before the new default goes live, or there's a window where existing users read `false`. I'd split this into two commits, backfill first and then the default, like the digest change. Tell me if you want me to make those commits.
- This makes activity email opt-in for new users, so they'll need a visible way to turn `notify` on. If they don't have one, almost no new users will get these emails.