Leave `handleWebhook` as it is. That line would write each partner's bearer token into the hosted logs.

`Authorization: Bearer <token>` is the partner credential (`src/auth.js`). `docs/partners.md` says each partner has one static token and a rotation takes them weeks to redeploy. `docs/logging.md` says stdout is shipped to the log service, support and two outside contractors can search it, and lines are kept for 90 days. The same doc says never to write credentials, and to pass headers and payloads through `redact()` first, which `src/admin.js` already does.

Putting the log on the first line of `handleWebhook` also records every successful delivery, not only failures. `redact()` masks `authorization`, `cookie`, `x-api-key`, `token`, `password`, and `secret` at any depth and still leaves `type`, `orderId`, and the other non-secret fields visible.

On the two reject paths, this matches the logging policy and still shows what the partner sent:

```js
logger.warn('webhook rejected', {
  reason: 'unknown token',
  headers: redact(req.headers),
  body: redact(req.body),
});
```

Say if you want that version added.