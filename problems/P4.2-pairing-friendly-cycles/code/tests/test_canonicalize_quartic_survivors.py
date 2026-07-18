from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from canonicalize_quartic_survivors import canonicalize_survivors  # noqa: E402


class CanonicalQuarticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = canonicalize_survivors(251)

    def test_51_rows_reduce_to_31_curves(self) -> None:
        self.assertEqual(len(self.rows), 51)
        self.assertEqual(len({row.canonical_curve_id for row in self.rows}), 31)

    def test_duplicate_multiplicities_are_consistent(self) -> None:
        actual = Counter(row.canonical_curve_id for row in self.rows)
        for row in self.rows:
            self.assertEqual(row.multiplicity, actual[row.canonical_curve_id])
        self.assertEqual(Counter(actual.values()), Counter({1: 11, 2: 20}))

    def test_all_removed_contents_are_squares(self) -> None:
        self.assertEqual({row.square_content for row in self.rows}, {1, 2})
        self.assertEqual({row.squarefree_twist for row in self.rows}, {1, 13})

    def test_odd_prime_obstructions_leave_47_rows_on_29_curves(self) -> None:
        rows = canonicalize_survivors(251, exclude_odd_obstructions=True)
        self.assertEqual(len(rows), 47)
        self.assertEqual(len({row.canonical_curve_id for row in rows}), 29)


if __name__ == "__main__":
    unittest.main()
