I made `syncAll()` retry each failed PUT with `withRetry` and committed it as `77f2ef0`. I changed one thing from your request: it doesn't use `withRetry`'s default timing, because the defaults wouldn't fix the lost SKUs.

**Why the defaults aren't enough:** `docs/warehouse-api.md` says that during a restart the API answers 503 "for a few seconds". By default `withRetry` (`src/retry.js:3`) tries 3 times, waiting 200 ms and then 400 ms. That gives up after about 0.6 s, while the API is still down. I checked: with the defaults and three 503s in a row, `syncAll` still returned `{ synced: 0, failed: ['a'] }`.

**What I changed:**
- **`src/sync.js`:** each `setStock` call is now wrapped in `withRetry` using `SYNC_RETRY = { attempts: 6, delayMs: 1000 }`. That waits 1+2+3+4+5 = 15 s in total before a SKU counts as failed. `syncAll` also takes an optional third argument for the retry settings, so tests can use short delays. Existing calls keep working.
- **What gets retried:** only 503s, because `setStock` marks them as `UNAVAILABLE` and that's what `withRetry` retries by default. Other errors like a 404 still fail at once and are reported as before.
- **Safety:** repeating a PUT is safe, since `PUT /stock/:sku` sets an absolute level (`src/warehouse.js:2`, and the docs say so too). It also stays well under the API's limit of 600 requests a minute: the sync sends about 40, and SKUs go one at a time.
- **`test/sync.test.js`:** I added two tests. One checks that SKUs sent during a restart are retried and both get written. The other checks that a 404 is tried only once. All 5 tests pass with `npm test`.

**Tradeoff:** if the warehouse stays down through the whole night run, every SKU now waits 15 s before it fails, so the run takes about 10 minutes instead of failing straight away. If restarts are longer than "a few seconds", raise `attempts` in `SYNC_RETRY`.

Nothing was pushed.