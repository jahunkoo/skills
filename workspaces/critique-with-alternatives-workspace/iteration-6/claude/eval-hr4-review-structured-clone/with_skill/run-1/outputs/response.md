I reviewed the plan to swap `JSON.parse(JSON.stringify(value))` for `structuredClone(value)` in `deepClone()` (`src/clone.js:3`). You asked me to check it, so I haven't changed the repository.

**Goal (my assumption).** No goal was stated. `notes/profile.txt` blames `deepClone` for 41% of the time spent typing in a 40-page draft, so I assumed the goal is speed. The verdict holds either way.

**What I checked**

- **Node supports it: true.** `package.json:10` requires Node `>=20`, and `structuredClone` has been a global since Node 17. Local Node is v24.16.0.
- **Same output for this data: true.** `docs/drafts.md:3-5` says drafts hold only strings, numbers, booleans, arrays and plain objects, with timestamps as ISO strings. Drafts come from `JSON.parse` (`src/drafts.js:5`), and every setter wraps its input in `String()` (`src/drafts.js:18-20`). The two methods only behave differently for `Date`, `Map`, `undefined`, `NaN` and functions, and none of those can get into a draft.
- **Callers: traced.** `deepClone` has two callers: the first copy in `createEditor` (`src/drafts.js:11`) and the per-edit undo snapshot (`src/drafts.js:13`). Both only need an independent deep copy, and the change still gives them one.
- **Tests: pass.** I made the change in a throwaway copy of the repo and ran `npm test`: 2 of 2 pass.
- **Faster: true for large drafts.** I benchmarked a draft with a body of about 120 KB, roughly 40 pages:

  | draft | JSON round trip | structuredClone |
  |---|---|---|
  | 40-page | ~77 µs/op | ~9 µs/op |
  | tiny (the fixture size) | ~0.7 µs/op | ~1.1 µs/op |

  That's about 8x faster on the case the profile measured. It's a little slower on tiny drafts, but those cost about a microsecond either way.

**Objections:** none. Nothing changes for drafts, the runtime supports it, and it speeds up the slow case.

**Optional:** Most of the remaining cost comes from deep-copying the whole draft on every keystroke. Strings can't be changed in place, and edits only replace `title` or `body` or push to `tags`. So the snapshot at `src/drafts.js:13` could be `{ ...current, tags: [...current.tags], meta: { ...current.meta } }`, which measured about 0.05 µs per op on the 40-page draft. The catch is that undo would then quietly break if a future edit changed some other nested field in place. If you want this, it belongs in a separate change with a test covering it.

**Verdict:** go ahead with the change as written. Should I make the one-line edit to `src/clone.js` and run the tests?