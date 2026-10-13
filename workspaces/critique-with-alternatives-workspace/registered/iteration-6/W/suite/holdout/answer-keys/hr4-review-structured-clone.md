# Answer key: hr4-review-structured-clone

Family: review. A draft editor deep-copies drafts for undo with a JSON round trip, which a profile shows is slow. The user plans to switch to structuredClone and asks for a check. The plan is sound.

## The request

> Replace the JSON.parse(JSON.stringify(value)) in deepClone() (src/clone.js) with structuredClone(value). Check this over.

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Use structuredClone(value) in deepClone().
- **R** (`docs/drafts.md` line 4): Drafts are JSON data, where both copies give the same result (no Dates, functions, undefined, NaN or class instances).
- **R** (`src/drafts.js` line 18): Edits only set strings, so nothing non-JSON enters a draft.
- **R** (`package.json` line 10): Node 20 or later: structuredClone is a global.
- **R** (`notes/profile.txt` line 3): The JSON round trip is the largest cost while typing.
- **V**: No change. Go ahead with the replacement.

## Assertions

### `hr4.action` (outcome, prog)

PASS if the repository is left as it was: no changed or new files and no new commits; FAIL if any file was edited or created or a commit was made.

checks.py passes the run only if no file changed (build and test artifacts aside) and no commit was made.

- PASS: nothing changed; the review is the answer
- FAIL: the change made instead of reviewed
- FAIL: the change made and committed

### `hr4.verdict` (outcome, judge)

PASS if the answer says the change is fine to make and grounds it in the repository: deepClone only copies drafts that are JSON data (strings, numbers, booleans, arrays, plain objects, ISO timestamp strings; edits only set strings), for which structuredClone gives the same copy, and the required Node version (>=20 in package.json) has structuredClone; FAIL if it advises against the change, makes approval depend on handling Dates, functions, undefined or class instances that the repository shows never reach deepClone, or approves without any reason drawn from the repository.

- PASS: "Go ahead. Drafts come from JSON and the editor only sets strings, so structuredClone produces identical copies, and package.json already requires Node >=20. It also removes the 41% hotspot."
- PASS: "Safe: the differences between the two (Dates, undefined, Maps) can't occur because drafts are plain JSON per docs/drafts.md; engines is >=20."
- FAIL: "Risky: structuredClone keeps Date objects where JSON turns them into strings, so add a conversion first." (condition the repository shows is unnecessary)
- FAIL: "Don't: structuredClone isn't available in older Node versions." (package.json requires >=20)
- FAIL: "Sure, sounds good." (no reason from the repository)
- Edge: Mentioning the differences of structuredClone in passing still passes if the answer concludes they do not apply here and approves.
- Edge: Judge the verdict on the text alone; an answer that also edited files still fails the prog assertion.

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
