"""Tests for the classical sieve simulation and fit."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, CODE / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SIMULATE = load("simulate_sieve")
FIT = load("fit_sieve")


class SieveTests(unittest.TestCase):
    def test_exact_occupancy_pair_count(self) -> None:
        counts = np.asarray([0, 1, 2, 3, 4])
        self.assertEqual(SIMULATE.occupancy_pairs(counts), 4)

    def test_seeded_simulation_is_reproducible(self) -> None:
        first = SIMULATE.simulate((12, 16), 2, 1234)
        second = SIMULATE.simulate((12, 16), 2, 1234)
        self.assertEqual(first, second)

    def test_noiseless_fit_recovers_known_parameters(self) -> None:
        log_n = np.asarray([4.0, 5.0, 6.0, 8.0, 10.0, 12.0])
        expected = np.asarray([2.25, -0.75, 1.5])
        log_q = FIT.design_matrix(log_n) @ expected
        actual = FIT.fit_parameters(log_n, log_q)
        np.testing.assert_allclose(actual, expected, rtol=1e-10, atol=1e-10)

    def test_regression_rmse_is_zero_for_exact_linear_features(self) -> None:
        feature = np.arange(1.0, 6.0)[:, np.newaxis]
        response = 3.0 * feature[:, 0] - 2.0
        self.assertAlmostEqual(FIT.regression_rmse(feature, response), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
