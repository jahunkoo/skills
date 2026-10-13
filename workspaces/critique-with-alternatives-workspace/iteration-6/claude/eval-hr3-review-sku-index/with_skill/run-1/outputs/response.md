**Target:** adding `migrations/003_unique_sku.sql` with `CREATE UNIQUE INDEX products_sku ON products (sku);` so that a bad import can't insert the same product twice.

Your goal is right, but the index is on the wrong key. As written, it would break the next deploy.

**The premise that's false: "a SKU appears once in `products`"**
- `migrations/001_init.sql` says the table holds "One row per product per warehouse that stocks it".
- `docs/inventory.md` says "the same SKU appears once per warehouse".
- `data/products-sample.csv`, which is a recent production export, already repeats SKUs. `TB-1` appears in north, south and east, and `CH-2` in north and south. Running `uniq -d` on the sku column returns both.

**What that would do here**
1. **The deploy fails.** `docs/migrations.md` says migrations run before the new version starts and a failing one aborts the deploy. `CREATE UNIQUE INDEX` on `(sku)` fails on the duplicates already in production, so 003 never applies and every later deploy is blocked until someone fixes it.
2. **Imports would break even if the index could be built.** `src/import.js` inserts a new row whenever the SKU is new for that warehouse, and the test `the same SKU in another warehouse is a new row` asserts exactly that. With a unique index on `sku` alone, every legitimate stocking of an existing SKU in a second warehouse would be rejected.

**The better way**
- **Index the real key.** Replace the planned statement with:
  ```sql
  -- A SKU repeats across warehouses, so it is unique per warehouse only.
  CREATE UNIQUE INDEX products_warehouse_sku ON products (warehouse_id, sku);
  ```
  This blocks the duplicate you're worried about (two rows for the same SKU in the same warehouse). It matches the key `planImport` already uses (`${warehouse_id}:${sku}`) and follows the pattern of `002_bins_code.sql`. The sample export has no duplicate `(warehouse_id, sku)` pairs, so it should build there.
- **Check production before the deploy.** The sample is only a sample. Run `SELECT warehouse_id, sku, count(*) FROM products GROUP BY 1, 2 HAVING count(*) > 1;` against production first. If it returns any rows, merge them before shipping 003, or the deploy aborts for the same reason as above.

**Optional (fix the source)**
`planImport` doesn't deduplicate within a single CSV. I ran it with two `north,X` rows and got two inserts back. With the new index, a CSV like that would make the import fail on the second insert instead of silently creating a duplicate. That's the safety you want, but it would be clearer to merge or reject repeated `(warehouse_id, sku)` rows in `planImport` and add a test for it.

I haven't changed anything in the repository.

**Verdict:** proceed with changes. Make the index `(warehouse_id, sku)` instead of `(sku)`, and run the duplicate query on production before deploying. Do you want me to add `migrations/003_unique_sku.sql` with the `(warehouse_id, sku)` index?