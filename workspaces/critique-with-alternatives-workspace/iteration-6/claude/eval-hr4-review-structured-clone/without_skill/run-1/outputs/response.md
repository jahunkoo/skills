I swapped `JSON.parse(JSON.stringify(value))` for `structuredClone(value)` in `src/clone.js:3`. Both tests pass (`npm test`, Node 24). I haven't committed it.

**Correctness: it's safe.** The two differ only for things a draft can't contain. `structuredClone` keeps `Date`, `Map`, `undefined` and `NaN`, ignores `toJSON`, and throws on functions. `docs/drafts.md` says a draft holds only strings, numbers, booleans, arrays and plain objects, with timestamps stored as ISO strings. For that data the two produce the same result. Node `>=20` (from `package.json`) has `structuredClone`.

**Speed: it helps here, but only because of what a draft looks like.** `notes/profile.txt` shows `deepClone` taking 41% of typing time in a 40-page draft, so I assume speed is the reason for the change. I benchmarked both locally:

| Data | JSON round trip | structuredClone |
|---|---|---|
| Draft with ~125 KB body (about 40 pages) | 0.087 ms | 0.010 ms |
| 5,000 small objects | 1.35 ms | 2.20 ms |

`structuredClone` is about 9x faster on a draft because most of a draft is one long string. On data made of many small objects it is about 1.6x slower. If drafts ever become structured (a list of blocks instead of one `body` string), this gain could turn into a loss.

**The bigger cost is copying the whole draft on every keystroke, whichever method does it.** `createEditor` in `src/drafts.js` pushes a full deep copy onto `history` for every edit. Over 200 keystrokes that is about 200 copies of a 125 KB body, roughly 25 MB of undo history, all of which stays in memory. Strings in JS can't be changed, so a snapshot doesn't need its own copy of `body`. Copying only the parts an edit can change is enough:

```js
const snapshot = (d) => ({ ...d, tags: [...d.tags], meta: { ...d.meta } });
```

In the same benchmark that took about 0.0001 ms and shares the body string instead of duplicating it. The catch is that it ties the snapshot to the draft's shape: a new nested field that edits change in place would also need copying. A safer version with the same speed is to make edits return a new object instead of changing `current`, so no deep copy is needed. I left these out because you asked for the one-line swap. If the 41% is what you're trying to fix, this is the change that removes it.