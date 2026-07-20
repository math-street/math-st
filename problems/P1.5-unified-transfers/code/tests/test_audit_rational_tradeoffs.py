"""Regression tests for the finite P1.5 overlap certificate."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "audit_rational_tradeoffs.py"
SPEC = importlib.util.spec_from_file_location("audit_rational_tradeoffs", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RationalTradeoffAuditTests(unittest.TestCase):
    def test_every_subset_through_order_seven_satisfies_exact_identity(self) -> None:
        for r in (2, 3, 5, 7):
            for mask in range(1, 1 << r):
                subset = frozenset(index for index in range(r) if mask >> index & 1)
                MODULE.verify_overlap_identity(r, subset)

    def test_strengthened_constant_has_no_small_integer_counterexample(self) -> None:
        for r in (2, 3, 5, 7, 11, 13, 17, 19):
            for branch_count in range(1, r + 1):
                for pole_degree in range(r + 1):
                    MODULE.certify_coarse_constant(r, branch_count, pole_degree)

    def test_order_seven_extremal_profile(self) -> None:
        profile = tuple(MODULE.minimum_peak_overlap(7, size) for size in range(1, 8))
        self.assertEqual(profile, (0, 1, 1, 2, 4, 5, 7))


if __name__ == "__main__":
    unittest.main()

