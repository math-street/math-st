"""Smoke tests for the Satoh MI reproduction experiment."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "reproduce_satoh_mi.py"
SPEC = importlib.util.spec_from_file_location("reproduce_satoh_mi", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("failed to load reproduce_satoh_mi.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SatohReproductionTests(unittest.TestCase):
    def test_published_example(self) -> None:
        row = MODULE.reproduce_published_example()
        self.assertTrue(row["satoh_example_reproduced"])
        self.assertEqual(row["satoh_example_u"], 131)

    def test_p43_transfer(self) -> None:
        row = MODULE.benchmark_parameter(43, trials=2, seed=2404)
        self.assertEqual(row["raw_targets_exhaustively_inverted"], 10)
        self.assertEqual(row["pullback_identity_checks"], 10)
        self.assertLessEqual(row["maximum_candidates_tested"], 4)
        self.assertEqual(row["maximum_undefined_candidates"], 0)


if __name__ == "__main__":
    unittest.main()
