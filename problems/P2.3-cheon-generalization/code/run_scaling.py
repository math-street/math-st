"""
run_scaling.py — measure Cheon's divisor-case quarter-power scaling.
Sub-goal: P2.3 / SG-02
Inputs:   --half-bits <csv> --trials <int> --seed <int> [--bootstrap <int>]
Outputs:  data/run_scaling_<params>_<date>.csv plus summary CSV and fit JSON
Runtime:  ~0.6 s on Python 3.13.4 for the default eight sizes and 41 trials
Validated against: exhaustive order-17 and order-19 known-answer tests
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.curves import is_prime  # noqa: E402

from cheon import OpaquePrimeOrderGroup, cheon_recover, primitive_root_mod_prime  # noqa: E402


def find_structured_prime(half_bits: int) -> tuple[int, int, int]:
    """Find prime n = d*e + 1 with d=2^half_bits and e near d."""

    if not 3 <= half_bits <= 29:
        raise ValueError("half_bits must keep the group order below the 60-bit ceiling")
    d = 1 << half_bits
    e = d + 1
    while True:
        order = d * e + 1
        if is_prime(order):
            return order, d, e
        e += 2


def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Return ordinary-least-squares intercept and slope."""

    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("a fit requires at least two paired observations")
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    denominator = sum((value - mean_x) ** 2 for value in xs)
    if denominator == 0:
        raise ValueError("fit x-values must not all be equal")
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denominator
    return mean_y - slope * mean_x, slope


def percentile(sorted_values: list[float], probability: float) -> float:
    """Return a linearly interpolated sample percentile."""

    position = probability * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def bootstrap_slope_ci(
    costs_by_order: dict[int, list[float]],
    *,
    repetitions: int,
    seed: int,
) -> tuple[float, float]:
    """Bootstrap trials within each size and return a percentile slope CI."""

    if repetitions < 100:
        raise ValueError("at least 100 bootstrap repetitions are required")
    rng = random.Random(seed)
    orders = sorted(costs_by_order)
    slopes: list[float] = []
    for _ in range(repetitions):
        medians = []
        for order in orders:
            costs = costs_by_order[order]
            resample = [costs[rng.randrange(len(costs))] for _ in costs]
            medians.append(statistics.median(resample))
        _, slope = linear_fit([math.log(order) for order in orders], [math.log(v) for v in medians])
        slopes.append(slope)
    slopes.sort()
    return percentile(slopes, 0.025), percentile(slopes, 0.975)


def parse_half_bits(value: str) -> list[int]:
    result = [int(item) for item in value.split(",") if item]
    if len(result) < 4:
        raise argparse.ArgumentTypeError("at least four sizes are required")
    if len(set(result)) != len(result):
        raise argparse.ArgumentTypeError("sizes must be distinct")
    return result


