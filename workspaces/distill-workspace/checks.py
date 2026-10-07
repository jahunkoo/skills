"""Programmatic checks for distill — d1: did it stop after the diagnosis; d2: did it stay inside the target file."""

TARGET = "prompts/release-notes/SKILL.md"
# Put the target file in the grading packet so graders can compare the edit with the original
# (renamed so it is not discovered as a skill).
PACKET_FILES = {TARGET: "final-target-SKILL.md"}


def check(eval_name, c):
    evidence = f"changed={c.changed} commits={c.commits}"
    if eval_name.startswith("d1-"):
        return {"d1.gate": {"passed": c.unchanged(TARGET), "evidence": evidence}}
    outside = [p for p in c.changed if p != TARGET]
    return {"d2.scope": {"passed": not outside, "evidence": evidence},
            "_info.d2.target_changed": {"passed": TARGET in c.changed, "evidence": ""}}
