I would not make that change. `scripts/import-orders.js` is unchanged.

Exiting 0 after a caught error tells the scheduler the import succeeded. `docs/jobs.md` says a non-zero exit is the only page for this job, and `deploy/schedule.yml` starts `publish-orders` only when `import-orders` exits 0. `publish-orders` then publishes whatever is already in the orders file, so a failed import that exits 0 republishes the previous night's orders and nobody is paged.

A failure that clears on its own belongs on the scheduler's `retries` field, the way `sync-rates` is set up. A real import error should keep exiting non-zero.