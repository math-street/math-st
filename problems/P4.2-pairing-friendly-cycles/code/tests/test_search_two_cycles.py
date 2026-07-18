from __future__ import annotations

import sys
import unittest
from itertools import combinations
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_two_cycles import (  # noqa: E402
    fundamental_discriminant_and_conductor,
    primes_below,
    search_two_cycles,
    smallest_prime_factors,
)


class TwoCycleSearchTests(unittest.TestCase):
    def test_fundamental_discriminant_decomposition(self) -> None:
        factors = smallest_prime_factors(200)
        self.assertEqual(fundamental_discriminant_and_conductor(123, factors), (-123, 1))
        self.assertEqual(fundamental_discriminant_and_conductor(20, factors), (-20, 1))
        self.assertEqual(fundamental_discriminant_and_conductor(48, factors), (-3, 4))

    def test_hasse_pair_count_matches_direct_reference(self) -> None:
        limit = 50
        result = search_two_cycles(limit=limit, max_degree=12)
        primes = [prime for prime in primes_below(limit) if prime >= 5]
        expected = 0
        for p, q in combinations(primes, 2):
            trace_e1 = p + 1 - q
            trace_e2 = q + 1 - p
            if trace_e1 * trace_e1 <= 4 * p and trace_e2 * trace_e2 <= 4 * q:
                expected += 1
        self.assertEqual(result.summary["hasse_valid_pair_count"], expected)

    def test_published_mnt_pairs_and_exact_degrees_are_recovered(self) -> None:
        result = search_two_cycles(limit=50, max_degree=12)
        rows = {
            (row.field_prime_e1, row.field_prime_e2): row
            for row in result.candidates
        }

        for pair in ((5, 7), (37, 43)):
            row = rows[pair]
            self.assertEqual((row.embedding_degree_e1, row.embedding_degree_e2), ("6", "4"))
            self.assertEqual(row.status, "hit")
            p, q = pair
            self.assertEqual(pow(p, 6, q), 1)
            self.assertNotIn(1, [pow(p, degree, q) for degree in range(1, 6)])
            self.assertEqual(pow(q, 4, p), 1)
            self.assertNotIn(1, [pow(q, degree, p) for degree in range(1, 4)])


if __name__ == "__main__":
    unittest.main()

