`syncAll()` now retries each stock PUT through `withRetry`, and the change is committed as `28bf508`.

Each SKU is sent with `withRetry(() => setStock(send, sku, quantity))`. A restart response (`UNAVAILABLE` / 503) or a timeout is tried up to 3 times, with the helper’s normal backoff. Any other failure, such as a 404, is still reported immediately and the remaining SKUs continue.

Existing tests passed. A separate check confirmed a SKU that returns 503 twice and then succeeds is synced, a SKU that stays down is failed after 3 attempts, and a 404 is not retried.