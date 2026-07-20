"""Known-answer tests for the finite-field Buell-form lift probe."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "probe_buell_reduction.py"
SPEC = importlib.util.spec_from_file_location("probe_buell_reduction", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BuellReductionTests(unittest.TestCase):
    def test_known_order_29_reduction(self) -> None:
        case = MODULE.Case(0, 1, -7, 23, 29)
        row = MODULE.analyze_case(case)
        self.assertEqual(row["curve_order"], 29)
        self.assertEqual(row["nonzero_points"], 28)
        self.assertTrue(row["all_congruent_mod_p"])

    def test_canonical_lifts_do_not_share_the_model_discriminant(self) -> None:
        case = MODULE.Case(0, 1, -7, 23, 29)
        row = MODULE.analyze_case(case)
        self.assertGreater(row["distinct_lifted_discriminants"], 1)
        self.assertFalse(row["one_fixed_target"])

    def test_group_law_closes_on_every_recorded_case(self) -> None:
        for case in MODULE.FULL_CASES:
            row = MODULE.analyze_case(case)
            self.assertEqual(row["curve_order"] % case.r, 0)
            self.assertEqual(row["nonzero_points"], case.r - 1)


if __name__ == "__main__":
    unittest.main()

