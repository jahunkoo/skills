Replaced the JSON round trip with `structuredClone(value)` in [src/clone.js](src/clone.js:3).

The documented draft format uses JSON values, and Node 20+ supports `structuredClone`. Both existing tests pass; `git diff --check` is clean. One behavior change to keep in mind: `structuredClone` throws for values such as functions, though those are outside the documented draft format.