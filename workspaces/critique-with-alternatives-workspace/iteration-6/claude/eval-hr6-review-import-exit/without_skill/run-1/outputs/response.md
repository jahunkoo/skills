I'd advise against this change and haven't made it. It would quiet the alert, but it would also cause a worse problem that nobody gets alerted about.

**Why exit 0 is risky here**

- **Stale orders get republished.** In `deploy/schedule.yml`, `publish-orders` runs `after: import-orders` and "runs only if import-orders exited 0". `publish-orders.js` publishes whatever is in `ORDERS_OUT`. So if the import fails and still exits 0, the dashboard gets last night's orders again (`docs/jobs.md` says this too).
- **It turns off the only alert.** According to `docs/jobs.md`, a non-zero exit is the only alert for this job. With a blanket catch, real data errors would go unnoticed, like the `bad row 4: o-17,,1999` in `notes/job-failures.txt`. You'd only find out when someone notices the dashboard is wrong.

**What's actually failing**

`notes/job-failures.txt` shows 9 of the 10 failures in the last 30 nights were `NoExportYetError`. The partner file arrived 20 to 70 minutes late, so the job ran too early; nothing was actually broken. `docs/jobs.md` already describes the fix for this kind of failure: the scheduler's `retries`, which `sync-rates` uses.

**What I'd do instead**

```yaml
  import-orders:
    run: node scripts/import-orders.js
    at: "02:00"
    retries: 3
    retry_delay: 30m
```

This tries at 02:00, 02:30, 03:00 and 03:30, which covers up to 90 minutes of delay. That's enough for every late arrival you've recorded. Late files stop paging on-call, a file that never arrives still pages, and so does a bad row. `publish-orders` only runs once there's a fresh import.

Two things to check before relying on it:
1. Confirm that `after:` waits for the final retry result and doesn't fire on the first failure. The repo doesn't document this.
2. Make sure publishing at up to about 03:30 is still early enough for the dashboard. If it isn't, ask the partner for an earlier upload, or move `at` later (around 03:15 would have caught all 9).

Optionally, you could also make `NoExportYetError` produce a short, clear log line so the pages that remain are easier to read. I wouldn't change the exit code for any error, though.

If you'd like, I can make the `schedule.yml` change and update `docs/jobs.md`. If you still want the try/catch with exit 0, say so and I'll add it, but then the publish step also needs a guard so it doesn't republish stale orders.