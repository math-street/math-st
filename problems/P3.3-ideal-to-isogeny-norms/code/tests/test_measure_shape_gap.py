from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from measure_shape_gap import (
    is_b_smooth,
    is_prime_power,
    run_instances,
    summarize_rows,
)


class ShapeGapTests(unittest.TestCase):
    def test_predicates_known_values(self) -> None:
        self.assertTrue(is_prime_power(1, 2))
        self.assertTrue(is_prime_power(64, 2))
        self.assertFalse(is_prime_power(12, 2))
        self.assertTrue(is_b_smooth(2**3 * 3**2 * 5, 5))
        self.assertFalse(is_b_smooth(14, 5))

    def test_small_run_validates_constrained_witnesses(self) -> None:
        rows = run_instances([11, 19], 1, 33032030, 16, 5)
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["power2_censored"], 0)
            self.assertEqual(row["power3_censored"], 0)
            self.assertEqual(row["smooth_censored"], 0)
            self.assertGreaterEqual(row["power2_over_unconstrained"], 1.0)
            self.assertGreaterEqual(row["power3_over_unconstrained"], 1.0)
            self.assertGreaterEqual(row["smooth_over_unconstrained"], 1.0)

    def test_summary_counts_all_rows(self) -> None:
        rows = run_instances([11], 2, 33032031, 16, 5)
        summaries = summarize_rows(rows)
        self.assertEqual(summaries[0]["n"], 2)
        self.assertEqual(summaries[0]["power2_observed"], 2)


if __name__ == "__main__":
    unittest.main()
