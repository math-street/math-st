from __future__ import annotations

import unittest

from lib.extension_curves import ExtensionCurve
from lib.finite_fields import cubic_field, find_irreducible_cubic


class FiniteFieldTests(unittest.TestCase):
    def test_irreducible_cubic_has_no_base_field_root(self) -> None:
        modulus = find_irreducible_cubic(5)
        self.assertTrue(
            all(
                sum(coefficient * value**degree for degree, coefficient in enumerate(modulus)) % 5
                for value in range(5)
            )
        )

    def test_every_nonzero_element_has_an_inverse(self) -> None:
        field = cubic_field(5)
        for value in field.elements():
            if value:
                self.assertEqual(value * value.inverse(), field.one)

    def test_frobenius_selects_exactly_the_base_field(self) -> None:
        field = cubic_field(5)
        selected = {value for value in field.elements() if value**5 == value}
        self.assertEqual(selected, set(field.base_elements()))

    def test_extension_curve_group_law(self) -> None:
        field = cubic_field(5)
        curve = ExtensionCurve(field, field.element(1), field.element((1, 1, 0)))
        points = list(curve.affine_points())
        point = points[0]
        self.assertIsNone(curve.add(point, curve.neg(point)))
        self.assertTrue(curve.contains(curve.add(point, point)))
        self.assertEqual(curve.scalar_mul(7, point), curve.add(curve.scalar_mul(3, point), curve.scalar_mul(4, point)))


if __name__ == "__main__":
    unittest.main()
