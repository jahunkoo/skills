**Verdict: completed.** `bob.k` is allowed in signup. Because `USERNAME_CHARS` also controls mentions, I adjusted mention parsing so `@alice.` still treats the final period as punctuation.

Committed as `cfc3483`. All 5 tests pass; the working tree is clean.