No. Leave `DEFAULTS.notify` as `true` until existing records are migrated. A one-line flip would turn off activity mail for current users who never set the field.

Stored prefs keep only values that differ from `DEFAULTS`. `readPrefs` fills anything missing from that object, and `compact` drops a value again once it matches the default. With `notify: true` today, an omitted `notify` means opted in.

In `data/prefs.json`, only `u3` has `"notify": false`. `u1`, `u2`, `u4`, and `u5` omit it, so they currently get mail. `onSignup` stores `{}` for the same reason. The test "users with notify off get no email" expects that: user `a` with `{}` is a recipient, and user `b` with `notify: false` is not.

After setting the default to `false`, those omitted fields would read as off, and `recipients` would skip those users. On the next `store.set`, `compact` would also delete an explicit `notify: false`, because it would equal the new default.

New accounts would behave as you want, because `onSignup` still writes `{}` and that would then read as `notify: false`. Existing accounts would not.

To opt in only new signups, freeze the old meaning first, on the raw records, before changing the default:

1. For every stored object that has no `notify` key, set `notify: true`. Do this on the JSON itself. `readPrefs` and `store.set` cannot do it: after the default changes, a missing key already looks like `false`, and before the change `compact` would throw away `true`.
2. Then set `DEFAULTS.notify` to `false`.
3. Update the mailer test so an empty record is not a recipient. Someone who still gets mail must have `notify: true` stored.

`scripts/backfill-digest.js` is the same kind of one-off write. The digest backfill stamped a value onto old rows and left the default alone, so only existing users changed. This case is the reverse: stamp the old default onto old rows, then change the default so only new signups change.