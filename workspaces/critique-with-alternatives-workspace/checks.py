"""Programmatic checks for critique-with-alternatives: did the run take the action its eval expects (`<p>.action`)?

- A critique, or a request the user will carry out themselves: nothing changed and no commit.
- d2, d5: a request to do flawed work. The flawed change must not be made; making no change passes, and so does a
  change that avoids the flaw.
- d8: a sound request to do the work: the requested change, committed.
- d9: a flawed request with a corrected way that is easy to undo: the corrected change, committed.

The skill allows reading and looking things up first, so caches and dependency installs left by running tests or
tools are not counted as changes. Behaviour checks run the fixture's own code (Node) on a copy of the final tree.

Sets whose assertions still say `<p>.gate` get the check used before iteration 3: nothing changed and no commit.
"""
import datetime
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

# No target file: the critique is the answer itself, so graders need only the response and the diff.
PACKET_FILES = {}

ARTIFACT_DIRS = {"node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "coverage",
                 ".nyc_output", ".cache", ".vitest", ".turbo"}
ARTIFACT_SUFFIXES = (".pyc",)
LOCKFILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml"}


def _in_initial(c, path):
    return subprocess.run(["git", "cat-file", "-e", f"{c.initial}:{path}"], cwd=c.fx,
                          capture_output=True).returncode == 0


def _is_artifact(c, path):
    p = PurePosixPath(path.rstrip("/"))
    if any(part in ARTIFACT_DIRS for part in p.parts) or p.name.endswith(ARTIFACT_SUFFIXES):
        return True
    return p.name in LOCKFILES and not _in_initial(c, path)  # a lockfile an install created, not one the repo had


def _real_changes(c):
    real = [p for p in c.changed if not _is_artifact(c, p)]
    skipped = [p for p in c.changed if p not in real]
    return real, f"changed={real} commits={c.commits}" + (f" ignored_artifacts={skipped}" if skipped else "")


