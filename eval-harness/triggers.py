#!/usr/bin/env python3
"""Trigger test: with the skill installed but not mentioned, does the agent load it for the right requests?

  triggers.py --config C --queries FILE --label L --out FILE [--executors claude,codex,grok] [--runs 2] [--jobs 4]

Each session gets a fresh temporary HOME with only this skill installed at user level (codex, grok:
~/.agents/skills/<name>/SKILL.md; claude: <config dir>/skills/<name>/SKILL.md) and an empty git project.
A session counts as triggered when the agent reads that SKILL.md or calls Skill(<name>). The session is stopped
as soon as it triggers or after a few tool calls, because only the decision to load the skill is measured.
`discovered` records whether the CLI listed the skill at startup (claude and grok report this; codex does not).
"""
import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import backends
from common import REPO, load_config, load_json, sha256, utc_date, write_json

MAX_TOOL_CALLS = 4
TIMEOUT = 300


def argv(backend, proj, query, model, effort):
    if backend == "claude":
        a = ["claude", "-p", query, "--output-format", "stream-json", "--verbose", "--model", model,
             "--no-session-persistence", "--disallowedTools", "Bash,Edit,Write,NotebookEdit,WebFetch,WebSearch,Agent"]
        return a + (["--effort", effort] if effort else []), None
    if backend == "codex":
        a = ["codex", "exec", "-C", str(proj), "--skip-git-repo-check", "--sandbox", "read-only", "--ignore-user-config",
             "--ignore-rules", "--ephemeral", "--json", "-m", model]
        return a + (["-c", f"model_reasoning_effort={effort}"] if effort else []) + ["-"], query
    if backend == "grok":
        a = ["grok", "--no-auto-update", "--cwd", str(proj), "-m", model, "-p", query, "--output-format",
             "streaming-messages-json", "--always-approve", "--max-turns", "3", "--tools", "read_file,list_dir,grep"]
        return a + (["--reasoning-effort", effort] if effort else []), None
    raise ValueError(backend)


def events(backend, ev, name, pat):
    """Yield ('discovered', bool) / ('tool', triggered: bool) from one output event."""
    if ev.get("type") == "system" and "skills" in ev:
        yield "discovered", any(str(s).split(":")[-1] == name for s in ev.get("skills") or [])
    if backend in ("claude", "grok") and ev.get("type") == "assistant":
        for b in (ev.get("message") or {}).get("content", []):
            if b.get("type") == "tool_use":
                inp = b.get("input") or {}
                hit = (b.get("name") == "Skill" and str(inp.get("skill", "")).split(":")[-1] == name) or bool(pat.search(json.dumps(inp)))
                yield "tool", hit
    if backend == "codex" and ev.get("type") == "item.started" and (ev.get("item") or {}).get("type") == "command_execution":
        yield "tool", bool(pat.search(ev["item"].get("command", "")))


def session(backend, query, cfg, skill_md, name, claude_login):
    tmp = Path(tempfile.mkdtemp(prefix="trig-"))
    try:
        proj, home = tmp / "project", tmp / "home"
        proj.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=proj, check=True)
        (proj / "README.md").write_text("# demo\n")
        env, isolation = backends.isolated_env(backend, home, claude_login)
        skill_dir = (Path(env["CLAUDE_CONFIG_DIR"]) / "skills" if backend == "claude" and isolation == "temp-home"
                     else home / ".agents" / "skills") / name
        if backend == "claude" and isolation == "none":
            raise SystemExit("the Claude trigger test needs an isolated token: installing into the real ~/.claude is not allowed")
        skill_dir.mkdir(parents=True)
        shutil.copy2(skill_md, skill_dir / "SKILL.md")
        ex = cfg["executors"][backend]
        a, stdin = argv(backend, proj, query, ex["model"], ex.get("effort"))
        pat = re.compile(r"skills/" + re.escape(name) + r"/SKILL\.md")
        p = subprocess.Popen(a, cwd=proj, env=env, stdin=subprocess.PIPE if stdin else subprocess.DEVNULL,
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, start_new_session=True)
        if stdin:
            p.stdin.write(stdin)
            p.stdin.close()
        triggered, discovered, tools, start = False, None, 0, time.monotonic()
        for line in p.stdout:
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            for kind, val in events(backend, ev, name, pat):
                if kind == "discovered":
                    discovered = val
                else:
                    tools += 1
                    triggered = triggered or val
            if triggered or tools >= MAX_TOOL_CALLS or time.monotonic() - start > TIMEOUT:
                break
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGTERM)
        p.wait(timeout=30)
        return {"triggered": triggered, "discovered": discovered, "tool_calls_seen": tools, "isolation": isolation}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--executors", default="claude,codex,grok")
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--claude-login", action="store_true")
    ap.add_argument("--skill", help="skill folder to test instead of the config's, e.g. candidates/distill")
    a = ap.parse_args()
    cfg = load_config(a.config)
    skill_md = (REPO / a.skill if a.skill else cfg["skill_dir"]) / "SKILL.md"
    spec = load_json(a.queries)
    name = spec["skill_name"]
    jobs = [(ex, i, q, r) for ex in a.executors.split(",") for i, q in enumerate(spec["queries"]) for r in range(a.runs)]
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(lambda j: (j, session(j[0], j[2]["q"], cfg, skill_md, name, a.claude_login)), jobs))
    out = {"label": a.label, "date_utc": utc_date(), "skill_sha256": sha256(skill_md), "queries_sha256": sha256(a.queries),
           "runs_per_query": a.runs, "max_tool_calls": MAX_TOOL_CALLS, "executors": {}}
    for ex in a.executors.split(","):
        rows = [(j, r) for j, r in results if j[0] == ex]
        pos = [r for j, r in rows if j[2]["target"] == name]
        neg = [r for j, r in rows if j[2]["target"] != name]
        out["executors"][ex] = {
            "model": cfg["executors"][ex], "isolation": sorted({r["isolation"] for _, r in rows}),
            "recall": [sum(r["triggered"] for r in pos), len(pos)],
            "false_trigger": [sum(r["triggered"] for r in neg), len(neg)],
            "discovered": [sum(1 for _, r in rows if r["discovered"]), sum(1 for _, r in rows if r["discovered"] is not None)],
            "queries": [{"index": i, "target": q["target"], "triggered": [r["triggered"] for j, r in rows if j[1] == i]}
                        for i, q in enumerate(spec["queries"])]}
        e = out["executors"][ex]
        print(f"{ex}: recall {e['recall'][0]}/{e['recall'][1]}, false triggers {e['false_trigger'][0]}/{e['false_trigger'][1]}, "
              f"discovered {e['discovered'][0]}/{e['discovered'][1]}")
    write_json(a.out, out)


if __name__ == "__main__":
    main()
