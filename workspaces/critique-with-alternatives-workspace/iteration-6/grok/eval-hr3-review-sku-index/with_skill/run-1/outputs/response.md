**Target:** adding `migrations/003_unique_sku.sql` with `CREATE UNIQUE INDEX products_sku ON products (sku)`, so a bad import cannot insert the same product twice.

**Goal:** stop a bad import from inserting the same product a second time.

## Premises

1. **A product is identified by SKU alone.** False. `docs/inventory.md` (lines 3–4) says a SKU names a product model and each warehouse that stocks it has its own `products` row. `migrations/001_init.sql` (lines 6–10) defines one row per product per warehouse. `src/import.js` (lines 1–4) keys a row on `warehouse_id` and `sku`, and `test/import.test.js` (lines 12–15) expects the same SKU in another warehouse to be a new row.

2. **Production rows already have unique SKUs, so this index builds.** False. `docs/inventory.md` (line 4) calls `data/products-sample.csv` a recent export of the production table. That file has six rows: `TB-1` in north, south, and east, and `CH-2` in north and south. `docs/migrations.md` (lines 3–5) says migrations run in name order on deploy, a failure aborts the deploy, and a migration has to succeed on data already in production.

3. **The duplicate a bad import would insert is a second row with the same SKU.** False. The importer’s product key is `warehouse_id` + `sku`. Commit `224d7fb` already handled the same shape for bins: “Bin codes like A1 exist in every warehouse, so the key is `(warehouse_id, code)`,” which is `bins_warehouse_code` in `migrations/002_bins_code.sql`.

4. **`003_….sql` is the next migration.** True. `migrations/` contains only `001_init.sql` and `002_bins_code.sql`.

5. **`(warehouse_id, sku)` is already unique in that export.** True on the file: all six pairs appear once. Whether production has changed since the export is unknown. The doc presents the file as the recent export.

## Objections

The single-column index uses the wrong identity. The schema, the importer, and the test all treat the same SKU in a second warehouse as a valid product row. Applied to the production export, `CREATE UNIQUE INDEX products_sku ON products (sku)` fails on `TB-1` and `CH-2` and aborts the deploy. The old version keeps running until that migration is fixed.

## Better way

Keep the new file `migrations/003_unique_sku.sql`. Replace the index statement with the same kind of key as `002_bins_code.sql`:

```sql
-- The same SKU is stocked in many warehouses; it is unique inside one warehouse.
CREATE UNIQUE INDEX products_warehouse_sku ON products (warehouse_id, sku);
```

Checked again: a second insert of the same warehouse and SKU fails, which is the duplicate product row. The six exported rows stay valid, and the import test’s south / `TB-1` insert stays valid. The name follows `bins_warehouse_code`. If production has a real duplicate pair, the deploy still aborts, which is the failure path `docs/migrations.md` already describes.

## Optional

`planImport` does not record an insert it has just planned (`src/import.js`, lines 5–12), so one CSV can still plan two inserts for a new warehouse and SKU. The index is what stops the second write. Collapsing those in the planner would surface the bad file earlier.

**Verdict:** Proceed with changes: in `migrations/003_unique_sku.sql`, create `products_warehouse_sku` on `(warehouse_id, sku)`.

The repository is unchanged. I would ask: add that composite unique index?