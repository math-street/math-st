"""Known-answer and independent validation tests for explicit CM units."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from cm_units import construct_cm_pair, unit_automorphism, validate_cm_case
from lib.curves import INFINITY
from lib.dlog import pollard_rho_orbits


class CMUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = construct_cm_pair(9, minimum_subgroup_bits=5)

    def test_pair_uses_one_prime_and_expected_models(self) -> None:
        minus_three, minus_four = self.cases
        self.assertEqual(minus_three.curve.p, minus_four.curve.p)
        self.assertEqual(minus_three.curve.a, 0)
        self.assertNotEqual(minus_three.curve.b, 0)
        self.assertEqual(minus_four.curve.b, 0)
        self.assertNotEqual(minus_four.curve.a, 0)

    def test_independent_counts_and_characteristic_equations(self) -> None:
        for case in self.cases:
            result = validate_cm_case(case, samples=8, seed=52)
            self.assertEqual(result["exhaustive_order"], case.group_order)
            self.assertEqual(result["bsgs_order"], case.group_order)

    def test_known_logs_recovered_with_full_unit_orbits(self) -> None:
        for case in self.cases:
            secret = min(17, case.subgroup_order - 1)
            target = case.curve.scalar_mul(secret, case.generator, charge=False)
            result = pollard_rho_orbits(
                case.curve,
                case.generator,
                target,
                case.subgroup_order,
                automorphism=lambda point, active=case: unit_automorphism(active, point),
                automorphism_scalar=case.automorphism_scalar,
                automorphism_order=case.automorphism_order,
                seed=52,
            )
            self.assertEqual(result.logarithm, secret)
            self.assertNotEqual(target, INFINITY)


if __name__ == "__main__":
    unittest.main()
