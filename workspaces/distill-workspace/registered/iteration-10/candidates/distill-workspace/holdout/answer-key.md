# distill 1.1.0 holdout answer key — agent/system_prompt.md

Fixture: the `helpdesk` repository (`files/support-prompt.mbox`, 4 commits). The target is `agent/system_prompt.md`, the system prompt of a customer-support chat agent. `agent/bot.py` sends it to the model with the tools registered in `agent/tools.py`. The ADRs are in `docs/adr/`.

## Residue (should be stripped)

| ID | Type | Location in the original | Correct handling |
| --- | --- | --- | --- |
| R1 | History | Language and tone: "Until March 2026 we answered in English only and ran every reply through a translation service; that service was retired, and now you reply in the language the customer writes in." | Delete the backstory; keep only "Reply in the language the customer writes in." |
| R2 | Rebuttal | Language and tone: "Earlier drafts told you to open every reply with an apology, but in fact you apologize only when the problem is on our side." | Delete the rebuttal; state "Apologize only when the problem is on our side." plainly |
| R3 | Meta note | End of Language and tone: `<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->` | Delete. It is a note to the authors about wording; it does not question any rule |
| R4 | Dead reference | Orders and refunds: "For orders placed before 2024, use `lookup_order_legacy` instead." — `agent/tools.py` neither defines nor registers `lookup_order_legacy` (removed in the third commit; `lookup_order` now covers the migrated orders) | Delete after confirming |
| R5 | Stacked duplicate (one file) | Orders and refunds: "Do not share order or contact information that belongs to another customer." ↔ Privacy: "Never reveal another customer's orders or contact details." | Keep one of them (either) |
| R6 | Superseded ADR | Escalation: "Send billing disputes to billing@northwind.example by email (ADR-0003)." — ADR-0003's status is superseded by ADR-0006 (2026-06-09) | Delete |
| R8 | Excess narrative | Language and tone: "We spent most of 2025 comparing models and prompt styles. Long answers tested worst … So keep replies under 120 words." | Keep the instruction "Keep replies under 120 words." and delete the background. A short reason such as "customers skim long answers and open a second ticket" may stay; keeping it and dropping it are both correct |
| R9 | History (whole section) | "## Prompt changelog" with v1–v4 | Delete the whole section. It records how the prompt changed and tells the agent nothing to do |
| R7 | Contradiction | Closing a chat: "End the chat after 24 hours without a reply from the customer." ↔ "Keep a chat open for 72 hours after the customer's last message, so they can come back to it." | **Do not delete; ask the user.** Nothing in the repository settles which is current |

## Live rules (should be kept — proposing to delete them, or deleting them, is wrong)

| ID | Type | Original |
| --- | --- | --- |
| K1 | WHY | Privacy: "Never paste more than the last four digits of a card number — chat transcripts are exported to our analytics vendor every night." (the reason must remain too; the analytics vendor is outside the repository; it came in with the most recent commit, 2026-08-20) |
| K2 | Trap warning | Orders and refunds: "`issue_refund` takes the amount in cents: pass 4999 for $49.99. Passing dollars refunds a hundredth of the amount." (it looks like a technical detail, and the docstring in `agent/tools.py` gives the unit and the 4999 example, but the consequence sentence "Passing dollars refunds a hundredth of the amount" is only in the prompt; it is the warning that prevents a wrong refund and must remain) |
| K3 | Rationale link | Escalation: "Escalate billing disputes with `create_ticket` at priority `high` (ADR-0006)." — ADR-0006 is accepted; keep the link |
| K4 | Rejected alternative | Orders and refunds: "Do not offer store credit in place of a refund — ADR-0005 rejected it because EU customers are entitled to a refund to the original payment method." |
| K5 | Conditional exception | Orders and refunds: "Exception: for orders marked `gift`, send refund details to the purchaser only, never to the recipient." |

## Other behavioral instructions (should remain)

- Greet the customer by first name · sign every reply "— Helpdesk" · look up the order with `lookup_order` before answering any question about it · refunds above $100 go to a `create_ticket` ticket (priority `normal`, tag `refund-approval`) instead of `issue_refund` · never ask for a password (h4.other_rules)
- One of the two R5 sentences (h4.other_rules)
- Reply in the language the customer writes in; apologize only when the problem is on our side; keep replies under 120 words (the instructions inside R1, R2 and R8; h4.conclusions)

## Notes for graders

- Three items have no counterpart in the other fixtures: R4 needs the code (`agent/tools.py`) to judge, R9 is a whole section of history, and K2 is a technical sentence that must be kept.
- h3.recall counts R1–R6 and R8 (seven items, at least six); h3.adr and h3.deadref require R6 and R4 with evidence. h4.recall requires R4 and R6 and at least four of R1, R2, R3, R5 and R8. R5 counts as stripped when exactly one of its two sentences remains. R9 is judged separately by h3.changelog and h4.changelog.
- R6 and K3 are two sentences about billing disputes; the ADR statuses (superseded / accepted) decide which is current. This is not a contradiction for the user to decide.
- K4 says "ADR-0005 rejected it": ADR-0005 is accepted, and what it rejected is the store-credit alternative.
- A diagnosis that proposes shortening a kept rule's wording without dropping its meaning or reason does not violate keep (for example, trimming K2's 4999 example while keeping the consequence sentence).
