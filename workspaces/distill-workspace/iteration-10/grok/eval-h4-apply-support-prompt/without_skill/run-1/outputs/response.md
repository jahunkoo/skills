`agent/system_prompt.md` is cleaned up. Current rules are unchanged. Stale history and leftovers are gone.

I removed:

- The retired English-only flow and the translation service, the old “always apologize” draft, and the 2025 prompt-length experiments. The live rules stay: match the customer’s language, apologize only when the problem is ours, and keep replies under 120 words.
- The `<!-- TODO(maria) -->` note.
- The `lookup_order_legacy` line. That tool is not registered, and `lookup_order` already covers orders imported from the old store.
- The billing-dispute email to `billing@northwind.example` (ADR-0003). ADR-0006 supersedes it: escalate with `create_ticket` at priority `high`.
- The whole prompt changelog.

Left as written, because the two lines contradict each other and nothing in the repo picks a winner:

- End the chat after 24 hours without a reply.
- Keep the chat open for 72 hours after the customer’s last message.