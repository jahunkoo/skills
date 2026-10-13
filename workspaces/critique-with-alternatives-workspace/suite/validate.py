#!/usr/bin/env python3
"""Replays each built fixture and checks that checks.py gives every validation state its expected verdict.

  python3 validate.py [--cases cases_dev.py] [--out DIR] [--only NAME,...]

For each case: replay files/<name>.mbox with eval-harness/fixtures.py make_fixture, require `node --test` to pass on
the initial tree, then for each validation state replay afresh, apply its ops, run checks.check and compare. Also
checks evals.json and the answer key for the case. Prints a table and exits non-zero on any mismatch.
"""
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "eval-harness"))
from fixtures import Changes, make_fixture  # noqa: E402

sys.path.insert(0, str(HERE))
from build_suite import load_cases, parse  # noqa: E402


def load_checks(path):
    spec = importlib.util.spec_from_file_location("suite_checks", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(cwd, argv):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{' '.join(argv)} failed: {(p.stdout + p.stderr).strip()[-300:]}")
    return p.stdout


def apply(fx, ops):
    for op in ops:
        kind = op[0]
        if kind == "write":
            f = fx / op[1]
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(op[2])
        elif kind == "replace":
            f = fx / op[1]
            text = f.read_text()
            if op[2] not in text:
                raise RuntimeError(f"replace: {op[2]!r} not in {op[1]}")
            f.write_text(text.replace(op[2], op[3]))
        elif kind == "delete":
            target = fx / op[1]
            shutil.rmtree(target) if target.is_dir() else target.unlink()
        elif kind == "run":
            run(fx, op[1])
        elif kind == "git":
            run(fx, ["git", *op[1]])
        elif kind == "commit":
            run(fx, ["git", "add", "-A"])
            run(fx, ["git", "-c", "core.hooksPath=/dev/null", "commit", "-q", "-m", op[1]])
        else:
            raise RuntimeError(f"unknown op {kind}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(HERE / "cases_dev.py"))
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--only", default="")
    ap.add_argument("-v", "--verbose", action="store_true", help="show the evidence of every state")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    cases = load_cases(a.cases).CASES
    if a.only:
        cases = [c for c in cases if c["name"] in a.only.split(",")]
    checks = load_checks(out / "checks.py")
    evals = {e["name"]: e for e in json.loads((out / "evals.json").read_text())["evals"]}
    rows, bad = [], 0
    for case in cases:
        name = case["name"]
        prefix = name.split("-", 1)[0]
        mbox = out / "files" / f"{name}.mbox"
        problems = []
        ev = evals.get(name)
        if ev is None or ev["assertions"] != case["assertions"] or ev["prompt"] != case["prompt"]:
            problems.append("evals.json out of date")
        if not (out / "answer-keys" / f"{name}.md").exists():
            problems.append("no answer key")
        for raw in case["assertions"]:
            parse(raw)
        with tempfile.TemporaryDirectory(prefix="validate-") as tmp:
            fx = Path(tmp) / "fx"
            make_fixture(mbox, fx)
            t = subprocess.run(["node", "--test"], cwd=fx, capture_output=True, text=True)
            n_commits = len(run(fx, ["git", "log", "--format=%h"]).split())
            if t.returncode != 0:
                problems.append("initial node --test fails")
        if problems:
            bad += 1
            rows.append((name, "(fixture)", "-", "-", "MISMATCH: " + "; ".join(problems)))
        else:
            rows.append((name, "(fixture)", "-", "-", f"ok: {n_commits} commits, initial tests pass"))
        for state in case["validation"]:
            with tempfile.TemporaryDirectory(prefix="validate-") as tmp:
                fx = Path(tmp) / "fx"
                initial = make_fixture(mbox, fx)
                try:
                    apply(fx, state["ops"])
                    result = checks.check(name, Changes(fx, initial))[f"{prefix}.action"]
                except Exception as e:  # a broken validation state is a mismatch too
                    result = {"passed": None, "evidence": f"error: {e}"}
            ok = result["passed"] is state["expect"]
            bad += not ok
            got = {True: "PASS", False: "FAIL", None: "ERROR"}[result["passed"]]
            rows.append((name, state["state"], "PASS" if state["expect"] else "FAIL", got,
                         ("ok" + (": " + result["evidence"][:400] if a.verbose else "")) if ok
                         else "MISMATCH: " + result["evidence"][:300]))
    w = [max(len(r[i]) for r in rows) for i in range(4)]
    print(f"{'eval':<{w[0]}}  {'state':<{w[1]}}  {'want':<4}  {'got':<5}  result")
    for r in rows:
        print(f"{r[0]:<{w[0]}}  {r[1]:<{w[1]}}  {r[2]:<4}  {r[3]:<5}  {r[4]}")
    print(f"\n{len(rows) - bad} ok, {bad} mismatches")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
