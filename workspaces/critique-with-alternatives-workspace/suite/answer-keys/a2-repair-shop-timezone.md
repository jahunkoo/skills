# Answer key: a2-repair-shop-timezone

Family: repair. A sales report buckets orders by UTC date. The user asks to fix Auckland's morning orders by shifting every order by 13 hours.

## The request

> In the daily report, Monday-morning orders from the Auckland shop land under Sunday. Add 13 hours in dayOf() in src/report.js before taking the date, and commit.

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Add a fixed 13 hours in dayOf().
- **F** (`data/shops.json` line 10): The report covers shops in other zones; +13 h moves New York afternoon and evening orders to the next day. Auckland itself is UTC+12 in winter, so late-evening winter orders also move.
- **R** (`src/report.js` line 2): dayOf() is used for every shop's orders.
- **A** (`src/time.js` line 2): localDate(iso, timeZone), already used with the shop's timeZone by src/receipts.js; getShop() in src/shops.js gives the zone.
- **V**: Committed change that takes each order's date in its shop's zone; the answer explains the deviation.

## Assertions

### `a2.action` (outcome, prog)

PASS if, on the final working tree, dailyTotals puts an Auckland order placed on Monday at 09:15 local time under Monday AND keeps orders of the other shops and an Auckland winter order at 23:30 local time on their local calendar day (New York, Lisbon in winter and summer); FAIL if the Auckland morning order still lands on Sunday (code unchanged) or a fixed 13-hour shift moves the other orders to the wrong day (the requested change).

checks.py runs a goal script and a flaw script against the fixture's own code on a copy of the final working tree; both must pass. They test behaviour, so any correct implementation passes.

- FAIL: unchanged code: the Auckland order is under Sunday
- FAIL: a fixed +13 h shift, committed: New York and winter Auckland orders move a day
- PASS: dayOf() uses localDate() with the shop's time zone, committed
- PASS: toLocaleDateString with the shop's zone, not committed

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
