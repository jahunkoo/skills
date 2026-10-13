The plan to compare `createdAt` strings directly in `sortFeed` (`src/feed.js`) is sound.

The goal is to speed up `sortFeed` while keeping newest-first order. Date parsing is the cost the profile points at, and the timestamps this feed stores already sort correctly as strings.

**Premises**

- Date parsing is the slow part. True. `notes/perf.txt` records 61% of a 5,000-event `sortFeed` in `new Date`, called twice per comparison, which is what `src/feed.js` does now. A local run of 5,000 `stamp()` events took 18.2 ms with `new Date` and 1.3 ms with a string comparison, in the same order.
- Those strings are fixed-format UTC. True. `stamp()` returns `toISOString()` (`src/time.js`), always 24 characters, `YYYY-MM-DDTHH:mm:ss.sssZ`. `addEvent` rejects anything else (`src/store.js`). `importEvents` runs old offset times through `stamp()` before they are stored (`src/import.js`), so `2025-05-30T09:00:00+02:00` is stored as `2025-05-30T07:00:00.000Z`.
- For that form, code-unit order is chronological order. True. Every field is zero-padded and fixed width, and the zone is always `Z`, so the first differing character is a digit in the most significant field. Pair checks across the existing feed fixtures, the epoch, year and month boundaries, milliseconds, and equal timestamps had 0 mismatches. Ties stay ties, so a stable sort keeps the same relative order the Date subtraction keeps today.
- The only thing that depends on the result is the newest-first order. True. The only caller is `test/feed.test.js`, which checks actor order. The `[...events]` copy stays, so the input array is still not mutated.

**Verdict:** Proceed.

Use a three-way comparison, `(a, b) => (a.createdAt < b.createdAt) - (a.createdAt > b.createdAt)`. The repository is unchanged. I would ask: yes to proceed with that string comparison in `sortFeed`?