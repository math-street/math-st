from __future__ import annotations

import sys
import unittest
from pathlib import Path
from random import Random

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from lib.curves import Curve, curve_order, curve_order_bsgs
from measure_smooth_orders import (
    count_smooth_in_interval,
    dickman_rho,
    largest_prime_factor,
    wilson_interval,
)
from random_order_lower_bound import (
    exhaustive_sequence_success,
    minimum_queries,
    optimal_success_probability,
)


class SmoothOrderMeasurementTests(unittest.TestCase):
    def test_random_order_query_bound_matches_exhaustive_sequences(self) -> None:
        self.assertEqual(optimal_success_probability(2, 5, 0), 0.0)
        self.assertAlmostEqual(optimal_success_probability(2, 5, 3), 1 - 0.6**3)
        self.assertAlmostEqual(
            exhaustive_sequence_success(1, 3, 2),
            5 / 9,
        )
        self.assertEqual(minimum_queries(2, 5, 0.5), 2)
        self.assertEqual(minimum_queries(0, 5, 0.5), None)
        self.assertEqual(minimum_queries(5, 5, 0.5), 1)

    def test_bsgs_counter_matches_exhaustive_known_orders(self) -> None:
        rng = Random(21)
        curves = (
            Curve(101, 2, 3),
            Curve(211, 0, 7),
            Curve(1019, 11, 19),
            Curve(65519, 2, 3),
        )
        for curve in curves:
            self.assertEqual(curve_order_bsgs(curve, rng), curve_order(curve))

    def test_segmented_smooth_count_matches_direct_factorization(self) -> None:
        cases = ((1, 100, 5), (91, 131, 11), (1000, 1200, 31))
        for lower, upper, bound in cases:
            expected = sum(
                largest_prime_factor(value) <= bound
                for value in range(lower, upper + 1)
            )
            self.assertEqual(
                count_smooth_in_interval(lower, upper, bound), expected
            )

    def test_statistical_helpers_known_values(self) -> None:
        self.assertAlmostEqual(dickman_rho(1.0), 1.0)
        self.assertAlmostEqual(dickman_rho(2.0), 1 - 0.693147, places=3)
        low, high = wilson_interval(0, 10)
        self.assertEqual(low, 0.0)
        self.assertGreater(high, 0.27)
        self.assertLess(high, 0.29)


if __name__ == "__main__":
    unittest.main()
