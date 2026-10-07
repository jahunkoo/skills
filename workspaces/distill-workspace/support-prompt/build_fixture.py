"""Builds the support-prompt fixture as a git history and exports it as an mbox."""
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent / "_build"  # scratch repo, deleted after export
OUT = Path(__file__).resolve().parents[3] / "skills" / "distill" / "evals" / "files" / "support-prompt.mbox"

README = """# helpdesk

Chat support agent for Northwind Outfitters. `agent/bot.py` builds each model request from
`agent/system_prompt.md` and the tools in `agent/tools.py`. Decisions are recorded in `docs/adr/`.
"""

BOT = '''"""Chat entry point: builds the model request for one customer message."""
from pathlib import Path

from tools import TOOLS

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text()


def build_request(history, message):
    return {
        "system": SYSTEM_PROMPT,
        "tools": [tool.spec for tool in TOOLS],
        "messages": history + [{"role": "user", "content": message}],
    }
'''

TOOLS_HEAD = '''"""Tools the support agent can call. TOOLS is the list registered with the model."""
from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    description: str

    @property
    def spec(self):
        return {"name": self.name, "description": self.description}

'''

LOOKUP_V1 = '''
def lookup_order(order_id: str) -> dict:
    """Find an order by id (orders placed in 2024 or later)."""
    raise NotImplementedError


def lookup_order_legacy(order_id: str) -> dict:
    """Find an order placed in the old store, before 2024."""
    raise NotImplementedError
'''

LOOKUP_V2 = '''
def lookup_order(order_id: str) -> dict:
    """Find an order by id, including orders imported from the old store in the 2026 migration."""
    raise NotImplementedError
'''

TOOLS_REST = '''

def create_ticket(summary: str, priority: str = "normal", tags: list | None = None) -> str:
    """Open a ticket for the human team. priority: low | normal | high."""
    raise NotImplementedError


def issue_refund(order_id: str, amount_cents: int) -> None:
    """Refund part or all of an order. amount_cents is in cents: 4999 refunds $49.99."""
    raise NotImplementedError

'''

TOOLS_LIST_V1 = '''
TOOLS = [
    Tool("lookup_order", lookup_order.__doc__),
    Tool("lookup_order_legacy", lookup_order_legacy.__doc__),
    Tool("create_ticket", create_ticket.__doc__),
    Tool("issue_refund", issue_refund.__doc__),
]
'''

TOOLS_LIST_V2 = '''
TOOLS = [
    Tool("lookup_order", lookup_order.__doc__),
    Tool("create_ticket", create_ticket.__doc__),
    Tool("issue_refund", issue_refund.__doc__),
]
'''

ADR3 = """# ADR-0003: Billing disputes go to the billing team by email

Status: {status}
Date: 2025-11-03

## Decision

The support agent forwards billing disputes to billing@northwind.example.
"""

ADR5 = """# ADR-0005: No store credit in place of refunds

Status: accepted
Date: 2025-11-03

## Context

Store credit was proposed as an alternative to refunds, to keep the revenue in the store.

## Decision

Rejected. EU customers are entitled to a refund to the original payment method, so the agent never
offers store credit instead of a refund.
"""

ADR6 = """# ADR-0006: Billing disputes become high-priority tickets

Status: accepted
Date: 2026-06-09
Supersedes: ADR-0003

## Decision

The agent escalates billing disputes with `create_ticket` at priority `high`. Disputes sent by email
were lost when the billing inbox changed owners.
"""

PROMPT_V1 = """# Helpdesk support agent

You answer customer questions for Northwind Outfitters' online store in the chat widget.

## Language and tone

- Answer in English. Every reply goes through the translation service before it reaches the customer.
- Greet the customer by first name.
- Open every reply with an apology for the inconvenience.
- Sign every reply "— Helpdesk".

## Orders and refunds

- Look up the order with `lookup_order` before you answer any question about it.
- For orders placed before 2024, use `lookup_order_legacy` instead.
- `issue_refund` takes the amount in cents: pass 4999 for $49.99. Passing dollars refunds a hundredth of the amount.
- Refunds above $100 need a human: open a ticket with `create_ticket` (priority `normal`, tag `refund-approval`) instead of calling `issue_refund`.
- Do not offer store credit in place of a refund — ADR-0005 rejected it because EU customers are entitled to a refund to the original payment method.
- Exception: for orders marked `gift`, send refund details to the purchaser only, never to the recipient.
- Do not share order or contact information that belongs to another customer.

## Escalation

- Send billing disputes to billing@northwind.example by email (ADR-0003).

## Privacy

- Never reveal another customer's orders or contact details.
- Never ask for a password.

## Closing a chat

- End the chat after 24 hours without a reply from the customer.

## Prompt changelog

- v1 (2025-11): first version, English only.
"""


