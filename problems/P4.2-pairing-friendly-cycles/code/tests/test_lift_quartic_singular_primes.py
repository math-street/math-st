from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from lift_quartic_singular_primes import audit_singular_primes  # noqa: E402


class QuarticSingularLiftTests(unittest.TestCase):
    def test_all_21_singular_row_prime_pairs_are_audited(self) -> None:
        rows = audit_singular_primes(4, 251)
        self.assertEqual(len(rows), 21)
        self.assertEqual({row.prime for row in rows}, {3, 7, 13})
        self.assertTrue(all(row.certificate_exponent <= 4 for row in rows))


if __name__ == "__main__":
    unittest.main()
