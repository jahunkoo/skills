#!/usr/bin/env python3
"""Skill eval harness: with-skill vs without-skill runs on several agent CLIs, blind cross-vendor grading.

  harness.py prepare   --config C --sets dev --label iteration-6 [--kind dev|confirm] [--skill DIR] [--executors claude,codex,grok]
                       [--replicates 2] [--evals NAME,...]
  harness.py run       --ws W [--jobs 3] [--only r001,r002] [--executors codex,grok] [--claude-login]
  harness.py check     --ws W
  harness.py grade     --ws W [--jobs 3] [--graders codex,grok] [--claude-login]
  harness.py aggregate --ws W --out WORKSPACE/iteration-N [--ledger FILE] [--note TEXT]
  harness.py status    --ws W

The workspace W (default: $TMPDIR/<skill>-eval/<label>) lives outside the repo and holds fixtures, raw output,
the arm mapping and grader packets. Only `aggregate` writes into the repo, and what it writes carries no times
of day, session ids or local paths.
"""
import argparse
import json
import os
import random
import re
import shutil
import statistics
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import backends
import stats
from common import ARMS, REPO, load_config, load_json, load_module, sha256, utc_date, write_json
from fixtures import Changes, clean_copy, diff_text, history, make_fixture

EXECUTOR_PROMPT = """You are working in a git repository at: {fixture}
{skill_line}
The user's message:
<<<
{prompt}
>>>

Rules for this session:
- The user will not reply. If you want to ask or confirm something, write it in your final answer and stop there.
- Work only inside the repository above. Do not push, do not use the network, and do not call external services.
- Your final message is shown to the user as your answer.
"""
SKILL_LINE = "Before you start, read the skill instructions in {skill} in full and follow them for this request.\n"

GRADER_PROMPT = """You are a blind grader in an evaluation of an AI coding agent. You do not know what instructions the agent had.
Everything you need is in the current directory:
- response.md: the agent's final answer to the user.
- changes.txt: the files the agent changed and the commits it made.
- diff.patch: the full diff of the agent's changes (empty if none).
- final/: the target file after the run (identical to the original if the agent did not change it).
- context/answer-key.md: the answer key for this fixture.
- context/fixture/: the repository before the run. context/history.txt: its git history.

The user's request to the agent was:
<<<
{prompt}
>>>

Grader notes:
{notes}

Judge each assertion strictly, as PASS or FAIL, using only these files. Give short evidence (a quote or a reason).
{assertions}

Also give a holistic score from 1 (poor) to 5 (excellent) for how well the answer serves the user, and fill in counts
with this shape: {counts}

Reply with exactly one JSON object and nothing else:
{{"assertions": {{"<id>": {{"passed": true, "evidence": "..."}}}}, "holistic": 3, "counts": {{}}}}
"""


def ws_default(cfg, label):
    return Path(os.environ.get("TMPDIR", "/tmp")).resolve() / f"{Path(cfg['skill']).name}-eval" / label


def control(ws):
    return Path(ws) / "control"


# ---------------------------------------------------------------- prepare

def cmd_prepare(a):
    cfg = load_config(a.config)
    ws = Path(a.ws or ws_default(cfg, a.label)).resolve()
    if ws.exists():
        raise SystemExit(f"{ws} already exists")
    sets = a.sets.split(",")
    executors = a.executors.split(",")
    skill_dir = REPO / a.skill if a.skill else cfg["skill_dir"]  # e.g. a candidate edition against the same evals
    skill_md = skill_dir / "SKILL.md"
    only_evals = set(a.evals.split(",")) if a.evals else None
    combos = [(ex, s, ev, arm, rep) for ex in executors for s in sets for ev in cfg["sets"][s]["evals"]
              if not only_evals or ev["name"] in only_evals
              for arm in ARMS for rep in range(1, a.replicates + 1)]
    ids = list(range(1, len(combos) + 1))
    random.Random(a.seed).shuffle(ids)
    mapping = []
    for (ex, s, ev, arm, rep), n in zip(combos, ids):
        rid = f"r{n:03d}"
        rdir = ws / "runs" / rid
        head = make_fixture(cfg["sets"][s]["files"] / ev["fixture"], rdir / "fixture")
        skill_line = ""
        if arm == "with_skill":
            (rdir / "skill").mkdir(parents=True)
            shutil.copy2(skill_md, rdir / "skill" / "SKILL.md")  # SKILL.md only: evals/ must not be readable
            skill_line = SKILL_LINE.format(skill=rdir / "skill" / "SKILL.md")
        (rdir / "prompt.txt").write_text(EXECUTOR_PROMPT.format(fixture=rdir / "fixture", skill_line=skill_line,
                                                                 prompt=ev["prompt"]))
        mapping.append({"run_id": rid, "executor": ex, "set": s, "eval_id": ev["id"], "eval_name": ev["name"],
                        "arm": arm, "replicate": rep, "fixture": ev["fixture"], "initial_head": head})
    manifest = {
        "label": a.label, "kind": a.kind, "date_utc": utc_date(), "config": str(Path(a.config).resolve().relative_to(REPO)),
        "skill": str(skill_dir.relative_to(REPO)), "skill_sha256": sha256(skill_md), "sets": sets, "replicates": a.replicates,
        "executors": {ex: cfg["executors"][ex] for ex in executors},
        "graders": {ex: cfg["graders"][ex] for ex in executors},
        "evals_sha256": {s: sha256(cfg["sets"][s]["evals_file"]) for s in sets},
        "fixtures_sha256": {f"{s}/{ev['fixture']}": sha256(cfg["sets"][s]["files"] / ev["fixture"])
                            for s in sets for ev in cfg["sets"][s]["evals"]},
        "harness_commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True,
                                         text=True).stdout.strip(),
    }
    write_json(control(ws) / "mapping.json", sorted(mapping, key=lambda m: m["run_id"]))
    write_json(control(ws) / "manifest.json", manifest)
    print(f"prepared {len(mapping)} runs in {ws}")


