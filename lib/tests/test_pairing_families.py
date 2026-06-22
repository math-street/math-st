from __future__ import annotations

import unittest

from lib.curves import (
    evaluate_pairing_family,
    generate_pairing_family,
    validate_pairing_family,
)


class PairingFamilyTests(unittest.TestCase):
    def test_small_prime_bn_bls12_and_bls24_fixtures(self) -> None:
        fixtures = (("BN", -2, 12), ("BLS12", -2, 12), ("BLS24", -5, 24))
        for family, seed, expected_degree in fixtures:
            parameters = generate_pairing_family(family, seed)
            validation = validate_pairing_family(parameters)
            self.assertTrue(validation.valid)
            self.assertEqual(parameters.embedding_degree, expected_degree)
            self.assertEqual((parameters.p + 1 - parameters.trace) % parameters.r, 0)

    def test_bls12_381_matches_published_seed_and_moduli(self) -> None:
        parameters = evaluate_pairing_family("BLS12", -0xD201000000010000)
        self.assertEqual(
            parameters.p,
            int(
                "1a0111ea397fe69a4b1ba7b6434bacd7"
                "64774b84f38512bf6730d2a0f6b0f624"
                "1eabfffeb153ffffb9feffffffffaaab",
                16,
            ),
        )
        self.assertEqual(
            parameters.r,
            int("73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001", 16),
        )
        validation = validate_pairing_family(parameters, check_primality=False)
        self.assertTrue(validation.order_divisible)
        self.assertTrue(validation.exact_embedding_degree)

    def test_kss16_integral_fixture_has_the_family_congruences(self) -> None:
        parameters = evaluate_pairing_family("KSS16", 25)
        self.assertEqual(parameters.p, 105_890_880_565)
        self.assertEqual(parameters.r, 2_491_537)
        self.assertEqual(parameters.trace, 558_066)
        validation = validate_pairing_family(parameters, check_primality=False)
        self.assertTrue(validation.order_divisible)
        self.assertTrue(validation.exact_embedding_degree)
        with self.assertRaises(ValueError):
            generate_pairing_family("KSS16", 25)

    def test_invalid_integrality_and_unknown_family_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_pairing_family("BLS12", 3)
        with self.assertRaises(ValueError):
            evaluate_pairing_family("unknown", 2)


if __name__ == "__main__":
    unittest.main()
