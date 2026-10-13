`syncAll()` now retries each stock PUT through `withRetry`, and the change is committed as `54f751b`.

The warehouse restart answers 503 for a few seconds (`docs/warehouse-api.md`), and `setStock` turns that into `code: 'UNAVAILABLE'`, which `withRetry` already treats as retryable. Repeating a PUT is safe because it sets an absolute level. The default retry schedule is not enough for that outage: three attempts, with waits of 200ms and 400ms, finish in under a second, while the API is still down, so the SKU would still end up in `failed`.

Each PUT is therefore tried at 0s, 1s, 3s, and 6s (`attempts: 4`, `delayMs: 1000`). Errors that `withRetry` does not consider retryable, such as a 404, are still reported for that SKU and the rest of the batch continues. The shared defaults stay as they are, so the catalog pull keeps its short window. About 40 SKUs, at most four tries each and one at a time, stays under the 600 requests per minute limit. An outage longer than about six seconds is still reported in `failed`.

All four tests passed.

Verdict: proceed with a per-PUT `withRetry` window that covers a few seconds, and keep other errors on the existing per-SKU failure report.