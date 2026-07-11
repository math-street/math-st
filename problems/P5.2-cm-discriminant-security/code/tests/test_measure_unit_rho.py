"""Tests for P5.2 measurement statistics and smoke execution."""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from measure_unit_rho import bootstrap_ratio, ols_slope, percentile


class MeasurementTests(unittest.TestCase):
    def test_percentile_known_values(self) -> None:
        self.assertEqual(percentile([1.0, 2.0, 3.0], 0.5), 2.0)
        self.assertEqual(percentile([1.0, 3.0], 0.25), 1.5)

    def test_bootstrap_ratio_matches_exact_ratio_of_means(self) -> None:
        ratio, low, high = bootstrap_ratio(
            [20, 22, 24, 26],
            [10, 11, 12, 13],
            rng=random.Random(52),
            resamples=100,
        )
        self.assertEqual(ratio, 2.0)
        self.assertAlmostEqual(low, 2.0)
        self.assertAlmostEqual(high, 2.0)

    def test_ols_known_line(self) -> None:
        intercept, slope = ols_slope([1.0, 2.0, 3.0], [5.0, 8.0, 11.0])
        self.assertAlmostEqual(intercept, 2.0)
        self.assertAlmostEqual(slope, 3.0)


if __name__ == "__main__":
    unittest.main()
