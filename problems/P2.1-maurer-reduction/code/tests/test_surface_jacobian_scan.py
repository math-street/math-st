from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from surface_jacobian_scan import (
    hnr_contains_jacobian,
    is_ordinary_surface_weil_polynomial,
    scan_prime,
    smooth_mask,
    split_traces,
)


class SurfaceJacobianScanTests(unittest.TestCase):
    def test_split_trace_products_are_recognized(self) -> None:
        for prime in (5, 7, 11):
            trace_limit = math.isqrt(4 * prime)
            for first in range(-trace_limit, trace_limit + 1):
                for second in range(-trace_limit, trace_limit + 1):
                    a = -(first + second)
                    b = first * second + 2 * prime
                    if b % prime == 0:
                        continue
                    self.assertTrue(
                        is_ordinary_surface_weil_polynomial(prime, a, b)
                    )
                    self.assertEqual(set(split_traces(prime, a, b)), {first, second})

    def test_published_ordinary_hnr_exceptions(self) -> None:
        self.assertFalse(hnr_contains_jacobian(11, -3, 24))
        self.assertFalse(hnr_contains_jacobian(7, -10, 39))
        self.assertFalse(hnr_contains_jacobian(11, 0, -21))
        self.assertFalse(hnr_contains_jacobian(11, 0, -20))
        self.assertFalse(hnr_contains_jacobian(17, 2, -13))
        self.assertTrue(hnr_contains_jacobian(17, 1, -16))

    def test_smooth_mask_matches_direct_trial_division(self) -> None:
        lower, upper, bound = 91, 180, 11
        mask = smooth_mask(lower, upper, bound)

        def is_smooth(value: int) -> bool:
            remainder = value
            for prime in (2, 3, 5, 7, 11):
                while remainder % prime == 0:
                    remainder //= prime
            return remainder == 1

        expected = [is_smooth(value) for value in range(lower, upper + 1)]
        self.assertEqual(mask.tolist(), expected)

    def test_tiny_scan_has_nested_counts(self) -> None:
        row = scan_prime(127, 7, 2)
        self.assertGreater(row.smooth_jacobian_admissible_orders, 0)
        self.assertLessEqual(
            row.smooth_jacobian_admissible_orders, row.smooth_surface_orders
        )
        self.assertLessEqual(
            row.jacobian_admissible_orders, row.ordinary_surface_orders
        )


if __name__ == "__main__":
    unittest.main()
