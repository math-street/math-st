from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_quartic_integral_points import search_integral_points  # noqa: E402


class QuarticIntegralPointSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = search_integral_points(1_000, 251)

    def test_every_final_curve_is_accounted_for(self) -> None:
        keys = {
            (row.degree_e1, row.degree_e2, row.quotient_difference_h)
            for row in self.rows
        }
        self.assertEqual(len(keys), 51)
        self.assertTrue(all(row.maximum_gap == 1_000 for row in self.rows))

    def test_no_short_range_exact_cycle(self) -> None:
        self.assertFalse(any(row.status == "exact_cycle" for row in self.rows))


if __name__ == "__main__":
    unittest.main()
