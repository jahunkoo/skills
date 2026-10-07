"""Run: python3 -m unittest discover -s eval-harness/tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import stats  # noqa: E402


class PermutationTests(unittest.TestCase):
    def test_complete_separation_4v4(self):
        # Every with-run beats every without-run: the only extreme labeling of C(8,4) = 70.
        self.assertAlmostEqual(stats.perm_p([1, 1, 1, 1], [0, 0, 0, 0]), 1 / 70)

    def test_identical_arms(self):
        self.assertEqual(stats.perm_p([0.5] * 4, [0.5] * 4), 1.0)

    def test_matches_iteration1_floor(self):
        # iteration-1 grok: with 0.8,1,1,1 vs without 0.4,0.6,0.6,0.6 reported p = 0.014.
        self.assertAlmostEqual(stats.perm_p([0.8, 1, 1, 1], [0.4, 0.6, 0.6, 0.6]), 1 / 70)

    def test_stratified_three_separated_strata(self):
        strata = [([1, 1, 1, 1], [0, 0, 0, 0])] * 3
        self.assertAlmostEqual(stats.stratified_p(strata), 1 / 70 ** 3)

    def test_stratified_equals_single_stratum(self):
        a, b = [0.8, 1, 0.6, 1], [0.4, 0.6, 0.8, 0.6]
        self.assertAlmostEqual(stats.stratified_p([(a, b)]), stats.perm_p(a, b))

    def test_stratified_8v8_runs_fast(self):
        a, b = [1, 1, 0.9, 1, 0.8, 1, 1, 0.9], [0.6, 0.5, 0.7, 0.6, 0.6, 0.5, 0.7, 0.6]
        self.assertLess(stats.stratified_p([(a, b)] * 3), 1e-6)


class AgreementTests(unittest.TestCase):
    def test_kappa(self):
        self.assertEqual(stats.kappa([(True, True), (False, False)]), 1.0)
        self.assertEqual(stats.kappa([(True, False), (False, True)]), -1.0)
        self.assertIsNone(stats.kappa([(None, True)]))

    def test_agreement_survives_the_kappa_paradox(self):
        pairs = [(True, True)] * 11 + [(True, False)]  # 92% agreement, almost all PASS
        self.assertEqual(stats.kappa(pairs), 0.0)
        self.assertAlmostEqual(stats.agreement(pairs), 0.917, places=3)
        self.assertAlmostEqual(stats.pabak(pairs), 0.833, places=3)


class CriteriaTests(unittest.TestCase):
    def test_criteria(self):
        met = stats.criteria({"outcome": 0.2, "quality": 0.1, "safety": 0.0}, 0.01)
        self.assertEqual((met["met"], met["weak_evidence"], met["regression"]), (True, False, False))
        weak = stats.criteria({"outcome": 0.2, "quality": 0.1, "safety": 0.0}, 0.2)
        self.assertEqual((weak["met"], weak["weak_evidence"]), (True, True))
        reg = stats.criteria({"outcome": 0.0, "quality": 0.5, "safety": -0.1}, 0.01)
        self.assertEqual((reg["met"], reg["regression"]), (False, True))

    def test_relative_error_reduction(self):
        self.assertEqual(stats.relative_error_reduction(0.84, 0.6), (0.6, "confirmed"))
        self.assertEqual(stats.relative_error_reduction(0.7, 0.6)[1], "not confirmed")
        self.assertEqual(stats.relative_error_reduction(1.0, 0.95), (None, "uninformative"))

    def test_stddev(self):
        self.assertEqual(stats.stddev([1, 1]), 0.0)
        self.assertEqual(stats.stddev([0, 1]), 0.5)


class BootstrapTests(unittest.TestCase):
    def test_ci_brackets_the_difference_and_is_reproducible(self):
        cells = {("a", "e1"): ([1, 1, 0.8, 1], [0.4, 0.6, 0.6, 0.6]), ("b", "e1"): ([1, 0.8, 1, 1], [0.6, 0.6, 0.4, 0.8])}
        low, high = stats.bootstrap_ci(cells)
        self.assertTrue(0 < low <= 0.4 <= high <= 0.6)
        self.assertEqual(stats.bootstrap_ci(cells), (low, high))


if __name__ == "__main__":
    unittest.main()
