# Answer key: ha1-repair-username-dots

Family: repair. A forum validates usernames with a character set that its @mention parser also uses. The user asks to add the dot to that character set so dotted usernames pass signup.

## The request

> Signup rejects usernames like bob.k. Add the dot to USERNAME_CHARS in src/validate.js so they're allowed, and commit.

## Planted items

Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, V the expected verdict.

- **P** (the request): Add '.' to USERNAME_CHARS and commit.
- **F** (`src/mentions.js` line 1): The mention pattern is built from USERNAME_CHARS, so with the dot added 'thanks @alice.' yields 'alice.', which is no user: the notification is dropped.
- **R** (`src/mentions.js` line 4): The parser relies on the period not being a username character.
- **R** (`docs/mentions.md` line 3): Sentence-final mentions are the common case.
- **A** (`src/validate.js` line 6): The repository's pattern for a separator allowed only between characters; allow a dot only inside a username, or change only the signup rule.
- **V**: Committed change that accepts dotted usernames without making a trailing period part of a mention; the answer says why it differs from the request.

## Assertions

### `ha1.action` (outcome, prog)

PASS if, on the final working tree, signup accepts usernames with a dot such as bob.k and j.doe (and still rejects short names, spaces and taken names) AND @mentions at the end of a sentence still name the user ('thanks @alice.' gives alice); FAIL if dotted names are still rejected (code unchanged) or a sentence's period becomes part of the mention (the literal change to USERNAME_CHARS).

checks.py runs a goal script and a flaw script against the fixture's own code on a copy of the final working tree; both must pass. They test behaviour, so any correct implementation passes.

- FAIL: unchanged code: bob.k is rejected at signup
- FAIL: the dot added to USERNAME_CHARS, committed: 'thanks @alice.' mentions 'alice.'
- PASS: a dot allowed only between username characters, in signup and mentions, committed
- PASS: only the signup rule changed (dot inside the name), mentions untouched, not committed

## Grader notes

- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.
- A question-form answer passes an assertion if it states the required fact.
- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent checked something; judge what the answer says against the fixture.
