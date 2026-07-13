from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from measure_power_targets import powers_through, run_instances, summarize_rows


class PowerTargetTests(unittest.TestCase):
    def test_powers_through_known_values(self) -> None:
        self.assertEqual(powers_through(2, 17), (1, 2, 4, 8, 16))
        self.assertEqual(powers_through(3, 10), (1, 3, 9))

    def test_smoke_instances_are_exact_and_uncensored(self) -> None:
        rows = run_instances([2203, 560083], 1, 33032028, 1_000_000_000)
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["power2_censored"], 0)
            self.assertEqual(row["power3_censored"], 0)
            self.assertGreaterEqual(row["power2_over_unconstrained"], 1.0)
            self.assertGreaterEqual(row["power3_over_unconstrained"], 1.0)
        summary = summarize_rows(rows)[0]
        self.assertEqual(summary["power2_observed"], 2)
        self.assertEqual(summary["power3_observed"], 2)


if __name__ == "__main__":
    unittest.main()
