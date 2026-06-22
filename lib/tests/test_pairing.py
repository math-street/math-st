"""Known-answer and structural tests for the staged Tate pairing."""

from __future__ import annotations

import unittest

from lib.extension_curves import ExtensionCurve
from lib.finite_fields import ExtensionField
from lib.pairing import (
    final_exponentiation,
    j1728_fapi1_miller_inverse_k2,
    j1728_distortion_map,
    lift_base_point,
    miller_loop,
    miller_loop_with_trace,
    reduced_tate_pairing,
    satoh_even_miller_inverse_k2,
)


class PairingTests(unittest.TestCase):
    """Use the published F_43 Appendix-B example as the fixed vector."""

    def setUp(self) -> None:
        self.field = ExtensionField(43, (1, 0, 1))
        self.curve = ExtensionCurve(
            self.field,
            self.field.element(1),
            self.field.zero,
        )
        self.order = 11
        self.i = self.field.element((0, 1))
        self.p_base = (23, 8)
        self.p = lift_base_point(self.field, self.p_base)
        self.q = j1728_distortion_map(self.field, self.p_base, self.i)

    def test_published_reduced_values(self) -> None:
        # The source's optimized loop representatives are 38 + 13t and
        # 28 + 40t.  Its vertical-line omissions can change a raw value by a
        # prime-subfield factor, but final exponentiation must reproduce the
        # published reduced values 11 + 3t and 26 + 23t exactly.
        self.assertEqual(
            final_exponentiation(self.field.element((38, 13)), self.order),
            self.field.element((11, 3)),
        )
        self.assertEqual(reduced_tate_pairing(self.curve, self.order, self.p, self.q), self.field.element((11, 3)))

        two_p = self.curve.scalar_mul(2, self.p)
        self.assertEqual(
            final_exponentiation(self.field.element((28, 40)), self.order),
            self.field.element((26, 23)),
        )
        self.assertEqual(reduced_tate_pairing(self.curve, self.order, two_p, self.q), self.field.element((26, 23)))

    def test_published_bilinearity_identity(self) -> None:
        value = reduced_tate_pairing(self.curve, self.order, self.p, self.q)
        doubled = reduced_tate_pairing(
            self.curve,
            self.order,
            self.curve.scalar_mul(2, self.p),
            self.q,
        )
        self.assertEqual(doubled, value**2)

    def test_trace_has_published_operation_sequence(self) -> None:
        _, trace = miller_loop_with_trace(self.curve, self.order, self.p, self.q)
        self.assertEqual(
            tuple(step.operation for step in trace),
            ("double", "double", "add", "double", "add"),
        )

    def test_final_exponentiation_lands_in_mu_r(self) -> None:
        for value in self.field.elements():
            if value:
                reduced = final_exponentiation(value, self.order)
                self.assertEqual(reduced**self.order, self.field.one)

    def test_distortion_pullback_and_satoh_invert_every_raw_target(self) -> None:
        inverse_distorted_p = j1728_distortion_map(self.field, self.p, -self.i)
        for scalar in range(1, self.order):
            base_multiple = self.curve.scalar_mul(scalar, self.p)
            distorted_multiple = j1728_distortion_map(
                self.field,
                base_multiple,
                self.i,
            )
            raw_target = miller_loop(
                self.curve,
                self.order,
                self.p,
                distorted_multiple,
            )
            transferred = miller_loop(
                self.curve,
                self.order,
                inverse_distorted_p,
                base_multiple,
            )
            self.assertEqual(raw_target, self.i ** (-self.order) * transferred)

            inversion = j1728_fapi1_miller_inverse_k2(
                self.curve,
                self.order,
                self.p_base,
                raw_target,
                self.i,
            )
            self.assertEqual(inversion.point, distorted_multiple)
            self.assertLessEqual(inversion.candidates_tested, 4)

    def test_satoh_published_example_4_4(self) -> None:
        field = ExtensionField(139, (4, 0, 1))
        curve = ExtensionCurve(field, field.element(-13), field.element(-7))
        theta = field.element((0, 1))
        fixed_point = field.element(67), 38 * theta
        raw_target = field.element((109, 25))

        inversion = satoh_even_miller_inverse_k2(
            curve,
            point_order=35,
            miller_scalar=140,
            fixed_point=fixed_point,
            raw_target=raw_target,
        )

        self.assertEqual(inversion.x_candidates, (59, 75))
        self.assertEqual(inversion.point, lift_base_point(field, (59, -54 % 139)))
        self.assertEqual(
            miller_loop(curve, 140, fixed_point, inversion.point),
            raw_target,
        )


if __name__ == "__main__":
    unittest.main()
