Updated [syncAll()](src/sync.js) to retry each SKU’s PUT with `withRetry`. Added tests for recovery from 503 responses and for continuing after retries are exhausted. All 5 tests pass.

Committed as `7b52682` (`fix: retry stock sync PUTs during warehouse outages`).