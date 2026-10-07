"""Run: python3 -m unittest discover -s eval-harness/tests"""
import argparse
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness  # noqa: E402

EV = {"id": 1, "prompt": "p", "parsed": [{"id": "x.gate", "kind": "gate", "check": "prog"},
                                         {"id": "x.recall", "kind": "outcome", "check": "judge", "text": "t"}]}
CFG = {"sets": {"dev": {"evals": [EV], "grader_notes": "", "grader_counts": None}},
       "executors": {"codex": {"model": "m"}, "grok": {"model": "m"}}}
MANIFEST = {"kind": "confirm", "sets": ["dev"], "executors": {"claude": {"model": "m"}}, "graders": {"claude": ["codex", "grok"]}}
MAPPING = [{"run_id": "r001", "executor": "claude", "set": "dev", "eval_id": 1, "eval_name": "e", "arm": "with_skill"}]
COMPLETE = {"assertions": {"x.recall": {"passed": True, "evidence": "a"}}, "holistic": 4, "counts": {}}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


class GradeGateTests(unittest.TestCase):
    def setUp(self):
        self.ws = Path(tempfile.mkdtemp())
        ctl = self.ws / "control"
        write(ctl / "results" / "r001.json", {"ok": True})
        write(ctl / "prog" / "r001.json", {})

    def tearDown(self):
        shutil.rmtree(self.ws, ignore_errors=True)

    def grade(self, grader, result):
        write(self.ws / "control" / "grades" / grader / "r001.json", {"result": result, "ok": True})

    def test_string_verdict_and_missing_score_are_problems(self):
        self.assertEqual(harness.grade_problems(COMPLETE, EV), [])
        bad = {"assertions": {"x.recall": {"passed": "false"}}, "holistic": 4}
        self.assertEqual(harness.missing_ids(bad, EV), ["x.recall"])
        self.assertEqual(harness.grade_problems({"assertions": COMPLETE["assertions"]}, EV), ["holistic"])
        self.assertEqual(harness.grade_problems({**COMPLETE, "holistic": True}, EV), ["holistic"])

    def test_gaps_ignore_a_stored_ok_flag(self):
        # iteration-10: a grade stored as ok whose reply had lost verdicts
        self.grade("codex", COMPLETE)
        self.grade("grok", {"assertions": {}, "holistic": 4})
        self.assertEqual(harness.grade_gaps(self.ws, MANIFEST, MAPPING, CFG), ["r001 by grok: missing x.recall"])

    def test_confirm_aggregate_refuses_incomplete_grades_before_touching_out(self):
        self.grade("codex", COMPLETE)
        out = self.ws / "iteration-9"
        write(out / "benchmark.json", {"kept": True})
        args = argparse.Namespace(ws=str(self.ws), out=str(out), ledger=None, note=None, allow_incomplete=False)
        with mock.patch.object(harness, "load_ws", return_value=(self.ws, MANIFEST, MAPPING, CFG)):
            with self.assertRaises(SystemExit) as raised:
                harness.cmd_aggregate(args)
        self.assertIn("r001 by grok", str(raised.exception))
        self.assertTrue((out / "benchmark.json").exists())

    def test_grader_runs_outside_the_workspace(self):
        (self.ws / "blind" / "r001").mkdir(parents=True)
        (self.ws / "blind" / "_context" / "dev").mkdir(parents=True)
        seen = {}

        def fake_run(backend, cwd, prompt, model, effort, mode, out_dir, home, extra, claude_login):
            seen.update(cwd=Path(cwd), home=Path(home))
            return {"text": json.dumps(COMPLETE), "error": None, "duration_s": 1.0}

        with mock.patch.object(harness.backends, "run", side_effect=fake_run):
            _, _, ok = harness.grade_one(self.ws, MAPPING[0], "codex", MANIFEST, CFG, False)
        self.assertTrue(ok)
        for path in (seen["cwd"], seen["home"]):
            self.assertNotIn(self.ws.resolve(), path.resolve().parents)
        self.assertFalse(seen["cwd"].exists())


if __name__ == "__main__":
    unittest.main()
