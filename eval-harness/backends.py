"""Headless agent CLIs behind one interface: claude (Claude Code), codex (Codex CLI), grok (Grok CLI).

Every run gets its own temporary HOME so user-level settings, memory files, hooks and skills do not leak in.
Only the CLI's credential file is linked into that home (never copied); for Codex that is the one in $CODEX_HOME
when it is set (an account manager may point it at another login), else ~/.codex. Claude Code keeps its login in the
macOS keychain, so an isolated Claude run needs a long-lived subscription token from `claude setup-token`,
read from $CLAUDE_CODE_OAUTH_TOKEN or the keychain item `claude-eval-oauth`. Further tokens (other accounts) go in
`claude-eval-oauth-2`, `claude-eval-oauth-3`, ... and are used in that order: a run that stops at a usage limit
before doing anything is run again with the next token. Without any token, Claude runs only with --claude-login,
which uses the normal login and is recorded as `isolation: none`.
"""
import json
import os
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path

USER_HOME = Path.home()
EXECUTOR_TIMEOUT = 45 * 60
GRADER_TIMEOUT = 20 * 60
KEYCHAIN_ITEM = "claude-eval-oauth"
MAX_KEYCHAIN_ITEMS = 9
LIMIT_RE = re.compile(r"hit your (\w+ )?limit|usage limit|rate limit", re.I)
_exhausted, _exhausted_lock = set(), threading.Lock()  # token slots that hit a limit in this process


def _version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout.strip().splitlines()[0]
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def _keychain(item):
    p = subprocess.run(["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", item, "-w"],
                       capture_output=True, text=True)
    return p.stdout.strip() or None


def claude_tokens():
    """[(slot, token)] in priority order: $CLAUDE_CODE_OAUTH_TOKEN, then keychain items claude-eval-oauth, -2, -3, ..."""
    tokens = []
    if os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"):
        tokens.append(("env", os.environ["CLAUDE_CODE_OAUTH_TOKEN"]))
    if shutil.which("security"):  # the keychain fallback is macOS only
        for n in range(1, MAX_KEYCHAIN_ITEMS + 1):
            item = KEYCHAIN_ITEM if n == 1 else f"{KEYCHAIN_ITEM}-{n}"
            token = _keychain(item)
            if token:
                tokens.append((item, token))
    return tokens


def claude_token():
    tokens = claude_tokens()
    return tokens[0][1] if tokens else None


def codex_home():
    """The Codex login the user's shell would use: $CODEX_HOME if set, else ~/.codex."""
    return Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else USER_HOME / ".codex"


