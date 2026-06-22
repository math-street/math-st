"""
measure_structured_candidates.py — Candidate B and Candidate D-proxy measurements.
Sub-goal: P1.2 / SG-04 and SG-06
Inputs:   --baseline-summary <csv> --seed <int>
Outputs:  data/measure_structured_candidates_<params>_<YYYYMMDD>.csv
Runtime:  under five seconds through p < 2^20 on the recorded curves.
Validated against: direct ratio enumeration at p=17 and curve membership checks.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from datetime import date
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve, square_root_multiplicities
from lib.heights import WeierstrassCurveQ


FIELDS = (
    "date",
    "candidate",
    "bits",
    "p",
    "a",
    "b",
    "r",
    "bound",
    "x_values_selected",
    "x_fraction",
    "factor_base_size",
    "factor_base_fraction",
    "size_over_sqrt_p",
    "ordered_triples_per_target",
    "reachable_targets_m3",
    "reachable_target_fraction_m3",
    "mean_canonical_height",
    "max_canonical_height",
    "max_height_convergence_delta",
    "height_iterations",
    "membership_method",
    "membership_polylog_certified",
    "elapsed_s",
)


def rational_height_residues(p: int, bound: int) -> bytearray:
    """Mark x = a/b mod p with |a|,|b| < bound and b nonzero."""
    selected = bytearray(p)
    if bound <= 1:
        return selected
    for denominator in range(1, bound):
        inverse = pow(denominator, p - 2, p)
        for numerator in range(-(bound - 1), bound):
            selected[numerator * inverse % p] = 1
    return selected


def factor_base_size_from_x_mask(curve: Curve, selected: Sequence[int]) -> int:
    roots = square_root_multiplicities(curve.p)
    total = 0
    for x, keep in enumerate(selected):
        if keep:
            rhs = (x * x * x + curve.a * x + curve.b) % curve.p
            total += roots[rhs]
    return total


def integral_lift_records(
    curve: Curve, bound: int, height_iterations: int = 7
) -> list[tuple[AffinePoint, float, float]]:
    """Reduce small integral points and estimate their canonical heights."""
    a_lift = curve.a if curve.a <= curve.p // 2 else curve.a - curve.p
    b_lift = curve.b if curve.b <= curve.p // 2 else curve.b - curve.p
    rational_curve = WeierstrassCurveQ.from_coefficients([0, 0, 0, a_lift, b_lift])
    records: dict[AffinePoint, tuple[float, float]] = {}
    for x_integer in range(-(bound - 1), bound):
        rhs = x_integer**3 + a_lift * x_integer + b_lift
        if rhs < 0:
            continue
        y_integer = math.isqrt(rhs)
        if y_integer * y_integer != rhs:
            continue
        for signed_y in {y_integer, -y_integer}:
            point: AffinePoint = (x_integer % curve.p, signed_y % curve.p)
            if not curve.contains(point):
                raise ArithmeticError("integral lift did not reduce to the prime-field curve")
            rational_point = (Fraction(x_integer), Fraction(signed_y))
            estimate = rational_curve.canonical_height_estimate(
                rational_point, iterations=height_iterations
            )
            records[point] = (estimate.value, 0.0 if estimate.delta is None else estimate.delta)
    return [
        (point, records[point][0], records[point][1])
        for point in sorted(records, key=lambda item: (-1, -1) if item is None else item)
    ]


def integral_lift_factor_base(curve: Curve, bound: int) -> list[AffinePoint]:
    return [point for point, _, _ in integral_lift_records(curve, bound)]


def reachable_three_sums(curve: Curve, factor_base: Sequence[AffinePoint]) -> set[AffinePoint]:
    pair_sums = {curve.add(left, right) for left in factor_base for right in factor_base}
    return {curve.add(pair, third) for pair in pair_sums for third in factor_base}


def load_curves(summary_path: Path) -> list[tuple[int, Curve, int]]:
    rows: dict[int, tuple[int, Curve, int]] = {}
    with summary_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            bits = int(row["bits"])
            rows.setdefault(
                bits,
                (bits, Curve(int(row["p"]), int(row["a"]), int(row["b"])), int(row["r"])),
            )
    return [rows[bits] for bits in sorted(rows)]


def measure_curve(bits: int, curve: Curve, order: int) -> list[dict[str, Any]]:
    bound = math.isqrt(curve.p)
    rows: list[dict[str, Any]] = []

    started = time.perf_counter()
    selected = rational_height_residues(curve.p, bound)
    x_count = sum(selected)
    rational_size = factor_base_size_from_x_mask(curve, selected)
    elapsed = time.perf_counter() - started
    rows.append(
        {
            "date": date.today().isoformat(),
            "candidate": "rational_height",
            "bits": bits,
            "p": curve.p,
            "a": curve.a,
            "b": curve.b,
            "r": order,
            "bound": bound,
            "x_values_selected": x_count,
            "x_fraction": f"{x_count / curve.p:.12g}",
            "factor_base_size": rational_size,
            "factor_base_fraction": f"{rational_size / order:.12g}",
            "size_over_sqrt_p": f"{rational_size / math.sqrt(curve.p):.12g}",
            "ordered_triples_per_target": f"{rational_size**3 / order:.12g}",
            "reachable_targets_m3": "not-enumerated-base-too-large",
            "reachable_target_fraction_m3": "not-enumerated-base-too-large",
            "mean_canonical_height": "",
            "max_canonical_height": "",
            "max_height_convergence_delta": "",
            "height_iterations": "",
            "membership_method": "explicit ratio-image table; O(p) build",
            "membership_polylog_certified": 0,
            "elapsed_s": f"{elapsed:.9f}",
        }
    )

    started = time.perf_counter()
    height_iterations = 7
    lift_records = integral_lift_records(curve, bound, height_iterations)
    lift_base = [point for point, _, _ in lift_records]
    heights = [height for _, height, _ in lift_records]
    deltas = [delta for _, _, delta in lift_records]
    reachable = reachable_three_sums(curve, lift_base)
    elapsed = time.perf_counter() - started
    selected_x = {point[0] for point in lift_base if point is not None}
    rows.append(
        {
            "date": date.today().isoformat(),
            "candidate": "integral_lift_proxy",
            "bits": bits,
            "p": curve.p,
            "a": curve.a,
            "b": curve.b,
            "r": order,
            "bound": bound,
            "x_values_selected": len(selected_x),
            "x_fraction": f"{len(selected_x) / curve.p:.12g}",
            "factor_base_size": len(lift_base),
            "factor_base_fraction": f"{len(lift_base) / order:.12g}",
            "size_over_sqrt_p": f"{len(lift_base) / math.sqrt(curve.p):.12g}",
            "ordered_triples_per_target": f"{len(lift_base) ** 3 / order:.12g}",
            "reachable_targets_m3": len(reachable),
            "reachable_target_fraction_m3": f"{len(reachable) / order:.12g}",
            "mean_canonical_height": "" if not heights else f"{sum(heights) / len(heights):.12g}",
            "max_canonical_height": "" if not heights else f"{max(heights):.12g}",
            "max_height_convergence_delta": "" if not deltas else f"{max(deltas):.12g}",
            "height_iterations": height_iterations,
            "membership_method": "unique centered x lift plus integer-square check",
            "membership_polylog_certified": 1,
            "elapsed_s": f"{elapsed:.9f}",
        }
    )
    return rows


def write_csv(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    default_summary = Path(__file__).resolve().parents[1] / "data" / (
        "measure_factor_bases_b16-18-20_t96_r3_s12022026_20260622_summary.csv"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-summary", type=Path, default=default_summary)
    parser.add_argument("--seed", type=int, default=12022028)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    curves = load_curves(args.baseline_summary)
    if args.smoke:
        curves = curves[:1]
    rows: list[dict[str, Any]] = []
    for bits, curve, order in curves:
        rows.extend(measure_curve(bits, curve, order))
    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(str(bits) for bits, _, _ in curves)
    output = args.output or Path(__file__).resolve().parents[1] / "data" / (
        f"measure_structured_candidates_b{bit_label}_s{args.seed}_{stamp}.csv"
    )
    write_csv(output, rows)
    for row in rows:
        print(
            f"candidate={row['candidate']} bits={row['bits']} "
            f"base_size={row['factor_base_size']} base_fraction={row['factor_base_fraction']} "
            f"reachable_m3={row['reachable_target_fraction_m3']}"
        )
    print(f"output={output}")


if __name__ == "__main__":
    main()
