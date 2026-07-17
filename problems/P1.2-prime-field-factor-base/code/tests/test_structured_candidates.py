from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from lib.curves import Curve
from measure_structured_candidates import (
    integral_lift_factor_base,
    integral_lift_records,
    rational_height_residues,
    reachable_three_sums,
)


class StructuredCandidateTests(unittest.TestCase):
    def test_rational_height_mask_matches_direct_definition(self) -> None:
        p = 17
        bound = 4
        measured = rational_height_residues(p, bound)
        direct = {
            numerator * pow(denominator, p - 2, p) % p
            for numerator in range(-(bound - 1), bound)
            for denominator in range(1, bound)
        }
        self.assertEqual({index for index, selected in enumerate(measured) if selected}, direct)

    def test_integral_lift_points_reduce_to_curve(self) -> None:
        curve = Curve(17, 2, 2)
        points = integral_lift_factor_base(curve, 5)
        self.assertTrue(all(curve.contains(point) for point in points))
        records = integral_lift_records(curve, 5)
        self.assertTrue(all(height >= 0 and delta >= 0 for _, height, delta in records))

    def test_reachable_sums_match_direct_triples(self) -> None:
        curve = Curve(17, 2, 2)
        generator = (5, 1)
        base = [curve.scalar_mul(index, generator) for index in (1, 3, 8)]
        measured = reachable_three_sums(curve, base)
        direct = {
            curve.add(curve.add(left, middle), right)
            for left in base
            for middle in base
            for right in base
        }
        self.assertEqual(measured, direct)


if __name__ == "__main__":
    unittest.main()
