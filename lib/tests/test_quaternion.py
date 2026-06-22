from __future__ import annotations

import itertools
import random
import unittest
from fractions import Fraction

from lib.quaternion import (
    MaximalOrder,
    Quaternion,
    exact_short_vector,
    first_represented_normalized_target,
    lll_short_vector,
    normalized_norm_spectrum,
    theta_series_prefix,
)


class QuaternionTests(unittest.TestCase):
    def test_defining_relations_and_multiplicative_norm(self) -> None:
        p = 11
        i = Quaternion(p, 0, 1)
        j = Quaternion(p, 0, 0, 1)
        one = Quaternion(p, 1)
        self.assertEqual(i * i, -one)
        self.assertEqual(j * j, -p * one)
        self.assertEqual(i * j, -(j * i))
        x = Quaternion(p, Fraction(3, 2), -2, Fraction(1, 2), 1)
        y = Quaternion(p, -1, Fraction(1, 2), 2, Fraction(-1, 2))
        self.assertEqual((x * y).reduced_norm(), x.reduced_norm() * y.reduced_norm())

    def test_order_norm_and_discriminant_known_values(self) -> None:
        order = MaximalOrder(11)
        self.assertEqual(order.norm((1, 0, 0, 0)), 1)
        self.assertEqual(order.norm((0, 0, 1, 0)), 3)
        self.assertEqual(order.norm((2, -1, 3, 4)), 82)
        self.assertEqual(abs(order.trace_discriminant()), 11 * 11)
        for left in order.basis:
            for right in order.basis:
                coordinates = order.coordinates(left * right)
                self.assertEqual(order.element(coordinates), left * right)

    def test_prime_ideal_index_closure_and_equivalent_ideal(self) -> None:
        order = MaximalOrder(11)
        ideal = order.prime_ideal(3, (1, 0, 2, 0))
        self.assertEqual(ideal.index, 9)
        self.assertEqual(ideal.norm, 3)
        self.assertTrue(ideal.verifies_left_closure())
        shortest = exact_short_vector(ideal)
        equivalent = ideal.equivalent_ideal_from_element(shortest.order_coordinates)
        self.assertEqual(equivalent.norm, shortest.norm // ideal.norm)
        self.assertTrue(equivalent.verifies_left_closure())
        self.assertEqual(
            theta_series_prefix(ideal, 8),
            theta_series_prefix(equivalent, 8),
        )

    def test_prime_ideal_right_order_known_invariants(self) -> None:
        order = MaximalOrder(11)
        ideal = order.prime_ideal(3, (1, 0, 2, 0))
        right_order = ideal.right_order()
        self.assertTrue(right_order.verifies_multiplicative_closure())
        self.assertEqual(abs(right_order.trace_discriminant()), 11 * 11)
        self.assertTrue(right_order.contains(Quaternion(11, 1)))
        self.assertTrue(ideal.verifies_dual_product_identity())
        for ideal_generator in (order.element(row) for row in ideal.basis):
            for right_element in right_order.basis:
                self.assertTrue(ideal.contains(ideal_generator * right_element))

    def test_exact_search_matches_wider_brute_force_box(self) -> None:
        order = MaximalOrder(19)
        ideal, _ = order.random_prime_ideal(5, random.Random(3301))
        exact = exact_short_vector(ideal)
        brute_norm = min(
            order.norm(
                tuple(
                    sum(coefficients[row] * exact.reduced_basis[row][col] for row in range(4))
                    for col in range(4)
                )
            )
            for coefficients in itertools.product(range(-4, 5), repeat=4)
            if any(coefficients)
        )
        self.assertEqual(exact.norm, brute_norm)
        self.assertLessEqual(exact.norm, lll_short_vector(ideal).norm)

    def test_seeded_random_prime_ideals_are_closed(self) -> None:
        rng = random.Random(33032026)
        for p in (11, 19, 43):
            order = MaximalOrder(p)
            for ell in (3, 5, 7):
                if ell == p:
                    continue
                ideal, _ = order.random_prime_ideal(ell, rng)
                self.assertEqual(ideal.index, ell * ell)
                self.assertTrue(ideal.verifies_left_closure())

    def test_large_prime_neighbor_uses_exact_isotropic_sampler(self) -> None:
        order = MaximalOrder(10007)
        ell = 10103
        ideal, alpha = order.random_prime_ideal(ell, random.Random(33032028))
        self.assertEqual(order.norm(alpha) % ell, 0)
        self.assertEqual(ideal.norm, ell)
        self.assertTrue(ideal.verifies_left_closure())

    def test_normalized_spectrum_matches_theta_support(self) -> None:
        order = MaximalOrder(19)
        ideal, _ = order.random_prime_ideal(23, random.Random(33032030))
        cutoff = 12
        spectrum = normalized_norm_spectrum(ideal, cutoff)
        theta = theta_series_prefix(ideal, cutoff)
        self.assertEqual(
            set(spectrum.witnesses),
            {norm for norm, count in enumerate(theta) if norm and count},
        )
        for norm, vector in spectrum.witnesses.items():
            self.assertEqual(order.norm(vector), norm * ideal.norm)
            self.assertTrue(ideal.contains_coordinates(vector))

    def test_sparse_target_solver_matches_exact_spectrum(self) -> None:
        order = MaximalOrder(43)
        ideal, _ = order.random_prime_ideal(47, random.Random(33032033))
        spectrum = normalized_norm_spectrum(ideal, 64)
        powers = (1, 2, 4, 8, 16, 32, 64)
        expected = min(norm for norm in powers if norm in spectrum.witnesses)
        result = first_represented_normalized_target(ideal, powers)
        self.assertEqual(result.normalized_norm, expected)
        self.assertIsNotNone(result.order_coordinates)
        self.assertEqual(
            order.norm(result.order_coordinates), expected * ideal.norm
        )
        eliminated = first_represented_normalized_target(
            ideal, powers, max_box_candidates=1
        )
        self.assertEqual(eliminated.normalized_norm, expected)
        self.assertIn("coordinate-elimination", eliminated.search_method)
        self.assertGreater(eliminated.elimination_triples_checked, 0)
        self.assertEqual(
            order.norm(eliminated.order_coordinates), expected * ideal.norm
        )


if __name__ == "__main__":
    unittest.main()