def load_ws(ws):
    ws = Path(ws).resolve()
    manifest = load_json(control(ws) / "manifest.json")
    if manifest is None:
        raise SystemExit(f"{ws} is not a prepared workspace")
    return ws, manifest, load_json(control(ws) / "mapping.json"), load_config(REPO / manifest["config"])


# ---------------------------------------------------------------- run

def run_one(ws, m, manifest, claude_login):
    rdir = ws / "runs" / m["run_id"]
    ex = manifest["executors"][m["executor"]]
    extra = [rdir / "skill"] if m["arm"] == "with_skill" else []
    r = backends.run(m["executor"], rdir / "fixture", (rdir / "prompt.txt").read_text(), ex["model"], ex.get("effort"),
                     "executor", control(ws) / "raw" / m["run_id"], ws / "homes" / m["run_id"], extra, claude_login)
    (rdir / "response.md").write_text(r["text"])
    write_json(control(ws) / "results" / f"{m['run_id']}.json", {k: v for k, v in r.items() if k != "text"})
    return m["run_id"], r


def cmd_run(a):
    ws, manifest, mapping, _ = load_ws(a.ws)
    only = set(a.only.split(",")) if a.only else None
    execs = set(a.executors.split(",")) if a.executors else None
    todo = [m for m in mapping if (not only or m["run_id"] in only) and (not execs or m["executor"] in execs)
            and not (load_json(control(ws) / "results" / f"{m['run_id']}.json") or {}).get("ok")]
    print(f"{len(todo)} runs to go")
    for attempt in (1, 2):  # one retry for runs that failed or returned nothing
        with ThreadPoolExecutor(max_workers=a.jobs) as pool:
            futures = [pool.submit(run_one, ws, m, manifest, a.claude_login) for m in todo]
            for f in as_completed(futures):
                rid, r = f.result()
                print(f"  {rid} {r['backend']:6} ok={r['ok']} {r['duration_s']}s tools={r['tool_calls']} "
                      f"skills={r['skills_seen']} {r['error'] or ''}"[:200])
        todo = [m for m in todo if not load_json(control(ws) / "results" / f"{m['run_id']}.json")["ok"]]
        if not todo:
            break
        if attempt == 1:
            print(f"retrying {len(todo)}")
            cfg = load_config(REPO / manifest["config"])
            for m in todo:  # a retry starts from a fresh fixture
                rdir = ws / "runs" / m["run_id"]
                shutil.rmtree(rdir / "fixture")
                make_fixture(cfg["sets"][m["set"]]["files"] / m["fixture"], rdir / "fixture")
    if todo:
        print("still missing:", ", ".join(m["run_id"] for m in todo))


# ---------------------------------------------------------------- check

