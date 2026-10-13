#!/usr/bin/env python3
"""Builds an eval set from a cases module: fixtures as mbox, answer keys, evals.json entries and check specs.

  python3 build_suite.py --cases cases_dev.py --set suite-dev [--out DIR]

A cases module defines CASES (a list of dicts) and may define GRADER_NOTES (a string) and PREFIX (a string put
before every family letter, e.g. 'h' for hr1; default ''). Each case has:

  id             int, unique in evals.json
  name           '<p>-<slug>'; <p> (before the first '-') is the assertion prefix: PREFIX, the family letter, a number
  family         'review' | 'pressure' | 'repair' | 'control'
  prompt, expected_output   str
  commits        [{date: 'YYYY-MM-DDTHH:MM:SS+00:00', message: 'subject' or 'subject\\n\\nbody',
                   files: {path: text, or None to delete}}], 2 to 5 of them, dated in 2025
  assertions     ['[kind·check] <p>.<id> — text', ...]: exactly one prog assertion '<p>.action'
                 (kind 'control' for the control family, 'outcome' otherwise); review and pressure have exactly one
                 judge assertion, repair and control none
  check          {kind: 'no_change'} | {kind: 'protected', paths: [...]} | {kind: 'repair', goal: JS, flaw: JS}
                 | {kind: 'control', goal: JS, git_untracked?: [...], git_ignored?: [...]}
                 JS is the body of an async function, run as an ES module at the root of a copy of the final working
                 tree: it throws to fail and may return a message; load fixture code with `await import('./src/x.js')`
  answer_key     {scenario: str,
                  planted: [{id: 'P'|'F'|'R'|'A'|'V', text: str, file: path, find: substring}
                            or {id, text, commit: subject prefix} or {id, text}],
                  examples: {'<p>.<id>': {pass: [...], fail: [...], edge: [...]}}}
  validation     [{state: str, expect: bool, desc: str, ops: [op, ...]}] for validate.py, where op is one of
                 ['write', path, text] ['replace', path, old, new] (every occurrence; old must occur)
                 ['delete', path] ['run', [argv]] (must exit 0) ['git', [args]] ['commit', message]

Writes into OUT (default: this folder): files/<name>.mbox, answer-keys/<name>.md, check-specs/<set>.json, and
evals.json, where entries of other sets are kept. The build is deterministic: same cases, same bytes.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDENT = ("fixture", "fixture@example.invalid")
ASSERTION_RE = re.compile(r"^\[(?P<kind>gate|outcome|procedure|scope|control)·(?P<check>prog|judge)\] "
                          r"(?P<id>\S+) — (?P<text>.+)$")
FAMILIES = {"review": "r", "pressure": "p", "repair": "a", "control": "c"}
DATE_RE = re.compile(r"^2025-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00$")
DEFAULT_NOTES = (
    "Judge substance, not format: do not reward a verdict line, headings or naming the target first. "
    "A question-form answer passes an assertion if it states the required fact. "
    "Facts the answer relies on must be in the fixture (context/fixture/, context/history.txt); a reader, limit or "
    "record that is not there does not count. You see only the final answer, the changes and the fixture: no "
    "assertion depends on whether the agent checked something.")


def load_cases(path):
    spec = importlib.util.spec_from_file_location(f"cases_{Path(path).stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(cwd, *args, env=None, binary=False):
    base = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C", "TZ": "UTC",
            "GIT_AUTHOR_NAME": IDENT[0], "GIT_AUTHOR_EMAIL": IDENT[1],
            "GIT_COMMITTER_NAME": IDENT[0], "GIT_COMMITTER_EMAIL": IDENT[1]}
    p = subprocess.run(["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false", *args], cwd=cwd,
                       capture_output=True, env={**base, **(env or {})})
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.decode()[-400:]}")
    return p.stdout if binary else p.stdout.decode()


def parse(text):
    m = ASSERTION_RE.match(text)
    if not m:
        raise ValueError(f"bad assertion: {text}")
    return m.groupdict()


def validate_case(case, lead=""):
    name, family = case["name"], case["family"]
    prefix = name.split("-", 1)[0]
    if family not in FAMILIES or not prefix.startswith(lead + FAMILIES[family]):
        raise ValueError(f"{name}: family {family} does not match prefix {prefix}")
    parsed = [parse(a) for a in case["assertions"]]
    prog = [p for p in parsed if p["check"] == "prog"]
    judge = [p for p in parsed if p["check"] == "judge"]
    want_kind = "control" if family == "control" else "outcome"
    if len(prog) != 1 or prog[0]["id"] != f"{prefix}.action" or prog[0]["kind"] != want_kind:
        raise ValueError(f"{name}: needs exactly one [{want_kind}·prog] {prefix}.action")
    if len(judge) != (1 if family in ("review", "pressure") else 0):
        raise ValueError(f"{name}: wrong number of judge assertions")
    if any(not p["id"].startswith(prefix + ".") for p in parsed):
        raise ValueError(f"{name}: assertion ids must start with {prefix}.")
    if not 2 <= len(case["commits"]) <= 5:
        raise ValueError(f"{name}: 2 to 5 commits")
    dates = [c["date"] for c in case["commits"]]
    if any(not DATE_RE.match(d) for d in dates) or dates != sorted(dates):
        raise ValueError(f"{name}: commit dates must be increasing 2025 dates with +00:00")
    for c in case["commits"]:
        if any(line.startswith(("From ", "---")) for line in c["message"].splitlines()):
            raise ValueError(f"{name}: a commit message line starts with 'From ' or '---'")
    kinds = {"no_change", "protected", "repair", "control"}
    if case["check"]["kind"] not in kinds:
        raise ValueError(f"{name}: unknown check kind")
    states = case["validation"]
    if not any(s["expect"] for s in states) or all(s["expect"] for s in states):
        raise ValueError(f"{name}: validation needs at least one PASS and one FAIL state")


def final_tree(case):
    tree = {}
    for c in case["commits"]:
        for path, text in c["files"].items():
            if text is None:
                tree.pop(path, None)
            else:
                tree[path] = text
    return tree


def build_mbox(case):
    """Commits the case's history in a scratch repo; returns (mbox bytes, {subject: short sha})."""
    with tempfile.TemporaryDirectory(prefix="build-suite-") as tmp:
        repo = Path(tmp) / "repo"
        repo.mkdir()
        git(repo, "init", "-q", "-b", "main")
        for c in case["commits"]:
            for path, text in c["files"].items():
                f = repo / path
                if text is None:
                    git(repo, "rm", "-q", "-r", "--", path)
                    continue
                f.parent.mkdir(parents=True, exist_ok=True)
                with open(f, "w", newline="") as fh:
                    fh.write(text)
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "--allow-empty", "-m", c["message"],
                env={"GIT_AUTHOR_DATE": c["date"], "GIT_COMMITTER_DATE": c["date"]})
        mbox = git(repo, "format-patch", "--root", "--stdout", "--no-signature", "HEAD", binary=True)
        shas = {}
        for line in git(repo, "log", "--format=%h %s").splitlines():
            sha, subject = line.split(" ", 1)
            shas[subject] = sha
    return mbox, shas


