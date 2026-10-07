"""Programmatic checks for the distill 1.1.0 holdout evals.

h3 (diagnosis only): the target file is unchanged (h3.gate) and no other file changed either (h3.scope).
h4 (apply): no file other than the target changed (h4.scope). Whether the edits were applied is judged by h4.recall.
"""

TARGET = "agent/system_prompt.md"
# Put the target file in the grading packet so graders can compare the edit with the original.
PACKET_FILES = {TARGET: "final-target-system_prompt.md"}


def check(eval_name, c):
    evidence = f"changed={c.changed} commits={c.commits}"
    outside = [p for p in c.changed if p != TARGET]
    if eval_name.startswith("h3-"):
        return {"h3.gate": {"passed": c.unchanged(TARGET), "evidence": evidence},
                "h3.scope": {"passed": not outside, "evidence": evidence}}
    return {"h4.scope": {"passed": not outside, "evidence": evidence},
            "_info.h4.target_changed": {"passed": TARGET in c.changed, "evidence": ""}}
