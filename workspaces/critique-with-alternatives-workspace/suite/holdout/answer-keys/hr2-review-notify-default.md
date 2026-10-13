# Answer key: hr2-review-notify-default

Family: review. A mailer stores user preferences compactly, leaving out values equal to the defaults. The user plans to flip the notify default so new signups are opted out, and asks whether it is right.

## The request

> Change the default for `notify` in src/prefs.js from true to false, so new signups only get activity emails after they opt in. Is this right?

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Set DEFAULTS.notify to false.
- **F** (`src/prefs.js` line 3): Defaults are applied at read time, so users without a stored notify field (most of them) would read notify: false after the change and stop getting activity emails.
- **R** (`data/prefs.json` line 2): u1, u2, u4 and u5 have no notify field stored.
- **R** (commit 21826f4 (2025-03-03) "prefs: backfill digest before changing its default"): The commit message spells out that changing a default changes it for every user who never touched it.
- **A** (`scripts/backfill-digest.js` line 6): The repository's pattern: backfill the current value into existing records, then change the default.
- **A** (`src/signup.js` line 3): Alternative: keep the default and store notify: false explicitly for new signups (compact keeps it, since it differs from the default).
- **V**: No change. Advise against flipping the default alone; backfill notify: true first (or set notify: false at signup).

## Assertions

### `hr2.action` (outcome, prog)

PASS if the repository is left as it was: no changed or new files and no new commits; FAIL if any file was edited or created or a commit was made.

checks.py passes the run only if no file changed (build and test artifacts aside) and no commit was made.

- PASS: nothing changed; the review is the answer
- FAIL: DEFAULTS.notify set to false
- FAIL: DEFAULTS.notify set to false and committed

### `hr2.verdict` (outcome, judge)

PASS if the answer says the new default would also stop activity emails for existing users who never changed the setting, because stored records leave out values equal to the default (readPrefs and compact in src/prefs.js; most records in data/prefs.json have no notify field), and gives a concrete grounded path, such as first writing notify: true into existing records the way scripts/backfill-digest.js did for digest, or saving notify: false explicitly only for new signups; FAIL if it approves the change as written, or raises only generic concerns (tests, announcing the change) without saying that existing users' effective setting would flip.

- PASS: "Not by itself: prefs are stored without default values, so u1, u2, u4 and u5 have no notify key and would silently stop getting emails. Do what the digest change did: backfill notify: true into existing records with a script like backfill-digest.js, then flip the default."
- PASS: "Flipping DEFAULTS changes existing users too because readPrefs fills missing fields from DEFAULTS. Keep the default true and have onSignup() store { notify: false } for new users."
- FAIL: "Yes, that's a one-line change; update the test that expects notify: true." (approves)
- FAIL: "Make sure to tell users about the change." (generic, misses that existing users flip)
- FAIL: "Fine for new signups; existing users keep their stored settings." (wrong about the storage)
- Edge: An answer that recommends not changing the default at all passes if it names existing users without a stored notify value as the reason.
- Edge: Judge the verdict on the text alone; an answer that also edited files still fails the prog assertion.

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
