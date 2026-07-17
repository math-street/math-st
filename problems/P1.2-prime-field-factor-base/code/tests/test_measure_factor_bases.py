from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from lib.curves import Curve
from measure_factor_bases import decomposition_count, find_first_decomposition, fit_scaling, pair_sum_counts


class MeasurementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = Curve(17, 2, 2)
        generator = (5, 1)
        self.base = [self.curve.scalar_mul(index, generator) for index in (1, 4, 7, 11)]

    def test_pair_table_matches_direct_ordered_triples(self) -> None:
        pair_counts, _ = pair_sum_counts(self.curve, self.base)
        self.assertEqual(sum(pair_counts.values()), len(self.base) ** 2)
        for target_scalar in range(19):
            target = self.curve.scalar_mul(target_scalar, (5, 1))
            measured = decomposition_count(self.curve, self.base, pair_counts, target)
            direct = 0
            for left in self.base:
                for middle in self.base:
                    for right in self.base:
                        if self.curve.add(self.curve.add(left, middle), right) == target:
                            direct += 1
            self.assertEqual(measured, direct)

    def test_search_agrees_with_count_and_returns_valid_sum(self) -> None:
        pair_counts, _ = pair_sum_counts(self.curve, self.base)
        for target_scalar in range(19):
            target = self.curve.scalar_mul(target_scalar, (5, 1))
            count = decomposition_count(self.curve, self.base, pair_counts, target)
            checked, triple, _ = find_first_decomposition(self.curve, self.base, target)
            self.assertGreaterEqual(checked, 1)
            self.assertEqual(triple is not None, count > 0)
            if triple is not None:
                self.assertEqual(self.curve.add(self.curve.add(triple[0], triple[1]), triple[2]), target)

    def test_scaling_fit_retains_residuals(self) -> None:
        summaries = [
            {"base_kind": "demo", "bits": bits, "p": p, "mean_pair_checks": checks}
            for bits, p, checks in ((4, 16, 2), (6, 64, 4), (8, 256, 8))
        ]
        fit = fit_scaling(summaries)
        self.assertEqual(len(fit), 3)
        self.assertAlmostEqual(float(fit[0]["log_log_slope"]), 0.5)
        self.assertTrue(all(abs(float(row["log_residual"])) < 1e-12 for row in fit))


if __name__ == "__main__":
    unittest.main()
