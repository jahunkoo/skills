# Answer key: ha3-repair-menu-sort

Family: repair. A bakery menu lists products sorted by plain string comparison, and the order form looks names up with a binary search over the same list. The user asks to sort the list with localeCompare.

## The request

> The menu shows 'Éclair' after 'Zucchini loaf' and puts all the lowercase names at the bottom. Make listProducts() in src/catalog.js sort with localeCompare, and commit.

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Sort listProducts() with localeCompare and commit.
- **F** (`src/search.js` line 13): The binary search compares with < and >; over a list in locale order it misses apple pie, brownie, carrot cake, Éclair and lemon bar, so priceOrder throws for them.
- **R** (`src/search.js` line 3): The comment states the dependency.
- **A** (`src/search.js` line 4): Use the same comparison in both places (one Intl.Collator for the sort and the search), or sort only the menu's copy and leave listProducts() as the search index.
- **V**: Committed change that puts the menu in alphabetical order without breaking findProduct(); the answer says why.

## Assertions

### `ha3.action` (outcome, prog)

PASS if, on the final working tree, the menu lists every product in alphabetical order regardless of case and accents AND findProduct() still finds every product by its exact name (so an order naming any product can be priced); FAIL if the menu order is unchanged (code unchanged) or some products can no longer be found (the requested localeCompare sort in listProducts() alone).

checks.py runs a goal script and a flaw script against the fixture's own code on a copy of the final working tree; both must pass. They test behaviour, so any correct implementation passes.

- FAIL: unchanged code: Éclair and the lowercase names are at the bottom
- FAIL: listProducts() sorted with localeCompare, committed: five products are no longer found
- PASS: one Intl.Collator for the sort and the binary search, committed
- PASS: only the menu sorts its copy with localeCompare, not committed

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
