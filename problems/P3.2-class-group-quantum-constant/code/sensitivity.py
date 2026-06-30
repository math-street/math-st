"""
sensitivity.py — one-at-a-time sensitivity for the named cost model.
Sub-goal: P3.2 / SG-06
Inputs:   --cost-report <JSON> --ranges <JSON>
Outputs:  data/sensitivity_n<N>_<YYYYMMDD>.json
Runtime:  under 1 second for the default range file
Validated against: nested-parameter override and ranking unit tests
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

CODE_DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("p32_cost_model", CODE_DIR / "cost_model.py")
assert SPEC is not None and SPEC.loader is not None
COST_MODEL = importlib.util.module_from_spec(SPEC)
sys.modules["p32_cost_model"] = COST_MODEL
SPEC.loader.exec_module(COST_MODEL)


def set_nested(config: dict[str, Any], path: str, value: float) -> None:
    """Set a dot-separated numeric configuration value."""
    parts = path.split(".")
    target = config
    for part in parts[:-1]:
        child = target.get(part)
        if not isinstance(child, dict):
            raise KeyError(path)
        target = child
    if parts[-1] not in target:
        raise KeyError(path)
    target[parts[-1]] = value


def analyze(
    counters: dict[str, float],
    base_config: dict[str, Any],
    ranges: dict[str, list[float]],
) -> dict[str, Any]:
    """Rank configured parameter ranges by physical spacetime impact."""
    base = COST_MODEL.calculate_cost(counters, base_config)
    base_metric = base["physical_resources"]["spacetime_qubit_seconds"]
    entries = []
    for path, endpoints in ranges.items():
        if len(endpoints) != 2 or endpoints[0] <= 0 or endpoints[1] <= 0:
            raise ValueError(f"range for {path} must contain two positive endpoints")
        endpoint_reports = []
        for value in endpoints:
            varied = deepcopy(base_config)
            set_nested(varied, path, value)
            report = COST_MODEL.calculate_cost(counters, varied)
            metric = report["physical_resources"]["spacetime_qubit_seconds"]
            endpoint_reports.append(
                {
                    "value": value,
                    "spacetime_qubit_seconds": metric,
                    "log2_change_from_base": math.log2(metric / base_metric),
                    "runtime_seconds": report["physical_resources"]["runtime_seconds"],
                    "physical_qubits": report["physical_resources"]["physical_qubits"],
                    "code_distance": report["physical_resources"]["code_distance"],
                }
            )
        score = max(abs(item["log2_change_from_base"]) for item in endpoint_reports)
        entries.append(
            {
                "parameter": path,
                "impact_score_max_abs_log2_spacetime_change": score,
                "endpoints": endpoint_reports,
            }
        )
    entries.sort(
        key=lambda item: item["impact_score_max_abs_log2_spacetime_change"],
        reverse=True,
    )
    return {
        "schema_version": 1,
        "metric": "physical qubit-seconds",
        "method": "one parameter at a time over explicitly configured endpoints",
        "base_spacetime_qubit_seconds": base_metric,
        "ranking": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cost-report", type=Path)
    parser.add_argument("--ranges", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        base_config = json.loads(
            (CODE_DIR / "configs" / "illustrative_surface_code.json").read_text(
                encoding="utf-8"
            )
        )
        counters = {
            "n_bits": 12.0,
            "query_count": 100.0,
            "combination_attempts": 200.0,
            "list_size": 64.0,
            "trial_count": 1.0,
        }
        ranges = {"surface_code.code_cycle_seconds": [2e-7, 2e-6]}
    else:
        if args.cost_report is None or args.ranges is None:
            parser.error("--cost-report and --ranges are required unless --smoke is used")
        cost_report = json.loads(args.cost_report.read_text(encoding="utf-8"))
        counters = cost_report["sieve_counters"]
        base_config = cost_report["assumptions"]
        ranges = json.loads(args.ranges.read_text(encoding="utf-8"))
    report = analyze(counters, base_config, ranges)
    n_bits = int(counters["n_bits"])
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / (
                f"sensitivity_smoke_{date.today():%Y%m%d}.json"
                if args.smoke
                else f"sensitivity_n{n_bits}_{date.today():%Y%m%d}.json"
            )
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "most_influential_parameter": report["ranking"][0]["parameter"],
        "impact_score": report["ranking"][0]["impact_score_max_abs_log2_spacetime_change"],
    }, sort_keys=True))
    print(output)


if __name__ == "__main__":
    main()
