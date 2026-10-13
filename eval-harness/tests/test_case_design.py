"""Run: python3 -m unittest discover -s eval-harness/tests

The design with many cases and one run per arm: a programmatic headline, judged outcome assertions as a secondary
metric, control cases as a guard, a paired test and a bootstrap over cases; and the `room` report of a pilot."""
import argparse
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness  # noqa: E402


def ev(i, name, family, control=False):
    if control:
        parsed = [{"id": f"{name}.action", "kind": "control", "check": "prog"}]
    else:
        parsed = [{"id": f"{name}.action", "kind": "outcome", "check": "prog"},
                  {"id": f"{name}.verdict", "kind": "outcome", "check": "judge"}]
    return {"id": i, "name": name, "prompt": "p", "family": family, "parsed": parsed,
            "assertions": [f"[{p['kind']}·{p['check']}] {p['id']} — t" for p in parsed]}


EVALS = [ev(1, "r1", "review"), ev(2, "r2", "review"), ev(3, "a1", "repair"), ev(4, "c1", "control", control=True)]
RULE = {"headline_check": "prog", "test": "paired", "resample": "cases"}
CFG = {"sets": {"s": {"evals": EVALS, "grader_notes": "", "grader_counts": None}}, "rule": RULE,
       "executors": {"claude": {"model": "m"}, "grok": {"model": "m"}}}
MANIFEST = {"label": "pilot", "kind": "dev", "config": "candidates/x-workspace/eval-config.json", "sets": ["s"], "date_utc": "2026-10-13", "skill": "candidates/x",
            "skill_sha256": "0" * 64, "replicates": 1, "arms": ["with_skill", "without_skill"],
            "executors": {"codex": {"cli": "Codex CLI", "model": "m", "effort": "high"}},
            "graders": {"codex": ["claude", "grok"]}, "evals_sha256": {}, "fixtures_sha256": {}, "harness_commit": "x"}
# Without the skill: r1 and r2 change files (fail), a1 passes; the control passes in both arms.
PASSES = {("r1", "with_skill"): True, ("r1", "without_skill"): False, ("r2", "with_skill"): True,
          ("r2", "without_skill"): False, ("a1", "with_skill"): True, ("a1", "without_skill"): True,
          ("c1", "with_skill"): True, ("c1", "without_skill"): True}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


