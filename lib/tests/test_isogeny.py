"""Known-answer and invariant tests for the toy isogeny helpers."""

from __future__ import annotations

import unittest

from lib.curves import Curve, curve_order, quadratic_twist
from lib.isogeny import (
    QuadraticExtensionCurve,
    canonical_curve,
    class_number_from_reduced_forms,
    curve_class_key,
    deuring_curve_key,
    extension_kernel_points,
    extension_velu_map,
    extension_velu_quotient,
    find_extension_torsion_generator,
    find_rational_torsion_generator,
    least_quadratic_nonresidue,
    quadratic_curve_key,
    quadratic_curve_order,
    quadratic_field,
    reduced_positive_forms,
    velu_map,
    velu_quotient,
)


class QuadraticExtensionCurveTests(unittest.TestCase):
    def test_frobenius_and_curve_class_keys(self) -> None:
        for prime in (7, 11):
            field = quadratic_field(prime)
            nonresidue = least_quadratic_nonresidue(prime)
            generator = (0, 1)
            self.assertEqual(field.mul(generator, generator), field.constant(nonresidue))
            for value in field.elements():
                self.assertEqual(field.pow(value, prime * prime), value)
                self.assertEqual(
                    field.pow(value, prime),
                    field.normalize((value[0], -value[1])),
                )

        field = quadratic_field(7)
        curve = QuadraticExtensionCurve(
            field,
            (1, 1),
            (2, 1),
        )
        key = quadratic_curve_key(curve)
        for scalar in field.elements():
            if scalar != field.zero:
                self.assertEqual(quadratic_curve_key(curve.scale(scalar)), key)
        self.assertEqual(
            deuring_curve_key(curve),
            deuring_curve_key(curve.frobenius_twist()),
        )

    def test_extension_velu_step_on_supersingular_fixture(self) -> None:
        field = quadratic_field(11)
        curve = QuadraticExtensionCurve(field, field.constant(-1), field.zero)
        self.assertEqual(quadratic_curve_order(curve), 144)
        generator = find_extension_torsion_generator(curve, 3, 144)
        kernel = extension_kernel_points(curve, generator, 3)
        self.assertEqual(len(kernel), 2)
        quotient = extension_velu_quotient(curve, generator, 3)
        self.assertEqual(quadratic_curve_order(quotient), 144)
        for kernel_point in kernel:
            self.assertIsNone(extension_velu_map(curve, kernel_point, generator, 3))

        checked = 0
        for point in curve.affine_points():
            image = extension_velu_map(curve, point, generator, 3)
            if image is not None:
                self.assertTrue(quotient.contains(image))
                checked += 1
            if checked == 20:
                break
        self.assertEqual(checked, 20)


class ReducedFormTests(unittest.TestCase):
    def test_hand_checkable_class_numbers(self) -> None:
        self.assertEqual(
            reduced_positive_forms(-23),
            ((1, 1, 6), (2, -1, 3), (2, 1, 3)),
        )
        self.assertEqual(class_number_from_reduced_forms(-20), 2)
        self.assertEqual(class_number_from_reduced_forms(-4), 1)


class VeluTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = Curve(419, 1, 0)
        self.order = 420
        self.generator = find_rational_torsion_generator(self.curve, 3, self.order)
        self.quotient = velu_quotient(self.curve, self.generator, 3)

    def test_starting_curve_has_expected_trace_zero_order(self) -> None:
        self.assertEqual(curve_order(self.curve), self.order)

    def test_velu_map_lands_on_quotient(self) -> None:
        checked = 0
        for point in self.curve.affine_points():
            image = velu_map(self.curve, point, self.generator, 3)
            if image is not None:
                self.assertTrue(self.quotient.contains(image))
                checked += 1
            if checked == 20:
                break
        self.assertEqual(checked, 20)

    def test_quotient_preserves_point_count(self) -> None:
        self.assertEqual(curve_order(self.quotient), self.order)

    def test_canonicalization_preserves_twists(self) -> None:
        nonsquare_twist = quadratic_twist(self.quotient)
        self.assertNotEqual(
            curve_class_key(self.quotient), curve_class_key(nonsquare_twist)
        )
        self.assertEqual(canonical_curve(canonical_curve(self.curve)), canonical_curve(self.curve))


if __name__ == "__main__":
    unittest.main()
