from __future__ import annotations

import unittest

from lib.curves import Curve
from lib.semaev import (
    f3_value,
    f4_value,
    f5_value,
    f6_value,
    polynomial_resultant,
    quadratic_resultant,
)


class SemaevTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = Curve(101, 2, 3)
        self.points = list(self.curve.affine_points())

    def test_quadratic_resultant_known_values(self) -> None:
        # (z-1)(z-2) and (z-3)(z-4) have resultant 12.
        self.assertEqual(quadratic_resultant((1, -3, 2), (1, -7, 12), 101), 12)
        self.assertEqual(polynomial_resultant([2, -3, 1], [12, -7, 1], 101), 12)

    def test_published_formula_and_recursive_resultants_at_fixed_inputs(self) -> None:
        # Values independently expanded with SymPy's symbolic resultant.
        self.assertEqual(f3_value(1, 2, 3, 2, 3, 101), 67)
        self.assertEqual(f4_value(1, 2, 3, 4, 2, 3, 101), 2)
        self.assertEqual(f5_value(1, 2, 3, 4, 5, 2, 3, 101), 51)

    def test_f3_vanishes_on_three_points_summing_to_zero(self) -> None:
        p1, p2 = self.points[2], self.points[7]
        p3 = self.curve.neg(self.curve.add(p1, p2))
        self.assertIsNotNone(p3)
        assert p3 is not None
        self.assertEqual(f3_value(p1[0], p2[0], p3[0], 2, 3, 101), 0)

    def test_f4_vanishes_on_four_points_summing_to_zero(self) -> None:
        p1, p2, p3 = self.points[2], self.points[7], self.points[11]
        p4 = self.curve.neg(self.curve.add(self.curve.add(p1, p2), p3))
        self.assertIsNotNone(p4)
        assert p4 is not None
        self.assertEqual(f4_value(p1[0], p2[0], p3[0], p4[0], 2, 3, 101), 0)

    def test_f5_vanishes_on_five_points_summing_to_zero(self) -> None:
        p1, p2, p3, p4 = self.points[2], self.points[7], self.points[11], self.points[16]
        partial = self.curve.add(self.curve.add(p1, p2), self.curve.add(p3, p4))
        p5 = self.curve.neg(partial)
        self.assertIsNotNone(p5)
        assert p5 is not None
        self.assertEqual(f5_value(p1[0], p2[0], p3[0], p4[0], p5[0], 2, 3, 101), 0)

    def test_f6_vanishes_on_six_points_summing_to_zero(self) -> None:
        p1, p2, p3, p4, p5 = (
            self.points[2],
            self.points[7],
            self.points[11],
            self.points[16],
            self.points[20],
        )
        partial = self.curve.add(
            self.curve.add(self.curve.add(p1, p2), self.curve.add(p3, p4)), p5
        )
        p6 = self.curve.neg(partial)
        self.assertIsNotNone(p6)
        assert p6 is not None
        self.assertEqual(
            f6_value(p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], 2, 3, 101), 0
        )


if __name__ == "__main__":
    unittest.main()
