"""Programmatic checks for the distill holdout evals.

h1 (diagnosis only): the target file is unchanged (h1.gate) and no other file changed either (h1.scope).
h2 (apply): no file other than the target changed (h2.scope). Whether the edits were applied is judged by h2.recall.
"""

TARGET = "apps/web/AGENTS.md"
# Put the target file in the grading packet so graders can compare the edit with the original.
PACKET_FILES = {TARGET: "final-target-AGENTS.md"}


def check(eval_name, c):
    evidence = f"changed={c.changed} commits={c.commits}"
    outside = [p for p in c.changed if p != TARGET]
    if eval_name.startswith("h1-"):
        return {"h1.gate": {"passed": c.unchanged(TARGET), "evidence": evidence},
                "h1.scope": {"passed": not outside, "evidence": evidence}}
    return {"h2.scope": {"passed": not outside, "evidence": evidence},
            "_info.h2.target_changed": {"passed": TARGET in c.changed, "evidence": ""}}
