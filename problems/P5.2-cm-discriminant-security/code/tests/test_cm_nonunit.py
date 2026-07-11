"""Known-answer tests for the norm-two discriminant -7 endomorphism."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from cm_nonunit import (
    canonicalize_cm7_orbit,
    cm7_endomorphism,
    construct_cm7_case,
    multiplicative_order_mod_prime,
    validate_cm7_case,
)
from lib.dlog import pollard_rho_orbits


class CMNonunitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.case = construct_cm7_case(9, minimum_subgroup_bits=5)

    def test_independent_counts_and_endomorphism_relation(self) -> None:
        result = validate_cm7_case(self.case, samples=8, seed=7)
        self.assertEqual(result["exhaustive_order"], self.case.group_order)
        self.assertEqual(result["bsgs_order"], self.case.group_order)

    def test_scalar_order_is_exact(self) -> None:
        scalar = self.case.endomorphism_scalar
        order = self.case.scalar_order
        prime = self.case.subgroup_order
        self.assertEqual(multiplicative_order_mod_prime(scalar, prime), order)
        self.assertEqual(pow(scalar, order, prime), 1)

    def test_canonicalizer_is_constant_on_the_orbit(self) -> None:
        point = self.case.curve.scalar_mul(7, self.case.generator, charge=False)
        image = cm7_endomorphism(self.case, point)
        representative, exponent, evaluations = canonicalize_cm7_orbit(self.case, point)
        image_representative, image_exponent, _ = canonicalize_cm7_orbit(self.case, image)
        self.assertEqual(representative, image_representative)
        self.assertEqual(
            (exponent - image_exponent - 1) % self.case.scalar_order,
            0,
        )
        self.assertEqual(evaluations, self.case.scalar_order - 1)

    def test_quotient_rho_recovers_a_known_log(self) -> None:
        secret = 17
        self.assertLess(secret, self.case.subgroup_order)
        target = self.case.curve.scalar_mul(secret, self.case.generator, charge=False)
        result = pollard_rho_orbits(
            self.case.curve,
            self.case.generator,
            target,
            self.case.subgroup_order,
            automorphism=lambda point: cm7_endomorphism(self.case, point),
            automorphism_scalar=self.case.endomorphism_scalar,
            automorphism_order=self.case.scalar_order,
            seed=77,
            partitions=8,
            max_restarts=128,
            collision_table=True,
        )
        self.assertEqual(result.logarithm, secret)


if __name__ == "__main__":
    unittest.main()
