"""
cost_model.py — map sieve counters to a named surface-code cost model.
Sub-goal: P3.2 / SG-04
Inputs:   --sieve-csv <CSV> --n-bits <int> --config <JSON>
Outputs:  data/cost_model_n<N>_<CONFIG>_<YYYYMMDD>.json
Runtime:  under 1 second for one scenario
Validated against: distance inequality and monotonicity unit tests
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from copy import deepcopy
from datetime import date
from pathlib import Path
from statistics import fmean
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("configuration must be a JSON object")
    return value


def load_sieve_counters(path: Path, n_bits: int) -> dict[str, float]:
    """Return geometric-mean work counters for one simulated size."""
    rows = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["n_bits"]) == n_bits:
                rows.append(row)
    if not rows:
        raise ValueError(f"no sieve rows found for n_bits={n_bits}")

    def geometric_mean(field: str) -> float:
        return math.exp(fmean(math.log(float(row[field])) for row in rows))

    list_sizes = {int(row["list_size"]) for row in rows}
    if len(list_sizes) != 1:
        raise ValueError("sieve rows disagree on list_size")
    return {
        "n_bits": float(n_bits),
        "query_count": geometric_mean("query_count"),
        "combination_attempts": geometric_mean("combination_attempts"),
        "list_size": float(list_sizes.pop()),
        "trial_count": float(len(rows)),
    }


def logical_error_rate(distance: int, model: dict[str, float]) -> float:
    """Evaluate the configured phenomenological suppression formula."""
    ratio = model["physical_error_rate"] / model["threshold_error_rate"]
    return model["logical_error_prefactor"] * ratio ** ((distance + 1) / 2)


def choose_code_distance(fault_locations: float, model: dict[str, float]) -> int:
    """Choose the least allowed odd distance satisfying the union-bound budget."""
    if fault_locations <= 0:
        raise ValueError("fault_locations must be positive")
    if not 0 < model["physical_error_rate"] < model["threshold_error_rate"]:
        raise ValueError("physical_error_rate must lie strictly between zero and threshold")
    target = model["failure_budget"] / fault_locations
    distance = int(model["minimum_code_distance"])
    if distance < 1:
        raise ValueError("minimum_code_distance must be positive")
    if distance % 2 == 0:
        distance += 1
    while logical_error_rate(distance, model) > target:
        distance += 2
    return distance


def calculate_cost(
    counters: dict[str, float],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Calculate logical counts and physical resources without hidden defaults."""
    operation = config["operation_costs"]
    architecture = config["logical_architecture"]
    surface = config["surface_code"]
    query_count = counters["query_count"]
    combinations = counters["combination_attempts"]
    list_size = counters["list_size"]

    total_t = (
        query_count * operation["oracle_t_gates"]
        + combinations * operation["combination_t_gates"]
    )
    total_clifford = (
        query_count * operation["oracle_clifford_gates"]
        + combinations * operation["combination_clifford_gates"]
    )
    total_measurements = (
        query_count * operation["oracle_measurements"]
        + combinations * operation["combination_measurements"]
    )
    serial_logical_depth = (
        query_count * operation["oracle_logical_depth"]
        + combinations * operation["combination_logical_depth"]
    )
    parallel_workers = architecture["parallel_workers"]
    utilization = architecture["average_parallel_utilization"]
    if parallel_workers <= 0 or not 0 < utilization <= 1:
        raise ValueError("parallel_workers must be positive and utilization must be in (0, 1]")
    logical_depth = serial_logical_depth / (parallel_workers * utilization)

    data_logical_qubits = (
        architecture["base_logical_qubits"]
        + list_size * architecture["phase_state_logical_qubits"]
        + parallel_workers * architecture["oracle_workspace_logical_qubits_per_worker"]
    )
    gate_locations = total_t + total_clifford + total_measurements
    memory_locations = data_logical_qubits * logical_depth
    fault_locations = gate_locations + memory_locations
    distance = choose_code_distance(fault_locations, surface)
    achieved_logical_error = logical_error_rate(distance, surface)

    physical_data_qubits = (
        data_logical_qubits * surface["data_physical_qubits_per_d2"] * distance**2
    )
    physical_factory_qubits = (
        architecture["magic_factory_count"]
        * surface["factory_physical_qubits_per_d2"]
        * distance**2
    )
    physical_qubits = physical_data_qubits + physical_factory_qubits
    algorithm_code_cycles = (
        logical_depth
        * surface["code_cycles_per_logical_layer_per_distance"]
        * distance
    )
    factory_count = architecture["magic_factory_count"]
    factory_rate = surface["t_states_per_factory_per_code_cycle"]
    if factory_count <= 0 or factory_rate <= 0:
        raise ValueError("magic factory count and T-state production rate must be positive")
    magic_factory_code_cycles = total_t / (factory_count * factory_rate)
    code_cycles = max(algorithm_code_cycles, magic_factory_code_cycles)
    runtime_bottleneck = (
        "logical_depth"
        if algorithm_code_cycles >= magic_factory_code_cycles
        else "magic_state_factories"
    )
    runtime_seconds = code_cycles * surface["code_cycle_seconds"]
    spacetime_qubit_seconds = physical_qubits * runtime_seconds
    energy_joules = (
        spacetime_qubit_seconds * surface["watts_per_active_physical_qubit"]
    )

    return {
        "schema_version": 1,
        "model_name": config["model_name"],
        "model_status": config["model_status"],
        "sieve_counters": deepcopy(counters),
        "assumptions": deepcopy(config),
        "logical_resources": {
            "t_gates": total_t,
            "clifford_gates": total_clifford,
            "measurements": total_measurements,
            "serial_logical_depth": serial_logical_depth,
            "parallel_logical_depth": logical_depth,
            "data_logical_qubits": data_logical_qubits,
            "fault_locations_union_bound": fault_locations,
            "abstract_query_security_bits": math.log2(query_count),
            "quantum_accessible_classical_memory_bits": architecture[
                "quantum_accessible_classical_memory_bits"
            ],
        },
        "physical_resources": {
            "code_distance": distance,
            "logical_error_per_location": achieved_logical_error,
            "logical_error_target_per_location": surface["failure_budget"] / fault_locations,
            "physical_data_qubits": physical_data_qubits,
            "physical_factory_qubits": physical_factory_qubits,
            "physical_qubits": physical_qubits,
            "algorithm_code_cycles": algorithm_code_cycles,
            "magic_factory_code_cycles": magic_factory_code_cycles,
            "code_cycles": code_cycles,
            "runtime_bottleneck": runtime_bottleneck,
            "runtime_seconds": runtime_seconds,
            "spacetime_qubit_seconds": spacetime_qubit_seconds,
            "energy_joules": energy_joules,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--sieve-csv", type=Path)
    inputs.add_argument("--counters-json", type=Path)
    inputs.add_argument("--smoke", action="store_true")
    parser.add_argument("--n-bits", type=int)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.smoke:
        if args.n_bits is not None:
            parser.error("--n-bits is not used with --smoke")
        counters = {
            "n_bits": 12.0,
            "query_count": 100.0,
            "combination_attempts": 200.0,
            "list_size": 64.0,
            "trial_count": 1.0,
        }
        config_path = (
            Path(__file__).resolve().parent
            / "configs"
            / "illustrative_surface_code.json"
        )
    elif args.sieve_csv is not None:
        if args.n_bits is None:
            parser.error("--n-bits is required with --sieve-csv")
        counters = load_sieve_counters(args.sieve_csv, args.n_bits)
    else:
        if args.n_bits is not None:
            parser.error("--n-bits is only used with --sieve-csv")
        counters = load_json(args.counters_json)
        config_path = args.config
    if not args.smoke:
        if args.config is None:
            parser.error("--config is required unless --smoke is used")
        config_path = args.config
    config = load_json(config_path)
    report = calculate_cost(counters, config)
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"cost_model_n{int(counters['n_bits'])}_{config_path.stem}_{date.today():%Y%m%d}.json"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "query_security_bits": report["logical_resources"]["abstract_query_security_bits"],
        "logical_t_gate_log2": math.log2(report["logical_resources"]["t_gates"]),
        "code_distance": report["physical_resources"]["code_distance"],
        "physical_qubits": report["physical_resources"]["physical_qubits"],
        "runtime_seconds": report["physical_resources"]["runtime_seconds"],
    }
    print(json.dumps(summary, sort_keys=True))
    print(output)


if __name__ == "__main__":
    main()
