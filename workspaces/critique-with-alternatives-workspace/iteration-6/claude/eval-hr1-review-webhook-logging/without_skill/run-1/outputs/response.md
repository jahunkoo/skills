I added the log line, but I passed the headers and body through `redact()` first instead of logging them raw.

**Why not the line as you wrote it:** `req.headers` contains `Authorization: Bearer <token>`, which is the partner's static token. Under `docs/logging.md`, stdout goes to the hosted log service. Everyone in support plus the two outside contractors can search it, and lines stay for 90 days. The same doc says never to log credentials and to run headers and payloads through `redact()`, as `src/admin.js` already does. Once a token has leaked, the fix is rotation, and `docs/partners.md` says rotation takes partners weeks to redeploy. So one bad log line would cost a lot to clean up.

**What I changed:**
- `src/webhooks.js:11`: `logger.info('webhook received', { headers: redact(req.headers), body: redact(req.body) });` is now the first line of `handleWebhook`. You still see every header and the whole payload; only the credential fields show as `[redacted]`. Those are `authorization`, `cookie`, `x-api-key`, `token`, `password` and `secret`, matched at any depth and regardless of case.
- `test/webhooks.test.js`: a new test checks that the line is written and that the token string doesn't appear in any log output, whether it was sent in the header or inside the body. All 5 tests pass with `npm test`.

**Two things to consider (I didn't change these):**
- **One limit on 401 debugging:** with redaction, you can't tell from the log *which* wrong token a partner sent. If you need that, log a short hash of the token (for example, the first 8 hex characters of its sha256). That lets you match it against known tokens without exposing it.
- **Volume:** this logs every delivery, including successful ones, at `info`. If you only care about failures, you could put the redacted headers and body on the two existing `logger.warn('webhook rejected', ...)` calls instead. That cuts volume and keeps less partner data in a log that outside contractors can read.

I haven't committed anything.