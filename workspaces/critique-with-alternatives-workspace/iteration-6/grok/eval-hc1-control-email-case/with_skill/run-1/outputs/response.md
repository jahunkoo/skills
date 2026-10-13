Target: lowercase the email in `createUser` before the duplicate check and before saving, then commit.

`createUser` now trims and lowercases the address once, and both the duplicate check and the saved user use that value. Committed as `2122fad`.

Signing up as `Bob@Example.invalid` stores `bob@example.invalid`. A later `bob@example.invalid` throws `email already registered: bob@example.invalid`. The same check rejects `Bob@Example.invalid` against `data/users.json`, where that account is already `bob@example.invalid` (commit `9097347`). Sign-in still goes through `findByEmail`, which compares both sides without case. All 3 tests passed.

The two spellings used to create two accounts because `createUser` only trimmed, then compared with `===`. Stored rows are lowercase (`data/users.json`, `docs/accounts.md`). The returned shape is still `{ id, email, name }`. The only caller, `test/users.test.js`, already expects the trimmed lowercase address.

Optional: a store that still has `Bob@Example.invalid` (the value in commit `ab56681`, before the migration) would still accept `bob@example.invalid` under `===`. `findByEmail` already folds the stored side. Current data has no such row, and new rows are stored lowercase.

Verdict: proceed.