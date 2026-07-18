from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from analyze_mnt_three_chains import (  # noqa: E402
    analyze_mnt_three_chains,
    power_remainder_coefficients,
)


class MntThreeChainTests(unittest.TestCase):
    def test_power_remainder_table_through_degree_12(self) -> None:
        self.assertEqual(
            power_remainder_coefficients(12),
            [
                (1, 0), (2, -4), (0, -8), (-8, 0), (-16, 32), (0, 64),
                (64, 0), (128, -256), (0, -512), (-512, 0),
                (-1024, 2048), (0, 4096),
            ],
        )

    def test_x480_matches_recorded_near_miss(self) -> None:
        rows = {row.parameter_x: row for row in analyze_mnt_three_chains(480)}
        row = rows[480]
        self.assertEqual((row.field_a, row.field_b, row.field_c), (920641, 921601, 922561))
        self.assertEqual(row.degree_c_to_a, 2055)
        self.assertEqual(row.degree_a_to_c, 115320)
        self.assertFalse(row.forward_closes_at_most_12)
        self.assertFalse(row.reverse_closes_at_most_12)

    def test_complete_finite_remainder_has_no_closing_hit(self) -> None:
        rows = analyze_mnt_three_chains(1025)
        self.assertEqual([row.parameter_x for row in rows], [3, 45, 480, 987])
        self.assertEqual(
            [(row.degree_c_to_a, row.degree_a_to_c) for row in rows],
            [(30, 21), (445, 78), (2055, 115320), (556386, 1949325)],
        )
        self.assertFalse(
            any(
                row.forward_closes_at_most_12 or row.reverse_closes_at_most_12
                for row in rows
            )
        )


if __name__ == "__main__":
    unittest.main()
