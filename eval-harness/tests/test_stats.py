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


class MonteCarloTests(unittest.TestCase):
    def test_small_strata_stay_exact(self):
        self.assertEqual(stats.p_method([([1] * 8, [0] * 8)]), "exact")

    def test_large_strata_are_estimated_with_a_fixed_seed(self):
        a = [1, 0.8, 1, 0.6, 1, 1, 0.8, 1, 1] * 2
        b = [0.6, 0.4, 0.8, 0.4, 0.6, 0.2, 0.6, 0.4, 0.6] * 2
        self.assertEqual(stats.p_method([(a, b)]), "monte carlo")
        p = stats.stratified_p([(a, b)])
        self.assertEqual(p, stats.stratified_p([(a, b)]))  # same seed, same estimate
        self.assertLess(p, 0.001)
        self.assertGreater(stats.stratified_p([(b, a)]), 0.99)

    def test_the_estimate_matches_the_exact_value(self):
        a, b = [0.8, 1, 0.6, 1, 0.4, 1, 0.8], [0.6, 0.8, 0.4, 1, 0.4, 0.6, 0.6]
        rule = {**stats.RULE, "permutations": 20000}
        exact = stats.stratified_p([(a, b)])
        estimate = stats._monte_carlo_p([(a, b)], round(sum(a) / 7 - sum(b) / 7, stats.ROUND), rule)
        self.assertAlmostEqual(estimate, exact, delta=0.01)


class CeilingAwareCriterionTests(unittest.TestCase):
    RULE = {**stats.RULE, "outcome_rer_min": 0.6}

    def test_off_by_default(self):
        self.assertIn("below 15 points", stats.criteria({"outcome": 0.10}, 0.01, stats.RULE, 0.88)["failed"][0])

    def test_a_ceiling_lowers_the_lift_needed(self):
        self.assertTrue(stats.criteria({"outcome": 0.09}, 0.01, self.RULE, 0.88)["met"])  # needs 7.2 of 12
        self.assertFalse(stats.criteria({"outcome": 0.10}, 0.01, self.RULE, 0.79)["met"])  # needs 12.6 of 21

    def test_a_large_room_still_needs_15_points(self):
        self.assertEqual(stats.outcome_lift_needed(0.40, self.RULE)[0], 0.15)
        self.assertTrue(stats.criteria({"outcome": 0.15}, 0.01, self.RULE, 0.40)["met"])

    def test_too_little_room_is_uninformative(self):
        failed = stats.criteria({"outcome": 0.05}, 0.01, self.RULE, 0.95)["failed"]
        self.assertTrue(failed and failed[0].startswith("uninformative"))


class ControlGuardTests(unittest.TestCase):
    def test_a_lower_control_rate_fails_and_is_a_regression(self):
        c = stats.criteria({"outcome": 0.5, "quality": 0.0, "safety": None, "control": -1 / 3}, 0.01)
        self.assertEqual((c["met"], c["regression"]), (False, True))
        self.assertIn("control pass rate lower with the skill", c["failed"])

    def test_no_control_cases_change_nothing(self):
        self.assertTrue(stats.criteria({"outcome": 0.5, "quality": 0.0, "safety": None, "control": None}, 0.01)["met"])


class QualityGuardTests(unittest.TestCase):
    def test_regression_guard_tolerates_a_small_drop(self):
        rule = {**stats.RULE, "quality_guard": "regression"}
        self.assertTrue(stats.criteria({"outcome": 0.5, "quality": -0.3}, 0.01, rule)["met"])
        failed = stats.criteria({"outcome": 0.5, "quality": -0.5}, 0.01, rule)["failed"]
        self.assertEqual(failed, ["judge quality score 0.5 or more lower with the skill"])
        self.assertFalse(stats.criteria({"outcome": 0.5, "quality": -0.3}, 0.01)["met"])  # strict by default


class PairedDesignTests(unittest.TestCase):
    def test_sign_flip_counts(self):
        self.assertAlmostEqual(stats.paired_p([[1, 1, 1, 1]]), 1 / 16)
        # Ties (difference 0) add nothing: eight +1 and one −1 of nine non-zero cases, P(sum ≥ 7) = 10 / 512.
        self.assertAlmostEqual(stats.paired_p([[1, -1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]]), 10 / 512)
        self.assertEqual(stats.paired_p([[0, 0, 0]]), 1.0)
        self.assertIsNone(stats.paired_p([[]]))

    def test_strata_combine_without_rounding_loss(self):
        self.assertAlmostEqual(stats.paired_p([[1] * 12] * 3), (1 / 4096) ** 3, delta=1e-20)

    def test_one_run_per_case_gets_an_interval_over_cases(self):
        # One run per arm per case: resampling runs inside a case cannot vary, resampling cases can.
        cells = {("a", f"e{i}"): ([w], [0]) for i, w in enumerate([1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0])}
        self.assertEqual(len(set(stats.bootstrap_ci(cells))), 1)
        low, high = stats.bootstrap_ci_cases(cells)
        self.assertTrue(0.4 < low < 0.75 < high <= 1.0)
        self.assertEqual(stats.bootstrap_ci_cases(cells), (low, high))


if __name__ == "__main__":
    unittest.main()
