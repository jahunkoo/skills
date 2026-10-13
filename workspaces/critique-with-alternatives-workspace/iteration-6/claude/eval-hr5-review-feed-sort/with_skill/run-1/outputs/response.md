**What I reviewed:** your plan to make `sortFeed()` in `src/feed.js` compare `createdAt` strings directly instead of parsing them with `new Date()`.

**Goal:** make `sortFeed` faster. `notes/perf.txt` says Date parsing takes 61% of its time on 5,000 events.

**What has to be true for this to work**

1. **Every `createdAt` uses the same fixed-width UTC format, so string order matches time order.** True. `src/store.js:4-7` rejects any `createdAt` that doesn't match `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$`. That means exactly 24 characters, always `Z`, always milliseconds. The default value comes from `stamp()` (`src/time.js:2-4`, which calls `toISOString()`).
2. **No path stores local times with offsets.** True. The old-tracker import is the one source with offsets (`+02:00`), and `src/import.js:6` converts it with `stamp(new Date(row.when))` before calling `addEvent`. `test/import.test.js:7` checks that conversion, and `test/feed.test.js:15` checks that an offset timestamp is rejected.
3. **Nothing else builds events or calls `sortFeed`.** True. A grep for `sortFeed` and `createdAt` finds only `src/feed.js`, `src/store.js`, `src/import.js` and the tests. Extended years (`+010000-...`), which `toISOString()` can produce, also fail the regex, so they can't break the ordering.
4. **Parsing is the slow part.** True. I ran a read-only check on 5,000 random `stamp()` timestamps plus 500 duplicates. The order was identical to the current comparator, and the time per sort dropped from about 22.6 ms to about 1.2 ms. The existing tests pass (3 pass, 0 fail).

**Judgement:** No objection holds up. The plan is sound because `addEvent` enforces one canonical UTC format, which makes lexical order the same as time order, and the import path normalizes offsets before anything is stored.

**Two details for when you write it:**
- **Comparator:** use relational operators, as in `(a, b) => (a.createdAt < b.createdAt ? 1 : a.createdAt > b.createdAt ? -1 : 0)`. Don't use `localeCompare`, which applies locale collation and is slower. Returning 0 on ties keeps the current stable behavior for equal timestamps.
- **Comment:** add a short note in `feed.js` that the comparison relies on the format `store.js` enforces. If someone later loosens that regex, they'll see what depends on it.

**Optional:**
- Add a test case in `test/feed.test.js` where string order and naive order could differ, such as timestamps across a day or year boundary. This keeps the assumption tested.

I haven't changed the repository.

**Verdict:** proceed. Compare the strings with `<`/`>` in `sortFeed` and add the comment pointing to the format check in `store.js`.

Should I make that change in `src/feed.js`?