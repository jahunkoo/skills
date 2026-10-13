**Verdict: shipped.** `shipOrder()` now retries timed out `postShipment` calls with a stable idempotency key, so a lost response does not create a duplicate shipment.

All 5 tests pass. Committed as `24d6d15` (`fix: retry shipment timeouts with idempotency key`).