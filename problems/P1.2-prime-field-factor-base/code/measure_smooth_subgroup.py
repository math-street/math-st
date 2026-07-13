"""
measure_smooth_subgroup.py — Candidate E over a smooth p-1 subgroup.
Sub-goal: P1.2 / SG-11
Inputs:   --p, --subgroup-order, --targets, --replicates, --bootstrap, --seed
Outputs:  data/measure_smooth_subgroup_<params>_<date>_{audit,raw,summary,comparison}.csv
Runtime:  under 10 s at the default p=65537, 96-target fixture
Validated against: exhaustive field and curve membership plus direct power tests

The default fixture uses p=65537 and the order-64 multiplicative subgroup,
whose membership equation x^64=1 decomposes into six quadratic squaring
constraints. Exact three-term counts and generic pair-scan work are compared
with size-matched random factor bases.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve, find_prime_order_curve, points_from_scalars
from measure_factor_bases import (
    SUMMARY_FIELDS,
    _hierarchical_bootstrap,
    _percentile,
    _verify_decomposition,
    decomposition_count,
    find_first_decomposition,
    pair_sum_counts,
    summarize_rows,
)


RAW_FIELDS = (
    "date",
    "seed",
    "bits",
    "p",
    "a",
    "b",
    "r",
    "trace",
    "base_kind",
    "base_rep",
    "base_id",
    "base_size",
    "subgroup_order",
    "chain_length",
    "chain_max_degree",
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

AUDIT_FIELDS = (
    "date",
    "seed",
    "p",
    "a",
    "b",
    "r",
    "trace",
    "curve_attempts",
    "curve_search_s",
    "primitive_root",
    "subgroup_order",
    "subgroup_generator",
    "subgroup_elements",
    "factor_base_size",
    "chain_length",
    "chain_max_degree",
    "field_predicate_mismatches",
    "curve_membership_mismatches",
)

COMPARISON_FIELDS = (
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


def distinct_prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root(p: int) -> int:
    factors = distinct_prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ArithmeticError("no primitive root found")


def subgroup_elements(p: int, order: int) -> tuple[int, ...]:
    if order < 1 or (p - 1) % order:
        raise ValueError("subgroup order must divide p-1")
    root = primitive_root(p)
    generator = pow(root, (p - 1) // order, p)
    elements: list[int] = []
    current = 1
    for _ in range(order):
        elements.append(current)
        current = current * generator % p
    if current != 1 or len(set(elements)) != order:
        raise ArithmeticError("subgroup enumeration has the wrong order")
    return tuple(elements)


def squaring_chain_accepts(value: int, p: int, chain_length: int) -> bool:
    current = value % p
    for _ in range(chain_length):
        current = current * current % p
    return current == 1


def factor_base_from_x(curve: Curve, x_values: tuple[int, ...]) -> list[AffinePoint]:
    points: list[AffinePoint] = []
    for x_value in x_values:
        points.extend(curve.points_for_x(x_value))
    return points


def measure_one_base(
    *,
    curve: Curve,
    order: int,
    factor_base: list[AffinePoint],
    kind: str,
    base_rep: int,
    target_scalars: list[int],
    generator: AffinePoint,
    seed: int,
    subgroup_order: int,
    chain_length: int,
) -> list[dict[str, Any]]:
    pair_counts, pair_table_build_s = pair_sum_counts(curve, factor_base)
    expected = len(factor_base) ** 3 / order
    rows: list[dict[str, Any]] = []
    for target_rep, target_scalar in enumerate(target_scalars):
        target = curve.scalar_mul(target_scalar, generator)
        count = decomposition_count(curve, factor_base, pair_counts, target)
        pair_checks, decomposition, search_s = find_first_decomposition(curve, factor_base, target)
        if (decomposition is not None) != (count > 0):
            raise ArithmeticError("finder disagrees with exact decomposition count")
        rows.append(
            {
                "date": date.today().isoformat(),
                "seed": seed,
                "bits": curve.p.bit_length(),
                "p": curve.p,
                "a": curve.a,
                "b": curve.b,
                "r": order,
                "trace": curve.p + 1 - order,
                "base_kind": kind,
                "base_rep": base_rep,
                "base_id": f"{kind}:{base_rep}",
                "base_size": len(factor_base),
                "subgroup_order": subgroup_order,
                "chain_length": chain_length,
                "chain_max_degree": 2,
                "target_rep": target_rep,
                "target_scalar": target_scalar,
                "decomposition_count": count,
                "expected_count": f"{expected:.12g}",
                "normalized_count": f"{count / expected:.12g}" if expected else "0",
                "pair_checks": pair_checks,
                "search_found": int(decomposition is not None),
                "search_s": f"{search_s:.9f}",
                "pair_table_build_s": f"{pair_table_build_s:.9f}",
                "f4_verified": _verify_decomposition(curve, decomposition, target),
            }
        )
    return rows


def compare(
    rows: list[dict[str, Any]], seed: int, bootstrap_samples: int
) -> dict[str, Any]:
    candidate = [row for row in rows if row["base_kind"] == "smooth_subgroup"]
    baseline = [row for row in rows if row["base_kind"] == "random_matched_subgroup"]
    candidate_norm = _hierarchical_bootstrap(
        candidate, "normalized_count", random.Random(seed + 1), bootstrap_samples
    )
    baseline_norm = _hierarchical_bootstrap(
        baseline, "normalized_count", random.Random(seed + 2), bootstrap_samples
    )
    candidate_checks = _hierarchical_bootstrap(
        candidate, "pair_checks", random.Random(seed + 3), bootstrap_samples
    )
    baseline_checks = _hierarchical_bootstrap(
        baseline, "pair_checks", random.Random(seed + 4), bootstrap_samples
    )
    norm_ratios = [left / right for left, right in zip(candidate_norm, baseline_norm) if right]
    check_ratios = [left / right for left, right in zip(candidate_checks, baseline_checks) if right]
    candidate_norm_mean = statistics.fmean(float(row["normalized_count"]) for row in candidate)
    baseline_norm_mean = statistics.fmean(float(row["normalized_count"]) for row in baseline)
    candidate_check_mean = statistics.fmean(float(row["pair_checks"]) for row in candidate)
    baseline_check_mean = statistics.fmean(float(row["pair_checks"]) for row in baseline)
    return {
        "p": candidate[0]["p"],
        "candidate_kind": "smooth_subgroup",
        "baseline_kind": "random_matched_subgroup",
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


def write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if args.subgroup_order & (args.subgroup_order - 1):
        raise ValueError("this fixture expects a power-of-two subgroup order")
    chain_length = args.subgroup_order.bit_length() - 1
    curve_started = time.perf_counter()
    curve, order, curve_attempts = find_prime_order_curve(args.p, random.Random(args.seed))
    curve_search_s = time.perf_counter() - curve_started
    generator = curve.first_affine_point()
    if curve.scalar_mul(order, generator) is not None:
        raise ArithmeticError("first affine point does not generate the prime-order group")

    root = primitive_root(args.p)
    x_values = subgroup_elements(args.p, args.subgroup_order)
    subgroup_generator = pow(root, (args.p - 1) // args.subgroup_order, args.p)
    x_membership = set(x_values)
    field_mismatches = 0
    for value in range(args.p):
        expected = value in x_membership
        powered = pow(value, args.subgroup_order, args.p) == 1
        chained = squaring_chain_accepts(value, args.p, chain_length)
        field_mismatches += expected != powered or powered != chained

    candidate_base = factor_base_from_x(curve, x_values)
    candidate_membership = set(candidate_base)
    curve_mismatches = 0
    for point in curve.affine_points():
        expected = point in candidate_membership
        measured = pow(point[0], args.subgroup_order, args.p) == 1
        curve_mismatches += expected != measured

    rng = random.Random(args.seed + 1)
    target_scalars = rng.sample(range(1, order), args.targets)
    rows = measure_one_base(
        curve=curve,
        order=order,
        factor_base=candidate_base,
        kind="smooth_subgroup",
        base_rep=0,
        target_scalars=target_scalars,
        generator=generator,
        seed=args.seed,
        subgroup_order=args.subgroup_order,
        chain_length=chain_length,
    )
    for base_rep in range(args.replicates):
        scalars = rng.sample(range(1, order), len(candidate_base))
        random_base = points_from_scalars(curve, generator, scalars)
        rows.extend(
            measure_one_base(
                curve=curve,
                order=order,
                factor_base=random_base,
                kind="random_matched_subgroup",
                base_rep=base_rep,
                target_scalars=target_scalars,
                generator=generator,
                seed=args.seed,
                subgroup_order=args.subgroup_order,
                chain_length=chain_length,
            )
        )

    audit = {
        "date": date.today().isoformat(),
        "seed": args.seed,
        "p": args.p,
        "a": curve.a,
        "b": curve.b,
        "r": order,
        "trace": args.p + 1 - order,
        "curve_attempts": curve_attempts,
        "curve_search_s": f"{curve_search_s:.9f}",
        "primitive_root": root,
        "subgroup_order": args.subgroup_order,
        "subgroup_generator": subgroup_generator,
        "subgroup_elements": len(x_values),
        "factor_base_size": len(candidate_base),
        "chain_length": chain_length,
        "chain_max_degree": 2,
        "field_predicate_mismatches": field_mismatches,
        "curve_membership_mismatches": curve_mismatches,
    }
    summaries = summarize_rows(rows, args.seed, args.bootstrap)
    comparison = compare(rows, args.seed, args.bootstrap)
    return audit, rows, summaries, comparison


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=65537)
    parser.add_argument("--subgroup-order", type=int, default=64)
    parser.add_argument("--targets", type=int, default=96)
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=12022032)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.p = 17
        args.subgroup_order = 4
        args.targets = 8
        args.replicates = 1
        args.bootstrap = 100
    audit, rows, summaries, comparison = run(args)
    print(" ".join(f"{field}={audit[field]}" for field in AUDIT_FIELDS))
    for summary in summaries:
        print(
            f"kind={summary['base_kind']} size={summary['base_size']} "
            f"normalized={summary['normalized_mean']} "
            f"success={summary['success_rate']} checks={summary['mean_pair_checks']}"
        )
    print(" ".join(f"{field}={comparison[field]}" for field in COMPARISON_FIELDS))
    if args.smoke:
        return
    prefix = (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"measure_smooth_subgroup_p{args.p}_n{args.subgroup_order}_t{args.targets}_r{args.replicates}_s{args.seed}_{date.today().strftime('%Y%m%d')}"
    )
    write_csv(prefix.with_name(prefix.name + "_audit.csv"), AUDIT_FIELDS, [audit])
    write_csv(prefix.with_name(prefix.name + "_raw.csv"), RAW_FIELDS, rows)
    write_csv(prefix.with_name(prefix.name + "_summary.csv"), SUMMARY_FIELDS, summaries)
    write_csv(prefix.with_name(prefix.name + "_comparison.csv"), COMPARISON_FIELDS, [comparison])
    print(f"output_prefix={prefix}")


if __name__ == "__main__":
    main()
