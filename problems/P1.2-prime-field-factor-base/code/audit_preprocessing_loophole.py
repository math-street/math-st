"""
audit_preprocessing_loophole.py — expose the nonuniform preprocessing loophole.

For a cyclic group of prime order r, positional digits give a factor base of
size at most m*ceil(r**(1/m)) that covers every target with exactly m terms.
The online decoder below is fast only because preprocessing stores one
decomposition for each of the r targets.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve, is_prime


FIELDS = (
    "date",
    "p",
    "a",
    "b",
    "r",
    "m",
    "radix",
    "radix_power",
    "factor_base_size",
    "factor_base_upper_bound",
    "sqrt_p_baseline",
    "base_over_sqrt_p",
    "target_table_entries",
    "stored_point_references",
    "coverage_targets",
    "coverage_fraction",
    "invalid_memberships",
    "invalid_sums",
    "preprocessing_target_steps",
    "preprocessing_s",
    "online_lookups",
    "online_lookup_mean_ns",
)


def ceil_nth_root(value: int, degree: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    if degree < 1:
        raise ValueError("degree must be positive")
    low, high = 1, value
    while low < high:
        middle = (low + high) // 2
        if middle**degree >= value:
            high = middle
        else:
            low = middle + 1
    return low


@dataclass(frozen=True)
class DigitTable:
    radix: int
    factor_base: frozenset[AffinePoint]
    decompositions: dict[AffinePoint, tuple[AffinePoint, ...]]
    preprocessing_s: float
    invalid_memberships: int
    invalid_sums: int


def build_digit_table(
    curve: Curve,
    order: int,
    generator: AffinePoint,
    summands: int,
) -> DigitTable:
    """Build the deliberately nonuniform all-target decomposition table."""
    if summands < 1:
        raise ValueError("summands must be positive")
    if generator is None or not curve.contains(generator):
        raise ValueError("generator must be an affine point on the curve")
    if curve.scalar_mul(order, generator) is not None:
        raise ValueError("the supplied point does not have the supplied order")

    radix = ceil_nth_root(order, summands)
    digit_points: list[list[AffinePoint]] = []
    factor_base: set[AffinePoint] = set()
    for position in range(summands):
        place = radix**position
        points = [curve.scalar_mul(digit * place, generator) for digit in range(radix)]
        digit_points.append(points)
        factor_base.update(points)

    started = time.perf_counter()
    decompositions: dict[AffinePoint, tuple[AffinePoint, ...]] = {}
    invalid_memberships = 0
    invalid_sums = 0
    target: AffinePoint = None
    for scalar in range(order):
        remaining = scalar
        terms: list[AffinePoint] = []
        for position in range(summands):
            digit = remaining % radix
            remaining //= radix
            terms.append(digit_points[position][digit])
        if remaining:
            raise ArithmeticError("radix did not provide enough digit positions")
        decomposition = tuple(terms)
        invalid_memberships += sum(point not in factor_base for point in decomposition)
        total: AffinePoint = None
        for point in decomposition:
            total = curve.add(total, point)
        if total != target:
            invalid_sums += 1
        if target in decompositions:
            raise ArithmeticError("generator walk repeated before the supplied order")
        decompositions[target] = decomposition
        target = curve.add(target, generator)
    if target is not None:
        raise ArithmeticError("generator walk did not close at the supplied order")

    return DigitTable(
        radix=radix,
        factor_base=frozenset(factor_base),
        decompositions=decompositions,
        preprocessing_s=time.perf_counter() - started,
        invalid_memberships=invalid_memberships,
        invalid_sums=invalid_sums,
    )


def audit_curve(
    curve: Curve,
    order: int,
    summands: int,
) -> dict[str, int | float | str]:
    if not is_prime(order):
        raise ValueError("this audit expects a prime-order group")
    generator = curve.first_affine_point()
    if curve.scalar_mul(order, generator) is not None:
        raise ArithmeticError("first affine point does not generate the supplied prime-order group")

    table = build_digit_table(curve, order, generator, summands)
    if len(table.factor_base) > summands * table.radix:
        raise ArithmeticError("factor-base union exceeded its construction bound")
    if len(table.decompositions) != order:
        raise ArithmeticError("target table does not cover the group")

    lookup_started = time.perf_counter_ns()
    target: AffinePoint = None
    for _ in range(order):
        decomposition = table.decompositions[target]
        if len(decomposition) != summands:
            raise ArithmeticError("online table returned the wrong number of summands")
        target = curve.add(target, generator)
    lookup_elapsed_ns = time.perf_counter_ns() - lookup_started
    sqrt_baseline = math.isqrt(curve.p)
    return {
        "date": date.today().isoformat(),
        "p": curve.p,
        "a": curve.a,
        "b": curve.b,
        "r": order,
        "m": summands,
        "radix": table.radix,
        "radix_power": table.radix**summands,
        "factor_base_size": len(table.factor_base),
        "factor_base_upper_bound": summands * table.radix,
        "sqrt_p_baseline": sqrt_baseline,
        "base_over_sqrt_p": f"{len(table.factor_base) / sqrt_baseline:.12g}",
        "target_table_entries": len(table.decompositions),
        "stored_point_references": len(table.decompositions) * (summands + 1),
        "coverage_targets": len(table.decompositions),
        "coverage_fraction": "1",
        "invalid_memberships": table.invalid_memberships,
        "invalid_sums": table.invalid_sums,
        "preprocessing_target_steps": order,
        "preprocessing_s": f"{table.preprocessing_s:.9f}",
        "online_lookups": order,
        "online_lookup_mean_ns": f"{lookup_elapsed_ns / order:.3f}",
    }


def write_row(path: Path, row: dict[str, int | float | str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow(row)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=65519)
    parser.add_argument("--a", type=int, default=20289)
    parser.add_argument("--b", type=int, default=54970)
    parser.add_argument("--order", type=int, default=65537)
    parser.add_argument("--summands", type=int, default=3)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.p, args.a, args.b, args.order = 17, 2, 2, 19
    curve = Curve(args.p, args.a, args.b)
    row = audit_curve(curve, args.order, args.summands)
    if args.smoke:
        for field in FIELDS:
            print(f"{field}={row[field]}")
        return
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"audit_preprocessing_loophole_p{args.p}_m{args.summands}_{date.today().strftime('%Y%m%d')}.csv"
    )
    write_row(output, row)
    for field in FIELDS:
        print(f"{field}={row[field]}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
