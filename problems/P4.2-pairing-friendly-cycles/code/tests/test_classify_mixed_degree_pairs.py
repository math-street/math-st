from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_mixed_degree_pairs import classify_mixed_cases  # noqa: E402


class MixedDegreeClassificationTests(unittest.TestCase):
    def test_complete_108_case_certificate(self) -> None:
        rows = classify_mixed_cases()
        cases = {
            (
                row.degree_e1,
                row.degree_e2,
                row.bounded_side,
                row.bounded_multiplier,
            )
            for row in rows
        }
        self.assertEqual(len(cases), 108)
        self.assertEqual(len(rows), 116)
        self.assertFalse(any(row.status == "identity_remainder" for row in rows))
        self.assertEqual(
            max(
                row.exhaustive_gap_bound
                for row in rows
                if row.exhaustive_gap_bound is not None
            ),
            2649,
        )

    def test_unique_exact_cycle_is_degree_10_3_over_7_11(self) -> None:
        exact = [row for row in classify_mixed_cases() if row.status == "exact_cycle"]
        self.assertEqual(len(exact), 1)
        row = exact[0]
        self.assertEqual(
            (
                row.degree_e1,
                row.degree_e2,
                row.field_p,
                row.field_q,
                row.gap_c,
            ),
            (10, 3, 7, 11, 4),
        )

    def test_every_retained_gap_is_even_and_within_its_bound(self) -> None:
        for row in classify_mixed_cases():
            if row.gap_c is None:
                continue
            self.assertEqual(row.gap_c % 2, 0)
            self.assertIsNotNone(row.exhaustive_gap_bound)
            self.assertLessEqual(row.gap_c, row.exhaustive_gap_bound)


if __name__ == "__main__":
    unittest.main()
