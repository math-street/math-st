from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_quadratic_degree_pairs import (  # noqa: E402
    classify_multiplier_equations,
)


class QuadraticDegreeClassificationTests(unittest.TestCase):
    def test_complete_multiplier_certificate(self) -> None:
        rows = classify_multiplier_equations()
        self.assertEqual(len(rows), 11)
        self.assertFalse(any(row.status == "exact_finite_cycle" for row in rows))
        families = {
            (row.degree_e1, row.degree_e2, row.multiplier_m, row.multiplier_n)
            for row in rows
            if row.status == "infinite_mnt_family"
        }
        self.assertEqual(families, {(6, 4, 1, 1), (4, 6, 1, 1)})
        parity_rows = [
            row for row in rows if row.status == "identity_case_rejected"
        ]
        self.assertEqual(len(parity_rows), 1)
        self.assertEqual(
            (
                parity_rows[0].degree_e1,
                parity_rows[0].degree_e2,
                parity_rows[0].multiplier_m,
            ),
            (6, 6, 2),
        )

    def test_every_finite_root_satisfies_its_equation(self) -> None:
        for row in classify_multiplier_equations():
            if row.gap_c is None:
                continue
            value = (
                row.equation_a * row.gap_c * row.gap_c
                + row.equation_b * row.gap_c
                + row.equation_c
            )
            self.assertEqual(value, 0)


if __name__ == "__main__":
    unittest.main()
