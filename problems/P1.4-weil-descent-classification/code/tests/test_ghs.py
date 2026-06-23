from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from ghs import (
    apply_frobenius_polynomial,
    format_binary_polynomial,
    frobenius_annihilator,
    gf2_basis,
    gf2_in_span,
    ghs_profile,
)
from lib.curves import BinaryField


class GHSTests(unittest.TestCase):
    def setUp(self) -> None:
        self.field = BinaryField(4, 0b1_0011)

    def test_binary_rank_and_membership(self) -> None:
        basis = gf2_basis((0b1010, 0b0110, 0b1100, 0b0001))
        self.assertEqual(len(basis), 3)
        self.assertTrue(gf2_in_span(0b1100, basis))
        self.assertFalse(gf2_in_span(0b0010, basis))

    def test_base_field_parameter_has_genus_one(self) -> None:
        profile = ghs_profile(self.field, 1)
        self.assertEqual(profile.conjugate_rank, 1)
        self.assertTrue(profile.one_in_conjugate_span)
        self.assertEqual(profile.magic_number, 1)
        self.assertEqual(profile.genus, 1)

    def test_profile_is_frobenius_invariant(self) -> None:
        for b in range(1, self.field.order):
            profile = ghs_profile(self.field, b)
            conjugate = ghs_profile(self.field, self.field.square(b))
            self.assertEqual(profile.conjugate_rank, conjugate.conjugate_rank)
            self.assertEqual(profile.one_in_conjugate_span, conjugate.one_in_conjugate_span)
            self.assertEqual(profile.magic_number, conjugate.magic_number)
            self.assertEqual(profile.genus, conjugate.genus)

    def test_frobenius_polynomial(self) -> None:
        value = 0b0010
        polynomial = 0b1011
        expected = value ^ self.field.square(value) ^ self.field.frobenius(value, 3)
        self.assertEqual(
            apply_frobenius_polynomial(self.field, value, polynomial, 1), expected
        )

    def test_annihilator_degree_equals_orbit_span_rank(self) -> None:
        for value in range(1, self.field.order):
            annihilator = frobenius_annihilator(self.field, value, 1)
            profile = ghs_profile(self.field, self.field.square(value))
            self.assertEqual(annihilator, profile.annihilator_polynomial)
            self.assertEqual(annihilator.bit_length() - 1, profile.conjugate_rank)
        self.assertEqual(format_binary_polynomial(0b100101), "t^5+t^2+1")


if __name__ == "__main__":
    unittest.main()
