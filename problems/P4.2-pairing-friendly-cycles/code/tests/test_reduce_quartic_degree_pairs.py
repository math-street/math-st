from __future__ import annotations

from collections import Counter
import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from reduce_quartic_degree_pairs import (  # noqa: E402
    quotient_difference_bound,
    reduce_quartic_pairs,
)


class QuarticDegreeReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = reduce_quartic_pairs(24)

    def test_complete_large_gap_reduction(self) -> None:
        self.assertEqual(len(self.rows), 16 * 49)
        self.assertEqual(
            Counter(row.classification for row in self.rows),
            Counter(
                {
                    "genus_one_after_square_removal": 750,
                    "constant_nonsquare_times_square": 10,
                    "genus_zero_after_square_removal": 8,
                    "h0_finite_divisibility": 12,
                    "h0_impossible_zero_g": 4,
                }
            ),
        )

    def test_no_discriminant_is_a_square_polynomial(self) -> None:
        self.assertFalse(
            any(
                row.classification == "perfect_square_polynomial"
                for row in self.rows
            )
        )

    def test_large_gap_h_bound_crosses_below_25_at_108(self) -> None:
        self.assertGreaterEqual(quotient_difference_bound(106), 25)
        self.assertLess(quotient_difference_bound(108), 25)

    def test_every_ordered_pair_has_all_49_h_values(self) -> None:
        for degree_e1 in (5, 8, 10, 12):
            for degree_e2 in (5, 8, 10, 12):
                values = {
                    row.quotient_difference_h
                    for row in self.rows
                    if row.degree_e1 == degree_e1
                    and row.degree_e2 == degree_e2
                }
                self.assertEqual(values, set(range(-24, 25)))


if __name__ == "__main__":
    unittest.main()
