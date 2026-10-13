The target is the proposal to make `logger.info('webhook received', { headers: req.headers, body: req.body })` the first line of `handleWebhook`.

The goal is to see what partners send when a delivery fails. The repository stays as it is.

## Premises

- A log at the top of `handleWebhook` runs for both failures. **True.** `partnerFor` and the handler lookup return 401 and 400 only after that point (`src/webhooks.js` lines 9–20). It also runs for every successful `order.paid` and `order.cancelled`.
- Those failures are otherwise unlogged. **False.** Both rejection paths already call `logger.warn('webhook rejected', …)` before returning (`src/webhooks.js` lines 12 and 17). They record the reason, and on an unknown type the partner and `req.body.type`. They omit the rest of the headers and body, so the diagnostic gap is real. The place to fill it already exists.
- Raw `req.headers` and `req.body` are safe to write. **False.** `logger` JSON-stringifies fields onto stdout with no filtering (`src/logger.js` lines 1 and 8–9). `docs/logging.md` says stdout is shipped to the hosted log service, searchable by support and two outside contractors, kept for 90 days, and that credentials must never be written. Partners authenticate with one static bearer token (`src/auth.js` lines 1–6, `docs/partners.md` line 3). That value lives in `headers.authorization`. Rotating it takes the partner weeks (`docs/partners.md` line 4).
- Nothing in the repo can log a request without the secret. **False.** `redact()` masks `authorization`, `cookie`, `x-api-key`, `token`, `password`, and `secret` at any depth (`src/redact.js` lines 2–8). `test/redact.test.js` shows `Authorization: 'Bearer x'` becoming `'[redacted]'` while `accept` is kept. `logAdminRequest` already logs headers only after `redact()` (`src/admin.js` line 5). `docs/logging.md` lines 5–6 require that same pass for headers and payloads.

## Objections

Logging raw headers writes every partner bearer token into retained, widely searchable logs. It happens on the failing calls you care about and on every success. The token is long-lived, so the leak outlasts the incident.

The new info line also misses the stated scope. Failures are already logged at warn. An unconditional info line adds a second line and records successful deliveries, which this goal does not ask for.

## Better way

Reuse `redact()`. Drop the new first line. On the two existing `logger.warn('webhook rejected', …)` calls in `src/webhooks.js`, add `headers: redact(req.headers)` and `body: redact(req.body)`, and import `redact` from `./redact.js`.

That reaches the goal. A 401 or 400 still carries the reason, and now the non-secret headers and the payload. `type` and `orderId` are not secret keys, so they stay visible. A present `authorization` header remains as a key whose value is `[redacted]`; a missing one stays missing, so you can still tell those cases apart. The success path stays quiet. The residual limit is the same one the admin log already accepts: `redact()` only masks the key names in `src/redact.js`, and `docs/partners.md` documents only the bearer token.

## Optional

Point the webhook tests’ log sink at an array and assert that a rejection line contains the event body and does not contain `tok-north`. Current tests set the sink to a no-op (`test/webhooks.test.js` line 6), so neither version is checked.

**Verdict:** Proceed with changes — add redacted headers and body only to the two existing `webhook rejected` warnings, and do not add the raw first-line info log.

The change is not applied. Yes to log redacted headers and body only on those two rejection paths?