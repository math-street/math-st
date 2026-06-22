"""Known-answer tests for the toy Smart anomalous-curve attack."""

from __future__ import annotations

import unittest

from lib.anomalous import additive_transfer, smart_attack
from lib.curves import Curve, curve_order


class AnomalousAttackTests(unittest.TestCase):
    def test_all_nonzero_logs_on_order_17_curve(self) -> None:
        curve = Curve(17, 1, 3)
        generator = (2, 8)
        self.assertEqual(curve_order(curve), 17)
        for secret in range(1, 17):
            target = curve.scalar_mul(secret, generator)
            self.assertEqual(smart_attack(curve, generator, target), secret)

    def test_transfer_is_a_nonzero_homomorphism(self) -> None:
        curve = Curve(17, 1, 3)
        generator = (2, 8)
        image = additive_transfer(curve, generator)
        self.assertNotEqual(image, 0)
        for scalar in range(17):
            self.assertEqual(
                additive_transfer(curve, curve.scalar_mul(scalar, generator)),
                scalar * image % curve.p,
            )

    def test_rejects_non_anomalous_curve(self) -> None:
        curve = Curve(17, 2, 2)
        with self.assertRaises(ValueError):
            smart_attack(curve, (5, 1), curve.scalar_mul(7, (5, 1)))


if __name__ == "__main__":
    unittest.main()
