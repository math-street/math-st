from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from certify_quartic_odd_local import certify_odd_local  # noqa: E402


class QuarticOddLocalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = certify_odd_local(251)

    def test_all_final_rows_are_audited(self) -> None:
        self.assertEqual(len(self.rows), 51)
        self.assertEqual(
            len(
                {
                    (row.degree_e1, row.degree_e2, row.quotient_difference_h)
                    for row in self.rows
                }
            ),
            51,
        )

    def test_critical_prime_lists_include_small_primes(self) -> None:
        for row in self.rows:
            primes = {int(value) for value in row.critical_primes.split(",")}
            self.assertTrue({3, 5, 7, 11, 13, 17}.issubset(primes))


if __name__ == "__main__":
    unittest.main()
