Do not add `CREATE UNIQUE INDEX products_sku ON products (sku)`. I did not create `migrations/003_unique_sku.sql`.

A SKU is a product model, and each warehouse that stocks it has its own `products` row. `docs/inventory.md` says the same SKU appears once per warehouse. The production export in `data/products-sample.csv` already has `TB-1` in north, south, and east, and `CH-2` in north and south. `planImport` keys on `warehouse_id` plus `sku`, and the test expects the same SKU in another warehouse to be a new row.

Migrations run before the new version starts and must succeed on the data already in production. A unique index on `sku` alone would abort the deploy on those existing rows, and it would also reject a legitimate insert of `TB-1` into a second warehouse.

The constraint that matches the table, the importer, and `002_bins_code.sql` is uniqueness per warehouse:

```sql
-- A SKU is stocked once per warehouse. The same SKU appears in every warehouse that carries it.
CREATE UNIQUE INDEX products_warehouse_sku ON products (warehouse_id, sku);
```

That stops a second insert of the same product in one warehouse, and it succeeds on the current rows. Say if you want that written to `migrations/003_unique_sku.sql`.