Signup now accepts usernames like `bob.k`. The change is committed as `a33a7f1`.

`USERNAME_CHARS` in `src/validate.js` is now `a-z0-9_.`. A dot can appear inside a name, and the name still has to be 3–20 characters and cannot start or end with a dot.

Mentions share that rule. `thanks @alice.` still mentions `alice`, and `@bob.k` mentions `bob.k`. All 9 tests passed.