def _link(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        dest.symlink_to(src)


def isolated_env(backend, home, claude_login=False, token=None):
    """Environment for one run. Returns (env, isolation) where isolation is 'temp-home' or 'none'."""
    home = Path(home)
    if home.exists():
        shutil.rmtree(home)
    home.mkdir(parents=True)
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDE_CODE_OAUTH_TOKEN",)}
    if backend == "codex":
        _link(codex_home() / "auth.json", home / ".codex" / "auth.json")
        env.update(HOME=str(home), CODEX_HOME=str(home / ".codex"))
        return env, "temp-home"
    if backend == "grok":
        _link(USER_HOME / ".grok" / "auth.json", home / ".grok" / "auth.json")
        env.update(HOME=str(home), GROK_HOME=str(home / ".grok"),
                   GROK_CLAUDE_SKILLS_ENABLED="false", GROK_CURSOR_SKILLS_ENABLED="false")
        return env, "temp-home"
    if backend == "claude":
        token = None if claude_login else (token or claude_token())
        if token:
            env.update(HOME=str(home), CLAUDE_CONFIG_DIR=str(home / ".claude"), CLAUDE_CODE_OAUTH_TOKEN=token)
            return env, "temp-home"
        if not claude_login:
            raise SystemExit("isolated Claude runs need a token: run `claude setup-token` and put it in "
                             "$CLAUDE_CODE_OAUTH_TOKEN (on macOS, or store it with "
                             f"`security add-generic-password -a \"$USER\" -s {KEYCHAIN_ITEM} -w`), "
                             "or pass --claude-login to use the normal login (recorded as isolation: none)")
        return os.environ.copy(), "none"
    raise ValueError(backend)


def _jsonl(text):
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def _anthropic_peak(usage):
    return sum(usage.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def parse_claude(stdout):
    r = {"text": "", "tool_calls": 0, "turns": None, "peak_context": None, "tokens_total": None,
         "model_effective": [], "skills_seen": None, "error": None, "cli_version": None}
    peak, tool_ids = 0, set()
    for ev in _jsonl(stdout):
        if ev.get("type") == "system" and ev.get("subtype") == "init":
            r["skills_seen"] = ev.get("skills") or []
            r["cli_version"] = ev.get("claude_code_version")
        elif ev.get("type") == "assistant":
            msg = ev.get("message") or {}
            peak = max(peak, _anthropic_peak(msg.get("usage") or {}))
            tool_ids.update(b.get("id") for b in msg.get("content", []) if b.get("type") == "tool_use")
        elif ev.get("type") == "result":
            r["text"] = ev.get("result") or ""
            r["turns"] = ev.get("num_turns")
            u = ev.get("usage") or {}
            r["tokens_total"] = _anthropic_peak(u) + (u.get("output_tokens") or 0)
            r["model_effective"] = sorted((ev.get("modelUsage") or {}).keys())
            if ev.get("is_error"):
                r["error"] = (ev.get("result") or "error")[:300]
    r["tool_calls"], r["peak_context"] = len(tool_ids), peak or None
    return r


def parse_codex(stdout, last_message):
    r = {"text": last_message or "", "tool_calls": 0, "turns": None, "peak_context": None, "tokens_total": None,
         "model_effective": [], "skills_seen": None, "error": None, "cli_version": None}
    for ev in _jsonl(stdout):
        item = ev.get("item") or {}
        if ev.get("type") == "item.completed" and item.get("type") in ("command_execution", "file_change", "mcp_tool_call", "web_search"):
            r["tool_calls"] += 1
        elif ev.get("type") == "turn.completed":
            u = ev.get("usage") or {}
            r["tokens_total"] = (r["tokens_total"] or 0) + (u.get("input_tokens") or 0) + (u.get("output_tokens") or 0)
            r["turns"] = (r["turns"] or 0) + 1
        elif ev.get("type") in ("error", "turn.failed"):
            r["error"] = json.dumps(ev)[:300]
    return r


def parse_grok(stdout):
    r = {"text": "", "tool_calls": 0, "turns": None, "peak_context": None, "tokens_total": None,
         "model_effective": [], "skills_seen": None, "error": None, "cli_version": None}
    peak, tool_ids = 0, set()
    for ev in _jsonl(stdout):
        if ev.get("type") == "system":
            r["skills_seen"] = ev.get("skills") or []
        elif ev.get("type") == "assistant":
            msg = ev.get("message") or {}
            peak = max(peak, _anthropic_peak(msg.get("usage") or {}))
            tool_ids.update(b.get("id") for b in msg.get("content", []) if b.get("type") == "tool_use")
        elif ev.get("type") == "result":
            r["text"] = ev.get("result") or ev.get("text") or ""
            r["turns"] = ev.get("num_turns")
            u = ev.get("usage") or {}
            r["tokens_total"] = _anthropic_peak(u) + (u.get("output_tokens") or 0)
            r["model_effective"] = sorted((ev.get("modelUsage") or {}).keys())
            if ev.get("is_error"):
                r["error"] = str(ev.get("result"))[:300]
    r["tool_calls"], r["peak_context"] = len(tool_ids), peak or None
    return r


def command(backend, cwd, prompt, model, effort, mode, out_dir, extra_dirs=()):
    """argv and stdin for one run. mode is 'executor' or 'grader'."""
    if backend == "claude":
        argv = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", model,
                "--disable-slash-commands", "--permission-mode", "bypassPermissions", "--no-session-persistence"]
        if effort:
            argv += ["--effort", effort]
        for d in extra_dirs:
            argv += ["--add-dir", str(d)]
        return argv, None
    if backend == "codex":
        sandbox = "workspace-write" if mode == "executor" else "read-only"
        argv = ["codex", "exec", "-C", str(cwd), "--skip-git-repo-check", "--sandbox", sandbox, "--ignore-user-config",
                "--ignore-rules", "--ephemeral", "--json", "-o", str(Path(out_dir) / "last-message.txt"), "-m", model]
        if effort:
            argv += ["-c", f"model_reasoning_effort={effort}"]
        git_dir = Path(cwd) / ".git"
        if mode == "executor" and git_dir.is_dir():  # workspace-write keeps .git read-only, so a run could not commit
            argv += ["-c", f"sandbox_workspace_write.writable_roots={json.dumps([str(git_dir)])}"]
        return argv + ["-"], prompt
    if backend == "grok":
        argv = ["grok", "--no-auto-update", "--cwd", str(cwd), "-m", model, "-p", prompt,
                "--output-format", "streaming-messages-json", "--always-approve", "--max-turns", "80"]
        if effort:
            argv += ["--reasoning-effort", effort]
        return argv, None
    raise ValueError(backend)


VERSION_CMD = {"claude": ["claude", "--version"], "codex": ["codex", "--version"], "grok": ["grok", "--version"]}


def run(backend, cwd, prompt, model, effort, mode, out_dir, home, extra_dirs=(), claude_login=False):
    """Run one agent session. Raw output stays in out_dir (private); the returned dict is what gets kept.
    An isolated Claude run tries the tokens in priority order, skipping slots that already hit a limit."""
    if backend != "claude" or claude_login:
        return _run_once(backend, cwd, prompt, model, effort, mode, out_dir, home, extra_dirs, claude_login)
    tokens = claude_tokens()
    if not tokens:
        isolated_env(backend, home)  # raises with the setup hint
    with _exhausted_lock:
        todo = [t for t in tokens if t[0] not in _exhausted] or tokens[-1:]
    for slot, token in todo:
        r = _run_once(backend, cwd, prompt, model, effort, mode, out_dir, home, extra_dirs, False, token)
        r["auth_slot"] = slot
        if not (r["error"] and LIMIT_RE.search(r["error"]) and not r["tool_calls"]):
            return r
        with _exhausted_lock:
            _exhausted.add(slot)
    return r


def _run_once(backend, cwd, prompt, model, effort, mode, out_dir, home, extra_dirs, claude_login, token=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    env, isolation = isolated_env(backend, home, claude_login, token)
    argv, stdin = command(backend, cwd, prompt, model, effort, mode, out_dir, extra_dirs)
    timeout = EXECUTOR_TIMEOUT if mode == "executor" else GRADER_TIMEOUT
    start = time.monotonic()
    try:
        p = subprocess.run(argv, cwd=cwd, env=env, input=stdin, capture_output=True, text=True, timeout=timeout,
                           stdin=None if stdin is not None else subprocess.DEVNULL)
        code, stdout, stderr = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, stdout, stderr = -1, e.stdout or "", f"timeout after {timeout}s"
        stdout = stdout.decode() if isinstance(stdout, bytes) else stdout
    duration = round(time.monotonic() - start, 1)
    (out_dir / "stdout.jsonl").write_text(stdout)
    (out_dir / "stderr.txt").write_text(stderr[-20000:])
    if backend == "claude":
        r = parse_claude(stdout)
    elif backend == "codex":
        last = out_dir / "last-message.txt"
        r = parse_codex(stdout, last.read_text() if last.exists() else "")
    else:
        r = parse_grok(stdout)
    r["cli_version"] = r["cli_version"] or _version(VERSION_CMD[backend])
    if code != 0 and not r["error"]:
        r["error"] = f"exit {code}: {stderr.strip()[-300:]}"
    r.update(backend=backend, model_requested=model, effort=effort, isolation=isolation, exit_code=code,
             duration_s=duration, ok=code == 0 and bool(r["text"].strip()) and not r["error"])
    shutil.rmtree(home, ignore_errors=True)
    return r
