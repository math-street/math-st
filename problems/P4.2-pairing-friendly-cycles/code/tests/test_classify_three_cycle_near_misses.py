from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_three_cycle_near_misses import (  # noqa: E402
    DEFAULT_CANDIDATES,
    classify_rows,
    load_rows,
)


class NearMissClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = classify_rows(load_rows(DEFAULT_CANDIDATES))

    def test_all_42_source_rows_are_preserved_once(self) -> None:
        self.assertEqual(len(self.rows), 42)
        source_fields = {
            (row.source_field_e1, row.source_field_e2, row.source_field_e3)
            for row in self.rows
        }
        self.assertEqual(len(source_fields), 42)

    def test_x480_both_orientations_are_mnt_chain_rows(self) -> None:
        rows = [row for row in self.rows if row.parameter_x == 480]
        self.assertEqual(len(rows), 2)
        self.assertEqual({row.closing_degree_r_to_p for row in rows}, {2055, 115320})
        self.assertEqual({row.family for row in rows}, {"consecutive_mnt_chain"})

    def test_degree_483882_row_is_the_unique_high_residual(self) -> None:
        rows = [
            row
            for row in self.rows
            if row.first_appears_above_16bit
            and row.family == "unclassified_residual"
        ]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            (row.canonical_field_p, row.canonical_field_q, row.canonical_field_r),
            (483883, 483481, 482659),
        )
        self.assertEqual(
            (
                row.target_degree_p_to_q,
                row.target_degree_q_to_r,
                row.closing_degree_r_to_p,
            ),
            (5, 11, 483882),
        )

    def test_28bit_ledger_adds_only_proved_mnt_rows_after_26_bits(self) -> None:
        candidates = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "search_three_cycles_roots_p5-268435455_k3-12_20260708_candidates.csv"
        )
        rows = classify_rows(load_rows(candidates))
        self.assertEqual(len(rows), 61)
        self.assertEqual(
            sum(row.family == "consecutive_mnt_chain" for row in rows),
            26,
        )
        self.assertEqual(
            sum(row.family == "unclassified_residual" for row in rows),
            35,
        )
        new_rows = [row for row in rows if row.maximum_field_prime >= 2**26]
        self.assertEqual({row.parameter_x for row in new_rows}, {5967, 7095})
        self.assertEqual(
            {row.family for row in new_rows},
            {"consecutive_mnt_chain"},
        )


if __name__ == "__main__":
    unittest.main()