class CaseDesignTests(unittest.TestCase):
    def setUp(self):
        self.ws = Path(tempfile.mkdtemp())
        ctl = self.ws / "control"
        self.mapping = []
        for n, ((name, arm), passed) in enumerate(sorted(PASSES.items()), 1):
            e = next(x for x in EVALS if x["name"] == name)
            rid = f"r{n:03d}"
            self.mapping.append({"run_id": rid, "executor": "codex", "set": "s", "eval_id": e["id"], "eval_name": name,
                                 "arm": arm, "replicate": 1})
            write(ctl / "results" / f"{rid}.json", {"ok": True, "duration_s": 1.0, "tokens_total": 10})
            write(ctl / "prog" / f"{rid}.json", {f"{name}.action": {"passed": passed, "evidence": "e"}})
            verdict = {f"{name}.verdict": {"passed": arm == "with_skill", "evidence": "e"}} if name != "c1" else {}
            for g in ("claude", "grok"):
                write(ctl / "grades" / g / f"{rid}.json",
                      {"result": {"assertions": verdict, "holistic": 4, "counts": {}}, "ok": True})

    def tearDown(self):
        shutil.rmtree(self.ws, ignore_errors=True)

    def test_aggregate(self):
        out = self.ws / "iteration-x"
        args = argparse.Namespace(ws=str(self.ws), out=str(out), ledger=None, note=None, allow_incomplete=False)
        with mock.patch.object(harness, "load_ws", return_value=(self.ws, MANIFEST, self.mapping, CFG)), \
                mock.patch.object(harness, "write_run"), contextlib.redirect_stdout(io.StringIO()) as shown:
            harness.cmd_aggregate(args)
        b = json.loads((out / "benchmark.json").read_text())
        o = b["outcome"]
        # Headline over the three programmatic outcome assertions only: 3/3 with, 1/3 without.
        self.assertEqual((o["with_skill"], o["without_skill"]), (1.0, 0.3333))
        self.assertEqual(o["p_method"], "exact paired sign-flip")
        self.assertAlmostEqual(o["p"], 0.25)  # two cases improved, one tie: 1 of 4 sign assignments
        self.assertIsNotNone(o["ci95"])
        s = b["by_agent"]["codex"]["run_summary"]
        self.assertEqual((s["with_skill"]["judge_outcome_pass_rate"]["mean"], s["without_skill"]["judge_outcome_pass_rate"]["mean"]), (1.0, 0.0))
        self.assertEqual(s["delta"]["control_pass_rate"], 0.0)
        self.assertTrue(b["by_agent"]["codex"]["criteria"]["met"])
        self.assertIn("Control with / without", shown.getvalue())
        self.assertIn("programmatic assertions only", shown.getvalue())

    def test_a_confirmation_set_need_not_be_called_holdout(self):
        out = self.ws / "iteration-c"
        args = argparse.Namespace(ws=str(self.ws), out=str(out), ledger=None, note=None, allow_incomplete=False)
        with mock.patch.object(harness, "load_ws", return_value=(self.ws, {**MANIFEST, "kind": "confirm"}, self.mapping, CFG)), \
                mock.patch.object(harness, "write_run"), contextlib.redirect_stdout(io.StringIO()):
            harness.cmd_aggregate(args)
        b = json.loads((out / "benchmark.json").read_text())
        self.assertEqual(b["by_set"]["s"]["relative_error_reduction"]["status"], "confirmed")
        self.assertTrue(b["decision"]["publish"])

    def test_a_skill_that_stops_sound_work_fails_the_control_guard(self):
        write(self.ws / "control" / "prog" / f"{next(m for m in self.mapping if m['eval_name'] == 'c1' and m['arm'] == 'with_skill')['run_id']}.json",
              {"c1.action": {"passed": False, "evidence": "stopped"}})
        out = self.ws / "iteration-y"
        args = argparse.Namespace(ws=str(self.ws), out=str(out), ledger=None, note=None, allow_incomplete=False)
        with mock.patch.object(harness, "load_ws", return_value=(self.ws, MANIFEST, self.mapping, CFG)), \
                mock.patch.object(harness, "write_run"), contextlib.redirect_stdout(io.StringIO()):
            harness.cmd_aggregate(args)
        c = json.loads((out / "benchmark.json").read_text())["by_agent"]["codex"]["criteria"]
        self.assertEqual((c["met"], c["regression"]), (False, True))

    def test_room_on_a_without_skill_pilot(self):
        pilot = [m for m in self.mapping if m["arm"] == "without_skill"]
        manifest = {**MANIFEST, "arms": ["without_skill"]}
        report = self.ws / "room.json"
        with mock.patch.object(harness, "load_ws", return_value=(self.ws, manifest, pilot, CFG)), \
                contextlib.redirect_stdout(io.StringIO()):
            harness.cmd_room(argparse.Namespace(ws=[str(self.ws)], out=str(report)))
        fam = {f["family"]: f for f in json.loads(report.read_text())["families"]}
        self.assertEqual((fam["review"]["room"], fam["review"]["status"]), (1.0, "room"))
        self.assertEqual((fam["repair"]["room"], fam["repair"]["status"]), (0.0, "saturated"))
        self.assertEqual(fam["control"]["status"], "control")
        self.assertIsNone(json.loads(report.read_text())["skill_sha256"])

    def test_room_pairs_a_with_skill_check_with_the_pilot_it_reuses(self):
        pilot = [m for m in self.mapping if m["arm"] == "without_skill"]
        check = [m for m in self.mapping if m["arm"] == "with_skill"]
        loads = [(self.ws, {**MANIFEST, "label": "pilot", "arms": ["without_skill"]}, pilot, CFG),
                 (self.ws, {**MANIFEST, "label": "check", "arms": ["with_skill"]}, check, CFG)]
        report = self.ws / "room.json"
        with mock.patch.object(harness, "load_ws", side_effect=loads), contextlib.redirect_stdout(io.StringIO()):
            harness.cmd_room(argparse.Namespace(ws=["a", "b"], out=str(report)))
        r = json.loads(report.read_text())
        self.assertEqual(r["label"], "pilot + check")
        paired = r["paired"][0]
        self.assertEqual((paired["cases"], paired["with"], paired["without"]), (3, 1.0, 0.3333))
        self.assertAlmostEqual(paired["p"], 0.25)
        self.assertEqual((paired["control_with"], paired["control_without"]), (1.0, 1.0))
        self.assertTrue(paired["programmatic_criteria_met"])
        self.assertEqual(r["pooled_relative_error_reduction"], {"value": 1.0, "status": "confirmed"})

    def test_cases_without_judge_assertions_are_not_graded(self):
        for m in self.mapping:
            if m["eval_name"] == "c1":
                for g in ("claude", "grok"):
                    (self.ws / "control" / "grades" / g / f"{m['run_id']}.json").unlink()
        self.assertEqual(harness.grade_gaps(self.ws, MANIFEST, self.mapping, CFG), [])
        self.assertFalse(harness.graded(EVALS[3]))
        self.assertTrue(harness.graded(EVALS[0]))


if __name__ == "__main__":
    unittest.main()
