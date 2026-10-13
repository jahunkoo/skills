"""Run: python3 -m unittest discover -s eval-harness/tests"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import backends  # noqa: E402


class CodexLoginTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_an_isolated_run_links_the_login_from_codex_home(self):
        account = self.tmp / "account"
        account.mkdir()
        (account / "auth.json").write_text("{}")
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(account)}):
            env, isolation = backends.isolated_env("codex", self.tmp / "home")
        link = self.tmp / "home" / ".codex" / "auth.json"
        self.assertEqual(isolation, "temp-home")
        self.assertEqual(link.resolve(), (account / "auth.json").resolve())
        self.assertEqual(env["CODEX_HOME"], str(self.tmp / "home" / ".codex"))

    def test_without_codex_home_the_default_login_is_used(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CODEX_HOME", None)
            self.assertEqual(backends.codex_home(), backends.USER_HOME / ".codex")


if __name__ == "__main__":
    unittest.main()


def _result(error=None, tool_calls=0):
    return {"text": "" if error else "ok", "tool_calls": tool_calls, "error": error}


class ClaudeTokenOrderTests(unittest.TestCase):
    def setUp(self):
        backends._exhausted.clear()
        self.calls = []

    def tearDown(self):
        backends._exhausted.clear()

    def _run(self, outcomes):
        def fake(backend, cwd, prompt, model, effort, mode, out_dir, home, extra_dirs, claude_login, token=None):
            self.calls.append(token)
            return dict(outcomes[token])
        with mock.patch.object(backends, "_run_once", side_effect=fake):
            return backends.run("claude", "cwd", "p", "m", "high", "grader", "out", "home")

    def test_keychain_items_are_read_in_priority_order(self):
        found = {"claude-eval-oauth": "t1", "claude-eval-oauth-3": "t3"}
        with mock.patch.dict(os.environ, {}, clear=False), \
                mock.patch.object(backends.shutil, "which", return_value="/usr/bin/security"), \
                mock.patch.object(backends, "_keychain", side_effect=lambda item: found.get(item)):
            os.environ.pop("CLAUDE_CODE_OAUTH_TOKEN", None)
            self.assertEqual(backends.claude_tokens(), [("claude-eval-oauth", "t1"), ("claude-eval-oauth-3", "t3")])

    def test_a_limit_moves_on_to_the_next_token_and_is_remembered(self):
        tokens = [("claude-eval-oauth", "t1"), ("claude-eval-oauth-2", "t2")]
        outcomes = {"t1": _result("You've hit your weekly limit · resets Oct 11"), "t2": _result()}
        with mock.patch.object(backends, "claude_tokens", return_value=tokens):
            r = self._run(outcomes)
            self.assertEqual((r["auth_slot"], self.calls), ("claude-eval-oauth-2", ["t1", "t2"]))
            self._run(outcomes)  # the exhausted slot is not tried again in this process
            self.assertEqual(self.calls[2:], ["t2"])

    def test_other_failures_and_limits_after_work_do_not_switch_tokens(self):
        tokens = [("claude-eval-oauth", "t1"), ("claude-eval-oauth-2", "t2")]
        for outcome in (_result("exit 1: something else"), _result("You've hit your weekly limit", tool_calls=4)):
            backends._exhausted.clear()
            self.calls = []
            with mock.patch.object(backends, "claude_tokens", return_value=tokens):
                r = self._run({"t1": outcome, "t2": _result()})
            self.assertEqual((r["auth_slot"], self.calls), ("claude-eval-oauth", ["t1"]))


class CodexCommandTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_an_executor_may_write_the_fixtures_git_folder(self):
        (self.tmp / ".git").mkdir()
        argv, _ = backends.command("codex", self.tmp, "p", "m", None, "executor", self.tmp)
        self.assertIn(f'sandbox_workspace_write.writable_roots=["{self.tmp / ".git"}"]', argv)

    def test_a_grader_gets_no_writable_root(self):
        (self.tmp / ".git").mkdir()
        argv, _ = backends.command("codex", self.tmp, "p", "m", None, "grader", self.tmp)
        self.assertFalse(any("writable_roots" in a for a in argv))
        self.assertIn("read-only", argv)

