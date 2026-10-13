Committed as `43db785` (`feat: include phone in customer CSV export`). The CSV now ends with `phone`; missing values export as blank. All 4 tests pass.

The existing finance import still reads only `id`, `name`, and `email`, so it will ignore the new column until its mapping is updated.