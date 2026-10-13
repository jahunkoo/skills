**Target:** wrapping `main()` in `scripts/import-orders.js` in a try/catch that logs the error and exits 0, so the scheduler stops flagging the nightly import as failed.

That would mark a failed import as success. The page would stop, including for a bad export, and `publish-orders` would send the previous night's orders to the fulfilment dashboard. The repeated failure is a late partner file, and the scheduler already has retries for a failure that clears on its own.

### Premises

1. **The page is the non-zero exit. True.** `main()` at `scripts/import-orders.js:4-10` has no handler. An uncaught throw exits 1 (Node v24.16.0). `deploy/schedule.yml:1` pages on-call on a non-zero exit, and `docs/jobs.md:3-4` says that page is the only alert for this import.

2. **Every recent failure is a false alarm. False.** `notes/job-failures.txt:3-4` lists 10 nights. Nine are `NoExportYetError` because `/data/partner/orders.csv` arrived 20 to 70 minutes later (`src/importer.js:5-7`). One is `bad row 4: o-17,,1999`, an empty customer, which `parseOrders` rejects at `src/importer.js:17`. Exit 0 would clear the page for that bad export as well.

3. **Exit 0 leaves the rest of the night correct. False.** `publish-orders` runs only when import-orders exits 0 (`deploy/schedule.yml:11-13`, `docs/jobs.md:5-6`). It publishes whatever is already in `ORDERS_OUT` (`scripts/publish-orders.js:1-4`). `main()` writes that file only after a successful parse (`scripts/import-orders.js:5-6`). A caught error leaves the previous file in place, and the jobs doc says publish would then send the previous night's orders again.

4. **Nothing here can absorb a failure that clears itself. False.** `docs/jobs.md:7-8` says to use the scheduler's `retries`, as `sync-rates` does (`deploy/schedule.yml:3-7`: `retries: 2`, `retry_delay: 30m`).

5. **Those same retry numbers cover this job. False.** sync-rates is down for a few minutes (`scripts/sync-rates.js:1-2`). This file is late by up to 70 minutes. The repo does not say whether `retries: 2` means two extra attempts or two runs in total, so the last attempt falls at 30 or 60 minutes.

### What the try/catch would change

- The exit code the scheduler pages on, and the exit code `publish-orders` waits for.
- The orders file, which would stay stale while publish treats the job as success.
- The late export: exit 0 does not run the import again, so a file that arrives 20 to 70 minutes later is never loaded that night.

### Better way

Replace the try/catch. On `import-orders` in `deploy/schedule.yml`, add `retries: 3` and `retry_delay: 40m`. Leave `main()` throwing, so a real error still exits non-zero.

This is the retry hook the jobs doc already points at, with a window for this file. Three runs, 40 minutes apart, put the last attempt at 80 minutes if `retries` counts total runs, or at 120 minutes if it counts extra attempts. Both are past the latest arrival in the notes (70 minutes). sync-rates' `2` and `30m` end at 30 or 60 minutes.

Checked against the repo:

- A late file is read on a later attempt, written to `ORDERS_OUT`, and the process exits 0. The scheduler records success and does not page. `publish-orders` then publishes that night's orders. The write happens only after a full parse (`scripts/import-orders.js:5-6`), so a failed attempt leaves no partial file.
- A bad row, or a file that never arrives, exits non-zero on every attempt. On-call is still paged, and `publish-orders` does not run.
- Assumption: `publish-orders` follows the job's final exit status after retries. In this file, retries appear only on `sync-rates` (no dependent) and `after` appears only on `publish-orders` (no retries), so the two are not combined here. The jobs doc treats them as one model: retry a failure that clears, and publish only after exit 0. If a later success does not release `after`, the file would import and the dashboard would stay on the old orders. The wait would then belong in `import-orders`: poll for the export for about 80 minutes, write it, and exit 0 only after that write. Same exit-code contract, no new scheduler behavior.

### Optional

One line in `docs/jobs.md` noting that import-orders retries because the partner file is often 20 to 70 minutes late.

**Verdict:** Stop. Add `retries: 3` and `retry_delay: 40m` to `import-orders` in `deploy/schedule.yml`, and leave `main()` exiting non-zero on error.

Should I add those two schedule fields and leave `scripts/import-orders.js` unchanged?