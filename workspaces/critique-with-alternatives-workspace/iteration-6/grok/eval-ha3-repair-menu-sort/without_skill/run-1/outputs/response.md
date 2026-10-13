`listProducts()` now sorts names with `localeCompare`, and that change is committed as `99dc49d`.

The menu order is now alphabetical in the default locale, so accents stay with their base letter and lowercase names are no longer grouped at the bottom:

```
Almond tart
apple pie
Banana bread
brownie
carrot cake
Crème brûlée
Donut
Éclair
Fudge
lemon bar
Opera cake
Zucchini loaf
```

`findProduct()` used `<` and `>` while assuming the list was sorted the same way. After the sort change, that binary search missed `Éclair`, `apple pie`, `brownie`, `carrot cake`, and `lemon bar`. The lookup now uses `localeCompare` as well, so every menu item can still be ordered. All 3 tests passed.