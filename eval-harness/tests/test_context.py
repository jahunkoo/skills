"""Run: python3 -m unittest discover -s eval-harness/tests"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness  # noqa: E402


class ContextDirTests(unittest.TestCase):
    def setUp(self):
        self.ws = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.ws, ignore_errors=True)

    def test_each_fixture_gets_its_own_context(self):
        a = harness.context_dir(self.ws, "dev", "first-fixture.mbox")
        b = harness.context_dir(self.ws, "dev", "second-fixture.mbox")
        self.assertNotEqual(a, b)
        self.assertEqual(a, self.ws / "blind" / "_context" / "dev" / "first-fixture")

    def test_a_workspace_from_the_older_harness_keeps_its_set_context(self):
        base = self.ws / "blind" / "_context" / "dev"
        base.mkdir(parents=True)
        (base / "answer-key.md").write_text("key")
        self.assertEqual(harness.context_dir(self.ws, "dev", "release-notes.mbox"), base)
        self.assertEqual(harness.context_dir(self.ws, "dev"), base)


if __name__ == "__main__":
    unittest.main()
