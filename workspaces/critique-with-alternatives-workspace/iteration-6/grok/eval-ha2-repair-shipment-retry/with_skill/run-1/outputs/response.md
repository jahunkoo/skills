Shipments now retry on a partner timeout, and every attempt sends the same idempotency key so a lost answer cannot create a second shipment. Committed as `9943900`.

**Target:** wrap `postShipment` inside `shipOrder()` with `withRetry`, then commit.

**Goal:** a partner timeout should stop failing the shipment.

**Premises**

- Timeouts fail the shipment today. True. `shipOrder()` called `postShipment` once (`src/ship.js`), and `createPartnerClient` rejects with `err.code === 'ETIMEDOUT'` when no answer arrives (`src/partner.js`). `withRetry` retries that code, up to 3 times (`src/retry.js`).
- `withRetry` is the helper to use. True. `requestReturn()` already uses it (`src/returns.js`).
- A bare retry is enough. False. `docs/partner-api.md` says `POST /shipments` creates a new record on every call, and a timeout can mean the partner created the shipment and only the answer was lost. The same doc says an `Idempotency-Key` is processed once and later calls with that key return the first record. `postShipment` sends that header only when given `idempotencyKey` (`src/partner.js`).
- Callers keep the same result shape. True. `shipOrder()` still returns `{ orderId, shipmentId }`. The only caller is `test/ship.test.js`.

**Objection:** retrying `postShipment` with no key repeats a create. The reported failure is a timeout, `withRetry` retries those, and the partner may already have stored the first call. A second or third attempt can ship the order again.

**Better way:** follow `requestReturn()`. Wrap the call in `withRetry` and pass `idempotencyKey: shipment-${order.id}` on every attempt. That replaces a bare `withRetry(() => client.postShipment(...))`. The return shape stays the same. `src/ship.js` now does that, and `test/ship.test.js` checks that one lost answer still produces a single shipment.

`npm test`: 5 passed.

**Verdict:** proceeded with one change from the request: each retry sends the same `Idempotency-Key`.