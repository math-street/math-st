"""Exact tests for the A002 affine-collision verifier."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "verify_generic_oracle_bound.py"
SPEC = importlib.util.spec_from_file_location("verify_generic_oracle_bound", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load verify_generic_oracle_bound.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GenericOracleBoundTests(unittest.TestCase):
    def test_known_fixture_attains_three_distinct_collision_roots(self) -> None:
        roots = MODULE.informative_challenges(MODULE.known_fixture(), 5)
        self.assertEqual(roots, frozenset((0, 2, 4)))

    def test_all_p5_three_form_sets_respect_and_attain_pair_bound(self) -> None:
        row = MODULE.audit_parameter(5, handles=3, trials=1, seed=2404)
        self.assertEqual(row["mode"], "exhaustive")
        self.assertEqual(row["sets_checked"], 2300)
        self.assertEqual(row["maximum_bad_challenges"], 3)
        self.assertEqual(row["violations"], 0)


if __name__ == "__main__":
    unittest.main()
