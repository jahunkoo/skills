I cleaned up `agent/system_prompt.md` and left two spots that contradict themselves.

**Removed**

- The language-and-tone backstory (English-only replies, the retired translation service, the old apology opener, and the 2025 length tests). The current rules are still there: reply in the customer's language, apologize only when the problem is on our side, and keep replies under 120 words.
- Maria's HTML TODO about rewriting that section before Q4.
- The `lookup_order_legacy` line. The June 2026 migration removed that tool, and `lookup_order` now covers old-store orders.
- The prompt changelog (v1–v4).

**Left as written**

- **Escalation.** One line sends billing disputes to billing@northwind.example (ADR-0003). The next opens a `high` priority ticket (ADR-0006). Those conflict, so both lines are still in the file. The ADR files record 0006 as superseding 0003, but I did not apply that to the prompt.
- **Closing a chat.** One line ends a chat after 24 hours without a reply. The next keeps it open for 72 hours. Nothing else in the repo decides between them.