"""Shared helpers: repo paths, JSON I/O, eval config, assertion parsing, UTC dates."""
import hashlib
import importlib.util
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ASSERTION_RE = re.compile(r"^\[(?P<kind>gate|outcome|procedure|scope)·(?P<check>prog|judge)\] (?P<id>\S+) — (?P<text>.+)$")
ARMS = ("with_skill", "without_skill")


def load_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def utc_date():
    """Dates only: public artifacts carry no times of day."""
    return datetime.now(timezone.utc).date().isoformat()


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_assertion(text):
    m = ASSERTION_RE.match(text)
    if not m:
        raise ValueError(f"assertion must look like '[kind·check] id — text': {text}")
    return m.groupdict()


def load_module(path):
    """Import a per-set checks.py by path (it defines TARGET, PACKET_FILES and check())."""
    spec = importlib.util.spec_from_file_location(f"checks_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_config(path):
    """Eval config: skill folder, eval sets, executors and grader assignment. Paths are relative to the repo root."""
    cfg = load_json(path)
    if cfg is None:
        raise SystemExit(f"cannot read eval config {path}")
    cfg["skill_dir"] = REPO / cfg["skill"]
    for name, s in cfg["sets"].items():
        for key in ("evals", "files", "checks", "answer_key"):
            s[key] = REPO / s[key]
        s["evals_file"] = s["evals"]
        data = load_json(s["evals_file"])
        if data is None:
            raise SystemExit(f"cannot read {s['evals_file']}")
        meta = (data.get("sets") or {}).get(name, data)  # one evals.json may hold several sets
        s["grader_notes"] = meta.get("grader_notes", "")
        s["grader_counts"] = meta.get("grader_counts")
        s["evals"] = [{**ev, "set": ev.get("set", name), "parsed": [parse_assertion(a) for a in ev["assertions"]]}
                      for ev in data["evals"] if ev.get("set", name) == name]
        if not s["evals"]:
            raise SystemExit(f"no evals of set '{name}' in {s['evals_file']}")
    return cfg


def rel(path, ws):
    """Scrub a workspace path to a placeholder before it goes into anything kept."""
    return str(path).replace(str(ws), "<ws>")
