`listProducts()` now sorts with `localeCompare`, and it's committed. I also changed `src/search.js`, which you didn't ask for, because the sort change alone would have broken the order form.

**Why the extra change:** `findProduct()` in `src/search.js` binary-searches the output of `listProducts()` using `<` and `>`. Its own comment says it relies on the list being sorted that same way. When I sorted with `localeCompare` but left the search alone, it couldn't find 5 of the 12 products: `lemon bar`, `brownie`, `Éclair`, `apple pie` and `carrot cake`. Anyone ordering one of those would get "unknown product". The existing tests didn't catch it because they only order `Fudge` and `Donut`.

**What I did:**
- **`src/catalog.js`:** added a `compareNames()` function that uses `localeCompare`, and `listProducts()` sorts with it, as you asked.
- **`src/search.js`:** `findProduct()` now compares with that same `compareNames()`, so the sort and the search always agree.
- **Tests:** one checks that every product on the menu can be ordered; it fails if the search change is undone. Another checks that `apple pie` comes before `Banana bread` and `Éclair` before `Fudge`.

All 5 tests pass. The menu now reads Almond tart, apple pie, Banana bread, brownie, carrot cake, Crème brûlée, Donut, Éclair, Fudge, lemon bar, Opera cake, Zucchini loaf.

**Optional:** `localeCompare()` with no locale uses the server's default locale, so the menu order could differ between machines. The order form keeps working either way, because the sort and the search use the same function. If you want the same order everywhere, change it to `a.localeCompare(b, 'en')`.

Verdict: proceed with one change, which is done. The search uses the same comparison as the sort, so the order form keeps finding every product.