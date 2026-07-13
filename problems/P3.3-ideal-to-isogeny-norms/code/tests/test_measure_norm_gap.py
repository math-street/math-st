from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from measure_norm_gap import run_instances, scaling_rows, summarize_rows


class MeasureNormGapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = run_instances([11], 4, [3, 5, 7], 33032026)

    def test_rows_satisfy_norm_and_certificate_invariants(self) -> None:
        self.assertEqual(len(self.rows), 4)
        for row in self.rows:
            self.assertEqual(row["ideal_index"], row["input_ideal_norm"] ** 2)
            self.assertEqual(
                row["exact_element_reduced_norm"],
                row["exact_equivalent_ideal_norm"] * row["input_ideal_norm"],
            )
            self.assertGreaterEqual(row["lll_approximation_factor"], 1.0)
            self.assertGreater(row["exact_candidates_checked"], 0)
            self.assertEqual(
                row["norm_convention"],
                "nrd(element)/N(input ideal)=N(equivalent ideal)",
            )

    def test_seeded_run_is_algebraically_deterministic(self) -> None:
        repeat = run_instances([11], 4, [3, 5, 7], 33032026)
        volatile = {"lll_seconds", "exact_seconds"}
        stable_rows = [
            {key: value for key, value in row.items() if key not in volatile}
            for row in self.rows
        ]
        stable_repeat = [
            {key: value for key, value in row.items() if key not in volatile}
            for row in repeat
        ]
        self.assertEqual(stable_rows, stable_repeat)

    def test_summary_contains_required_dependence_groups(self) -> None:
        summaries = summarize_rows(self.rows)
        families = {row["group_family"] for row in summaries}
        self.assertTrue(
            {"overall", "p", "p_bits", "p_mod_8", "input_ideal_norm", "ell_mod_4", "theta_fingerprint"}
            <= families
        )
        overall = summaries[0]
        self.assertEqual(overall["n"], 4)
        self.assertGreaterEqual(overall["lll_exact_hit_rate"], 0.0)
        self.assertLessEqual(overall["lll_exact_hit_rate"], 1.0)

    def test_near_p_policy_avoids_trivially_small_input_ideals(self) -> None:
        rows = run_instances([2203], 2, [], 33032028, "near-p")
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertGreater(row["input_ideal_norm"], row["p"])
            self.assertLess(row["input_ideal_norm"], 2 * row["p"])
            self.assertIn("near-p", row["sampler"])

    def test_scaling_rows_store_fit_residuals(self) -> None:
        rows = run_instances([2203, 560083], 2, [], 33032029, "near-p")
        scaling = scaling_rows(rows)
        self.assertEqual([row["p_bits"] for row in scaling], [12, 20])
        for row in scaling:
            self.assertIn("log2_exact_seconds_residual", row)
            self.assertGreaterEqual(row["lll_exact_hit_rate"], 0.0)
            self.assertLessEqual(row["lll_exact_hit_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