def run(args: argparse.Namespace) -> tuple[Path, Path, Path, dict[str, object]]:
    half_bits_values = [4, 5, 6, 7] if args.smoke else args.half_bits
    trials = 3 if args.smoke else args.trials
    bootstrap_repetitions = 100 if args.smoke else args.bootstrap
    rng = random.Random(args.seed)
    rows: list[dict[str, object]] = []

    for half_bits in half_bits_values:
        order, d, quotient = find_structured_prime(half_bits)
        primitive_root = primitive_root_mod_prime(order)
        for trial in range(trials):
            secret = rng.randrange(1, order)
            group = OpaquePrimeOrderGroup(order)
            gx = group.scalar_mul(secret, group.generator)
            gxd = group.scalar_mul(pow(secret, d, order), group.generator)
            group.reset_trace()
            started = perf_counter()
            recovered, stats = cheon_recover(
                group,
                group.generator,
                group.identity,
                gx,
                gxd,
                order,
                d,
                primitive_root=primitive_root,
            )
            elapsed = perf_counter() - started
            verified = recovered == secret
            if not verified:
                raise AssertionError(f"recovery failed for order={order}, d={d}, trial={trial}")
            if stats.scalar_multiplications != group.trace["oracle_scalar_multiplication"]:
                raise AssertionError("local and simulator scalar-multiplication counts diverged")
            assert stats.stage_one is not None and stats.stage_two is not None
            rows.append(
                {
                    "half_bits": half_bits,
                    "trial": trial,
                    "seed": args.seed,
                    "order": order,
                    "order_bits": order.bit_length(),
                    "d": d,
                    "quotient": quotient,
                    "primitive_root": primitive_root,
                    "secret": secret,
                    "recovered": recovered,
                    "verified": verified,
                    "stage1_width": stats.stage_one.width,
                    "stage2_width": stats.stage_two.width,
                    "stage1_probes": stats.stage_one.giant_probes,
                    "stage2_probes": stats.stage_two.giant_probes,
                    "scalar_multiplications": stats.scalar_multiplications,
                    "group_operations": group.trace["group_operation"],
                    "normalized_group_operations": group.trace["group_operation"] / order.bit_length(),
                    "theory_shape": math.sqrt(quotient) + math.sqrt(d),
                    "elapsed_seconds": elapsed,
                }
            )

    grouped: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["order"])].append(row)
    orders = sorted(grouped)
    median_scalar_calls = [
        statistics.median(float(row["scalar_multiplications"]) for row in grouped[order])
        for order in orders
    ]
    intercept, slope = linear_fit(
        [math.log(order) for order in orders],
        [math.log(value) for value in median_scalar_calls],
    )
    ci_low, ci_high = bootstrap_slope_ci(
        {
            order: [float(row["scalar_multiplications"]) for row in grouped[order]]
            for order in orders
        },
        repetitions=bootstrap_repetitions,
        seed=args.seed ^ 0xC4E0,
    )

    summary_rows: list[dict[str, object]] = []
    for order, median_calls in zip(orders, median_scalar_calls):
        size_rows = grouped[order]
        predicted_log = intercept + slope * math.log(order)
        summary_rows.append(
            {
                "half_bits": size_rows[0]["half_bits"],
                "order": order,
                "order_bits": size_rows[0]["order_bits"],
                "d": size_rows[0]["d"],
                "quotient": size_rows[0]["quotient"],
                "trials": len(size_rows),
                "median_scalar_multiplications": median_calls,
                "median_group_operations": statistics.median(
                    float(row["group_operations"]) for row in size_rows
                ),
                "median_normalized_group_operations": statistics.median(
                    float(row["normalized_group_operations"]) for row in size_rows
                ),
                "median_elapsed_seconds": statistics.median(
                    float(row["elapsed_seconds"]) for row in size_rows
                ),
                "theory_shape": size_rows[0]["theory_shape"],
                "fitted_scalar_multiplications": math.exp(predicted_log),
                "log_residual": math.log(median_calls) - predicted_log,
            }
        )

    fit = {
        "metric": "median scalar-multiplication calls",
        "sizes": len(orders),
        "trials_per_size": trials,
        "seed": args.seed,
        "bootstrap_repetitions": bootstrap_repetitions,
        "intercept": intercept,
        "slope": slope,
        "slope_ci_95": [ci_low, ci_high],
        "target_interval": [0.20, 0.30],
        "target_interval_intersects_ci": ci_high >= 0.20 and ci_low <= 0.30,
        "all_recoveries_verified": all(bool(row["verified"]) for row in rows),
    }

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    sizes_token = f"hb{min(half_bits_values)}-{max(half_bits_values)}"
    run_token = f"{sizes_token}_t{trials}_s{args.seed}_{date.today():%Y%m%d}"
    rows_path = output_dir / f"run_scaling_{run_token}.csv"
    summary_path = output_dir / f"run_scaling_summary_{run_token}.csv"
    fit_path = output_dir / f"run_scaling_fit_{run_token}.json"

    with rows_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)
    with fit_path.open("w", encoding="utf-8") as handle:
        json.dump(fit, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return rows_path, summary_path, fit_path, fit


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--half-bits",
        type=parse_half_bits,
        default=parse_half_bits("8,10,12,14,16,18,20,22"),
        help="comma-separated exponents m giving d=2^m (at least four)",
    )
    parser.add_argument("--trials", type=int, default=41)
    parser.add_argument("--seed", type=int, default=2303)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.trials < 1:
        raise ValueError("trials must be positive")
    rows_path, summary_path, fit_path, fit = run(args)
    print(rows_path)
    print(summary_path)
    print(fit_path)
    print(json.dumps(fit, sort_keys=True))


if __name__ == "__main__":
    main()
