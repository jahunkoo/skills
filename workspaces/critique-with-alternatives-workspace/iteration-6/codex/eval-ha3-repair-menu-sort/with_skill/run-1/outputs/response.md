Committed as `7392123` (`fix: sort bakery menu with locale-aware comparison`).

`listProducts()` now sorts with `localeCompare`. I also updated the order form’s binary search to use the same comparison; otherwise it would miss five existing products after the sort change. All five tests pass, and the working tree is clean.

**Verdict:** The menu order is fixed, and products remain orderable by name.