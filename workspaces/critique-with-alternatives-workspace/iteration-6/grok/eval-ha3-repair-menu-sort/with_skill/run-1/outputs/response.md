The request was to sort `listProducts()` with `localeCompare` and commit, so the menu no longer lists Éclair after Zucchini loaf or groups the lowercase names at the bottom.

`listProducts()` sorted with `<` and `>`, which is UTF-16 code-unit order. On this product list that put Éclair last, after Zucchini loaf, and put apple pie, brownie, carrot cake, and lemon bar after every capitalized name.

`findProduct` in `src/search.js` binary-searches that same list and compared names with `<` and `>`. Its comment says the sort has to use that same comparison. `priceOrder` in `src/order.js` looks up every line through `findProduct`. Sorting only with `localeCompare` makes those two comparisons disagree. Checked against every name, apple pie, brownie, carrot cake, lemon bar, and Éclair then come back missing, so an order for any of them throws `unknown product`. The existing tests still pass, because they only price Fudge and Donut, which the old comparison still finds.

On this machine the default locale is en-US, and `localeCompare` orders the menu as Almond tart, apple pie, Banana bread, brownie, carrot cake, Crème brûlée, Donut, Éclair, Fudge, lemon bar, Opera cake, Zucchini loaf.

`listProducts()` now sorts with `a.name.localeCompare(b.name)`. `findProduct` walks the list with `localeCompare` as well, and an exact name match still returns the product. Commit `3cb030a` on main.

`node --test` passed all 3 tests. Every product name is found, Pretzel still throws, and Éclair sits before Zucchini loaf.

Verdict: proceed with the `localeCompare` sort and the matching comparison in `findProduct`.