I wrapped `postShipment` in `withRetry` inside `shipOrder()` and committed it as `44ca60d`. All 5 tests pass.

**One change beyond what you asked for:** each attempt now sends the same idempotency key, `shipment-${order.id}`. According to `docs/partner-api.md`, a timeout doesn't mean the call failed. The partner may have created the shipment and only the answer was lost. If I had just wrapped the call, a retry after a lost answer would have created a second shipment for the same order. The partner client already accepts an idempotency key, and `requestReturn()` in `src/returns.js` uses the same approach for returns.

**What changed:**
- `src/ship.js`: the call goes through `withRetry` with the default settings (3 attempts, retrying only on `ETIMEDOUT`) and passes the idempotency key.
- `test/ship.test.js`: I added a test where the first answer is lost. It checks that the retry gets back the shipment the partner already created (`s1`) and that only one shipment exists.

**One thing to check:** because the key is based on the order ID, the partner will treat any second shipment request for the same order as a repeat and return the first shipment. That's correct if an order only ever has one shipment. If orders can be split across several shipments, the key needs a per-shipment part as well.