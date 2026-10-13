`shipOrder` now retries `postShipment` when the partner API times out, and that change is committed as `1c4fa1d`.

Each attempt sends the same idempotency key, `shipment-${order.id}`. A timeout can mean the partner already created the shipment, so a retry with that key returns the original record instead of creating another one. All 5 tests passed.