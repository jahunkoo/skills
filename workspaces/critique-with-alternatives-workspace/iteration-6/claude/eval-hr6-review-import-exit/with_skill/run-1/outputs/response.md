**Target:** your plan to wrap `main()` in `scripts/import-orders.js` in a try/catch that logs the error and exits 0, so the scheduler stops flagging the nightly import.

My recommendation is to not do this. It would stop the alerts, but it would also republish stale orders to the dashboard and hide the one failure that actually needs attention. Adding scheduler retries handles the real cause.

## What I checked

- **Exiting 0 stops the alert: true.** `deploy/schedule.yml:1` says the scheduler pages on-call when a job exits non-zero.
- **Nothing else depends on the exit code: false.** `publish-orders` has `after: import-orders # runs only if import-orders exited 0` (`deploy/schedule.yml:13`). It publishes whatever is in `/data/orders.json` (`scripts/publish-orders.js:1,4`). When the import fails, `writeFileSync` in `import-orders.js:6` never runs, so that file still holds the previous night's orders. `docs/jobs.md:5-6` describes exactly this: after a failed import it "would publish the previous night's orders again". With your change, every failed night would quietly put yesterday's orders back on the fulfilment dashboard.
- **The failures are noise: mostly true, not entirely.** `notes/job-failures.txt` lists 30 nights: 9 failures are `NoExportYetError` because the partner file came 20 to 70 minutes late. That's temporary and fixes itself. One failure is `bad row 4: o-17,,1999`, which is real bad data from the partner that someone needs to look at. `docs/jobs.md:3-4` says the page is the only alert for this job, so a blanket catch would make that kind of failure invisible.
- **The repo already handles temporary failures: true.** `docs/jobs.md:7-8` says jobs whose failures clear up on their own should use the scheduler's `retries`, and `sync-rates` does this (`deploy/schedule.yml:6-7`). `import-orders` has no retries.

## Objections and a better way

1. **Exit 0 starts publish-orders on stale data.** Keep the non-zero exit so `publish-orders` stays blocked when there's no fresh import.
2. **It hides real data errors.** Don't catch everything. A malformed export should keep paging.
3. **Better way: reuse the existing retries.** Use this instead of the try/catch, in `deploy/schedule.yml`:
   ```yaml
   import-orders:
     run: node scripts/import-orders.js
     at: "02:00"
     retries: 3
     retry_delay: 30m
   ```
   That gives attempts at 02:00, 02:30, 03:00 and 03:30, which covers the 20 to 70 minute delays in the notes. Late-file nights would succeed on a retry with fresh data, so nothing pages and `publish-orders` publishes the right orders. A bad row would still page, about 90 minutes later than now. No change to `import-orders.js` is needed.

   I couldn't verify one thing from the repo: whether the scheduler starts an `after:` job only after the final retry. `sync-rates` has retries but nothing depends on it. Check the scheduler's docs before relying on this.

**Optional:** If the partner is sometimes later than 90 minutes, increase `retries`, or move the `at:` time later.

**Verdict:** Stop. Don't add the try/catch with exit 0. Add `retries: 3` and `retry_delay: 30m` to `import-orders` in `deploy/schedule.yml` instead.

I haven't changed anything in the repository. Should I make that `deploy/schedule.yml` change instead of the try/catch?