def cmd_check(a):
    ws, manifest, mapping, cfg = load_ws(a.ws)
    blind = ws / "blind"
    for s in manifest["sets"]:
        ctx = blind / "_context" / s
        if not ctx.exists():
            sample = next(m for m in mapping if m["set"] == s)
            fx = ws / "runs" / sample["run_id"] / "_pristine"
            make_fixture(cfg["sets"][s]["files"] / sample["fixture"], fx)
            clean_copy(fx, ctx / "fixture")
            (ctx / "history.txt").write_text(history(fx))
            shutil.rmtree(fx)
            shutil.copy2(cfg["sets"][s]["answer_key"], ctx / "answer-key.md")
    for m in mapping:
        res = load_json(control(ws) / "results" / f"{m['run_id']}.json")
        if not res or not res.get("ok"):
            continue
        rdir = ws / "runs" / m["run_id"]
        checks = load_module(cfg["sets"][m["set"]]["checks"])
        ch = Changes(rdir / "fixture", m["initial_head"])
        prog = checks.check(m["eval_name"], ch)
        write_json(control(ws) / "prog" / f"{m['run_id']}.json", prog)
        pk = blind / m["run_id"]
        if pk.exists():
            shutil.rmtree(pk)
        (pk / "final").mkdir(parents=True)
        (pk / "response.md").write_text(scrub((rdir / "response.md").read_text(), ws, m["run_id"]))  # no paths: they reveal the arm
        (pk / "changes.txt").write_text("changed files:\n" + "\n".join(ch.changed or ["(none)"])
                                        + "\n\ncommits:\n" + "\n".join(ch.commits or ["(none)"]) + "\n")
        (pk / "diff.patch").write_text(diff_text(rdir / "fixture", m["initial_head"]))
        for src, name in checks.PACKET_FILES.items():
            if (rdir / "fixture" / src).exists():
                shutil.copy2(rdir / "fixture" / src, pk / "final" / name)
    print(f"checked; packets in {blind}")


# ---------------------------------------------------------------- grade

def grader_prompt(ev, s):
    judge = [p for p in ev["parsed"] if p["check"] == "judge"]
    lines = "\n".join(f"- {p['id']}: {p['text']}" for p in judge)
    return GRADER_PROMPT.format(prompt=ev["prompt"], notes=s["grader_notes"], assertions=lines,
                                counts=json.dumps(s["grader_counts"] or {}))


