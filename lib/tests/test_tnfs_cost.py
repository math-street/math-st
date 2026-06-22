from __future__ import annotations

import unittest
from dataclasses import replace

from lib.tnfs_cost import (
    FiniteTNFSParameters,
    finite_tnfs_cost,
    log2_dickman_rho,
    tnfs_model_preset,
)


class TNFSCostTests(unittest.TestCase):
    def test_dickman_values_match_bn_worked_example(self) -> None:
        self.assertAlmostEqual(log2_dickman_rho(2.0), -1.704381, places=5)
        self.assertAlmostEqual(log2_dickman_rho(414.7 / 57.0), -21.41, delta=0.02)
        self.assertAlmostEqual(log2_dickman_rho(460.8 / 57.0), -25.30, delta=0.02)

    def test_dickman_values_match_bls12_worked_example(self) -> None:
        self.assertAlmostEqual(log2_dickman_rho(791.2 / 73.5), -39.17, delta=0.01)
        self.assertAlmostEqual(log2_dickman_rho(584.8 / 73.5), -24.67, delta=0.01)

    def test_high_precision_dickman_matches_bls24_worked_example(self) -> None:
        self.assertAlmostEqual(log2_dickman_rho(1295.0 / 109.8), -44.85, delta=0.01)
        self.assertAlmostEqual(log2_dickman_rho(1460.0 / 109.8), -53.42, delta=0.01)

    def test_finite_model_reproduces_bn_security_with_stated_tolerance(self) -> None:
        parameters = FiniteTNFSParameters(
            coefficient_bound=2.0**7.36,
            smoothness_bound_bits=57.0,
            eta=6,
            roots_of_unity_index=1,
            relation_automorphisms=2,
            linear_algebra_automorphisms=1,
        )
        result = finite_tnfs_cost(414.7, 460.8, parameters)
        self.assertGreater(result.relation_yield_log2 - result.factor_base_log2, -0.1)
        self.assertAlmostEqual(result.sieve_space_log2, 99.45, delta=0.1)
        self.assertAlmostEqual(result.total_cost_log2, 99.69, delta=0.2)

        reduced_linear_algebra = finite_tnfs_cost(
            414.7,
            460.8,
            replace(parameters, linear_algebra_automorphisms=2),
        )
        self.assertLess(reduced_linear_algebra.total_cost_log2, result.total_cost_log2)

    def test_finite_model_reproduces_bls12_security(self) -> None:
        parameters = FiniteTNFSParameters(
            coefficient_bound=1169,
            smoothness_bound_bits=73.5,
            eta=6,
            roots_of_unity_index=1,
            relation_automorphisms=2,
            linear_algebra_automorphisms=2,
        )
        result = finite_tnfs_cost(791.2, 584.8, parameters)
        self.assertAlmostEqual(result.sieve_space_log2, 133.30, delta=0.01)
        self.assertAlmostEqual(result.relation_yield_log2, 69.46, delta=0.01)
        self.assertAlmostEqual(result.reduced_factor_base_log2, 67.83, delta=0.01)
        self.assertTrue(result.enough_relations)
        self.assertAlmostEqual(result.total_cost_log2, 131.8, delta=0.01)

    def test_finite_model_reproduces_kss16_and_bls24_rows(self) -> None:
        kss16 = finite_tnfs_cost(
            920.4,
            628.9,
            FiniteTNFSParameters(
                coefficient_bound=12,
                smoothness_bound_bits=80.0,
                eta=16,
                roots_of_unity_index=17,
                relation_automorphisms=16,
                linear_algebra_automorphisms=16,
            ),
        )
        self.assertAlmostEqual(kss16.relation_yield_log2, 76.08, delta=0.02)
        self.assertAlmostEqual(kss16.total_cost_log2, 139.0, delta=0.3)

        bls24 = finite_tnfs_cost(
            1295.0,
            1460.0,
            FiniteTNFSParameters(
                coefficient_bound=9,
                smoothness_bound_bits=109.8,
                eta=24,
                roots_of_unity_index=1,
                relation_automorphisms=1,
                linear_algebra_automorphisms=1,
            ),
        )
        self.assertAlmostEqual(bls24.relation_yield_log2, 104.63, delta=0.02)
        self.assertAlmostEqual(bls24.total_cost_log2, 203.72, delta=0.7)

    def test_o1less_and_calibrated_presets(self) -> None:
        asymptotic = tnfs_model_preset("sextnfs-o1less")
        self.assertAlmostEqual(asymptotic.security_bits_from_field_bits(5004), 128.0, delta=0.02)

        calibrated = tnfs_model_preset("bn254-calibrated")
        self.assertAlmostEqual(calibrated.security_bits_from_field_bits(3072), 99.69, places=10)
        self.assertLess(
            calibrated.security_bits_from_field_bits(3072),
            asymptotic.security_bits_from_field_bits(3072),
        )


if __name__ == "__main__":
    unittest.main()
