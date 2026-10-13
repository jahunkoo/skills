I added `phone` as the last column of the customer export and committed it as `16eeb06`. All 4 tests pass.

- **`src/export.js`**: the column list is now `id, name, email, city, phone`. If a customer has no phone (customer 3 has `null`), that field is left empty, not filled with the word "null".
- **`test/export.test.js`**: I added one test. It checks that `phone` is the last column, that the first customer's number comes out right, and that a missing phone gives an empty field.

Adding a column at the end shouldn't break Finance's import. According to `docs/export.md`, it finds columns by header name and skips any it doesn't know. The existing check in `scripts/check-import.js` still passes.

Finance's import will skip `phone` until they add it to the list of columns it reads. They'll need to make that change on their side before the numbers show up there.