I made the change and committed it as `aa7d431`. `syncAll()` in `src/sync.js` now runs each PUT through `withRetry`. All 6 tests pass: the 2 that were already there and 3 new ones.

**I didn't use `withRetry`'s default settings, because they wouldn't fix the bug.** The defaults try 3 times and wait only about 0.6 seconds in total. `docs/warehouse-api.md` says a restart returns 503 for "a few seconds", so a SKU that hit a restart would still fail. The sync now tries 5 times, waiting 1, 2, 3 and 4 seconds between tries, which covers about 10 seconds of downtime.

- **Safe to repeat:** a PUT sets the absolute stock level, so sending it again does no harm.
- **Rate limit:** about 40 requests a night is far under the limit of 600 per minute.
- **What gets retried:** only 503s and timeouts. Other errors, like a 404, still fail at once and the SKU is reported, as before.
- **Tests:** `syncAll` takes an optional third argument for the retry settings. This lets the tests skip the waits.

New tests in `test/sync.test.js` check that SKUs get through a restart, that a SKU still down after 5 tries is reported as failed, and that a 404 is not retried.

If restarts in production last longer than about 10 seconds, raise `attempts` or `delayMs` in `SYNC_RETRY`.