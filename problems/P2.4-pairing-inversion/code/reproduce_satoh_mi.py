"""
reproduce_satoh_mi.py -- validate Satoh MI and the FAPI-1 orientation transfer.
Sub-goal: P2.4 / SG-07
Inputs:   --p <prime> --trials <int> --seed <int> [--smoke]
Outputs:  data/reproduce_satoh_mi_<params>_<date>.csv
Runtime:  ~3.0 s for the default six curves and 50 trials on Python 3.13
Validated against: Satoh (ePrint 2019/385, revised 2025), Example 4.4
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from datetime import date
from pathlib import Path
from random import Random
from time import perf_counter_ns

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve, curve_order, is_prime  # noqa: E402
from lib.extension_curves import ExtensionCurve  # noqa: E402
from lib.finite_fields import ExtensionField  # noqa: E402
from lib.pairing import (  # noqa: E402
    final_exponentiation,
    j1728_distortion_map,
    j1728_fapi1_miller_inverse_k2,
    lift_base_point,
    miller_loop,
    satoh_even_miller_inverse_k2,
)


def prime_factors(value: int) -> list[int]:
    """Return the distinct prime factors of a positive toy integer."""
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def first_order_r_point(curve: Curve, subgroup_order: int) -> tuple[int, int]:
    """Find the first deterministic point of order r on a toy curve."""
    cofactor = curve_order(curve) // subgroup_order
    for candidate in curve.affine_points():
        point = curve.scalar_mul(cofactor, candidate)
        if point is not None and curve.scalar_mul(subgroup_order, point) is None:
            return point
    raise RuntimeError("failed to find a point of the requested order")


def reproduce_published_example() -> dict[str, object]:
    """Reproduce all displayed values in Satoh's Example 4.4."""
    field = ExtensionField(139, (4, 0, 1))
    curve = ExtensionCurve(field, field.element(-13), field.element(-7))
    theta = field.element((0, 1))
    fixed_point = field.element(67), 38 * theta
    raw_target = field.element((109, 25))
    u = raw_target**70
    inversion = satoh_even_miller_inverse_k2(
        curve,
        point_order=35,
        miller_scalar=140,
        fixed_point=fixed_point,
        raw_target=raw_target,
    )
    expected = lift_base_point(field, (59, -54 % 139))
    if u != field.element(131):
        raise AssertionError("Satoh Example 4.4 u value did not reproduce")
    if inversion.x_candidates != (59, 75) or inversion.point != expected:
        raise AssertionError("Satoh Example 4.4 inverse did not reproduce")
    if miller_loop(curve, 140, fixed_point, expected) != raw_target:
        raise AssertionError("published inverse failed raw Miller validation")
    return {
        "satoh_example_p": 139,
        "satoh_example_point_order": 35,
        "satoh_example_miller_scalar": 140,
        "satoh_example_u": int(u),
        "satoh_example_x_candidates": "59;75",
        "satoh_example_solution": "(59,85)",
        "satoh_example_reproduced": True,
    }


