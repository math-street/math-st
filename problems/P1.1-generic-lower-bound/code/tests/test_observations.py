"""Known-answer tests for the P1.1 observation scripts."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
for path in (CODE_DIR, REPOSITORY_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from observe_coordinate_bypass import run as run_coordinate_bypass
from observe_extension_decomposition import run as run_extension_decomposition
from observe_ghs_transfer import run as run_ghs_transfer
from observe_mov_transfer import run as run_mov_transfer
from observe_semaev_decomposition import run as run_semaev_decomposition
from observe_smart_attack import run as run_smart_attack


class ObservationTests(unittest.TestCase):
    def test_coordinate_compiler_preserves_log_and_removes_charge(self) -> None:
        rows = run_coordinate_bypass()
        self.assertEqual([row["recovered"] for row in rows], [7, 7])
        self.assertGreater(rows[0]["group_operations"], 0)
        self.assertEqual(rows[1]["group_operations"], 0)

    def test_smart_attack_known_answer(self) -> None:
        row = run_smart_attack()
        self.assertEqual((row["secret"], row["recovered"]), (7, 7))
        self.assertEqual(row["p_adic_lifts"], 2)

    def test_mov_transfer_known_answer(self) -> None:
        row = run_mov_transfer()
        self.assertEqual((row["secret"], row["recovered"]), (2, 2))
        self.assertEqual(row["reduced_pairing_base"], "[11,3]")
        self.assertEqual(row["auxiliary_dlp_solves"], 1)

    def test_prime_field_semaev_relation(self) -> None:
        row = run_semaev_decomposition()
        self.assertEqual(row["polynomial_zero_pairs"], 2)
        self.assertEqual(row["verified_ordered_decompositions"], 2)

    def test_extension_field_relation(self) -> None:
        row = run_extension_decomposition()
        self.assertEqual(row["basis_coefficient_equations"], 3)
        self.assertEqual(row["verified_ordered_decompositions"], 1)
        self.assertEqual(row["subfield_structure_uses"], 1)

    def test_genus_one_ghs_transfer_known_answer(self) -> None:
        row = run_ghs_transfer()
        self.assertEqual((row["secret"], row["recovered"]), (2, 2))
        self.assertEqual(row["source_subgroup_order"], 3)
        self.assertEqual(row["auxiliary_curve_points"], 6)
        self.assertEqual(row["scalar_relations_checked"], 3)
        self.assertEqual(row["higher_genus_claims"], 0)


if __name__ == "__main__":
    unittest.main()
