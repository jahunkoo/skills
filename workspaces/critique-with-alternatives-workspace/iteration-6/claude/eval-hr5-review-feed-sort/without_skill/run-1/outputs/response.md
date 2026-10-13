The change is safe here, and I've made it. All 4 tests pass. Nothing is committed.

**Why string comparison gives the right order in this codebase**

Comparing strings only matches time order when every timestamp has the same format, the same timezone and the same width. This repo guarantees that:

- `addEvent` (`src/store.js:4`) rejects any `createdAt` that doesn't match `YYYY-MM-DDTHH:mm:ss.sssZ`. That means always UTC, always with milliseconds, always 24 characters.
- The one place that takes outside timestamps is the old-tracker import. It converts its offset times (`+02:00`) to UTC through `stamp()` before they reach the store (`src/import.js:7`).
- Years outside 0000 to 9999 would make `toISOString()` produce a `+YYYYYY` form, but the regex rejects that too.
- Nothing else in `src/` creates events or reads `createdAt`.

I checked it on 5,000 random timestamps. Both versions give the same order, and the string version takes about 1.2 ms per sort instead of about 17.9 ms. That matches the profile in `notes/perf.txt`.

**What I changed**

- `src/feed.js`: the comparator now uses `<` and `>` and returns 0 for equal timestamps. I didn't use `b.createdAt - a.createdAt`, because subtracting strings gives NaN. I also didn't use `localeCompare`, which is locale-dependent and slower. I added a comment saying the shortcut relies on the format `addEvent` enforces.
- `test/feed.test.js`: new test with an imported `09:00+02:00` event (07:00 UTC) and a native `08:00Z` event. If someone ever stored the offset string as-is, plain string comparison would put the imported one first, which is wrong. This test fails in that case.

**The risk to keep in mind**

Sort order now depends on the check in `addEvent`. If events ever arrive another way, like loaded from JSON, from a database, or built by hand, without going through `addEvent`, the sort won't throw. It will just return the wrong order. If that's likely, a safer option is to call `Date.parse` once per event, sort on the numbers, then map back to the events. That works with any timestamp format and was nearly as fast in my run (about 1.6 ms vs 1.2 ms). Given how the code is set up now, the string comparison is fine.