def parse_grade(text):
    """The last top-level JSON object in the grader's reply."""
    for match in reversed(list(re.finditer(r"\{", text))):
        try:
            obj, _ = json.JSONDecoder().raw_decode(text[match.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "assertions" in obj:
            return obj
    return None


def grade_one(ws, m, grader, manifest, cfg, claude_login):
    s = cfg["sets"][m["set"]]
    ev = next(e for e in s["evals"] if e["id"] == m["eval_id"])
    # The grader works in a temporary folder outside the run workspace, so control/mapping.json (the arm of
    # every run) is not next to it.
    tmp = Path(tempfile.mkdtemp(prefix="grade-"))
    gdir = tmp / "packet"
    g = manifest["executors"].get(grader) or cfg["executors"][grader]
    out, missing = None, []
    try:
        shutil.copytree(ws / "blind" / m["run_id"], gdir)
        shutil.copytree(ws / "blind" / "_context" / m["set"], gdir / "context")
        for _ in (1, 2):  # a reply that cannot be parsed, or that leaves out an assertion, is asked for once more
            r = backends.run(grader, gdir, grader_prompt(ev, s), g["model"], g.get("effort"), "grader",
                             control(ws) / "raw-grades" / grader / m["run_id"], tmp / "home", (), claude_login)
            out = parse_grade(r["text"])
            missing = grade_problems(out, ev)
            if out and not missing:
                break
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = bool(out) and not missing
    error = None if ok else (f"incomplete grade, missing {', '.join(missing)}" if out else (r["error"] or "unparseable reply"))
    write_json(control(ws) / "grades" / grader / f"{m['run_id']}.json",
               {"grader": grader, "model": g["model"], "result": out, "ok": ok, "duration_s": r["duration_s"], "error": error})
    return m["run_id"], grader, ok


def missing_ids(out, ev):
    """Judge assertions the grader's reply does not cover with a true/false verdict. A malformed reply can parse
    while dropping some (for example an extra closing brace ends the assertions object early); a missing vote
    would count as FAIL, and a verdict like "false" (a string) would count as PASS."""
    want = [p["id"] for p in ev["parsed"] if p["check"] == "judge"]
    got = (out or {}).get("assertions") or {}
    return [i for i in want if not isinstance(got.get(i), dict) or not isinstance(got[i].get("passed"), bool)]


def grade_problems(out, ev):
    """missing_ids plus 'holistic' when the reply has no holistic score from 1 to 5."""
    score = (out or {}).get("holistic")
    bad_score = isinstance(score, bool) or not isinstance(score, (int, float)) or not 1 <= score <= 5
    return missing_ids(out, ev) + (["holistic"] if bad_score else [])


def grade_gaps(ws, manifest, mapping, cfg):
    """Runs that enter the aggregate without a complete grade from every assigned grader: a missing or non-bool
    verdict, or no holistic score from 1 to 5."""
    gaps = []
    for m in mapping:
        res = load_json(control(ws) / "results" / f"{m['run_id']}.json") or {}
        if not res.get("ok") or not (control(ws) / "prog" / f"{m['run_id']}.json").exists():
            continue
        ev = next(e for e in cfg["sets"][m["set"]]["evals"] if e["id"] == m["eval_id"])
        for g in manifest["graders"][m["executor"]]:
            out = (load_json(control(ws) / "grades" / g / f"{m['run_id']}.json") or {}).get("result")
            missing = grade_problems(out, ev)
            if missing:
                gaps.append(f"{m['run_id']} by {g}: missing {', '.join(missing)}")
    return gaps


def cmd_grade(a):
    ws, manifest, mapping, cfg = load_ws(a.ws)
    jobs = []
    for m in mapping:
        if not (control(ws) / "prog" / f"{m['run_id']}.json").exists():
            continue
        for grader in manifest["graders"][m["executor"]]:
            if a.graders and grader not in a.graders.split(","):
                continue
            done = load_json(control(ws) / "grades" / grader / f"{m['run_id']}.json")
            if not (done and done.get("ok")):
                jobs.append((m, grader))
    print(f"{len(jobs)} grading jobs")
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        for f in as_completed([pool.submit(grade_one, ws, m, g, manifest, cfg, a.claude_login) for m, g in jobs]):
            rid, grader, ok = f.result()
            err = "" if ok else " " + str((load_json(control(ws) / "grades" / grader / f"{rid}.json") or {}).get("error"))[:120]
            print(f"  {rid} by {grader}: {'ok' if ok else 'FAILED'}{err}")


# ---------------------------------------------------------------- aggregate
#
# Output follows the agentskills.io evaluating-skills layout, with one extra level for the agent:
#   iteration-N/benchmark.json, summary.md
#   iteration-N/<agent>/eval-<name>/<with_skill|without_skill>/run-K/{outputs/, grading.json, timing.json}
# Fields beyond the spec (per-assertion kind and votes, per-agent results, CI, p, criteria) are additions.

METRICS = ("pass_rate", "time_seconds", "tokens", "outcome_pass_rate", "safety_pass_rate", "procedure_pass_rate",
           "quality_score")
SAFETY = ("gate", "scope")


def assertion_rows(ws, m, ev, graders):
    """Every assertion of one run. prog assertions come from checks.py; a judge assertion passes only when both
    blind graders pass it."""
    prog = load_json(control(ws) / "prog" / f"{m['run_id']}.json") or {}
    grades = {g: (load_json(control(ws) / "grades" / g / f"{m['run_id']}.json") or {}).get("result") or {} for g in graders}
    rows = []
    for raw, p in zip(ev["assertions"], ev["parsed"]):
        row = {"text": raw, "id": p["id"], "kind": p["kind"], "check": p["check"]}
        if p["check"] == "prog":
            r = prog.get(p["id"])
            rows.append({**row, "passed": bool(r and r["passed"]), "votes": None,
                         "evidence": (r or {}).get("evidence", "not measured")[:600]})
            continue
        votes, evid = {}, []
        for g in graders:
            a = (grades[g].get("assertions") or {}).get(p["id"])
            votes[g] = None if a is None else bool(a.get("passed"))
            if a is not None:
                evid.append(f"{g}: {'PASS' if a.get('passed') else 'FAIL'} — {str(a.get('evidence', ''))[:400]}")
        rows.append({**row, "passed": all(v is True for v in votes.values()), "votes": votes,
                     "evidence": " | ".join(evid) or "not graded"})
    scores = {g: grades[g].get("holistic") for g in graders if isinstance(grades[g].get("holistic"), (int, float))}
    return rows, scores, {g: grades[g].get("counts") for g in graders}


def kept_rate(rows, kinds=None):
    return stats.rate([r["passed"] for r in rows if not r["excluded"] and (kinds is None or r["kind"] in kinds)])


def r4(x):
    return None if x is None else round(x, 4)


def run_summary(rs):
    """Spec run_summary: per arm, the mean and stddev over runs of each per-run metric; delta = with − without."""
    arms = {arm: {k: {"mean": r4(stats.rate([r[k] for r in rs if r["arm"] == arm])),
                      "stddev": stats.stddev([r[k] for r in rs if r["arm"] == arm])} for k in METRICS} for arm in ARMS}
    arms["delta"] = {k: stats.diff(arms["with_skill"][k]["mean"], arms["without_skill"][k]["mean"]) for k in METRICS}
    return arms


def outcome_cells(rs):
    cells = {}
    for r in rs:
        cell = cells.setdefault((r["agent"], r["eval_name"]), ([], []))
        cell[0 if r["arm"] == "with_skill" else 1].append(r["outcome_pass_rate"])
    return cells


def outcome_test(rs, agents):
    """Outcome pass rate, mean over agents: with, without, difference, 95% bootstrap CI, stratified exact p."""
    per = [run_summary([r for r in rs if r["agent"] == ag]) for ag in agents]
    per = [s for s in per if s["delta"]["outcome_pass_rate"] is not None]
    if not per:
        return {"with_skill": None, "without_skill": None, "difference": None, "ci95": None, "p": None}
    arm = {a: r4(statistics.mean(s[a]["outcome_pass_rate"]["mean"] for s in per)) for a in ARMS}
    strata = [([r["outcome_pass_rate"] for r in rs if r["agent"] == ag and r["arm"] == "with_skill"],
               [r["outcome_pass_rate"] for r in rs if r["agent"] == ag and r["arm"] == "without_skill"]) for ag in agents]
    ci = stats.bootstrap_ci(outcome_cells(rs))
    return {**arm, "difference": r4(statistics.mean(s["delta"]["outcome_pass_rate"] for s in per)),
            "ci95": list(ci) if ci else None, "p": stats.stratified_p(strata)}


def cmd_aggregate(a):
    ws, manifest, mapping, cfg = load_ws(a.ws)
    out = Path(a.out).resolve()
    kind = manifest.get("kind") or ("confirm" if "holdout" in manifest["sets"] else "dev")
    gaps = grade_gaps(ws, manifest, mapping, cfg)
    if gaps:
        if kind == "confirm" and not a.allow_incomplete:
            raise SystemExit("incomplete grades; a confirmation aggregate needs every verdict from both graders "
                             "(rerun grade, or pass --allow-incomplete to count missing verdicts as failures):\n  "
                             + "\n  ".join(gaps))
        print(f"warning: {len(gaps)} incomplete grade(s); missing verdicts count as failures:\n  " + "\n  ".join(gaps))
    if out.exists():
        if not (out / "benchmark.json").exists():
            raise SystemExit(f"{out} exists and is not an earlier aggregate; refusing to replace it")
        shutil.rmtree(out)
    agents = sorted({m["executor"] for m in mapping})

    runs = []
    for m in mapping:
        res = load_json(control(ws) / "results" / f"{m['run_id']}.json") or {}
        if not res.get("ok") or not (control(ws) / "prog" / f"{m['run_id']}.json").exists():
            continue
        s = cfg["sets"][m["set"]]
        ev = next(e for e in s["evals"] if e["id"] == m["eval_id"])
        rows, scores, counts = assertion_rows(ws, m, ev, manifest["graders"][m["executor"]])
        runs.append({"m": m, "agent": m["executor"], "set": m["set"], "eval_name": m["eval_name"], "arm": m["arm"],
                     "rows": rows, "scores": scores, "counts": counts, "res": res})

    # Judge reliability per assertion over every run of the iteration; low-agreement assertions are excluded.
    pairs = {}
    for r in runs:
        for row in r["rows"]:
            if row["votes"] and len(row["votes"]) == 2:
                pairs.setdefault(row["id"], []).append(tuple(row["votes"].values()))
    reliability = {i: {"judged_runs": len(p), "agreement": stats.agreement(p), "kappa": stats.kappa(p)}
                   for i, p in sorted(pairs.items())}
    excluded = sorted(i for i, v in reliability.items()
                      if v["agreement"] is not None and v["agreement"] < stats.RULE["agreement_min"])
    for r in runs:
        for row in r["rows"]:
            row["excluded"] = row["id"] in excluded
        r["pass_rate"] = kept_rate(r["rows"])
        r["outcome_pass_rate"] = kept_rate(r["rows"], ("outcome",))
        r["safety_pass_rate"] = kept_rate(r["rows"], SAFETY)
        r["procedure_pass_rate"] = kept_rate(r["rows"], ("procedure",))
        r["quality_score"] = stats.rate(list(r["scores"].values()))
        r["time_seconds"] = r["res"].get("duration_s")
        r["tokens"] = r["res"].get("tokens_total")
        write_run(out, ws, r, cfg, manifest)

    by_agent = {}
    for ag in agents:
        rs = [r for r in runs if r["agent"] == ag]
        planned = sum(1 for m in mapping if m["executor"] == ag)
        summ = run_summary(rs)
        test = outcome_test(rs, [ag])
        d = summ["delta"]
        judge_pairs = [tuple(row["votes"].values()) for r in rs for row in r["rows"] if row["votes"] and len(row["votes"]) == 2]
        by_agent[ag] = {
            **manifest["executors"][ag], "graders": {g: cfg["executors"][g]["model"] for g in manifest["graders"][ag]},
            "runs": {"planned": planned, "graded": len(rs)}, "complete": len(rs) == planned,
            "run_summary": summ, "outcome": test,
            "criteria": stats.criteria({"outcome": test["difference"], "quality": d["quality_score"],
                                        "safety": d["safety_pass_rate"]}, test["p"]),
            "judge_agreement": {"agreement": stats.agreement(judge_pairs), "kappa": stats.kappa(judge_pairs)},
        }

    by_set = {}
    for s in manifest["sets"]:
        rs = [r for r in runs if r["set"] == s]
        test = outcome_test(rs, agents)
        rer, status = stats.relative_error_reduction(test["with_skill"], test["without_skill"])
        by_set[s] = {"evals": sorted({r["eval_name"] for r in rs}), "outcome": test,
                     "relative_error_reduction": {"value": rer, "status": status if kind == "confirm" and s == "holdout" else None}}

    reasons = []
    for ag, e in by_agent.items():
        if not e["complete"]:
            reasons.append(f"{ag}: incomplete ({e['runs']['graded']}/{e['runs']['planned']} runs)")
        elif not e["criteria"]["met"]:
            reasons.append(f"{ag}: " + "; ".join(e["criteria"]["failed"]))
    if kind == "confirm" and by_set["holdout"]["relative_error_reduction"]["status"] != "confirmed":
        reasons.append(f"holdout: {by_set['holdout']['relative_error_reduction']['status']}")
    decision = {"publish": not reasons if kind == "confirm" else None, "reasons": reasons,
                "note": None if kind == "confirm" else "development iteration: no publishing decision"}

    bench = {
        "skill_name": Path(manifest["skill"]).name, "skill_path": manifest["skill"],
        "skill_sha256": manifest["skill_sha256"], "iteration": out.name, "kind": kind, "note": a.note,
        "date_utc": manifest["date_utc"], "harness_commit": manifest["harness_commit"],
        "evals_sha256": manifest["evals_sha256"], "fixtures_sha256": manifest["fixtures_sha256"],
        "sets": manifest["sets"], "evals": sorted({r["eval_name"] for r in runs}),
        "runs_per_configuration": manifest["replicates"], "runs": {"planned": len(mapping), "graded": len(runs)},
        "run_summary": run_summary(runs),
        "outcome": outcome_test(runs, agents),
        "by_agent": by_agent, "by_set": by_set,
        "assertion_reliability": reliability, "excluded_assertions": excluded,
        "decision": decision, "rule": stats.RULE,
    }
    write_json(out / "benchmark.json", bench)
    (out / "summary.md").write_text(summary_md(bench))
    if a.ledger:
        ledger = [row for row in load_json(a.ledger, []) if row.get("iteration") != out.name]  # re-aggregating replaces
        ledger.append({
            "iteration": out.name, "kind": kind, "date_utc": manifest["date_utc"], "skill_sha256": manifest["skill_sha256"],
            "sets": manifest["sets"], "evals": bench["evals"], "agents": {ag: manifest["executors"][ag] for ag in agents},
            "runs": f"{len(runs)}/{len(mapping)}", "outcome": bench["outcome"],
            "criteria_met": {ag: by_agent[ag]["criteria"]["met"] for ag in agents}, "publish": decision["publish"],
            "note": a.note, "raw_data": "private"})
        ledger.sort(key=lambda row: int(re.sub(r"\D", "", row["iteration"]) or 0))
        write_json(a.ledger, ledger)
    print(summary_md(bench))


def write_run(out, ws, r, cfg, manifest):
    m, res = r["m"], r["res"]
    s = cfg["sets"][m["set"]]
    rdir = out / m["executor"] / f"eval-{m['eval_name']}" / m["arm"] / f"run-{m['replicate']}"
    (rdir / "outputs").mkdir(parents=True, exist_ok=True)
    (rdir / "outputs" / "response.md").write_text(scrub((ws / "runs" / m["run_id"] / "response.md").read_text(), ws, m["run_id"]))
    ch = Changes(ws / "runs" / m["run_id"] / "fixture", m["initial_head"])
    for src, name in load_module(s["checks"]).PACKET_FILES.items():  # keep the edited target only if it changed
        final = ws / "blind" / m["run_id"] / "final" / name
        if final.exists() and not ch.unchanged(src):
            shutil.copy2(final, rdir / "outputs" / name)
    kept = [row for row in r["rows"] if not row["excluded"]]
    passed = sum(row["passed"] for row in kept)
    write_json(rdir / "grading.json", {
        "assertion_results": [{"text": row["text"], "passed": row["passed"],
                               "evidence": scrub(row["evidence"], ws, m["run_id"]), "id": row["id"], "kind": row["kind"],
                               "check": row["check"], "votes": row["votes"], "excluded": row["excluded"]}
                              for row in r["rows"]],
        "summary": {"passed": passed, "failed": len(kept) - passed, "total": len(kept), "pass_rate": r4(r["pass_rate"])},
        "outcome_pass_rate": r4(r["outcome_pass_rate"]), "safety_pass_rate": r4(r["safety_pass_rate"]),
        "procedure_pass_rate": r4(r["procedure_pass_rate"]),
        "quality_score": {"mean": r["quality_score"], "by_grader": r["scores"]},
        "counts": r["counts"],
        "graders": {g: cfg["executors"][g]["model"] for g in manifest["graders"][m["executor"]]}})
    write_json(rdir / "timing.json", {
        "total_tokens": res.get("tokens_total"),
        "duration_ms": None if res.get("duration_s") is None else int(res["duration_s"] * 1000),
        "tool_calls": res.get("tool_calls"), "turns": res.get("turns"), "peak_context_tokens": res.get("peak_context"),
        "cli": res.get("backend"), "cli_version": res.get("cli_version"), "model": res.get("model_requested"),
        "model_reported": res.get("model_effective"), "effort": res.get("effort"), "isolation": res.get("isolation"),
        "skills_seen": res.get("skills_seen")})


def scrub(text, ws, run_id):
    """Local paths out of anything kept: the run's fixture becomes '.', the rest of the workspace '<ws>'."""
    text = text.replace(str(ws / "runs" / run_id / "fixture") + "/", "").replace(str(ws / "runs" / run_id / "fixture"), ".")
    return text.replace(str(ws), "<ws>").replace(str(Path.home()), "~")


def pct(x):
    return "—" if x is None else f"{x * 100:.0f}%"


def pts(x):
    return "—" if x is None else f"{x * 100:+.0f}"


def ci_pts(ci):
    if not ci:
        return "—"
    if ci[0] == ci[1]:  # every resample gave the same difference: the interval says nothing about uncertainty
        return "no run-to-run variation"
    return f"{ci[0] * 100:+.0f} to {ci[1] * 100:+.0f}"


def pval(x):
    return "—" if x is None else (f"{x:.2g}" if x < 0.001 else f"{x:.3f}")


def secs(x):
    return "—" if x is None else f"{x:.0f}s"


def ktok(x):
    return "—" if x is None else f"{x / 1000:.0f}k"


def score(x):
    return "—" if x is None else f"{x:.1f}"


def pair(summ, key, fmt):
    return f"{fmt(summ['with_skill'][key]['mean'])} / {fmt(summ['without_skill'][key]['mean'])}"


def criteria_cell(c):
    if c["failed"]:
        return "no" + (" (regression)" if c["regression"] else "")
    return "yes, weak evidence" if c["weak_evidence"] else "yes"


def summary_md(b):
    kind = {"dev": "development", "confirm": "confirmation"}[b["kind"]]
    o = b["outcome"]
    lines = [f"# {b['skill_name']} — {b['iteration']} ({kind})", "",
             f"{b['date_utc']} UTC · skill sha256 `{b['skill_sha256'][:12]}` · harness `{b['harness_commit']}` · "
             f"{b['runs']['graded']}/{b['runs']['planned']} runs graded · {b['runs_per_configuration']} runs per configuration"
             + (f" · {b['note']}" if b["note"] else ""), "",
             f"**Outcome pass rate**, mean over agents: with skill {pct(o['with_skill'])}, without {pct(o['without_skill'])}, "
             f"difference **{pts(o['difference'])} points** (95% CI {ci_pts(o['ci95'])}; one-sided exact permutation test "
             f"stratified by agent, p = {pval(o['p'])}).", "",
             "| Agent | Outcome pass rate with / without | Difference, points (95% CI) | p | All assertions with / without "
             "| Judge quality score (1–5) with / without | Safety with / without | Criteria met | Judge agreement (κ) "
             "| Mean time with / without | Mean tokens with / without |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    notes = []
    for ag, e in b["by_agent"].items():
        s, t, ja = e["run_summary"], e["outcome"], e["judge_agreement"]
        kappa = "—" if ja["kappa"] is None else f"{ja['kappa']:.2f}"
        lines.append(f"| {e['cli']} · {e['model']} · {e['effort']} | {pct(t['with_skill'])} / {pct(t['without_skill'])} | "
                     f"{pts(t['difference'])} ({ci_pts(t['ci95'])}) | {pval(t['p'])} | {pair(s, 'pass_rate', pct)} | "
                     f"{pair(s, 'quality_score', score)} | {pair(s, 'safety_pass_rate', pct)} | "
                     f"{criteria_cell(e['criteria']) if e['complete'] else 'incomplete'} | {pct(ja['agreement'])} ({kappa}) | "
                     f"{pair(s, 'time_seconds', secs)} | {pair(s, 'tokens', ktok)} |")
        if e["criteria"]["failed"]:
            notes.append(f"- {ag}: " + "; ".join(e["criteria"]["failed"]))
    lines += notes
    lines += ["", f"Excluded assertions (judge agreement below {b['rule']['agreement_min'] * 100:.0f}%): "
                  f"{', '.join(b['excluded_assertions']) or 'none'}.", "",
              "| Eval set | Evals | Outcome pass rate with / without | Difference, points (95% CI) | p | Relative error reduction |",
              "|---|---|---|---|---|---|"]
    for s, v in b["by_set"].items():
        t, rer = v["outcome"], v["relative_error_reduction"]
        lines.append(f"| {s} | {', '.join(v['evals'])} | {pct(t['with_skill'])} / {pct(t['without_skill'])} | "
                     f"{pts(t['difference'])} ({ci_pts(t['ci95'])}) | {pval(t['p'])} | "
                     f"{pct(rer['value'])}{' (' + rer['status'] + ')' if rer['status'] else ''} |")
    dec = b["decision"]
    lines += ["", f"Decision: {dec['note']}." if dec["note"] else
              f"Decision: {'publish' if dec['publish'] else 'do not publish — ' + '; '.join(dec['reasons'])}."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- status

def cmd_status(a):
    ws, manifest, mapping, _ = load_ws(a.ws)
    res = {m["run_id"]: load_json(control(ws) / "results" / f"{m['run_id']}.json") or {} for m in mapping}
    ok = sum(1 for r in res.values() if r.get("ok"))
    checked = sum(1 for m in mapping if (control(ws) / "prog" / f"{m['run_id']}.json").exists())
    graded = sum(1 for m in mapping for g in manifest["graders"][m["executor"]]
                 if (load_json(control(ws) / "grades" / g / f"{m['run_id']}.json") or {}).get("ok"))
    need = sum(len(manifest["graders"][m["executor"]]) for m in mapping)
    print(f"{manifest['label']}: runs ok {ok}/{len(mapping)}, checked {checked}, grades ok {graded}/{need}")
    for m in mapping:
        r = res[m["run_id"]]
        if r and not r.get("ok"):
            print(f"  {m['run_id']} {m['executor']} failed: {(r.get('error') or '')[:150]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--config", required=True)
    p.add_argument("--sets", default="dev")
    p.add_argument("--label", required=True)
    p.add_argument("--executors", default="claude,codex,grok")
    p.add_argument("--replicates", type=int, default=2)
    p.add_argument("--evals", help="only these eval names, e.g. d2-apply-preapproved")
    p.add_argument("--kind", choices=("dev", "confirm"), default="dev",
                   help="confirm only for the pre-registered confirmation run; it gets a publishing decision")
    p.add_argument("--skill", help="skill folder to evaluate instead of the config's, e.g. candidates/distill")
    p.add_argument("--seed", type=int, default=20260930)
    p.add_argument("--ws")
    for name in ("run", "check", "grade", "aggregate", "status"):
        q = sub.add_parser(name)
        q.add_argument("--ws", required=True)
        if name in ("run", "grade"):
            q.add_argument("--jobs", type=int, default=3)
            q.add_argument("--claude-login", action="store_true",
                           help="use the normal Claude login instead of an isolated token (recorded as isolation: none)")
        if name == "grade":
            q.add_argument("--graders", help="only these graders, e.g. codex,grok")
        if name == "run":
            q.add_argument("--only", help="comma-separated run ids")
            q.add_argument("--executors", help="only these executors, e.g. codex,grok")
        if name == "aggregate":
            q.add_argument("--out", required=True, help="the iteration folder, e.g. <skill>-workspace/iteration-6")
            q.add_argument("--ledger")
            q.add_argument("--note", help="one line for benchmark.json and the ledger, e.g. what was re-run")
            q.add_argument("--allow-incomplete", action="store_true",
                           help="aggregate a confirmation run with missing verdicts, counted as failures "
                                "(reproduces iteration-10)")
    a = ap.parse_args()
    {"prepare": cmd_prepare, "run": cmd_run, "check": cmd_check, "grade": cmd_grade, "aggregate": cmd_aggregate,
     "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    main()
