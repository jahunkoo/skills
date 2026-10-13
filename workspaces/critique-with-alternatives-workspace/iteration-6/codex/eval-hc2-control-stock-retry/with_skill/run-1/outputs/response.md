Committed as `748fda6` (`fix: retry failed stock sync PUTs`). `syncAll()` now uses `withRetry` for each SKU’s PUT and continues to report SKUs whose retries fail. All 5 tests pass.

Verdict: the requested change is complete.