`shipOrder()` now retries the partner call on timeouts through `withRetry`. I made one change you didn't ask for: every attempt also sends an idempotency key. Without it, a retry could ship the same order twice. It's committed as `ffc9fd5` and the tests pass (5 of 5).

**Why the key was needed:** `docs/partner-api.md` says `POST /shipments` "create[s] a new record on every call". It also says a timeout can happen after the partner has already created the record, when only the answer was lost. So wrapping the call as it was would turn some lost answers into two real shipments for one order. The doc also says a request with an `Idempotency-Key` header is processed only once. `requestReturn` in `src/returns.js` already relies on this, so I did the same here.

**What changed:**
- `src/ship.js`: `postShipment` is wrapped in `withRetry` with `{ idempotencyKey: \`shipment-${order.id}\` }`. Retry settings are the defaults: 3 attempts, and only `ETIMEDOUT` errors are retried. That matches how returns are handled.
- `test/ship.test.js`: a new test copies the one for returns. The first answer is lost, the call is retried, and the result is still one shipment (`s1`).

**One assumption to check:** the key is built from `order.id`, so it only works if each order gets exactly one shipment. If one order can be split into several shipments, or shipped again on purpose later, the partner would return the first shipment instead of creating a new one. In that case the key needs a shipment-specific ID. Tell me if that applies and I'll change it.

**Verdict:** go ahead with the change. The idempotency key is the only thing I added beyond your request.