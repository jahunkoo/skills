**Review target:** replacing `new Date()` calls in `sortFeed()` with direct `createdAt` string comparison.

Valid timestamps from [stamp()](src/time.js:2) have a fixed UTC format, so string order works for them. But [addEvent()](src/store.js:4) checks only the format: it accepts `2025-02-30`. Node parses that as March 2, while string comparison places it before March 1. The proposed change would therefore alter the order of accepted events.

A safer fix is to parse each timestamp **once per event** in [sortFeed()](src/feed.js:2), sort by the cached numeric values, and return the events. That preserves current ordering while removing the repeated parsing identified in [perf.txt](notes/perf.txt:1). A local 5,000-event comparison took about 18 ms per run currently versus 1.3 ms with parsing once. The repository is unchanged.

**Verdict: Stop the direct-string change; parse once per event instead.**