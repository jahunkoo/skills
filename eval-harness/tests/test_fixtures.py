"""Run: python3 -m unittest discover -s eval-harness/tests"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fixtures import Changes, make_fixture  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
MBOX = REPO / "skills" / "distill" / "evals" / "files" / "release-notes.mbox"
TARGET = "prompts/release-notes/SKILL.md"


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.fx = self.tmp / "fx"
        self.head = make_fixture(MBOX, self.fx)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_replay_is_clean_and_deterministic(self):
        ch = Changes(self.fx, self.head)
        self.assertEqual(ch.changed, [])
        self.assertEqual(ch.commits, [])
        self.assertEqual(make_fixture(MBOX, self.tmp / "again"), self.head)  # same SHAs every time

    def test_edit_untracked_and_ignored_files_are_seen(self):
        (self.fx / TARGET).write_text("changed\n")
        (self.fx / "notes.txt").write_text("new\n")
        (self.fx / ".gitignore").write_text("*.log\n")
        (self.fx / "debug.log").write_text("ignored but still a change\n")
        ch = Changes(self.fx, self.head)
        self.assertFalse(ch.unchanged(TARGET))
        for path in (TARGET, "notes.txt", ".gitignore", "debug.log"):
            self.assertIn(path, ch.changed)

    def test_commits_are_listed(self):
        (self.fx / TARGET).write_text("changed\n")
        import subprocess
        subprocess.run(["git", "commit", "-qam", "edit"], cwd=self.fx, check=True)
        ch = Changes(self.fx, self.head)
        self.assertEqual(len(ch.commits), 1)
        self.assertIn(TARGET, ch.changed)


if __name__ == "__main__":
    unittest.main()