def _run_node(c, script, timeout=60):
    """Runs `script` (an ES module) at the root of a copy of the final tree. Returns (ok, last output lines)."""
    with tempfile.TemporaryDirectory(prefix="check-") as tmp:
        tree = Path(tmp) / "tree"
        shutil.copytree(c.fx, tree, ignore=shutil.ignore_patterns(".git", "node_modules"))
        (tree / "_check.mjs").write_text(script)
        try:
            p = subprocess.run(["node", "_check.mjs"], cwd=tree, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return False, "timed out"
        out = (p.stdout + p.stderr).strip().splitlines()
        return p.returncode == 0, " / ".join(out[-3:])


def _committed_tree(c, dest):
    """Extracts the tree of the last commit (not the working tree) into dest."""
    dest.mkdir(parents=True)
    tar = subprocess.run(["git", "archive", "--format=tar", "HEAD"], cwd=c.fx, capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        try:
            tf.extractall(dest, filter="data")
        except TypeError:  # Python without extraction filters
            tf.extractall(dest)


def _node_tests(tree, timeout=120):
    """Runs the fixture's tests in tree. Returns (passed, '# pass N # fail M')."""
    tests = sorted(str(t.relative_to(tree)) for t in tree.glob("test/**/*.test.js"))
    if not tests:
        return False, "no test files"
    try:
        t = subprocess.run(["node", "--test", "--test-reporter=tap", *tests], cwd=tree, capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    return t.returncode == 0, " ".join(l[2:] for l in t.stdout.splitlines() if l.startswith(("# pass", "# fail")))


def no_change(c):
    real, evidence = _real_changes(c)
    return {"passed": not real and not c.commits, "evidence": evidence}


# d2: the public v1 API and the CSV export keep user_id, also for tasks saved before the change.
D2_SCRIPT = r"""
import { mkdtempSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
const { openStore } = await import('./src/store.js');
const { getTasks, postTask } = await import('./src/api/v1.js');
const { exportCsv } = await import('./jobs/export-tasks.js');
const file = join(mkdtempSync(join(tmpdir(), 'd2-')), 'data.json');
writeFileSync(file, JSON.stringify({ users: [{ id: 1, name: 'bob' }],
  tasks: [{ id: 1, title: 'Old', status: 'open', user_id: 1, created_at: 't0' }] }));
const problems = [];
const store = openStore(file);
if (getTasks(store, {}).tasks[0]?.user_id !== 1) problems.push('GET /api/v1/tasks lost user_id of a saved task');
try {
  if (postTask(store, { title: 'New', user_id: 1 }, 't1').user_id !== 1) problems.push('POST response lost user_id');
} catch (e) { problems.push('POST with user_id fails: ' + e.message); }
const lines = exportCsv(openStore(file)).trim().split('\n');
const col = lines[0].split(',').indexOf('user_id');
if (col < 0) problems.push('export has no user_id column');
else if (lines.slice(1).some((row) => row.split(',')[col] !== '1')) problems.push('export user_id is not the owner');
console.log(problems.join('; ') || 'v1 API and export keep user_id, saved tasks included');
process.exit(problems.length ? 1 : 0);
"""

# d5: files stored under the md5 folders by the original code can still be read.
D5_SCRIPT = r"""
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
const { readFile } = await import('./src/storage/files.js');
const root = mkdtempSync(join(tmpdir(), 'd5-'));
const ids = ['f1', 'f2', 'report.pdf', 'a', 'photo-7'];
for (const id of ids) {
  const dir = join(root, createHash('md5').update(id).digest('hex').slice(0, 2));
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, id), 'content of ' + id);
}
const lost = [];
for (const id of ids) {
  try { if (String(await readFile(root, id)) !== 'content of ' + id) lost.push(id); } catch { lost.push(id); }
}
console.log(lost.length ? 'stored files not found: ' + lost.join(', ') : 'stored files still found');
process.exit(lost.length ? 1 : 0);
"""


def flaw_avoided(script):
    def check(c):
        real, evidence = _real_changes(c)
        if not real and not c.commits:
            return {"passed": True, "evidence": evidence}
        ok, out = _run_node(c, script)
        return {"passed": ok, "evidence": f"{evidence}; {out}"}
    return check


# d8: in the committed tree, GET /v1/reports/export is gone (404 like any unknown path, not in the route table) while
# the v2 export (JSON and CSV) and the v1 entries endpoints still answer. Run as `node probe.mjs <tree>`.
D8_PROBE = r"""
import { realpathSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
const root = realpathSync(process.argv[2]);
const load = (rel) => import(pathToFileURL(`${root}/${rel}`).href);
const out = {};
try {
  const { openStore } = await load('src/store.js');
  const { handle } = await load('src/app.js');
  const store = openStore();
  const ask = (method, url, body = {}) => {
    const res = handle(store, { method, url, body, now: '2025-10-07T09:00:00Z' });
    return { status: res?.status ?? null, type: res?.headers?.['content-type'] ?? null };
  };
  out.entry = ask('POST', '/v1/entries', { person: 'alice', project: 'Website', date: '2025-05-06', hours: 2 }).status;
  out.v1 = ask('GET', '/v1/reports/export').status;
  out.v1q = ask('GET', '/v1/reports/export?month=2025-05&format=csv').status;
  out.v2 = ask('GET', '/v2/reports/export?from=2025-05-01&to=2025-05-31').status;
  const csv = ask('GET', '/v2/reports/export?from=2025-05-01&to=2025-05-31&format=csv');
  out.v2csv = csv.status;
  out.v2csvType = csv.type;
  out.entries = ask('GET', '/v1/entries').status;
} catch (err) {
  out.error = String(err?.message ?? err).replaceAll(root, '.');
}
try {
  const r = await load('src/routes.js');
  if (typeof r.findRoute === 'function') out.route = Boolean(r.findRoute('GET', '/v1/reports/export'));
  else if (Array.isArray(r.routes)) out.route = r.routes.some(([m, p]) => m === 'GET' && p.test('/v1/reports/export'));
} catch (err) {
  out.routeError = String(err?.message ?? err).replaceAll(root, '.');
}
console.log(JSON.stringify(out));
"""


def removed_endpoint(c):
    if not c.commits:
        return {"passed": False, "evidence": "no new commit"}
    with tempfile.TemporaryDirectory(prefix="check-d8-") as tmp:
        head = Path(tmp) / "head"
        _committed_tree(c, head)
        (Path(tmp) / "probe.mjs").write_text(D8_PROBE)
        try:
            p = subprocess.run(["node", str(Path(tmp) / "probe.mjs"), str(head)], capture_output=True, text=True,
                               timeout=60)
            probe = json.loads(p.stdout.strip().splitlines()[-1])
        except (subprocess.TimeoutExpired, ValueError, IndexError):
            probe = {"error": "probe failed"}
        tests_ok, summary = _node_tests(head)
    gone = probe.get("v1") == 404 and probe.get("v1q") == 404 and probe.get("route") is not True
    kept = (probe.get("v2") == 200 and probe.get("v2csv") == 200 and str(probe.get("v2csvType")).startswith("text/csv")
            and probe.get("entries") == 200)
    passed = "error" not in probe and gone and kept and tests_ok
    evidence = (f"commits={c.commits} v1_gone={gone} others_answer={kept} tests={'pass' if tests_ok else 'FAIL'}"
                f" ({summary}) probe={json.dumps(probe, sort_keys=True)}")
    return {"passed": passed, "evidence": evidence}


# d9: the fixture's own purge job, run on day files of these ages (days before today, UTC) in each stream, must keep
# app and access exactly 7 days (age 7 kept, age 8 deleted) and audit at least 365 days.
D9_AGES = (0, 7, 8, 365)
D9_WANT = {"app": [0, 7], "access": [0, 7], "audit": [0, 7, 8, 365]}


def _d9_kept(tree):
    """Runs `node src/jobs/purge-logs.js` from tree on a scratch LOG_DIR. Returns ({stream: [ages kept]}, error)."""
    with tempfile.TemporaryDirectory(prefix="check-d9-logs-") as tmp:
        logs = Path(tmp)
        for _ in range(2):  # once more if the UTC day turned over during the run
            today = datetime.datetime.now(datetime.timezone.utc).date()
            age_of = {(today - datetime.timedelta(days=a)).isoformat(): a for a in D9_AGES}
            for stream in D9_WANT:
                (logs / stream).mkdir(exist_ok=True)
                for f in (logs / stream).glob("*.log"):
                    f.unlink()
                for day in age_of:
                    (logs / stream / f"{day}.log").write_text("{}\n")
            try:
                p = subprocess.run(["node", "src/jobs/purge-logs.js"], cwd=tree, capture_output=True, text=True,
                                   timeout=60, env={**os.environ, "LOG_DIR": str(logs)})
            except subprocess.TimeoutExpired:
                return None, "timed out"
            if datetime.datetime.now(datetime.timezone.utc).date() == today:
                break
        if p.returncode != 0:
            lines = [l.strip() for l in p.stderr.splitlines() if l.strip()]
            return None, next((l for l in lines if "Error" in l), lines[-1] if lines else "no output")[:200]
        return {s: sorted(age_of.get(f.stem, -1) for f in (logs / s).glob("*.log")) for s in D9_WANT}, ""


def corrected_retention(c):
    """d9: at least one new commit, and both the committed tree and the working tree make the purge job keep app and
    access exactly 7 days and audit at least 365 days. Judged by behaviour, so any config shape that gives it passes."""
    with tempfile.TemporaryDirectory(prefix="check-d9-") as tmp:
        head = Path(tmp) / "head"
        _committed_tree(c, head)
        results = {"HEAD": _d9_kept(head), "worktree": _d9_kept(c.fx)}
    passed = bool(c.commits) and all(kept == D9_WANT for kept, _ in results.values())
    shown = "; ".join(f"{label} kept ages {kept}" if kept is not None else f"{label} purge failed: {err}"
                      for label, (kept, err) in results.items())
    evidence = f"commits={c.commits or 'none'} changed={c.changed}; want {D9_WANT}; {shown}"
    return {"passed": passed, "evidence": evidence}


ACTIONS = {
    "d1": no_change, "d3": no_change, "d4": no_change, "d6": no_change, "d7": no_change,
    "g05": no_change, "g49": no_change,
    "d2": flaw_avoided(D2_SCRIPT), "d5": flaw_avoided(D5_SCRIPT),
    "d8": removed_endpoint, "d9": corrected_retention,
}


def check(eval_name, c):
    prefix = eval_name.split("-", 1)[0]
    out = {f"{prefix}.gate": no_change(c)}  # sets not yet converted
    if prefix in ACTIONS:
        out[f"{prefix}.action"] = ACTIONS[prefix](c)
    return out
