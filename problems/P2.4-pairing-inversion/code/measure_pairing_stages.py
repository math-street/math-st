"""
measure_pairing_stages.py — exhaustively measure the two reduced-Tate stages.
Sub-goal: P2.4 / SG-01, SG-02, SG-04, SG-05
Inputs:   --p <prime> --trials <int> --seed <int> [--smoke]
Outputs:  data/measure_pairing_stages_<params>_<date>.csv
Runtime:  ~3 s for the default four curves and 50 trials on Python 3.13
Validated against: published F_43 vector P=(23,8), Q=(20,8t), r=11
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from random import Random
from time import perf_counter_ns
from typing import Callable, Iterable, TypeVar

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve, curve_order, is_prime  # noqa: E402
from lib.extension_curves import ExtensionCurve, ExtensionPoint  # noqa: E402
from lib.finite_fields import ExtensionElement, ExtensionField  # noqa: E402
from lib.pairing import (  # noqa: E402
    final_exponentiation,
    j1728_distortion_map,
    lift_base_point,
    miller_loop,
    reduced_tate_pairing,
)


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class TimingSummary:
    mean_ns: float
    median_ns: float
    ci95_halfwidth_ns: float
    mean_probes: float


def prime_factors(value: int) -> list[int]:
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
    cofactor = curve_order(curve) // subgroup_order
    for candidate in curve.affine_points():
        point = curve.scalar_mul(cofactor, candidate)
        if point is not None and curve.scalar_mul(subgroup_order, point) is None:
            return point
    raise RuntimeError("failed to find a point of the requested prime order")


def primitive_element(field: ExtensionField) -> ExtensionElement:
    group_order = field.order - 1
    factors = prime_factors(group_order)
    for candidate in field.elements():
        if candidate and all(candidate ** (group_order // factor) != field.one for factor in factors):
            return candidate
    raise RuntimeError("failed to find a multiplicative generator")


def summarize(samples_ns: list[int], probes: list[int]) -> TimingSummary:
    if not samples_ns:
        raise ValueError("at least one timing sample is required")
    mean = statistics.fmean(samples_ns)
    if len(samples_ns) == 1:
        halfwidth = 0.0
    else:
        halfwidth = 1.96 * statistics.stdev(samples_ns) / math.sqrt(len(samples_ns))
    return TimingSummary(
        mean_ns=mean,
        median_ns=statistics.median(samples_ns),
        ci95_halfwidth_ns=halfwidth,
        mean_probes=statistics.fmean(probes),
    )


def time_inverter(
    targets: Iterable[T],
    inverter: Callable[[T], tuple[object, int]],
    validator: Callable[[T, object], bool],
) -> TimingSummary:
    elapsed: list[int] = []
    probes: list[int] = []
    for target in targets:
        started = perf_counter_ns()
        candidate, probe_count = inverter(target)
        elapsed.append(perf_counter_ns() - started)
        probes.append(probe_count)
        if not validator(target, candidate):
            raise AssertionError("inversion result failed validation")
    return summarize(elapsed, probes)


def benchmark_parameter(p: int, trials: int, seed: int) -> dict[str, object]:
    if not is_prime(p) or p % 4 != 3:
        raise ValueError("p must be prime and congruent to 3 modulo 4")
    subgroup_order = max(factor for factor in prime_factors(p + 1) if factor > 2)
    if not is_prime(subgroup_order):
        raise AssertionError("selected subgroup order is not prime")

    base_curve = Curve(p, 1, 0)
    base_order = curve_order(base_curve)
    if base_order != p + 1:
        raise AssertionError("unexpected order for the supersingular j=1728 curve")
    base_point = (23, 8) if p == 43 else first_order_r_point(base_curve, subgroup_order)
    if base_curve.scalar_mul(subgroup_order, base_point) is not None:
        raise AssertionError("base point does not have the requested order")

    field = ExtensionField(p, (1, 0, 1))
    curve = ExtensionCurve(field, field.element(1), field.zero)
    point = lift_base_point(field, base_point)
    square_root_minus_one = field.element((0, 1))
    q_generator = j1728_distortion_map(field, base_point, square_root_minus_one)
    if not curve.contains(q_generator) or curve.scalar_mul(subgroup_order, q_generator) is not None:
        raise AssertionError("distorted point did not generate the expected subgroup")

    base_pairing = reduced_tate_pairing(curve, subgroup_order, point, q_generator)
    if base_pairing == field.one or base_pairing**subgroup_order != field.one:
        raise AssertionError("pairing failed non-degeneracy or target-order validation")

    rng = Random(seed + p)
    bilinear_trials = max(32, trials)
    for _ in range(bilinear_trials):
        left_scalar = rng.randrange(1, subgroup_order)
        right_scalar = rng.randrange(1, subgroup_order)
        observed = reduced_tate_pairing(
            curve,
            subgroup_order,
            curve.scalar_mul(left_scalar, point),
            curve.scalar_mul(right_scalar, q_generator),
        )
        if observed != base_pairing ** (left_scalar * right_scalar):
            raise AssertionError("bilinearity check failed")

    nonzero_field = [value for value in field.elements() if value]
    fibre_started = perf_counter_ns()
    final_fibres = Counter(final_exponentiation(value, subgroup_order) for value in nonzero_field)
    fibre_enumeration_ns = perf_counter_ns() - fibre_started
    exponent = (field.order - 1) // subgroup_order
    if len(final_fibres) != subgroup_order or set(final_fibres.values()) != {exponent}:
        raise AssertionError("final-exponentiation fibres disagree with the homomorphism count")

    q_candidates: list[ExtensionPoint] = [
        curve.scalar_mul(scalar, q_generator) for scalar in range(1, subgroup_order)
    ]
    raw_values = [miller_loop(curve, subgroup_order, point, candidate) for candidate in q_candidates]
    pairing_values = [final_exponentiation(value, subgroup_order) for value in raw_values]
    raw_fibres = Counter(raw_values)
    pairing_fibres = Counter(pairing_values)
    if len(pairing_fibres) != subgroup_order - 1 or set(pairing_fibres.values()) != {1}:
        raise AssertionError("nonidentity FAPI-1 map was not injective")

    compatible_per_target = Counter(pairing_values)
    compatible_counts = list(compatible_per_target.values())
    raw_value_set = set(raw_values)

    generator_setup_started = perf_counter_ns()
    multiplicative_generator = primitive_element(field)
    generator_setup_ns = perf_counter_ns() - generator_setup_started
    target_generator = multiplicative_generator**exponent
    if target_generator**subgroup_order != field.one or target_generator == field.one:
        raise AssertionError("failed to construct a target-subgroup generator")

    def invert_final_scan(target: ExtensionElement) -> tuple[ExtensionElement, int]:
        for probe, candidate in enumerate(nonzero_field, 1):
            if candidate**exponent == target:
                return candidate, probe
        raise LookupError("target has no final-exponentiation preimage")

    def invert_final_target_dlog(target: ExtensionElement) -> tuple[ExtensionElement, int]:
        power = field.one
        for discrete_log in range(subgroup_order):
            if power == target:
                return multiplicative_generator**discrete_log, discrete_log + 1
            power = power * target_generator
        raise LookupError("target is outside the final-exponentiation image")

    def invert_miller(target: ExtensionElement) -> tuple[ExtensionPoint, int]:
        for probe, candidate in enumerate(q_candidates, 1):
            if miller_loop(curve, subgroup_order, point, candidate) == target:
                return candidate, probe
        raise LookupError("target is outside the raw Miller image")

    def invert_pairing(target: ExtensionElement) -> tuple[ExtensionPoint, int]:
        for probe, candidate in enumerate(q_candidates, 1):
            if reduced_tate_pairing(curve, subgroup_order, point, candidate) == target:
                return candidate, probe
        raise LookupError("target is outside the nonidentity pairing image")

    def invert_g2_dlog(target: ExtensionPoint) -> tuple[ExtensionPoint, int]:
        for probe, candidate in enumerate(q_candidates, 1):
            if candidate == target:
                return candidate, probe
        raise LookupError("target is outside G2")

    scalars = [rng.randrange(1, subgroup_order) for _ in range(trials)]
    selected_points = [q_candidates[scalar - 1] for scalar in scalars]
    selected_raw = [raw_values[scalar - 1] for scalar in scalars]
    selected_pairing = [pairing_values[scalar - 1] for scalar in scalars]

    final_scan = time_inverter(
        selected_pairing,
        invert_final_scan,
        lambda target, candidate: isinstance(candidate, ExtensionElement)
        and final_exponentiation(candidate, subgroup_order) == target,
    )
    final_dlog = time_inverter(
        selected_pairing,
        invert_final_target_dlog,
        lambda target, candidate: isinstance(candidate, ExtensionElement)
        and final_exponentiation(candidate, subgroup_order) == target,
    )
    miller_inverse = time_inverter(
        selected_raw,
        invert_miller,
        lambda target, candidate: candidate is not None
        and miller_loop(curve, subgroup_order, point, candidate) == target,
    )
    direct_pairing_inverse = time_inverter(
        selected_pairing,
        invert_pairing,
        lambda target, candidate: candidate is not None
        and reduced_tate_pairing(curve, subgroup_order, point, candidate) == target,
    )
    g2_dlog = time_inverter(
        selected_points,
        invert_g2_dlog,
        lambda target, candidate: candidate == target,
    )

    canonical_roots = [invert_final_target_dlog(target)[0] for target in pairing_values]
    compatible_canonical_roots = sum(root in raw_value_set for root in canonical_roots)

    row: dict[str, object] = {
        "p": p,
        "p_bits": p.bit_length(),
        "embedding_degree": 2,
        "subgroup_order_r": subgroup_order,
        "base_point_x": base_point[0],
        "base_point_y": base_point[1],
        "field_multiplicative_order": field.order - 1,
        "final_exponent_d": exponent,
        "final_image_size": len(final_fibres),
        "final_fibre_min": min(final_fibres.values()),
        "final_fibre_max": max(final_fibres.values()),
        "fibre_enumeration_ns": fibre_enumeration_ns,
        "raw_domain_size_nonidentity": len(q_candidates),
        "raw_image_size": len(raw_fibres),
        "raw_fibre_min": min(raw_fibres.values()),
        "raw_fibre_max": max(raw_fibres.values()),
        "pairing_image_size_nonidentity": len(pairing_fibres),
        "compatible_raw_per_nonidentity_target_min": min(compatible_counts),
        "compatible_raw_per_nonidentity_target_max": max(compatible_counts),
        "compatible_fraction_of_final_fibre": 1 / exponent,
        "canonical_root_compatible_count": compatible_canonical_roots,
        "canonical_root_target_count": len(canonical_roots),
        "bilinear_trials": bilinear_trials,
        "nondegenerate": True,
        "timing_trials": trials,
        "seed": seed,
        "generator_setup_ns": generator_setup_ns,
    }
    for prefix, summary in (
        ("final_scan", final_scan),
        ("final_target_dlog", final_dlog),
        ("miller_inverse", miller_inverse),
        ("pairing_inverse", direct_pairing_inverse),
        ("g2_dlog_scan", g2_dlog),
    ):
        row[f"{prefix}_mean_ns"] = round(summary.mean_ns, 3)
        row[f"{prefix}_median_ns"] = round(summary.median_ns, 3)
        row[f"{prefix}_ci95_halfwidth_ns"] = round(summary.ci95_halfwidth_ns, 3)
        row[f"{prefix}_mean_probes"] = round(summary.mean_probes, 6)
    return row


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
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
    primes = args.p or [43, 59, 83, 131]
    trials = args.trials
    if args.smoke:
        primes = [43]
        trials = min(trials, 3)
    rows = [benchmark_parameter(p, trials, args.seed) for p in primes]
    parameter_label = "-".join(str(p) for p in primes)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"measure_pairing_stages_p{parameter_label}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    print(output)


if __name__ == "__main__":
    main()

