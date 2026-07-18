from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from analyze_three_cycle_near_misses import exact_multiplicative_order  # noqa: E402
from search_two_cycles import primes_below  # noqa: E402


class NearMissDegreeTests(unittest.TestCase):
    def test_exact_orders_include_large_20bit_missing_degree(self) -> None:
        factors = primes_below(1000)
        self.assertEqual(exact_multiplicative_order(7, 13, factors), 12)
        self.assertEqual(
            exact_multiplicative_order(482659, 483883, factors),
            483882,
        )


if __name__ == "__main__":
    unittest.main()

