Target: making activity emails opt-in for new signups by changing `DEFAULTS.notify` to `false`.

That would work for new users: [signup](src/signup.js:2) uses the defaults, and [mailer](src/mailer.js:2) checks `notify`. But existing records omit values equal to the current default. Four users in [prefs.json](data/prefs.json:1) have no `notify` field, so a direct change would stop their emails too.

Backfill `notify: true` for existing records where it is absent, preserving explicit `false`, then change the default and update the tests. Write the backfill directly to stored records: [compact](src/prefs.js:8) would discard `true` while it remains the default. The baseline tests pass (3/3). I made no changes because this was a request for a verdict.

**Verdict: Proceed with the backfill, default change, and tests together.**