# Held-out evals h1 and h2 for distill 1.0.0

Answer key and programmatic checks for the evals first run in the distill 1.0.0 confirmation (iteration-6, 2026-09-30). From distill 1.1.0 onward they are development evals. The set name is `dev-web`. In iteration-6 the set name was `holdout`.

- Eval definitions: [`skills/distill/evals/evals.json`](../../../skills/distill/evals/evals.json) (`"set": "dev-web"`). Fixture: [`skills/distill/evals/files/web-agents.mbox`](../../../skills/distill/evals/files/web-agents.mbox).
- [`answer-key.md`](answer-key.md): grader answer key (residue R1-R8, rules to keep K1-K5).
- [`checks.py`](checks.py): programmatic assertions (`h1.gate`, `h1.scope`, `h2.scope`).
