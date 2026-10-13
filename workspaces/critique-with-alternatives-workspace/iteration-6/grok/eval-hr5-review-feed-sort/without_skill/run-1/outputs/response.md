The change is correct. Compare `createdAt` with `<` and `>`. For values from `stamp()`, that order matches `new Date()` and drops the date parsing that `notes/perf.txt` says is 61% of `sortFeed`.

`stamp()` always returns `date.toISOString()`: 24 characters, `YYYY-MM-DDTHH:mm:ss.sssZ`. `addEvent` only accepts that shape (`/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/`). Every field is fixed-width and zero-padded, and the suffix is always `Z`, so code-unit order is chronological order, newest first when the comparator is reversed. I checked 5,000 `stamp()` values (including ties) and the calendar edges from year 0001 through 9999, including the leap-day and year-boundary cases in the feed test. String order and `new Date` order agreed, including which side of a tie stayed first.

```js
// Newest first. stamp() values are fixed-width UTC, so code-unit order matches time order.
export function sortFeed(events) {
  return [...events].sort((a, b) => (a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : 0));
}
```

Return `0` when the strings are equal. A comparator that returns `-1` on a tie is inconsistent and can scramble a stable sort. Keep the `[...events]` copy so the caller's array stays in insertion order. `localeCompare` is the wrong tool here: it is slower and follows locale collation.

This only holds for `stamp()` strings. `sortFeed` does not re-check the format. These pairs are the same instant to `new Date` and a different order as strings: `2025-05-06T09:00:00.000Z` versus `2025-05-06T09:00:00Z`, `2025-05-06T11:00:00+02:00`, or `2025-05-06T09:00:00.000+00:00`. A fractional second that is not exactly three digits also diverges (`...00.20Z` versus `...00.100Z`). `addEvent` already rejects those, and `importEvents` runs offsets through `stamp(new Date(row.when))` before insert, so the feed never sees them. If `stamp()` ever stops being fixed-width UTC, this sort becomes wrong while `new Date` subtraction would keep working.

Parsing each timestamp once before sorting would also cut the per-comparison `Date` work, and it would still be extra work the string compare does not need. The existing newest-first test already covers a previous-day timestamp (`2025-05-05T23:59:59.999Z` before `2025-05-06T09:00:00.000Z`). I did not change `src/feed.js`.