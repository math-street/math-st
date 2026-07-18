from __future__ import annotations

import sys
import unittest
from itertools import combinations, permutations
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_three_cycles import search_three_cycles  # noqa: E402
from search_two_cycles import primes_below  # noqa: E402


class ThreeCycleSearchTests(unittest.TestCase):
    def test_directed_cycle_count_matches_permutation_reference(self) -> None:
        limit = 50
        result = search_three_cycles(limit=limit, max_degree=12)
        primes = [prime for prime in primes_below(limit) if prime >= 5]
        expected = 0
        for triple in combinations(primes, 3):
            p1 = min(triple)
            others = [prime for prime in triple if prime != p1]
            for p2, p3 in permutations(others):
                edges = ((p1, p2), (p2, p3), (p3, p1))
                if all((field + 1 - order) ** 2 <= 4 * field for field, order in edges):
                    expected += 1
        self.assertEqual(result.summary["directed_three_cycle_count"], expected)

    def test_candidate_rows_close_and_have_two_target_degrees(self) -> None:
        result = search_three_cycles(limit=128, max_degree=12)
        for row in result.candidates:
            self.assertEqual(row.trace_e1 + row.trace_e2 + row.trace_e3, 3)
            self.assertGreaterEqual(row.target_position_count, 2)
            fields = (row.field_prime_e1, row.field_prime_e2, row.field_prime_e3)
            degrees = (
                row.embedding_degree_e1,
                row.embedding_degree_e2,
                row.embedding_degree_e3,
            )
            for field, order, degree in zip(fields, fields[1:] + fields[:1], degrees):
                if degree.startswith(">"):
                    continue
                exact_degree = int(degree)
                self.assertEqual(pow(field, exact_degree, order), 1)
                self.assertNotIn(
                    1,
                    [pow(field, exponent, order) for exponent in range(1, exact_degree)],
                )


if __name__ == "__main__":
    unittest.main()

