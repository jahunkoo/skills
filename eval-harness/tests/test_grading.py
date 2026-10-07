"""Run: python3 -m unittest discover -s eval-harness/tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness  # noqa: E402

EV = {"parsed": [{"id": "x.gate", "check": "prog"}, {"id": "x.recall", "check": "judge"},
                 {"id": "x.keep", "check": "judge"}]}


class GradeParsingTests(unittest.TestCase):
    def test_complete_reply(self):
        out = harness.parse_grade('{"assertions": {"x.recall": {"passed": true, "evidence": "a"}, '
                                  '"x.keep": {"passed": false, "evidence": "b"}}, "holistic": 4, "counts": {}}')
        self.assertEqual(harness.missing_ids(out, EV), [])

    def test_extra_brace_drops_verdicts_and_is_caught(self):
        # iteration-10: one closing brace too many after each verdict ends the assertions object early
        text = ('{"assertions": {"x.recall": {"passed": true, "evidence": "a"}}, '
                '"x.keep": {"passed": true, "evidence": "b"}}, "holistic": 4, "counts": {}}')
        out = harness.parse_grade(text)
        self.assertIsNotNone(out)
        self.assertEqual(harness.missing_ids(out, EV), ["x.keep"])

    def test_unparseable(self):
        self.assertIsNone(harness.parse_grade("no json here"))
        self.assertEqual(harness.missing_ids(None, EV), ["x.recall", "x.keep"])


if __name__ == "__main__":
    unittest.main()