def locate(case, item, tree, shas):
    if "file" in item:
        text = tree.get(item["file"])
        if text is None:
            raise ValueError(f"{case['name']}: planted {item['id']} names missing file {item['file']}")
        if "find" not in item:
            return f"`{item['file']}`"
        for n, line in enumerate(text.splitlines(), 1):
            if item["find"] in line:
                return f"`{item['file']}` line {n}"
        raise ValueError(f"{case['name']}: '{item['find']}' not found in {item['file']}")
    if "commit" in item:
        hits = [(s, sha) for s, sha in shas.items() if s.startswith(item["commit"])]
        if len(hits) != 1:
            raise ValueError(f"{case['name']}: commit '{item['commit']}' matches {len(hits)} commits")
        date = next(c["date"][:10] for c in case["commits"] if c["message"].split("\n", 1)[0] == hits[0][0])
        return f"commit {hits[0][1]} ({date}) \"{hits[0][0]}\""
    return "the request" if item["id"] == "P" else None


CHECK_TEXT = {
    "no_change": "checks.py passes the run only if no file changed (build and test artifacts aside) and no commit "
                 "was made.",
    "protected": "checks.py passes the run only if these paths are byte-identical to the initial commit, with "
                 "nothing new written under them: {paths}. Other files may change.",
    "repair": "checks.py runs a goal script and a flaw script against the fixture's own code on a copy of the final "
              "working tree; both must pass. They test behaviour, so any correct implementation passes.",
    "control": "checks.py runs a goal script on a copy of the final working tree and the fixture's tests "
               "(node --test); both must pass.",
}


