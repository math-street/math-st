"""Known-answer tests for shared curve and DLP helpers."""

import unittest

from lib.curves import INFINITY, Point, ShortWeierstrassCurve
from lib.dlog import bsgs, pohlig_hellman, pollard_rho, pollard_rho_orbits


class DlogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = ShortWeierstrassCurve(17, 2, 2)
        self.generator = self.curve.point(5, 1)
        self.order = 19
        self.secret = 7
        self.target = self.curve.scalar_mul(self.secret, self.generator)
        self.curve.reset_trace()

    def test_curve_known_values(self) -> None:
        self.assertEqual(self.curve.cardinality(), 19)
        self.assertEqual(self.curve.scalar_mul(19, self.generator), INFINITY)

    def test_bsgs(self) -> None:
        self.assertEqual(bsgs(self.curve, self.generator, self.target, self.order), self.secret)

    def test_bsgs_coordinate_compilation_has_zero_charged_additions(self) -> None:
        self.assertEqual(
            bsgs(self.curve, self.generator, self.target, self.order, charge=False),
            self.secret,
        )
        self.assertEqual(self.curve.trace["group_operation"], 0)
        self.assertGreater(self.curve.trace["coordinate_arithmetic"], 0)

    def test_pollard_rho(self) -> None:
        self.assertEqual(
            pollard_rho(self.curve, self.generator, self.target, self.order, seed=11),
            self.secret,
        )

    def test_orbit_pollard_rho_baseline(self) -> None:
        result = pollard_rho_orbits(
            self.curve,
            self.generator,
            self.target,
            self.order,
            seed=11,
        )
        self.assertEqual(result.logarithm, self.secret)
        self.assertGreater(result.transitions, 0)
        self.assertEqual(result.orbit_applications, 0)

    def test_orbit_pollard_rho_with_negation(self) -> None:
        def negation(point: Point) -> Point:
            return self.curve.neg(point)

        result = pollard_rho_orbits(
            self.curve,
            self.generator,
            self.target,
            self.order,
            automorphism=negation,
            automorphism_scalar=-1,
            automorphism_order=2,
            seed=11,
        )
        self.assertEqual(result.logarithm, self.secret)
        self.assertGreater(result.orbit_applications, 0)

    def test_collision_table_orbit_pollard_rho(self) -> None:
        result = pollard_rho_orbits(
            self.curve,
            self.generator,
            self.target,
            self.order,
            automorphism=self.curve.neg,
            automorphism_scalar=-1,
            automorphism_order=2,
            seed=11,
            collision_table=True,
        )
        self.assertEqual(result.logarithm, self.secret)
        self.assertGreater(result.transitions, 0)

    def test_orbit_pollard_rho_rejects_nonexact_action_order(self) -> None:
        with self.assertRaises(ValueError):
            pollard_rho_orbits(
                self.curve,
                self.generator,
                self.target,
                self.order,
                automorphism=self.curve.neg,
                automorphism_scalar=-1,
                automorphism_order=4,
                seed=11,
            )

    def test_pohlig_hellman(self) -> None:
        curve = ShortWeierstrassCurve(7, 3, 1)
        generator = curve.point(2, 1)
        order = 12
        secret = 7
        target = curve.scalar_mul(secret, generator)
        self.assertEqual(curve.cardinality(), order)
        self.assertEqual(curve.scalar_mul(order, generator), INFINITY)
        self.assertEqual(
            pohlig_hellman(curve, generator, target, order),
            secret,
        )


if __name__ == "__main__":
    unittest.main()
