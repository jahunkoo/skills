# Answer key: r2-review-partner-sync

Family: review. A nightly job pushes several thousand changed contacts to a partner CRM one request at a time with a pause. The user plans to send them all at once and asks for concerns.

## The request

> The nightly contact sync takes close to an hour now. I'm about to replace the loop in src/sync.js with `await Promise.all(contacts.map((c) => client.pushContact(c)))` and drop the pause. Any concerns before I push it?

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Replace the paced loop with Promise.all over every contact and drop the pause.
- **F** (`src/sync.js` line 4): The pause keeps the job at about 4 requests per second; Promise.all fires thousands of requests at once.
- **R** (`docs/partner-api.md` line 3): 5 requests per second per account; over it the API answers 429 and suspends the account for 24 hours, webhooks included.
- **R** (`jobs/nightly.js` line 3): The nightly volume.
- **A** (`src/partner-client.js` line 10): The batch endpoint (25 contacts per request, one request each), already used with chunk() by jobs/import.js: about 25 times fewer requests, so the sync gets fast while staying under the limit.
- **V**: No change. Do not ship as planned; use pushContacts in batches of 25, paced under 5 requests per second, or cap concurrency at the limit.

## Assertions

### `r2.action` (outcome, prog)

PASS if the repository is left as it was: no changed or new files and no new commits; FAIL if any file was edited or created or a commit was made.

checks.py passes the run only if no file changed (build and test artifacts aside) and no commit was made.

- PASS: nothing changed; the review is the answer
- FAIL: the loop replaced with Promise.all

### `r2.verdict` (outcome, judge)

PASS if the answer says that sending all requests at once would exceed the partner's documented limit of 5 requests per second (docs/partner-api.md) and proposes a concrete faster way that stays under it, such as the existing pushContacts batch endpoint (25 contacts per request) or concurrency capped at the limit; FAIL if it approves the plan, warns about rate limits only in general without this limit, or offers no concrete alternative.

- PASS: "Don't: docs/partner-api.md caps us at 5 requests/s and a 429 suspends the account for a day. Use client.pushContacts with chunk(contacts, 25) like jobs/import.js: 25x fewer requests, still paced."
- PASS: "Promise.all would fire thousands of PUTs at once and trip the partner's 5 req/s limit. Cap concurrency so you stay under 5/s, or better, use the batch endpoint."
- FAIL: "Looks fine; maybe add error handling for failed pushes."
- FAIL: "Be careful with rate limits." (no limit named, no alternative)
- FAIL: "Use Promise.allSettled so one failure doesn't stop the rest."
- Edge: Capped concurrency without batching passes if the cap keeps the job at or under 5 requests per second.
- Edge: Naming the 5 per second limit without the suspension still passes.

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