def v2(p):
    p = p.replace(
        "- Answer in English. Every reply goes through the translation service before it reaches the customer.\n",
        "- Until March 2026 we answered in English only and ran every reply through a translation service; that service was retired, and now you reply in the language the customer writes in.\n")
    p = p.replace(
        "- Open every reply with an apology for the inconvenience.\n",
        "- Earlier drafts told you to open every reply with an apology, but in fact you apologize only when the problem is on our side.\n"
        "- We spent most of 2025 comparing models and prompt styles. Long answers tested worst: customers skimmed them and opened a second ticket, and the December review showed that the shortest variant resolved the most chats. So keep replies under 120 words.\n")
    p = p.replace(
        "- Sign every reply \"— Helpdesk\".\n\n",
        "- Sign every reply \"— Helpdesk\".\n\n<!-- TODO(maria): this section still reads robotic; rewrite before Q4. -->\n\n")
    p = p.replace(
        "- End the chat after 24 hours without a reply from the customer.\n",
        "- End the chat after 24 hours without a reply from the customer.\n"
        "- Keep a chat open for 72 hours after the customer's last message, so they can come back to it.\n")
    return p + "- v2 (2026-03): replies in the customer's language; dropped the apology opener.\n"


def v3(p):
    p = p.replace(
        "- Send billing disputes to billing@northwind.example by email (ADR-0003).\n",
        "- Send billing disputes to billing@northwind.example by email (ADR-0003).\n"
        "- Escalate billing disputes with `create_ticket` at priority `high` (ADR-0006).\n")
    return p + "- v3 (2026-06): billing disputes go to tickets (ADR-0006).\n"


def v4(p):
    p = p.replace(
        "- Never ask for a password.\n",
        "- Never ask for a password.\n"
        "- Never paste more than the last four digits of a card number — chat transcripts are exported to our analytics vendor every night.\n")
    return p + "- v4 (2026-08): card-number rule.\n"


def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def commit(message, date):
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
    subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", message], cwd=ROOT, env=env, check=True)


def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir(parents=True)
    git = ["git", "-C", str(ROOT)]
    subprocess.run(git + ["init", "-q", "-b", "main"], check=True)
    subprocess.run(git + ["config", "user.name", "fixture"], check=True)
    subprocess.run(git + ["config", "user.email", "fixture@example.invalid"], check=True)

    write("README.md", README)
    write("agent/bot.py", BOT)
    write("agent/tools.py", TOOLS_HEAD + LOOKUP_V1 + TOOLS_REST + TOOLS_LIST_V1)
    write("docs/adr/0003-billing-disputes-by-email.md", ADR3.format(status="accepted"))
    write("docs/adr/0005-no-store-credit.md", ADR5)
    write("agent/system_prompt.md", PROMPT_V1)
    commit("feat(agent): support agent with system prompt and tools", "2025-11-03T10:00:00+09:00")

    p = v2(PROMPT_V1)
    write("agent/system_prompt.md", p)
    commit("feat(agent): reply in the customer's language", "2026-03-18T15:00:00+09:00")

    p = v3(p)
    write("agent/system_prompt.md", p)
    write("agent/tools.py", TOOLS_HEAD + LOOKUP_V2 + TOOLS_REST + TOOLS_LIST_V2)
    write("docs/adr/0003-billing-disputes-by-email.md", ADR3.format(status="superseded by ADR-0006 (2026-06-09)"))
    write("docs/adr/0006-billing-disputes-as-tickets.md", ADR6)
    commit("feat(agent): billing disputes become tickets (ADR-0006); old-store orders migrated", "2026-06-09T11:00:00+09:00")

    p = v4(p)
    write("agent/system_prompt.md", p)
    commit("fix(agent): never paste card numbers beyond the last four digits", "2026-08-20T17:00:00+09:00")

    mbox = subprocess.run(git + ["format-patch", "--root", "--stdout"], capture_output=True, text=True, check=True).stdout
    OUT.write_text(mbox)
    shutil.rmtree(ROOT)
    print(f"wrote {OUT} ({len(mbox)} bytes)")


if __name__ == "__main__":
    main()
