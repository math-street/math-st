"""
measure_factor_bases.py — exact SG-01 and SG-03 toy measurements.
Sub-goal: P1.2 / SG-01 and SG-03
Inputs:   --bits 16 18 20 --targets <int> --replicates <int> --seed <int>
Outputs:  data/measure_factor_bases_<params>_<YYYYMMDD>_{raw,summary,comparison,scaling}.csv
Runtime:  measured by each run; intended to stay below the scaffold's 2^20 ceiling.
Validated against: exhaustive triple enumeration on E/F_17 and f4 vanishing tests.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve, find_prime_order_curve, points_from_scalars, prime_below_power_of_two
from lib.semaev import f4_value


RAW_FIELDS = (
    "date",
    "seed",
    "bits",
    "p",
    "a",
    "b",
    "r",
    "trace",
    "curve_attempts",
    "curve_search_s",
    "base_kind",
    "base_rep",
    "base_id",
    "base_size",
    "x_bound",
    "target_rep",
    "target_scalar",
    "decomposition_count",
    "expected_count",
    "normalized_count",
    "pair_checks",
    "search_found",
    "search_s",
    "pair_table_build_s",
    "f4_verified",
)

SUMMARY_FIELDS = (
    "bits",
    "p",
    "r",
    "a",
    "b",
    "base_kind",
    "base_size",
    "base_instances",
    "targets",
    "mean_decompositions",
    "decomp_ci_low",
    "decomp_ci_high",
    "expected_decompositions",
    "normalized_mean",
    "normalized_ci_low",
    "normalized_ci_high",
    "mean_pair_checks",
    "pair_checks_ci_low",
    "pair_checks_ci_high",
    "success_rate",
    "success_ci_low",
    "success_ci_high",
    "mean_search_ms",
    "mean_pair_table_build_s",
    "ci_method",
)

COMPARISON_FIELDS = (
    "bits",
    "p",
    "candidate_kind",
    "baseline_kind",
    "candidate_size",
    "baseline_size",
    "normalized_count_ratio",
    "normalized_count_ratio_ci_low",
    "normalized_count_ratio_ci_high",
    "pair_checks_ratio",
    "pair_checks_ratio_ci_low",
    "pair_checks_ratio_ci_high",
    "bootstrap_samples",
)

SCALING_FIELDS = (
    "base_kind",
    "points",
    "p_min",
    "p_max",
    "log_log_slope",
    "log_intercept",
    "bits",
    "p",
    "observed_mean_pair_checks",
    "fitted_mean_pair_checks",
    "log_residual",
)


def pair_sum_counts(curve: Curve, factor_base: Sequence[AffinePoint]) -> tuple[Counter[AffinePoint], float]:
    """Build ordered-pair sum multiplicities, exploiting P+Q = Q+P."""
    started = time.perf_counter()
    counts: Counter[AffinePoint] = Counter()
    for left_index, left in enumerate(factor_base):
        for right_index in range(left_index, len(factor_base)):
            total = curve.add(left, factor_base[right_index])
            counts[total] += 1 if left_index == right_index else 2
    return counts, time.perf_counter() - started


def decomposition_count(
    curve: Curve,
    factor_base: Sequence[AffinePoint],
    pair_counts: Counter[AffinePoint],
    target: AffinePoint,
) -> int:
    """Count ordered triples (P,Q,T) from the base with P+Q+T=target."""
    return sum(pair_counts[curve.add(target, curve.neg(point))] for point in factor_base)


def find_first_decomposition(
    curve: Curve, factor_base: Sequence[AffinePoint], target: AffinePoint
) -> tuple[int, tuple[AffinePoint, AffinePoint, AffinePoint] | None, float]:
    """Lexicographically scan ordered pairs and test the required third point."""
    membership = set(factor_base)
    checked = 0
    started = time.perf_counter()
    for left in factor_base:
        for right in factor_base:
            checked += 1
            pair_sum = curve.add(left, right)
            needed = curve.add(target, curve.neg(pair_sum))
            if needed in membership:
                return checked, (left, right, needed), time.perf_counter() - started
    return checked, None, time.perf_counter() - started


def integer_x_factor_base(curve: Curve, bound: int) -> list[AffinePoint]:
    """Enumerate F = {P: P affine and 0 <= x(P) < bound}."""
    return list(curve.affine_points(bound))


def _verify_decomposition(
    curve: Curve,
    triple: tuple[AffinePoint, AffinePoint, AffinePoint] | None,
    target: AffinePoint,
) -> int:
    if triple is None:
        return 0
    left, right, third = triple
    if curve.add(curve.add(left, right), third) != target:
        raise ArithmeticError("reported decomposition does not sum to the target")
    if None in triple or target is None:
        return 0
    assert left is not None and right is not None and third is not None and target is not None
    if f4_value(left[0], right[0], third[0], target[0], curve.a, curve.b, curve.p) != 0:
        raise ArithmeticError("f4 did not vanish on a verified decomposition")
    return 1


def measure_base(
    *,
    curve: Curve,
    order: int,
    bits: int,
    curve_attempts: int,
    curve_search_s: float,
    seed: int,
    kind: str,
    base_rep: int,
    factor_base: Sequence[AffinePoint],
    target_scalars: Sequence[int],
    generator: AffinePoint,
    x_bound: int,
) -> list[dict[str, Any]]:
    pair_counts, build_s = pair_sum_counts(curve, factor_base)
    if sum(pair_counts.values()) != len(factor_base) ** 2:
        raise ArithmeticError("pair table lost ordered pairs")
    expected = len(factor_base) ** 3 / order
    rows: list[dict[str, Any]] = []
    for target_rep, scalar in enumerate(target_scalars):
        target = curve.scalar_mul(scalar, generator)
        count = decomposition_count(curve, factor_base, pair_counts, target)
        checks, triple, search_s = find_first_decomposition(curve, factor_base, target)
        if (triple is not None) != (count > 0):
            raise ArithmeticError("search result disagrees with the exact count")
        f4_verified = _verify_decomposition(curve, triple, target)
        rows.append(
            {
                "date": date.today().isoformat(),
                "seed": seed,
                "bits": bits,
                "p": curve.p,
                "a": curve.a,
                "b": curve.b,
                "r": order,
                "trace": curve.p + 1 - order,
                "curve_attempts": curve_attempts,
                "curve_search_s": f"{curve_search_s:.9f}",
                "base_kind": kind,
                "base_rep": base_rep,
                "base_id": f"{bits}:{kind}:{base_rep}",
                "base_size": len(factor_base),
                "x_bound": x_bound,
                "target_rep": target_rep,
                "target_scalar": scalar,
                "decomposition_count": count,
                "expected_count": f"{expected:.12g}",
                "normalized_count": f"{count / expected:.12g}",
                "pair_checks": checks,
                "search_found": int(triple is not None),
                "search_s": f"{search_s:.9f}",
                "pair_table_build_s": f"{build_s:.9f}",
                "f4_verified": f4_verified,
            }
        )
    return rows


def _percentile(samples: Sequence[float], probability: float) -> float:
    ordered = sorted(samples)
    position = probability * (len(ordered) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _hierarchical_bootstrap(
    rows: Sequence[dict[str, Any]],
    field: str,
    rng: random.Random,
    samples: int,
) -> list[float]:
    clusters: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        clusters[str(row["base_id"])].append(float(row[field]))
    cluster_values = list(clusters.values())
    bootstrapped: list[float] = []
    for _ in range(samples):
        values: list[float] = []
        for _ in cluster_values:
            selected = rng.choice(cluster_values)
            values.extend(rng.choice(selected) for _ in selected)
        bootstrapped.append(statistics.fmean(values))
    return bootstrapped


def _wilson(successes: int, total: int) -> tuple[float, float]:
    z = 1.959963984540054
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    half = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / denominator
    return center - half, center + half


def summarize_rows(
    rows: Sequence[dict[str, Any]], seed: int, bootstrap_samples: int
) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["bits"]), str(row["base_kind"]))].append(row)
    summaries: list[dict[str, Any]] = []
    for group_index, ((bits, kind), group) in enumerate(sorted(grouped.items())):
        decomposition_boot = _hierarchical_bootstrap(
            group, "decomposition_count", random.Random(seed + group_index * 3 + 1), bootstrap_samples
        )
        normalized_boot = _hierarchical_bootstrap(
            group, "normalized_count", random.Random(seed + group_index * 3 + 2), bootstrap_samples
        )
        checks_boot = _hierarchical_bootstrap(
            group, "pair_checks", random.Random(seed + group_index * 3 + 3), bootstrap_samples
        )
        successes = sum(int(row["search_found"]) for row in group)
        success_low, success_high = _wilson(successes, len(group))
        first = group[0]
        base_sizes = {int(row["base_size"]) for row in group}
        if len(base_sizes) != 1:
            raise ArithmeticError("base size changed within a summary group")
        summaries.append(
            {
                "bits": bits,
                "p": first["p"],
                "r": first["r"],
                "a": first["a"],
                "b": first["b"],
                "base_kind": kind,
                "base_size": first["base_size"],
                "base_instances": len({row["base_id"] for row in group}),
                "targets": len(group),
                "mean_decompositions": f"{statistics.fmean(float(row['decomposition_count']) for row in group):.9g}",
                "decomp_ci_low": f"{_percentile(decomposition_boot, 0.025):.9g}",
                "decomp_ci_high": f"{_percentile(decomposition_boot, 0.975):.9g}",
                "expected_decompositions": first["expected_count"],
                "normalized_mean": f"{statistics.fmean(float(row['normalized_count']) for row in group):.9g}",
                "normalized_ci_low": f"{_percentile(normalized_boot, 0.025):.9g}",
                "normalized_ci_high": f"{_percentile(normalized_boot, 0.975):.9g}",
                "mean_pair_checks": f"{statistics.fmean(float(row['pair_checks']) for row in group):.9g}",
                "pair_checks_ci_low": f"{_percentile(checks_boot, 0.025):.9g}",
                "pair_checks_ci_high": f"{_percentile(checks_boot, 0.975):.9g}",
                "success_rate": f"{successes / len(group):.9g}",
                "success_ci_low": f"{success_low:.9g}",
                "success_ci_high": f"{success_high:.9g}",
                "mean_search_ms": f"{1000 * statistics.fmean(float(row['search_s']) for row in group):.9g}",
                "mean_pair_table_build_s": f"{statistics.fmean(float(row['pair_table_build_s']) for row in group):.9g}",
                "ci_method": f"hierarchical percentile bootstrap ({bootstrap_samples}); Wilson for success",
            }
        )
    return summaries


def compare_candidate(
    rows: Sequence[dict[str, Any]], seed: int, bootstrap_samples: int
) -> list[dict[str, Any]]:
    comparisons: list[dict[str, Any]] = []
    for bits in sorted({int(row["bits"]) for row in rows}):
        candidate = [row for row in rows if int(row["bits"]) == bits and row["base_kind"] == "integer_x"]
        baseline = [row for row in rows if int(row["bits"]) == bits and row["base_kind"] == "random_matched"]
        candidate_norm = _hierarchical_bootstrap(candidate, "normalized_count", random.Random(seed + bits * 11), bootstrap_samples)
        baseline_norm = _hierarchical_bootstrap(baseline, "normalized_count", random.Random(seed + bits * 13), bootstrap_samples)
        candidate_checks = _hierarchical_bootstrap(candidate, "pair_checks", random.Random(seed + bits * 17), bootstrap_samples)
        baseline_checks = _hierarchical_bootstrap(baseline, "pair_checks", random.Random(seed + bits * 19), bootstrap_samples)
        norm_ratios = [left / right for left, right in zip(candidate_norm, baseline_norm) if right]
        check_ratios = [left / right for left, right in zip(candidate_checks, baseline_checks) if right]
        candidate_norm_mean = statistics.fmean(float(row["normalized_count"]) for row in candidate)
        baseline_norm_mean = statistics.fmean(float(row["normalized_count"]) for row in baseline)
        candidate_check_mean = statistics.fmean(float(row["pair_checks"]) for row in candidate)
        baseline_check_mean = statistics.fmean(float(row["pair_checks"]) for row in baseline)
        comparisons.append(
            {
                "bits": bits,
                "p": candidate[0]["p"],
                "candidate_kind": "integer_x",
                "baseline_kind": "random_matched",
                "candidate_size": candidate[0]["base_size"],
                "baseline_size": baseline[0]["base_size"],
                "normalized_count_ratio": f"{candidate_norm_mean / baseline_norm_mean:.9g}",
                "normalized_count_ratio_ci_low": f"{_percentile(norm_ratios, 0.025):.9g}",
                "normalized_count_ratio_ci_high": f"{_percentile(norm_ratios, 0.975):.9g}",
                "pair_checks_ratio": f"{candidate_check_mean / baseline_check_mean:.9g}",
                "pair_checks_ratio_ci_low": f"{_percentile(check_ratios, 0.025):.9g}",
                "pair_checks_ratio_ci_high": f"{_percentile(check_ratios, 0.975):.9g}",
                "bootstrap_samples": bootstrap_samples,
            }
        )
    return comparisons


def fit_scaling(summaries: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Fit log(mean pair checks) against log(p) and retain every residual."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in summaries:
        grouped[str(row["base_kind"])].append(row)
    fit_rows: list[dict[str, Any]] = []
    for kind, group in sorted(grouped.items()):
        ordered = sorted(group, key=lambda row: int(row["p"]))
        if len(ordered) < 3:
            continue
        x_values = [math.log(float(row["p"])) for row in ordered]
        y_values = [math.log(float(row["mean_pair_checks"])) for row in ordered]
        x_mean = statistics.fmean(x_values)
        y_mean = statistics.fmean(y_values)
        denominator = sum((value - x_mean) ** 2 for value in x_values)
        slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values)) / denominator
        intercept = y_mean - slope * x_mean
        for row, x_value, y_value in zip(ordered, x_values, y_values):
            fitted_log = intercept + slope * x_value
            fit_rows.append(
                {
                    "base_kind": kind,
                    "points": len(ordered),
                    "p_min": ordered[0]["p"],
                    "p_max": ordered[-1]["p"],
                    "log_log_slope": f"{slope:.12g}",
                    "log_intercept": f"{intercept:.12g}",
                    "bits": row["bits"],
                    "p": row["p"],
                    "observed_mean_pair_checks": row["mean_pair_checks"],
                    "fitted_mean_pair_checks": f"{math.exp(fitted_log):.12g}",
                    "log_residual": f"{y_value - fitted_log:.12g}",
                }
            )
    return fit_rows


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(
    bits_values: Sequence[int],
    targets: int,
    replicates: int,
    seed: int,
) -> list[dict[str, Any]]:
    all_rows: list[dict[str, Any]] = []
    for bits in bits_values:
        p = prime_below_power_of_two(bits)
        curve_rng = random.Random(seed + bits * 1_000_003)
        curve_started = time.perf_counter()
        curve, order, attempts = find_prime_order_curve(p, curve_rng)
        curve_search_s = time.perf_counter() - curve_started
        trace = p + 1 - order
        if trace % p == 0:
            raise ArithmeticError("selected curve is not ordinary")
        generator = curve.first_affine_point()
        if curve.scalar_mul(order, generator) is not None:
            raise ArithmeticError("selected point does not have the prime group order")

        x_bound = math.isqrt(p)
        candidate = integer_x_factor_base(curve, x_bound)
        sqrt_size = math.isqrt(p)
        if not candidate:
            raise ArithmeticError("integer-x factor base is empty")
        target_rng = random.Random(seed + bits * 2_000_003)
        target_scalars = [target_rng.randrange(order) for _ in range(targets)]

        configurations: list[tuple[str, int, list[AffinePoint]]] = [("integer_x", 0, candidate)]
        for kind, size, offset in (
            ("random_sqrt", sqrt_size, 3_000_001),
            ("random_matched", len(candidate), 5_000_011),
        ):
            for base_rep in range(replicates):
                base_rng = random.Random(seed + bits * offset + base_rep * 97)
                scalars = base_rng.sample(range(order), size)
                factor_base = points_from_scalars(curve, generator, scalars)
                configurations.append((kind, base_rep, factor_base))

        for kind, base_rep, factor_base in configurations:
            print(
                f"bits={bits} p={p} curve=({curve.a},{curve.b}) r={order} "
                f"base={kind}:{base_rep} size={len(factor_base)}",
                flush=True,
            )
            all_rows.extend(
                measure_base(
                    curve=curve,
                    order=order,
                    bits=bits,
                    curve_attempts=attempts,
                    curve_search_s=curve_search_s,
                    seed=seed,
                    kind=kind,
                    base_rep=base_rep,
                    factor_base=factor_base,
                    target_scalars=target_scalars,
                    generator=generator,
                    x_bound=x_bound,
                )
            )
    return all_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", nargs="+", type=int, default=[16, 18, 20])
    parser.add_argument("--targets", type=int, default=96)
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=12022026)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-prefix", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bits_values = [10] if args.smoke else args.bits
    targets = 8 if args.smoke else args.targets
    replicates = 1 if args.smoke else args.replicates
    bootstrap_samples = 200 if args.smoke else args.bootstrap
    started = time.perf_counter()
    rows = run_experiment(bits_values, targets, replicates, args.seed)
    summaries = summarize_rows(rows, args.seed, bootstrap_samples)
    comparisons = compare_candidate(rows, args.seed, bootstrap_samples)
    scaling = fit_scaling(summaries)
    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(str(bits) for bits in bits_values)
    default_prefix = Path(__file__).resolve().parents[1] / "data" / (
        f"measure_factor_bases_b{bit_label}_t{targets}_r{replicates}_s{args.seed}_{stamp}"
    )
    prefix = args.output_prefix or default_prefix
    write_csv(Path(f"{prefix}_raw.csv"), RAW_FIELDS, rows)
    write_csv(Path(f"{prefix}_summary.csv"), SUMMARY_FIELDS, summaries)
    write_csv(Path(f"{prefix}_comparison.csv"), COMPARISON_FIELDS, comparisons)
    write_csv(Path(f"{prefix}_scaling.csv"), SCALING_FIELDS, scaling)
    print(f"rows={len(rows)} elapsed_s={time.perf_counter() - started:.3f}")
    print(f"output_prefix={prefix}")


if __name__ == "__main__":
    main()
