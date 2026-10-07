"""Fixture repositories: build them from a mbox or a directory, and see what a run changed."""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

FIXTURE_IDENT = ("fixture", "fixture@example.invalid")
DIR_FIXTURE_DATE = "2026-01-01T00:00:00+00:00"


def git(cwd, *args, check=True, env=None):
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False,
                       env={**os.environ, **(env or {})})
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {p.stderr.strip()}")
    return p.stdout


def make_fixture(src, dest):
    """A mbox (git format-patch --root --stdout) is replayed with its original dates, so SHAs and blame match.
    A directory is committed as one commit. Returns the initial HEAD."""
    src, dest = Path(src), Path(dest)
    if src.suffix == ".mbox":
        dest.mkdir(parents=True)
    else:
        shutil.copytree(src, dest)
    git(dest, "init", "-q", "-b", "main")
    git(dest, "config", "user.name", FIXTURE_IDENT[0])
    git(dest, "config", "user.email", FIXTURE_IDENT[1])
    git(dest, "config", "core.hooksPath", "/dev/null")
    if src.suffix == ".mbox":
        with open(src, "rb") as fh:
            p = subprocess.run(["git", "am", "-q", "--committer-date-is-author-date"], cwd=dest, stdin=fh, capture_output=True)
        if p.returncode != 0:
            raise RuntimeError(f"git am failed for {src}: {p.stderr.decode()[-500:]}")
    else:
        git(dest, "add", "-A")
        git(dest, "commit", "-q", "-m", "chore: initial", env={"GIT_AUTHOR_DATE": DIR_FIXTURE_DATE, "GIT_COMMITTER_DATE": DIR_FIXTURE_DATE})
    return git(dest, "rev-parse", "HEAD").strip()


def changed_paths(fx, initial):
    """Paths that differ from the initial commit: committed, staged, unstaged, untracked, and ignored files."""
    paths = set(filter(None, git(fx, "diff", "--name-only", initial, "HEAD").splitlines()))
    status = git(fx, "status", "--porcelain", "--untracked-files=all", "--ignored=matching")
    for line in status.splitlines():
        if line.strip():
            paths.add(line[3:].split(" -> ")[-1])
    return sorted(paths)


def unchanged(fx, initial, rel):
    same = subprocess.run(["git", "diff", "--quiet", initial, "--", rel], cwd=fx).returncode == 0
    return same and not git(fx, "status", "--porcelain", "--ignored=matching", "--", rel).strip()


def commits_since(fx, initial):
    return [line for line in git(fx, "log", "--format=%h %s", f"{initial}..HEAD").splitlines() if line.strip()]


def diff_text(fx, initial):
    """Full diff against the initial commit, untracked files included, without touching the run's own index."""
    tmp = Path(tempfile.mkdtemp(prefix="diff-"))
    try:
        shutil.copytree(fx, tmp / "fx", symlinks=True)
        git(tmp / "fx", "add", "-A", "--force")
        return git(tmp / "fx", "-c", "core.quotepath=off", "diff", "--cached", "--stat", "--patch", initial)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def history(fx):
    """Commit list and dates for graders (recency is part of some answer keys)."""
    return git(fx, "log", "--format=%h %ad %s", "--date=short")


def clean_copy(fx, dest):
    shutil.copytree(fx, dest, ignore=shutil.ignore_patterns(".git"))


class Changes:
    """What checks.py receives: `changed`, `commits`, and `unchanged(path)`."""

    def __init__(self, fx, initial):
        self.fx, self.initial = Path(fx), initial
        self.changed = changed_paths(fx, initial)
        self.commits = commits_since(fx, initial)

    def unchanged(self, rel):
        return unchanged(self.fx, self.initial, rel)
