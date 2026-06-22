from __future__ import annotations

import unittest
from random import Random

from lib.curves import (
    BinaryField,
    Curve,
    curve_order,
    curve_order_bsgs,
    find_irreducible_binary_polynomial,
    is_irreducible_binary_polynomial,
    is_prime,
    prime_below_power_of_two,
    quadratic_twist,
)


class CurveTests(unittest.TestCase):
    def test_known_prime_order_curve(self) -> None:
        curve = Curve(17, 2, 2)
        generator = (5, 1)
        self.assertEqual(curve_order(curve), 19)
        self.assertIsNone(curve.scalar_mul(19, generator))
        self.assertEqual(curve.scalar_mul(1, generator), generator)

    def test_bsgs_point_count_matches_exhaustive_count(self) -> None:
        rng = Random(20260722)
        for p in (101, 211, 509, 1019):
            for _ in range(8):
                while True:
                    try:
                        curve = Curve(p, rng.randrange(p), rng.randrange(p))
                        break
                    except ValueError:
                        pass
                self.assertEqual(curve_order_bsgs(curve, rng), curve_order(curve))

    def test_quadratic_twist_order_complements_curve_order(self) -> None:
        curve = Curve(101, 2, 3)
        twist = quadratic_twist(curve)
        self.assertEqual(curve_order(curve) + curve_order(twist), 2 * curve.p + 2)

    def test_group_law_and_membership(self) -> None:
        curve = Curve(17, 2, 2)
        point = (5, 1)
        doubled = curve.add(point, point)
        self.assertTrue(curve.contains(doubled))
        self.assertIsNone(curve.add(point, curve.neg(point)))
        self.assertEqual(curve.scalar_mul(7, point), curve.add(curve.scalar_mul(3, point), curve.scalar_mul(4, point)))

    def test_primality_and_prime_search(self) -> None:
        self.assertTrue(is_prime(104729))
        self.assertFalse(is_prime(104729 * 3))
        prime = prime_below_power_of_two(10)
        self.assertTrue(is_prime(prime))
        self.assertEqual(prime % 4, 3)


class BinaryFieldTests(unittest.TestCase):
    FIELDS = (
        BinaryField(4, 0b1_0011),
        BinaryField(6, 0b1_000011),
        BinaryField(8, 0x11B),
    )

    def test_known_irreducible_polynomials(self) -> None:
        for field in self.FIELDS:
            self.assertTrue(is_irreducible_binary_polynomial(field.modulus))
            self.assertEqual(
                find_irreducible_binary_polynomial(field.degree).bit_length() - 1,
                field.degree,
            )
        self.assertFalse(is_irreducible_binary_polynomial(0b1_0101))

    def test_multiplicative_inverse_and_sqrt_exhaustively(self) -> None:
        for field in self.FIELDS:
            for value in range(field.order):
                self.assertEqual(field.square(field.sqrt(value)), value)
                self.assertIn(field.absolute_trace(value), (0, 1))
                if value:
                    self.assertEqual(field.mul(value, field.inverse(value)), 1)

    def test_distributivity(self) -> None:
        for field in self.FIELDS:
            step = max(1, field.order // 16)
            values = range(0, field.order, step)
            for left in values:
                for middle in values:
                    for right in values:
                        self.assertEqual(
                            field.mul(left, field.add(middle, right)),
                            field.add(field.mul(left, middle), field.mul(left, right)),
                        )


if __name__ == "__main__":
    unittest.main()
