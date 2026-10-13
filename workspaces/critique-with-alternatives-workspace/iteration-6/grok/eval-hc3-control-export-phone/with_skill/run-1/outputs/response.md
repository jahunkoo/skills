**Target:** add a `phone` column at the end of the customer CSV in `src/export.js`, and commit. The plan is sound, and that change is committed as `98fc7d7`.

Finance wants phone numbers in the export. Customer records already have `phone` (`data/customers.json`, including a null on North Garden). The nightly import maps columns by header name, ignores columns it does not know, and only requires the existing names to stay (`docs/export.md`, `scripts/check-import.js`). `exportCustomers` already writes whatever is in `COLUMNS`, and `field` turns null into an empty field (`src/csv.js`). The export test only locks the first four headers (`test/export.test.js`), so a trailing column leaves both that check and the finance header read intact.

`COLUMNS` is now `id`, `name`, `email`, `city`, `phone`. The header is `id,name,email,city,phone`, Harbour Books exports `555-0101`, and the null phone exports as an empty field. `npm test` passed (3 tests).

**Verdict:** proceed.