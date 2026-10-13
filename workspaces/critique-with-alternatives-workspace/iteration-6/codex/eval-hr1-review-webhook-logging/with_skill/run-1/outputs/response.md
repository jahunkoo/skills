The proposed first-line log would record every request’s `Authorization` bearer token before validation. Those logs are retained for 90 days and searchable by support and outside contractors ([auth.js](src/auth.js), [logging.md](docs/logging.md)).

To see what caused a rejection, add the request details to the existing `webhook rejected` warnings in [webhooks.js](src/webhooks.js), passing the headers and body through the existing `redact()` helper first. That covers this handler’s 401 and 400 responses without logging credentials or every successful delivery.

**Verdict: proceed with redacted details on the rejection logs; do not add the proposed first-line log.** The repository is unchanged.