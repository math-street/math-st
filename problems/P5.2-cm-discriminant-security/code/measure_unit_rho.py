"""
measure_unit_rho.py — Measure Pollard-rho work with explicit CM unit orbits.
Sub-goal: P5.2 / SG-01a, SG-02a, SG-03a, SG-04a
Inputs:   --bits <comma-list> --trials <int> --seed <int>
Outputs:  data/measure_unit_rho_<params>_<date>_{raw,summary,residuals}.csv
Runtime:  about 1 minute at bits=12,14,16,18 and trials=200
Validated against: exhaustive and independent BSGS point counts; known DLPs
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import sys
import time
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

CODE_DIR = Path(__file__).resolve().parent
PROBLEM_DIR = CODE_DIR.parent
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from cm_units import CMCase, construct_cm_pair, unit_automorphism, validate_cm_case
from lib.dlog import PollardRhoResult, pollard_rho_orbits


def percentile(values: list[float], probability: float) -> float:
    """Return a linearly interpolated sample percentile."""

    if not values:
        raise ValueError("percentile requires at least one value")
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0, 1]")
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def bootstrap_ratio(
    baseline: list[int],
    quotient: list[int],
    *,
    rng: random.Random,
    resamples: int,
) -> tuple[float, float, float]:
    """Estimate the ratio of mean transition counts with a paired bootstrap."""

    if len(baseline) != len(quotient) or not baseline:
        raise ValueError("paired nonempty samples are required")
    ratios: list[float] = []
    sample_count = len(baseline)
    for _ in range(resamples):
        indices = [rng.randrange(sample_count) for _ in range(sample_count)]
        baseline_mean = statistics.fmean(baseline[index] for index in indices)
        quotient_mean = statistics.fmean(quotient[index] for index in indices)
        ratios.append(baseline_mean / quotient_mean)
    point_estimate = statistics.fmean(baseline) / statistics.fmean(quotient)
    return point_estimate, percentile(ratios, 0.025), percentile(ratios, 0.975)


def ols_slope(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Return intercept and slope for ordinary least squares."""

    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("at least two paired observations are required")
    x_mean = statistics.fmean(xs)
    y_mean = statistics.fmean(ys)
    denominator = sum((value - x_mean) ** 2 for value in xs)
    if denominator == 0:
        raise ValueError("regression inputs have zero variance")
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    return y_mean - slope * x_mean, slope


