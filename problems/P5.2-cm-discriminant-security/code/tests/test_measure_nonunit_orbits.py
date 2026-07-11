"""Tests for the non-unit orbit measurement helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from measure_nonunit_orbits import summarize_rows


class NonunitMeasurementTests(unittest.TestCase):
    def test_summary_uses_exact_orbit_arithmetic(self) -> None:
        rows = [
            {
                "bits": 9,
                "p": 401,
                "group_order": 436,
                "subgroup_order": 109,
                "cofactor": 4,
                "endomorphism_scalar": 30,
                "scalar_order": 108,
                "map_evaluations": 107,
                "elapsed_ns": elapsed,
            }
            for elapsed in (100, 300)
        ]
        summary = summarize_rows(rows)[0]
        self.assertEqual(summary["nonzero_quotient_orbits"], 1)
        self.assertEqual(summary["map_evaluations_per_normalization"], 107)
        self.assertEqual(summary["mean_elapsed_ns"], "200.000")
        self.assertAlmostEqual(float(summary["ideal_random_mapping_speedup"]), 108**0.5)

    def test_summary_rejects_incomplete_enumeration(self) -> None:
        row = {
            "bits": 9,
            "p": 401,
            "group_order": 436,
            "subgroup_order": 109,
            "cofactor": 4,
            "endomorphism_scalar": 30,
            "scalar_order": 108,
            "map_evaluations": 106,
            "elapsed_ns": 100,
        }
        with self.assertRaises(ArithmeticError):
            summarize_rows([row])


if __name__ == "__main__":
    unittest.main()
