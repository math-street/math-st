"""Known-answer tests for the P2.3 Cheon reproduction."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[4]
CODE_DIR = Path(__file__).resolve().parents[1]
for path in (PROJECT_ROOT, CODE_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cheon import OpaquePrimeOrderGroup, cheon_recover, primitive_root_mod_prime
from lib.curves import INFINITY, ShortWeierstrassCurve


class CheonTests(unittest.TestCase):
    def test_primitive_root_known_value(self) -> None:
        root = primitive_root_mod_prime(17)
        self.assertEqual(root, 3)
        self.assertEqual({pow(root, exponent, 17) for exponent in range(16)}, set(range(1, 17)))

    def test_exhaustive_opaque_groups(self) -> None:
        for order, d in ((17, 4), (19, 3), (31, 5)):
            group = OpaquePrimeOrderGroup(order)
            primitive_root = primitive_root_mod_prime(order)
            for secret in range(order):
                gx = group.scalar_mul(secret, group.generator)
                gxd = group.scalar_mul(pow(secret, d, order), group.generator)
                group.reset_trace()
                recovered, _ = cheon_recover(
                    group,
                    group.generator,
                    group.identity,
                    gx,
                    gxd,
                    order,
                    d,
                    primitive_root=primitive_root,
                )
                self.assertEqual(recovered, secret)

    def test_exhaustive_real_elliptic_curve_group(self) -> None:
        curve = ShortWeierstrassCurve(17, 2, 2)
        generator = curve.point(5, 1)
        order = 19
        for d in (3, 6):
            for secret in range(order):
                gx = curve.scalar_mul(secret, generator)
                gxd = curve.scalar_mul(pow(secret, d, order), generator)
                recovered, _ = cheon_recover(
                    curve,
                    generator,
                    INFINITY,
                    gx,
                    gxd,
                    order,
                    d,
                )
                self.assertEqual(recovered, secret)

    def test_nondivisor_is_rejected(self) -> None:
        group = OpaquePrimeOrderGroup(19)
        gx = group.scalar_mul(7, group.generator)
        gxd = group.scalar_mul(pow(7, 4, 19), group.generator)
        with self.assertRaisesRegex(ValueError, "divisor"):
            cheon_recover(group, group.generator, group.identity, gx, gxd, 19, 4)


if __name__ == "__main__":
    unittest.main()

