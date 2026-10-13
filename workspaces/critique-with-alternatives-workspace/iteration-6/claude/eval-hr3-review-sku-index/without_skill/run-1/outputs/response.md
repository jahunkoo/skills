I didn't add the index the way you wrote it. Unique on `sku` alone would break deploys, so I added `migrations/003_unique_sku.sql` with a per-warehouse version instead:

```sql
-- A SKU appears once per warehouse that stocks it, so it is unique per warehouse only.
CREATE UNIQUE INDEX products_warehouse_sku ON products (warehouse_id, sku);
```

**Why not `UNIQUE (sku)`:**

- **It would fail on production data.** `docs/inventory.md` says the same SKU has one `products` row per warehouse that stocks it. The production export in `data/products-sample.csv` shows this: `TB-1` is in north, south and east, and `CH-2` is in north and south. Building the index would fail. Per `docs/migrations.md`, that aborts the deploy and leaves the old version running.
- **It would block normal imports even if it could be built.** `planImport` inserts a new row when a known SKU arrives for a new warehouse, and the test "the same SKU in another warehouse is a new row" checks exactly that. A SKU-only index would reject that insert.

**Why `(warehouse_id, sku)` fits:** it's the same key `planImport` matches on, and it follows the pattern `002_bins_code.sql` already uses for bin codes. I checked the sample export and it has no duplicate `(warehouse_id, sku)` pairs, so the index should build. The sample is only a recent export, though, so run this against production before deploying:

```sql
SELECT warehouse_id, sku, count(*) FROM products GROUP BY 1, 2 HAVING count(*) > 1;
```

If that returns any rows, they need to be merged first, or this migration will also abort the deploy. The existing tests still pass, but nothing in this repo runs the SQL itself.

**One more gap:** `planImport` only checks for duplicates against rows already in the database. If one CSV lists the same warehouse and SKU twice and that product is new, both rows end up in `inserts`. The new index will now make that import fail instead of creating a duplicate, which is what you wanted. If you'd rather the import handle it (for example, last row wins), that's a small change to `planImport` plus a test. I haven't made it, so tell me if you want it.