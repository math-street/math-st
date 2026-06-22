from __future__ import annotations

import unittest

from lib.binary_curves import BinaryEllipticCurve
from lib.curves import BinaryField, find_irreducible_binary_polynomial
from lib.ghs_transfer import (
    GenusOneGHSTransfer,
    fixed_subfield_elements,
    is_in_subfield,
    relative_trace,
)


class BinaryEllipticCurveTests(unittest.TestCase):
    def test_group_law_exhaustively_over_f8(self) -> None:
        field = BinaryField(3, find_irreducible_binary_polynomial(3))
        curve = BinaryEllipticCurve(field, 0, 1)
        points = curve.points()

        for point in points:
            self.assertTrue(curve.contains(point))
            self.assertIsNone(curve.add(point, curve.neg(point)))
        for left in points:
            for right in points:
                self.assertTrue(curve.contains(curve.add(left, right)))
                self.assertEqual(curve.add(left, right), curve.add(right, left))
                for third in points:
                    self.assertEqual(
                        curve.add(curve.add(left, right), third),
                        curve.add(left, curve.add(right, third)),
                    )


class GenusOneGHSTransferTests(unittest.TestCase):
    def setUp(self) -> None:
        self.field = BinaryField(10, find_irreducible_binary_polynomial(10))
        self.source = BinaryEllipticCurve(self.field, 234, 236)
        self.transfer = GenusOneGHSTransfer.from_source(
            self.source,
            2,
            twist=3,
        )

    def test_relative_trace_and_descended_curve(self) -> None:
        self.assertEqual(self.field.modulus, 0b1_0000001001)
        self.assertEqual(relative_trace(self.field, self.source.a, 2), 236)
        self.assertEqual(self.transfer.target.a, 236)
        self.assertEqual(self.transfer.target.b, 236)
        self.assertFalse(is_in_subfield(self.field, self.source.a, 2))

        base_values = fixed_subfield_elements(self.field, 2)
        self.assertEqual(base_values, (0, 1, 236, 237))
        self.assertEqual(len(self.transfer.target.points(base_values)), 6)

    def test_transfer_preserves_the_toy_prime_subgroup_dlp(self) -> None:
        target_preimage = (237, 0)
        source_generator = self.transfer.inverse_isomorphism(target_preimage)
        image_generator = self.transfer.transfer(source_generator)

        self.assertEqual(source_generator, (237, 311))
        self.assertFalse(
            all(is_in_subfield(self.field, coordinate, 2) for coordinate in source_generator)
        )
        self.assertEqual(self.source.point_order(source_generator), 3)
        self.assertEqual(image_generator, (237, 237))
        self.assertEqual(self.transfer.target.point_order(image_generator), 3)

        for scalar in range(3):
            source_multiple = self.source.scalar_mul(scalar, source_generator)
            self.assertEqual(
                self.transfer.transfer(source_multiple),
                self.transfer.target.scalar_mul(scalar, image_generator),
            )

        secret = 2
        source_target = self.source.scalar_mul(secret, source_generator)
        image_target = self.transfer.transfer(source_target)
        recovered = next(
            scalar
            for scalar in range(3)
            if self.transfer.target.scalar_mul(scalar, image_generator) == image_target
        )
        self.assertEqual(recovered, secret)


if __name__ == "__main__":
    unittest.main()
