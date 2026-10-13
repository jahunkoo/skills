I added a `phone` column at the end of the customer CSV and committed it as `72a03fb`. All 4 tests pass.

**Change:** `src/export.js:3` now reads `const COLUMNS = ['id', 'name', 'email', 'city', 'phone'];`. I also added a test to `test/export.test.js` that checks `phone` is the last column and that a customer with no phone (customer 3 has `"phone": null`) gets an empty field.

Before changing it, I checked whether an extra column could break finance's nightly import:
- **Finance won't break:** their import matches columns by header name and ignores ones it doesn't know (`docs/export.md`). `scripts/check-import.js` reads the file the same way. The existing check that finance gets `id`, `name` and `email` still passes.
- **Existing tests still hold:** the export test only checks the first four columns, so adding a fifth doesn't affect them.
- **Values come out right:** a missing phone becomes an empty field. Any phone number containing a comma or quote would be quoted by `field()` in `src/csv.js`. Reading the new export the way finance does gives `555-0101`, `555-0102`, an empty value, and `555-0104` for the four sample customers.

**Verdict:** proceed. I found nothing in the request that needed changing.

Because finance's import ignores columns it doesn't know, phone numbers won't show up on their side until they add `phone` to their import's column list. That change is theirs to make, not something this repository can do.