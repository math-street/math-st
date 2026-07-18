from __future__ import annotations

import sys
import unittest
from pathlib import Path

import sympy

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_mixed_degree_pairs import PHI  # noqa: E402
from reduce_quartic_degree_pairs import C, _expression  # noqa: E402
from sieve_quartic_local_obstructions import (  # noqa: E402
    _has_odd_prime_solution,
    _has_two_power_solution,
    _square_roots,
    sieve_local_obstructions,
)


def direct_solution(degree_e1: int, degree_e2: int, h: int, modulus: int) -> bool:
    first = _expression(PHI[degree_e1], negative=True)
    second = _expression(PHI[degree_e2])
    g = sympy.cancel((first - second) / C)
    gaps = range(0, modulus, 2) if modulus % 2 == 0 else range(modulus)
    fields = range(1, modulus, 2) if modulus % 2 == 0 else range(modulus)
    for gap in gaps:
        for field_p in fields:
            if modulus % 2 and (field_p == 0 or (field_p + gap) % modulus == 0):
                continue
            if (
                h * field_p * field_p
                + (h * gap + int(g.subs(C, gap))) * field_p
                - int(second.subs(C, gap))
            ) % modulus == 0:
                return True
    return False


class QuarticLocalSieveTests(unittest.TestCase):
    def test_optimized_residue_checks_match_direct_enumeration(self) -> None:
        for degree_e1, degree_e2, h in ((5, 8, -3), (12, 10, 7), (8, 8, 5)):
            first = _expression(PHI[degree_e1], negative=True)
            second = _expression(PHI[degree_e2])
            g = sympy.cancel((first - second) / C)
            for modulus in (8, 16):
                self.assertEqual(
                    _has_two_power_solution(g, second, h, modulus),
                    direct_solution(degree_e1, degree_e2, h, modulus),
                )
            for prime in (3, 5, 7, 11):
                self.assertEqual(
                    _has_odd_prime_solution(
                        g, second, h, prime, _square_roots(prime)
                    ),
                    direct_solution(degree_e1, degree_e2, h, prime),
                )

    def test_sieve_accounts_for_all_750_rows(self) -> None:
        rows = sieve_local_obstructions(13)
        self.assertEqual(len(rows), 750)
        keys = {
            (row.degree_e1, row.degree_e2, row.quotient_difference_h)
            for row in rows
        }
        self.assertEqual(len(keys), 750)


if __name__ == "__main__":
    unittest.main()
