"""Tests for the SG-01 toy degree measurement."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from measure_toy_degrees import measure  # noqa: E402


class MeasureToyDegreesTest(unittest.TestCase):
    def test_q5_matches_caminata_gorla_example_4_2(self) -> None:
        result = measure(5)
        self.assertEqual(result["first_fall_degree"], 3)
        self.assertEqual(result["solving_degree"], 4)
        self.assertEqual(result["degree_of_regularity"], 8)

    def test_algorithm_trace_is_a_fourth_number(self) -> None:
        result = measure(5)
        self.assertEqual(result["algorithm_max_critical_pair_degree"], 9)
        values = {
            result["first_fall_degree"],
            result["solving_degree"],
            result["degree_of_regularity"],
            result["algorithm_max_critical_pair_degree"],
        }
        self.assertEqual(len(values), 4)


if __name__ == "__main__":
    unittest.main()