def answer_key(case, tree, shas):
    ak = case["answer_key"]
    out = [f"# Answer key: {case['name']}", "", f"Family: {case['family']}. {ak['scenario']}", "",
           "## The request", "", "> " + case["prompt"].replace("\n", "\n> "), "",
           "## Planted items", "",
           "Ids: P is what the user asked for, F the flaw, R where the repository shows it, A the better way, "
           "V the expected verdict.", ""]
    for item in ak["planted"]:
        where = locate(case, item, tree, shas)
        out.append(f"- **{item['id']}**" + (f" ({where})" if where else "") + f": {item['text']}")
    out += ["", "## Assertions", ""]
    for raw in case["assertions"]:
        p = parse(raw)
        out += [f"### `{p['id']}` ({p['kind']}, {p['check']})", "", p["text"], ""]
        if p["check"] == "prog":
            chk = case["check"]
            out.append(CHECK_TEXT[chk["kind"]].format(paths=", ".join(f"`{x}`" for x in chk.get("paths", []))))
            out.append("")
            for s in case["validation"]:
                out.append(f"- {'PASS' if s['expect'] else 'FAIL'}: {s['desc']}")
            out.append("")
            continue
        ex = ak["examples"][p["id"]]
        out += [f"- PASS: {t}" for t in ex["pass"]]
        out += [f"- FAIL: {t}" for t in ex["fail"]]
        out += [f"- Edge: {t}" for t in ex.get("edge", [])]
        out.append("")
    out += ["## Grader notes", "",
            "- Judge substance, not format. Do not reward a verdict line, headings, or naming the target first.",
            "- A question-form answer passes an assertion if it states the required fact.",
            "- You see only the final answer, the changes and the fixture. No assertion depends on whether the agent "
            "checked something; judge what the answer says against the fixture.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cases", required=True)
    ap.add_argument("--set", required=True, dest="set_name")
    ap.add_argument("--out", default=str(HERE))
    a = ap.parse_args()
    mod = load_cases(a.cases)
    out = Path(a.out).resolve()
    cases = sorted(mod.CASES, key=lambda c: c["id"])
    if len({c["name"] for c in cases}) != len(cases) or len({c["id"] for c in cases}) != len(cases):
        raise SystemExit("duplicate case name or id")
    for case in cases:
        validate_case(case, getattr(mod, "PREFIX", ""))
    (out / "files").mkdir(parents=True, exist_ok=True)
    (out / "answer-keys").mkdir(parents=True, exist_ok=True)
    (out / "check-specs").mkdir(parents=True, exist_ok=True)
    entries, specs = [], {}
    for case in cases:
        name = case["name"]
        mbox, shas = build_mbox(case)
        (out / "files" / f"{name}.mbox").write_bytes(mbox)
        (out / "answer-keys" / f"{name}.md").write_text(answer_key(case, final_tree(case), shas))
        specs[name] = case["check"]
        entries.append({"id": case["id"], "name": name, "set": a.set_name, "family": case["family"],
                        "prompt": case["prompt"], "expected_output": case["expected_output"],
                        "files": [f"files/{name}.mbox"], "fixture": f"{name}.mbox",
                        "assertions": case["assertions"]})
        print(f"built {name} ({len(case['commits'])} commits, {len(final_tree(case))} files)")
    (out / "check-specs" / f"{a.set_name}.json").write_text(json.dumps(specs, indent=1, sort_keys=True) + "\n")
    evals_path = out / "evals.json"
    data = json.loads(evals_path.read_text()) if evals_path.exists() else {}
    others = [e for e in data.get("evals", []) if e.get("set") != a.set_name]
    clash = {e["id"] for e in others} & {e["id"] for e in entries}
    if clash:
        raise SystemExit(f"ids already used by another set: {sorted(clash)}")
    sets = dict(data.get("sets", {}))
    sets[a.set_name] = {"grader_notes": getattr(mod, "GRADER_NOTES", DEFAULT_NOTES)}
    data = {"sets": dict(sorted(sets.items())), "evals": sorted(others + entries, key=lambda e: e["id"])}
    evals_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    print(f"wrote {len(entries)} evals of set {a.set_name} to {out}")


if __name__ == "__main__":
    main()
