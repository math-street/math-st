"""Tests for the named physical-cost layer and sensitivity analysis."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

CODE = Path(__file__).resolve().parents[1]


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, CODE / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


COST = load("cost_model")
SENSITIVITY = load("sensitivity")
CONFIG = json.loads(
    (CODE / "configs" / "illustrative_surface_code.json").read_text(encoding="utf-8")
)
COUNTERS = {
    "n_bits": 32.0,
    "query_count": 1e6,
    "combination_attempts": 2e6,
    "list_size": 4096.0,
    "trial_count": 10.0,
}


class CostModelTests(unittest.TestCase):
    def test_distance_satisfies_and_predecessor_fails_when_available(self) -> None:
        report = COST.calculate_cost(COUNTERS, CONFIG)
        distance = report["physical_resources"]["code_distance"]
        target = report["physical_resources"]["logical_error_target_per_location"]
        self.assertLessEqual(COST.logical_error_rate(distance, CONFIG["surface_code"]), target)
        if distance > CONFIG["surface_code"]["minimum_code_distance"]:
            self.assertGreater(COST.logical_error_rate(distance - 2, CONFIG["surface_code"]), target)

    def test_lower_physical_error_does_not_raise_distance(self) -> None:
        base = COST.calculate_cost(COUNTERS, CONFIG)
        improved = deepcopy(CONFIG)
        improved["surface_code"]["physical_error_rate"] /= 10
        better = COST.calculate_cost(COUNTERS, improved)
        self.assertLessEqual(
            better["physical_resources"]["code_distance"],
            base["physical_resources"]["code_distance"],
        )

    def test_report_exposes_both_runtime_limits(self) -> None:
        report = COST.calculate_cost(COUNTERS, CONFIG)
        physical = report["physical_resources"]
        self.assertEqual(
            physical["code_cycles"],
            max(physical["algorithm_code_cycles"], physical["magic_factory_code_cycles"]),
        )
        self.assertIn(physical["runtime_bottleneck"], {"logical_depth", "magic_state_factories"})

    def test_sensitivity_ranks_all_supplied_ranges(self) -> None:
        ranges = {
            "surface_code.code_cycle_seconds": [2e-7, 2e-6],
            "logical_architecture.parallel_workers": [1.0, 16.0],
        }
        report = SENSITIVITY.analyze(COUNTERS, CONFIG, ranges)
        self.assertEqual(len(report["ranking"]), 2)
        self.assertEqual({item["parameter"] for item in report["ranking"]}, set(ranges))

    def test_published_logical_endpoints_are_reproduced(self) -> None:
        fixtures = (
            (
                "bonnetain_schrottenloher_2020_section3_3",
                71.6,
            ),
            ("peikert_2020_optimistic_endpoint", 56.0),
        )
        for stem, expected_log2_t in fixtures:
            config = json.loads(
                (CODE / "configs" / f"{stem}.json").read_text(encoding="utf-8")
            )
            counters = json.loads(
                (CODE / "configs" / f"{stem}_counters.json").read_text(encoding="utf-8")
            )
            report = COST.calculate_cost(counters, config)
            self.assertAlmostEqual(
                __import__("math").log2(report["logical_resources"]["t_gates"]),
                expected_log2_t,
                places=10,
            )


if __name__ == "__main__":
    unittest.main()
