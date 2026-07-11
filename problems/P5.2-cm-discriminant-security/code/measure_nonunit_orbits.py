"""Measure eigenvalue orders and explicit D=-7 orbit-normalization costs.

Sub-goal: P5.2 / SG-07a, SG-07b
Inputs:   --bits <comma-list> --samples <int> --seed <int> --smoke
Outputs:  data/measure_nonunit_orbits_<params>_<date>_{raw,summary,validation}.csv
Runtime:  under 10 seconds at bits=10,12,14,16,18 and samples=16
Validated against: exhaustive and independent BSGS point counts, the GLV
                   characteristic equation, exact scalar orders, and orbit
                   closure checks
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
from typing import Any, Iterable

CODE_DIR = Path(__file__).resolve().parent
PROBLEM_DIR = CODE_DIR.parent
WORKSPACE_DIR = CODE_DIR.parents[2]
for import_dir in (CODE_DIR, WORKSPACE_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from cm_nonunit import canonicalize_cm7_orbit, construct_cm7_case, validate_cm7_case


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    """Write a CSV file with a fixed schema."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate raw timings and expose the ideal-gain/enumeration comparison."""

    grouped: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(int(row["bits"]), []).append(row)

    summaries: list[dict[str, Any]] = []
    for bits, group in sorted(grouped.items()):
        first = group[0]
        subgroup_order = int(first["subgroup_order"])
        scalar_order = int(first["scalar_order"])
        quotient_orbits = (subgroup_order - 1) // scalar_order
        expected_evaluations = scalar_order - 1
        evaluations = [int(row["map_evaluations"]) for row in group]
        if any(value != expected_evaluations for value in evaluations):
            raise ArithmeticError("canonicalizer did not enumerate the complete orbit")
        elapsed = [int(row["elapsed_ns"]) for row in group]
        ideal_speedup = math.sqrt(scalar_order)
        summaries.append(
            {
                "bits": bits,
                "p": first["p"],
                "group_order": first["group_order"],
                "subgroup_order": subgroup_order,
                "subgroup_bits": subgroup_order.bit_length(),
                "cofactor": first["cofactor"],
                "endomorphism_scalar": first["endomorphism_scalar"],
                "scalar_order": scalar_order,
                "nonzero_quotient_orbits": quotient_orbits,
                "orbit_fraction": f"{scalar_order / (subgroup_order - 1):.12f}",
                "samples": len(group),
                "map_evaluations_per_normalization": expected_evaluations,
                "mean_elapsed_ns": f"{statistics.fmean(elapsed):.3f}",
                "median_elapsed_ns": f"{statistics.median(elapsed):.3f}",
                "ideal_random_mapping_speedup": f"{ideal_speedup:.12f}",
                "enumeration_to_ideal_gain_ratio": f"{expected_evaluations / ideal_speedup:.12f}",
            }
        )
    return summaries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", default="10,12,14,16,18", help="comma-separated field sizes")
    parser.add_argument("--samples", type=int, default=16)
    parser.add_argument("--seed", type=int, default=72022026)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.samples < 1:
        raise ValueError("samples must be positive")
    bits_values = [int(value) for value in args.bits.split(",")]
    samples = args.samples
    output_dir = PROBLEM_DIR / "data"
    if args.smoke:
        bits_values = [9, 10]
        samples = min(samples, 3)
        output_dir /= "smoke"
    if not bits_values or len(set(bits_values)) != len(bits_values):
        raise ValueError("bits must be a nonempty list without duplicates")

    started = time.perf_counter()
    raw_rows: list[dict[str, Any]] = []
    validation_rows: list[dict[str, Any]] = []
    for bits in bits_values:
        threshold = 5 if args.smoke else max(5, bits - 2)
        case = construct_cm7_case(bits, minimum_subgroup_bits=threshold)
        validation = validate_cm7_case(case, samples=32, seed=args.seed + bits)
        if (case.subgroup_order - 1) % case.scalar_order:
            raise ArithmeticError("scalar order does not divide the subgroup unit-group order")
        validation_rows.append(
            {
                "bits": bits,
                "p": case.curve.p,
                "a": case.curve.a,
                "b": case.curve.b,
                "group_order": case.group_order,
                "subgroup_order": case.subgroup_order,
                "cofactor": case.cofactor,
                "omega": case.omega,
                "kernel_x": case.kernel_x,
                "endomorphism_scalar": case.endomorphism_scalar,
                "scalar_order": case.scalar_order,
                "nonzero_quotient_orbits": (case.subgroup_order - 1) // case.scalar_order,
                **validation,
            }
        )

        rng = random.Random(args.seed + 1_000_003 * bits)
        for sample in range(samples):
            secret = rng.randrange(1, case.subgroup_order)
            point = case.curve.scalar_mul(secret, case.generator, charge=False)
            tick = time.perf_counter_ns()
            representative, exponent, evaluations = canonicalize_cm7_orbit(case, point)
            elapsed_ns = time.perf_counter_ns() - tick
            expected = case.curve.scalar_mul(
                pow(case.endomorphism_scalar, exponent, case.subgroup_order) * secret,
                case.generator,
                charge=False,
            )
            if representative != expected:
                raise ArithmeticError("reported orbit exponent does not reproduce the representative")
            if representative.is_infinity:
                raise ArithmeticError("a nonzero subgroup point normalized to infinity")
            raw_rows.append(
                {
                    "bits": bits,
                    "p": case.curve.p,
                    "group_order": case.group_order,
                    "subgroup_order": case.subgroup_order,
                    "cofactor": case.cofactor,
                    "endomorphism_scalar": case.endomorphism_scalar,
                    "scalar_order": case.scalar_order,
                    "sample": sample,
                    "secret": secret,
                    "representative_x": representative.x,
                    "representative_y": representative.y,
                    "orbit_exponent": exponent,
                    "map_evaluations": evaluations,
                    "elapsed_ns": elapsed_ns,
                }
            )

    summary_rows = summarize_rows(raw_rows)
    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(str(value) for value in bits_values)
    stem = f"measure_nonunit_orbits_b{bit_label}_n{samples}_s{args.seed}_{stamp}"
    raw_path = output_dir / f"{stem}_raw.csv"
    summary_path = output_dir / f"{stem}_summary.csv"
    validation_path = output_dir / f"{stem}_validation.csv"
    write_csv(raw_path, raw_rows, list(raw_rows[0]))
    write_csv(summary_path, summary_rows, list(summary_rows[0]))
    write_csv(validation_path, validation_rows, list(validation_rows[0]))
    print(f"raw={raw_path}")
    print(f"summary={summary_path}")
    print(f"validation={validation_path}")
    print(f"elapsed_seconds={time.perf_counter() - started:.3f}")


if __name__ == "__main__":
    main()