def run_walk(
    case: CMCase,
    secret: int,
    *,
    seed: int,
    quotient: bool,
    partitions: int,
    max_restarts: int,
    cycle_escape: bool,
    collision_table: bool,
) -> PollardRhoResult:
    """Run one validated baseline or quotient DLP trial."""

    target = case.curve.scalar_mul(secret, case.generator, charge=False)
    if quotient:
        result = pollard_rho_orbits(
            case.curve,
            case.generator,
            target,
            case.subgroup_order,
            automorphism=lambda point: unit_automorphism(case, point),
            automorphism_scalar=case.automorphism_scalar,
            automorphism_order=case.automorphism_order,
            seed=seed,
            partitions=partitions,
            max_restarts=max_restarts,
            cycle_escape=cycle_escape,
            collision_table=collision_table,
        )
    else:
        result = pollard_rho_orbits(
            case.curve,
            case.generator,
            target,
            case.subgroup_order,
            seed=seed,
            partitions=partitions,
            max_restarts=max_restarts,
            cycle_escape=cycle_escape,
            collision_table=collision_table,
        )
    if result.logarithm != secret:
        raise ArithmeticError("rho returned the wrong logarithm")
    return result


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    """Write deterministic CSV output with an explicit schema."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize(
    rows: list[dict[str, Any]],
    *,
    bootstrap_seed: int,
    bootstrap_resamples: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Build group summaries, log-log residuals, and fit metadata."""

    grouped: dict[tuple[int, int], dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: {"baseline": [], "quotient": []}
    )
    for row in rows:
        grouped[(int(row["bits"]), int(row["discriminant"]))][str(row["walk"])].append(row)

    rng = random.Random(bootstrap_seed)
    summary_rows: list[dict[str, Any]] = []
    samples_for_fit: dict[int, list[tuple[int, int, list[int], list[int]]]] = defaultdict(list)
    for (bits, discriminant), walks in sorted(grouped.items()):
        baseline_rows = sorted(walks["baseline"], key=lambda row: int(row["trial"]))
        quotient_rows = sorted(walks["quotient"], key=lambda row: int(row["trial"]))
        baseline = [int(row["transitions"]) for row in baseline_rows]
        quotient = [int(row["transitions"]) for row in quotient_rows]
        ratio, ci_low, ci_high = bootstrap_ratio(
            baseline,
            quotient,
            rng=rng,
            resamples=bootstrap_resamples,
        )
        subgroup_order = int(baseline_rows[0]["subgroup_order"])
        orbit_order = int(baseline_rows[0]["automorphism_order"])
        summary_rows.append(
            {
                "bits": bits,
                "discriminant": discriminant,
                "p": baseline_rows[0]["p"],
                "subgroup_order": subgroup_order,
                "subgroup_bits": subgroup_order.bit_length(),
                "automorphism_order": orbit_order,
                "trials": len(baseline),
                "mean_baseline_transitions": f"{statistics.fmean(baseline):.6f}",
                "mean_quotient_transitions": f"{statistics.fmean(quotient):.6f}",
                "median_baseline_transitions": f"{statistics.median(baseline):.6f}",
                "median_quotient_transitions": f"{statistics.median(quotient):.6f}",
                "speedup_ratio_of_means": f"{ratio:.9f}",
                "speedup_ci95_low": f"{ci_low:.9f}",
                "speedup_ci95_high": f"{ci_high:.9f}",
                "sqrt_orbit_order": f"{math.sqrt(orbit_order):.9f}",
                "mean_baseline_restarts": f"{statistics.fmean(int(row['restarts']) for row in baseline_rows):.6f}",
                "mean_quotient_restarts": f"{statistics.fmean(int(row['restarts']) for row in quotient_rows):.6f}",
                "mean_quotient_cycle_escapes": f"{statistics.fmean(int(row['cycle_escapes']) for row in quotient_rows):.6f}",
            }
        )
        samples_for_fit[discriminant].append((bits, subgroup_order, baseline, quotient))

    fit_output: dict[str, Any] = {}
    residual_rows: list[dict[str, Any]] = []
    for discriminant, groups in sorted(samples_for_fit.items()):
        groups.sort()
        xs = [math.log(group[1]) for group in groups]
        ratios = [statistics.fmean(group[2]) / statistics.fmean(group[3]) for group in groups]
        ys = [math.log(ratio) for ratio in ratios]
        intercept, slope = ols_slope(xs, ys)

        bootstrap_slopes: list[float] = []
        for _ in range(bootstrap_resamples):
            sampled_ratios: list[float] = []
            for _, _, baseline, quotient in groups:
                indices = [rng.randrange(len(baseline)) for _ in range(len(baseline))]
                sampled_ratios.append(
                    statistics.fmean(baseline[index] for index in indices)
                    / statistics.fmean(quotient[index] for index in indices)
                )
            _, sampled_slope = ols_slope(xs, [math.log(value) for value in sampled_ratios])
            bootstrap_slopes.append(sampled_slope)

        fit_output[str(discriminant)] = {
            "model": "log(speedup_ratio_of_means) = intercept + slope * log(subgroup_order)",
            "group_count": len(groups),
            "intercept": intercept,
            "slope": slope,
            "slope_ci95_low": percentile(bootstrap_slopes, 0.025),
            "slope_ci95_high": percentile(bootstrap_slopes, 0.975),
            "bootstrap_resamples": bootstrap_resamples,
        }
        for (bits, subgroup_order, _, _), observed in zip(groups, ys):
            fitted = intercept + slope * math.log(subgroup_order)
            residual_rows.append(
                {
                    "bits": bits,
                    "discriminant": discriminant,
                    "subgroup_order": subgroup_order,
                    "observed_log_speedup": f"{observed:.12f}",
                    "fitted_log_speedup": f"{fitted:.12f}",
                    "residual": f"{observed - fitted:.12f}",
                }
            )
    return summary_rows, residual_rows, fit_output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", default="12,14,16,18", help="comma-separated field sizes")
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=52022026)
    parser.add_argument("--partitions", type=int, default=20)
    parser.add_argument("--max-restarts", type=int, default=128)
    parser.add_argument("--cycle-escape", action="store_true")
    parser.add_argument("--collision-table", action="store_true")
    parser.add_argument("--bootstrap-resamples", type=int, default=2000)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if (
        args.trials < 1
        or args.partitions < 3
        or args.max_restarts < 1
        or args.bootstrap_resamples < 20
    ):
        raise ValueError("trials, partitions, or bootstrap resamples are too small")
    if args.cycle_escape and args.collision_table:
        raise ValueError("cycle escape and collision-table modes are mutually exclusive")
    bits_values = [int(value) for value in args.bits.split(",")]
    trials = args.trials
    bootstrap_resamples = args.bootstrap_resamples
    output_dir = PROBLEM_DIR / "data"
    if args.smoke:
        bits_values = [9, 10]
        trials = min(trials, 4)
        bootstrap_resamples = min(bootstrap_resamples, 100)
        output_dir /= "smoke"
    if len(bits_values) < 2:
        raise ValueError("at least two field sizes are required for the fit")

    started = time.perf_counter()
    raw_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []
    for bits in bits_values:
        threshold = max(5, bits - 2) if not args.smoke else 5
        cases = construct_cm_pair(bits, minimum_subgroup_bits=threshold)
        for case in cases:
            validation = validate_cm_case(case, samples=32, seed=args.seed + bits)
            validation_rows.append(
                {
                    "bits": bits,
                    "discriminant": case.discriminant,
                    "p": case.curve.p,
                    "a": case.curve.a,
                    "b": case.curve.b,
                    "group_order": case.group_order,
                    "subgroup_order": case.subgroup_order,
                    "cofactor": case.cofactor,
                    "field_unit": case.field_unit,
                    "automorphism_scalar": case.automorphism_scalar,
                    "automorphism_order": case.automorphism_order,
                    **validation,
                }
            )
            secret_rng = random.Random(args.seed + 1009 * bits - case.discriminant)
            for trial in range(trials):
                secret = secret_rng.randrange(1, case.subgroup_order)
                trial_seed = args.seed + 1_000_003 * bits + 10_007 * (-case.discriminant) + trial
                for walk in ("baseline", "quotient"):
                    try:
                        result = run_walk(
                            case,
                            secret,
                            seed=trial_seed,
                            quotient=walk == "quotient",
                            partitions=args.partitions,
                            max_restarts=args.max_restarts,
                            cycle_escape=args.cycle_escape,
                            collision_table=args.collision_table,
                        )
                    except RuntimeError as error:
                        raise RuntimeError(
                            f"walk failed at bits={bits}, D={case.discriminant}, "
                            f"trial={trial}, walk={walk}, seed={trial_seed}"
                        ) from error
                    raw_rows.append(
                        {
                            "bits": bits,
                            "discriminant": case.discriminant,
                            "p": case.curve.p,
                            "a": case.curve.a,
                            "b": case.curve.b,
                            "group_order": case.group_order,
                            "subgroup_order": case.subgroup_order,
                            "cofactor": case.cofactor,
                            "automorphism_order": case.automorphism_order,
                            "trial": trial,
                            "secret": secret,
                            "walk": walk,
                            "seed": trial_seed,
                            "logarithm": result.logarithm,
                            "iterations": result.iterations,
                            "transitions": result.transitions,
                            "collisions": result.collisions,
                            "restarts": result.restarts,
                            "orbit_applications": result.orbit_applications,
                            "cycle_escapes": result.cycle_escapes,
                        }
                    )

    summary_rows, residual_rows, fit_output = summarize(
        raw_rows,
        bootstrap_seed=args.seed ^ 0xC0FFEE,
        bootstrap_resamples=bootstrap_resamples,
    )
    elapsed = time.perf_counter() - started
    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(str(value) for value in bits_values)
    mode_label = "table" if args.collision_table else ("escape" if args.cycle_escape else "naive")
    stem = (
        f"measure_unit_rho_{mode_label}_r{args.partitions}_"
        f"b{bit_label}_t{trials}_s{args.seed}_{stamp}"
    )
    raw_path = output_dir / f"{stem}_raw.csv"
    summary_path = output_dir / f"{stem}_summary.csv"
    residual_path = output_dir / f"{stem}_residuals.csv"
    validation_path = output_dir / f"{stem}_validation.csv"
    fit_path = output_dir / f"{stem}_fit.json"

    write_csv(raw_path, raw_rows, list(raw_rows[0]))
    write_csv(summary_path, summary_rows, list(summary_rows[0]))
    write_csv(residual_path, residual_rows, list(residual_rows[0]))
    write_csv(validation_path, validation_rows, list(validation_rows[0]))
    fit_output["metadata"] = {
        "bits": bits_values,
        "trials_per_case": trials,
        "seed": args.seed,
        "partitions": args.partitions,
        "max_restarts": args.max_restarts,
        "cycle_escape": args.cycle_escape,
        "collision_table": args.collision_table,
        "elapsed_seconds": elapsed,
        "raw_path": str(raw_path.relative_to(PROBLEM_DIR)),
    }
    fit_path.write_text(json.dumps(fit_output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"raw={raw_path}")
    print(f"summary={summary_path}")
    print(f"fit={fit_path}")
    print(f"elapsed_seconds={elapsed:.3f}")


if __name__ == "__main__":
    main()
