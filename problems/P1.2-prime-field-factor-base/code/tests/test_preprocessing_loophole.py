from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from audit_preprocessing_loophole import build_digit_table, ceil_nth_root
from lib.curves import Curve


class PreprocessingLoopholeTests(unittest.TestCase):
    def test_ceil_nth_root_is_exact(self) -> None:
        for degree in range(1, 6):
            for value in range(1, 200):
                root = ceil_nth_root(value, degree)
                self.assertGreaterEqual(root**degree, value)
                if root > 1:
                    self.assertLess((root - 1) ** degree, value)

    def test_digit_table_covers_order_19_group(self) -> None:
        curve = Curve(17, 2, 2)
        generator = (5, 1)
        table = build_digit_table(curve, 19, generator, 3)
        self.assertEqual(table.radix, 3)
        self.assertEqual(len(table.decompositions), 19)
        self.assertLessEqual(len(table.factor_base), 3 * table.radix)
        self.assertEqual(table.invalid_memberships, 0)
        self.assertEqual(table.invalid_sums, 0)
        for target, terms in table.decompositions.items():
            self.assertEqual(len(terms), 3)
            self.assertTrue(all(term in table.factor_base for term in terms))
            total = None
            for term in terms:
                total = curve.add(total, term)
            self.assertEqual(total, target)


if __name__ == "__main__":
    unittest.main()
