# Held-out evals h3 and h4 for distill 1.1.0

Answer key, programmatic checks, and the fixture builder for the evals first run in the distill 1.1.0 confirmation (iteration-10, 2026-10-01). From the next edition onward they are development evals.

- Eval definitions: [`skills/distill/evals/evals.json`](../../../skills/distill/evals/evals.json) (`"set": "holdout"`). Fixture: [`skills/distill/evals/files/support-prompt.mbox`](../../../skills/distill/evals/files/support-prompt.mbox), merged into the skill evals when 1.1.0 was promoted (2026-10-01 UTC).
- [`answer-key.md`](answer-key.md): grader answer key (residue R1-R9, rules to keep K1-K5).
- [`checks.py`](checks.py): programmatic assertions (`h3.gate`, `h3.scope`, `h4.scope`).
- [`build_fixture.py`](build_fixture.py): script that builds the fixture. Running it rewrites `skills/distill/evals/files/support-prompt.mbox`.
