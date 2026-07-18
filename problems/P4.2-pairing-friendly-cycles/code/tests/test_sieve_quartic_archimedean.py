from __future__ import annotations

import sys
import unittest
from pathlib import Path

import sympy

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from reduce_quartic_degree_pairs import C  # noqa: E402
from sieve_quartic_archimedean import (  # noqa: E402
    constant_sign_on_ray,
    sieve_archimedean,
)


class QuarticArchimedeanSieveTests(unittest.TestCase):
    def test_exact_sign_on_ray(self) -> None:
        self.assertEqual(constant_sign_on_ray((C - 107) ** 2 + 1), 1)
        self.assertEqual(constant_sign_on_ray(-C**4 - 1), -1)
        self.assertIsNone(constant_sign_on_ray(C - 200))
        self.assertIsNone(constant_sign_on_ray(C - 108))

    def test_every_reported_obstruction_has_the_required_signs(self) -> None:
        rows = sieve_archimedean(13)
        for row in rows:
            if row.status != "archimedean_obstructed":
                continue
            if row.obstruction_reason == "negative_discriminant_on_ray":
                self.assertEqual(row.discriminant_sign, -1)
            elif row.quotient_difference_h > 0:
                self.assertEqual(
                    (row.boundary_value_sign, row.boundary_derivative_sign),
                    (1, 1),
                )
            else:
                self.assertEqual(
                    (row.boundary_value_sign, row.boundary_derivative_sign),
                    (-1, -1),
                )


if __name__ == "__main__":
    unittest.main()
