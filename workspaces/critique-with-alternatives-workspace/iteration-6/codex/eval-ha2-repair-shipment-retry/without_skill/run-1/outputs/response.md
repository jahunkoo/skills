Updated `shipOrder()` to retry timed-out `postShipment` calls with a stable idempotency key, preventing a lost response from creating a duplicate shipment. Added a regression test; all 5 tests pass.

Committed as `9140fbc` (`Retry timed-out shipment posts safely`).