from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from sweep_ghs_genus import (
    distribution_rows,
    enumerate_rows,
    low_genus_locus_rows,
)
from verify_published_example import build_profile


class ScriptTests(unittest.TestCase):
    def test_degree_four_sweep_and_summaries(self) -> None:
        rows = enumerate_rows([4])
        self.assertEqual(len(rows), 15)
        self.assertEqual(
            Counter(int(row["genus"]) for row in rows),
            Counter({1: 1, 2: 2, 4: 4, 8: 8}),
        )
        self.assertEqual(sum(int(row["count"]) for row in distribution_rows(rows)), 15)
        locus = low_genus_locus_rows(rows, [4])[0]
        self.assertEqual(locus["defining_annihilator_hex"], "0xf")
        self.assertEqual(locus["parameter_count"], 7)
        self.assertEqual(locus["b_locus_equation"], "b^8+b^4+b^2+b=0")
        self.assertEqual(
            locus["j_locus_equation_for_nonzero_j"], "j^7+j^6+j^4+1=0"
        )
        self.assertEqual(locus["b_locus_additive_with_zero"], 1)
        self.assertEqual(locus["j_locus_additive_with_zero"], 0)

    def test_published_example_profile(self) -> None:
        label, _field, profile, expected_genus = build_profile(False)
        self.assertEqual(label, "magma-degree-31")
        self.assertEqual(profile.annihilator_polynomial, 0x25)
        self.assertEqual(profile.conjugate_rank, 5)
        self.assertEqual(profile.magic_number, 6)
        self.assertEqual(profile.genus, expected_genus)


if __name__ == "__main__":
    unittest.main()
