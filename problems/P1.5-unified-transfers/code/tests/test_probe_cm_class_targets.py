"""Invariant tests for the CM/class-group candidate probe."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "probe_cm_class_targets.py"
SPEC = importlib.util.spec_from_file_location("probe_cm_class_targets", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CmClassTargetTests(unittest.TestCase):
    def test_complete_order_17_subgroup_has_one_unoriented_label(self) -> None:
        row = MODULE.probe_case(53)
        self.assertEqual(row["subgroup_order"], 17)
        self.assertEqual(row["nonzero_points_checked"], 16)
        self.assertEqual(row["distinct_cm_eigenvalues"], 1)
        self.assertEqual(row["distinct_annihilator_labels"], 1)
        self.assertEqual(row["distinct_kernel_labels"], 1)
        self.assertEqual(row["distinct_velu_quotients"], 1)

    def test_ray_orders_separate_mod_r_and_mod_r_squared(self) -> None:
        for r in (3, 5, 7, 13):
            self.assertNotEqual(MODULE.ray_class_order_qi(r) % r, 0)
            self.assertEqual(
                MODULE.r_adic_valuation(MODULE.ray_class_order_qi(r, 2), r),
                2,
            )

    def test_principal_units_linearize_both_gaussian_coordinates(self) -> None:
        r = 13
        modulus = r * r
        left = (1 + 4 * r, 7 * r)
        right = (1 + 11 * r, 2 * r)
        product = MODULE.gaussian_multiply(left, right, modulus)
        self.assertEqual(MODULE.principal_unit_log(product, r), (2, 9))
        for scalar in range(r):
            power = MODULE.gaussian_power((1 + r, 0), scalar, modulus)
            self.assertEqual(MODULE.principal_unit_log(power, r), (scalar, 0))

    def test_principal_units_move_lifts_not_source_points(self) -> None:
        for r in (3, 5, 13):
            self.assertEqual(MODULE.level_lift_orbits(r), (r, 1, r - 1))

    def test_explicit_class_number_threshold(self) -> None:
        self.assertEqual(MODULE.size_obstruction_threshold_bits(), 21)
        self.assertGreaterEqual(MODULE.ring_class_number_upper_bound(2**20), 2**19)
        self.assertLess(MODULE.ring_class_number_upper_bound(2**21), 2**20)


if __name__ == "__main__":
    unittest.main()
