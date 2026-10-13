I made the `sortFeed()` change. Direct string comparison preserves newest-first order for the fixed-width UTC timestamps produced by `stamp()` and removes date parsing from each sort comparison.

The review found one prerequisite: `addEvent()` accepted impossible dates such as February 30. I tightened its validation and added a regression case, so stored timestamps satisfy the ordering assumption.

`npm test` passes (3 tests). I did not rerun the performance profile.