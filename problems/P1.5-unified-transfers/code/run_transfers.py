"""
run_transfers.py - Reproduce additive and pairing transfers at toy scale.
Sub-goal: P1.5 / SG-02 and SG-03
Inputs:   --seed <int> --repeats <int> [--smoke]
Outputs:  data/run_transfers_<profile>_<date>_{raw,scaling}.csv
Runtime:  about 21 seconds at --repeats 50 on Python 3.13
Validated against: exhaustive order-17 additive logs and the F_43 pairing vector
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from random import Random
from time import perf_counter_ns
from typing import Callable

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.anomalous import additive_transfer, smart_attack  # noqa: E402
from lib.curves import (  # noqa: E402
    curve_order,
    embedding_degree,
    find_anomalous_curve,
    is_prime,
    supersingular_k2_curve,
)
from lib.dlog import multiplicative_bsgs  # noqa: E402
from lib.extension_curves import ExtensionCurve, ExtensionPoint  # noqa: E402
from lib.finite_fields import ExtensionElement, ExtensionField  # noqa: E402
from lib.pairing import (  # noqa: E402
    j1728_distortion_map,
    lift_base_point,
    miller_loop_with_trace,
    reduced_tate_pairing,
)


def _median_call_ns(function: Callable[[], object], repeats: int) -> float:
    function()
    samples: list[float] = []
    for _ in range(7):
        start = perf_counter_ns()
        for _ in range(repeats):
            function()
        samples.append((perf_counter_ns() - start) / repeats)
    return statistics.median(samples)


def run_additive_case(
    p: int, seed: int, secret: int, repeats: int
) -> dict[str, object]:
    timing_repeats = max(repeats, 5_000)
    construction_start = perf_counter_ns()
    curve, generator, attempts = find_anomalous_curve(p, Random(seed + p))
    exact_order = curve_order(curve)
    construction_ns = perf_counter_ns() - construction_start
    if exact_order != p or curve.scalar_mul(p, generator) is not None:
        raise ArithmeticError("anomalous construction failed exact validation")
    target = curve.scalar_mul(secret, generator)
    if target is None:
        raise ArithmeticError("the selected target is the identity")

    generator_image = additive_transfer(curve, generator, validate_curve=False)
    target_image = additive_transfer(curve, target, validate_curve=False)
    recovered = target_image * pow(generator_image, -1, p) % p
    if recovered != secret or smart_attack(curve, generator, target) != secret:
        raise ArithmeticError("additive transfer failed to recover the known log")
    for scalar in (0, 1, 2, secret, p - 1):
        image = additive_transfer(
            curve,
            curve.scalar_mul(scalar, generator),
            validate_curve=False,
        )
        if image != scalar * generator_image % p:
            raise ArithmeticError("additive transfer failed a homomorphism check")

    trace: Counter[str] = Counter()
    additive_transfer(curve, target, trace=trace, validate_curve=False)
    return {
        "transfer": "additive",
        "p": p,
        "subgroup_order": p,
        "embedding_degree": "",
        "curve_a": curve.a,
        "curve_b": curve.b,
        "generator_x": generator[0],
        "generator_y": generator[1],
        "secret": secret,
        "recovered": recovered,
        "image_a": target_image,
        "image_b": 0,
        "construction_attempts": attempts,
        "construction_ns": construction_ns,
        "transfer_ns": round(
            _median_call_ns(
                lambda: additive_transfer(curve, target, validate_curve=False),
                timing_repeats,
            ),
            3,
        ),
        "target_dlog_ns": round(
            _median_call_ns(
                lambda: target_image * pow(generator_image, -1, p) % p,
                timing_repeats,
            ),
            3,
        ),
        "core_steps": trace["lifted_group_operation"],
        "transfer_work": trace["lifted_group_operation"],
        "dlog_work": 1,
        "seed": seed,
    }


def run_mov_case(
    p: int, subgroup_order: int, secret: int, repeats: int, seed: int
) -> dict[str, object]:
    if not is_prime(p) or not is_prime(subgroup_order):
        raise ValueError("the experiment requires prime p and r")
    curve, generator, exact_order = supersingular_k2_curve(p, subgroup_order)
    degree = embedding_degree(p, subgroup_order)
    if degree != 2:
        raise ArithmeticError("the selected subgroup does not have k=2")
    field = ExtensionField(p, (1, 0, 1))
    extension_curve = ExtensionCurve(field, field.element(1), field.zero)
    extension_generator = lift_base_point(field, generator)
    distorted = j1728_distortion_map(
        field, generator, field.element((0, 1))
    )
    if not extension_curve.contains(distorted):
        raise ArithmeticError("distortion-map image is not on the curve")

    def transfer(point: ExtensionPoint) -> ExtensionElement:
        return reduced_tate_pairing(
            extension_curve, subgroup_order, point, distorted
        )

    generator_image = transfer(extension_generator)
    if generator_image == field.one or generator_image**subgroup_order != field.one:
        raise ArithmeticError("the pairing image is degenerate or outside mu_r")
    target = extension_curve.scalar_mul(secret, extension_generator)
    target_image = transfer(target)
    recovered = multiplicative_bsgs(generator_image, target_image, subgroup_order)
    if recovered != secret or extension_curve.scalar_mul(recovered, extension_generator) != target:
        raise ArithmeticError("pairing transfer failed to recover the known log")
    for scalar in (1, 2, secret, subgroup_order - 1):
        if transfer(extension_curve.scalar_mul(scalar, extension_generator)) != generator_image**scalar:
            raise ArithmeticError("pairing transfer failed a bilinearity check")

    _, miller_trace = miller_loop_with_trace(
        extension_curve, subgroup_order, target, distorted
    )
    return {
        "transfer": "multiplicative",
        "p": p,
        "subgroup_order": subgroup_order,
        "embedding_degree": degree,
        "curve_a": 1,
        "curve_b": 0,
        "generator_x": generator[0],
        "generator_y": generator[1],
        "secret": secret,
        "recovered": recovered,
        "image_a": target_image.coefficients[0],
        "image_b": target_image.coefficients[1],
        "construction_attempts": 1,
        "construction_ns": 0,
        "transfer_ns": round(
            _median_call_ns(lambda: transfer(target), repeats), 3
        ),
        "target_dlog_ns": round(
            _median_call_ns(
                lambda: multiplicative_bsgs(
                    generator_image, target_image, subgroup_order
                ),
                repeats,
            ),
            3,
        ),
        "core_steps": len(miller_trace),
        "transfer_work": len(miller_trace) * p.bit_length(),
        "dlog_work": math.isqrt(subgroup_order - 1) + 1,
        "seed": seed,
    }


def _fit_scaling(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    models = (
        ("additive_transfer", "additive", "transfer_ns", "transfer_work"),
        ("pairing_transfer", "multiplicative", "transfer_ns", "transfer_work"),
        ("target_bsgs", "multiplicative", "target_dlog_ns", "dlog_work"),
    )
    output: list[dict[str, object]] = []
    for model, transfer_name, observed_key, predictor_key in models:
        selected = [row for row in rows if row["transfer"] == transfer_name]
        x_values = [math.log2(float(row[predictor_key])) for row in selected]
        y_values = [math.log2(float(row[observed_key])) for row in selected]
        x_mean = statistics.fmean(x_values)
        y_mean = statistics.fmean(y_values)
        denominator = sum((value - x_mean) ** 2 for value in x_values)
        slope = sum(
            (x_value - x_mean) * (y_value - y_mean)
            for x_value, y_value in zip(x_values, y_values, strict=True)
        ) / denominator
        intercept = y_mean - slope * x_mean
        for row, x_value, y_value in zip(
            selected, x_values, y_values, strict=True
        ):
            fitted = intercept + slope * x_value
            output.append(
                {
                    "model": model,
                    "p": row["p"],
                    "subgroup_order": row["subgroup_order"],
                    "predictor": row[predictor_key],
                    "observed_ns": row[observed_key],
                    "fitted_ns": round(2**fitted, 3),
                    "log2_residual": round(y_value - fitted, 6),
                    "fitted_exponent": round(slope, 6),
                    "log2_intercept": round(intercept, 6),
                }
            )
    return output


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(
    seed: int, repeats: int, smoke: bool
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    additive_primes = (101, 211) if smoke else (
        101, 211, 401, 809, 1601, 3203, 6421
    )
    mov_cases = ((43, 11), (211, 53)) if smoke else (
        (43, 11),
        (211, 53),
        (331, 83),
        (907, 227),
        (2011, 503),
        (4051, 1013),
        (8011, 2003),
    )
    raw_rows: list[dict[str, object]] = []
    for p in additive_primes:
        raw_rows.append(run_additive_case(p, seed, 37, repeats))
    for p, subgroup_order in mov_cases:
        secret = min(37, subgroup_order - 1)
        raw_rows.append(
            run_mov_case(p, subgroup_order, secret, repeats, seed)
        )
    return raw_rows, _fit_scaling(raw_rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=15072026)
    parser.add_argument("--repeats", type=int, default=50)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    arguments = parser.parse_args()
    if arguments.repeats < 1:
        parser.error("--repeats must be positive")
    repeats = min(arguments.repeats, 5) if arguments.smoke else arguments.repeats
    raw_rows, scaling_rows = run_experiment(
        arguments.seed, repeats, arguments.smoke
    )
    output_dir = arguments.output_dir or Path(__file__).resolve().parents[1] / "data"
    profile = "smoke" if arguments.smoke else "full"
    prefix = output_dir / f"run_transfers_{profile}_{date.today():%Y%m%d}"
    _write_csv(prefix.with_name(prefix.name + "_raw.csv"), raw_rows)
    _write_csv(prefix.with_name(prefix.name + "_scaling.csv"), scaling_rows)
    for row in raw_rows:
        print(
            f"{row['transfer']:14s} p={row['p']:>4} r={row['subgroup_order']:>4} "
            f"secret={row['secret']:>4} recovered={row['recovered']:>4} "
            f"map={row['transfer_ns']:>10} ns dlog={row['target_dlog_ns']:>10} ns"
        )


if __name__ == "__main__":
    main()