def benchmark_parameter(p: int, trials: int, seed: int) -> dict[str, object]:
    """Exhaustively validate the transfer and time seeded raw inversions."""
    if not is_prime(p) or p % 4 != 3:
        raise ValueError("p must be prime and congruent to 3 modulo 4")
    subgroup_order = max(factor for factor in prime_factors(p + 1) if factor > 2)
    if not is_prime(subgroup_order):
        raise AssertionError("selected subgroup order is not prime")

    base_curve = Curve(p, 1, 0)
    if curve_order(base_curve) != p + 1:
        raise AssertionError("unexpected order for the supersingular j=1728 curve")
    base_point = (23, 8) if p == 43 else first_order_r_point(base_curve, subgroup_order)
    field = ExtensionField(p, (1, 0, 1))
    curve = ExtensionCurve(field, field.element(1), field.zero)
    point = lift_base_point(field, base_point)
    i = field.element((0, 1))
    inverse_distorted_point = j1728_distortion_map(field, base_point, -i)

    raw_targets = []
    distorted_points = []
    maximum_candidates = 0
    maximum_undefined_candidates = 0
    transfer_checks = 0
    for scalar in range(1, subgroup_order):
        base_multiple = curve.scalar_mul(scalar, point)
        distorted = j1728_distortion_map(field, base_multiple, i)
        raw_target = miller_loop(curve, subgroup_order, point, distorted)
        transferred = miller_loop(
            curve,
            subgroup_order,
            inverse_distorted_point,
            base_multiple,
        )
        if raw_target != i ** (-subgroup_order) * transferred:
            raise AssertionError("distortion-map Miller pullback identity failed")
        inversion = j1728_fapi1_miller_inverse_k2(
            curve,
            subgroup_order,
            base_point,
            raw_target,
            i,
        )
        if inversion.point != distorted:
            raise AssertionError("Satoh transfer failed to invert a raw target")
        maximum_candidates = max(maximum_candidates, inversion.candidates_tested)
        maximum_undefined_candidates = max(
            maximum_undefined_candidates,
            inversion.undefined_candidates,
        )
        transfer_checks += 1
        raw_targets.append(raw_target)
        distorted_points.append(distorted)

    final_exponent = (field.order - 1) // subgroup_order
    canonical_compatible = 0
    for raw_target in raw_targets:
        reduced_target = final_exponentiation(raw_target, subgroup_order)
        canonical_root = reduced_target ** pow(final_exponent, -1, subgroup_order)
        inversion = j1728_fapi1_miller_inverse_k2(
            curve,
            subgroup_order,
            base_point,
            canonical_root,
            i,
        )
        if inversion.point is not None:
            observed = miller_loop(
                curve,
                subgroup_order,
                point,
                inversion.point,
            )
            canonical_compatible += int(observed == canonical_root)

    rng = Random(seed + p)
    samples: list[int] = []
    candidate_counts: list[int] = []
    for _ in range(trials):
        index = rng.randrange(len(raw_targets))
        started = perf_counter_ns()
        inversion = j1728_fapi1_miller_inverse_k2(
            curve,
            subgroup_order,
            base_point,
            raw_targets[index],
            i,
        )
        samples.append(perf_counter_ns() - started)
        candidate_counts.append(inversion.candidates_tested)
        if inversion.point != distorted_points[index]:
            raise AssertionError("timed inversion failed validation")

    mean_ns = statistics.fmean(samples)
    ci95 = (
        0.0
        if len(samples) == 1
        else 1.96 * statistics.stdev(samples) / math.sqrt(len(samples))
    )
    return {
        "p": p,
        "p_bits": p.bit_length(),
        "embedding_degree": 2,
        "subgroup_order_r": subgroup_order,
        "base_point_x": base_point[0],
        "base_point_y": base_point[1],
        "raw_targets_exhaustively_inverted": len(raw_targets),
        "pullback_identity_checks": transfer_checks,
        "maximum_candidates_tested": maximum_candidates,
        "maximum_undefined_candidates": maximum_undefined_candidates,
        "candidate_bound": 4,
        "final_exponent_d": final_exponent,
        "canonical_final_roots_compatible": canonical_compatible,
        "canonical_final_roots_tested": len(raw_targets),
        "timing_trials": trials,
        "seed": seed,
        "raw_mi_mean_ns": round(mean_ns, 3),
        "raw_mi_median_ns": round(statistics.median(samples), 3),
        "raw_mi_ci95_halfwidth_ns": round(ci95, 3),
        "raw_mi_mean_candidates": round(statistics.fmean(candidate_counts), 6),
    }


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    """Write deterministic result rows to a CSV file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, action="append", help="prime p = 3 mod 4; may be repeated")
    parser.add_argument("--trials", type=int, default=50)
    parser.add_argument("--seed", type=int, default=2404)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("trials must be positive")
    primes = args.p or [43, 59, 83, 103, 131, 163]
    trials = args.trials
    if args.smoke:
        primes = [43]
        trials = min(trials, 3)
    published = reproduce_published_example()
    rows = [{**published, **benchmark_parameter(p, trials, args.seed)} for p in primes]
    parameter_label = "-".join(str(p) for p in primes)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"reproduce_satoh_mi_p{parameter_label}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    print(output)


if __name__ == "__main__":
    main()
