I'd hold off on this line as written: it would put every partner's live token into the shared logs.

**What's wrong with it**

1. **It logs the partner's credential.** Partners authenticate with `Authorization: Bearer <token>` (`src/auth.js:4`). Logging `req.headers` as-is writes that token in plain text. This happens on every delivery, including the ones that succeed.
2. **Many people can read the logs, and a leak is slow to fix.** `docs/logging.md:3-4` says stdout goes to the hosted log service, where all of support and two outside contractors can search it, and lines are kept for 90 days. `docs/partners.md:4` says each partner has one static token, and rotating it takes them weeks. So one deploy would expose every partner's token, and cleaning up would take weeks of partner work.
3. **It breaks the repo's own logging rule.** `docs/logging.md:5-6` says to pass headers and payloads through `redact()` first, and `src/admin.js:5` already does that. The tool is already here; this line just doesn't use it.

**A better way**

Use `src/redact.js` instead of logging the raw values. I checked it on a webhook-shaped header object: `authorization` becomes `"[redacted]"` and `content-type` stays as it is. It matches key names in any letter case and at any depth, so the same call covers keys like `token` or `password` inside the body. Your requested line becomes:

```js
import { redact } from './redact.js';
// first line of handleWebhook
logger.info('webhook received', { headers: redact(req.headers), body: redact(req.body) });
```

You'd still see what partners send, minus the secret.

**Optional**

- Your goal is to see payloads from failed deliveries. Right now a delivery can only fail at the two early returns: 401 at `src/webhooks.js:13` and 400 at `src/webhooks.js:18`. Adding `headers: redact(req.headers), body: redact(req.body)` to those two existing `logger.warn` calls would capture exactly the failures. It would also skip logging every successful order body to a log that outsiders can read.
- With redaction, a 401 won't show what was wrong with the token. If you need that, log a safe hint instead, such as whether the header starts with `Bearer `.
- `test/webhooks.test.js` could get a test that captures the sink with `setSink` and asserts that `tok-north` never appears in a log line.

**Verdict:** go ahead with one change: wrap `req.headers` and `req.body` in `redact()` instead of logging them raw.

I haven't changed anything in the repository. Should I add the line with `redact()` as shown?