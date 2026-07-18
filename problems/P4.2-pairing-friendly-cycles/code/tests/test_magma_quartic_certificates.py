from __future__ import annotations

import ast
import unittest
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROBLEM_ROOT / "data"


class MagmaQuarticCertificateTests(unittest.TestCase):
    def test_two_cover_descent_has_expected_controls_and_obstructions(self) -> None:
        lines = (
            DATA_ROOT / "magma_two_cover_descent_20260718.txt"
        ).read_text(encoding="utf-8").splitlines()
        values = {
            identifier: int(size)
            for line in lines
            if "|" in line
            for identifier, size in [line.split("|")]
        }
        self.assertEqual(values["QG012"], 1)
        self.assertEqual(values["QG013"], 1)
        self.assertEqual(
            {key for key, value in values.items() if value == 0},
            {"QG018", "QG019", "QG026", "QG028", "QG029"},
        )

    def test_all_accepted_pointed_outputs_have_small_gap(self) -> None:
        lines = (
            DATA_ROOT / "magma_pointed_quartics_20260718.txt"
        ).read_text(encoding="utf-8").splitlines()
        accepted = [line for line in lines if "|OK|" in line]
        self.assertEqual(len(accepted), 22)
        for line in accepted:
            points = ast.literal_eval(line.split("|OK|", 1)[1])
            self.assertTrue(all(abs(point[0]) <= 1 for point in points))

    def test_reducible_curve_points_and_rank_certificate(self) -> None:
        def quartic(value: int) -> int:
            return (
                17 * value**4
                - 10 * value**3
                + 27 * value**2
                - 10 * value
                + 17
            )

        self.assertEqual(quartic(-1), 9**2)
        certificate = (
            DATA_ROOT / "magma_reducible_rank_20260718.txt"
        ).read_text(encoding="utf-8")
        self.assertIn("RankBounds: 0 0", certificate)
        self.assertIn("Torsion: Z/2", certificate)


if __name__ == "__main__":
    unittest.main()
