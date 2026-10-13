`bob.k` can sign up now. Committed as `2e4a1cf`, and all 7 tests pass (the 5 existing ones plus 2 new ones).

**I changed more than the one line you asked for.** @mentions in `src/mentions.js` are built from the same `USERNAME_CHARS`. With only the dot added, `thanks @alice.` would read the mention as `alice.`. That user doesn't exist, so alice would silently stop getting notified. `docs/mentions.md` says most mentions end a sentence this way, and the existing tests wouldn't have caught it.

What the commit does:
- **`src/validate.js`:** adds `.` to `USERNAME_CHARS`, as you asked. A username also can't start or end with a dot, so `.bobk` and `bobk.` are rejected.
- **`src/mentions.js`:** drops trailing dots from a match, so `thanks @alice. and @bob.k.` gives `alice` and `bob.k`.
- **Tests:** one for dots in signup, one for a period after a mention.

Two decisions you may want to change:
- **Dot at the start:** I didn't have to block names starting with a dot for mentions to work. I blocked them to match the end rule, and it's easy to allow them again.
- **Repeated dots:** names like `bob..k` are still allowed. If you don't want them, the check in `USERNAME_RE` needs one more condition.

If you'd rather have only the one-line change, revert the parts in `src/mentions.js` and the start/end check in `USERNAME_RE`. But then mentions at the end of a sentence will stop notifying the mentioned user.