"""Probe canonical finite-field lifts in the Buell point-to-form formula.

Sub-goal: P1.5 / SG-26
Inputs:   [--smoke] [--output-dir PATH]
Outputs:  data/probe_buell_reduction_<profile>_20260710.csv
Runtime:  under 2 seconds for the default complete toy matrix
Validated against: exhaustive order 29 for (B,C,D,p)=(0,1,-7,23)
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Iterable, NamedTuple


Point = tuple[int, int] | None
DATE_TAG = "20260710"


class Case(NamedTuple):
    B: int
    C: int
    D: int
    p: int
    r: int

    @property
    def label(self) -> str:
        return f"B{self.B}_C{self.C}_D{self.D}_p{self.p}"


FULL_CASES = (
    Case(0, 1, -7, 23, 29),
    Case(0, 1, -7, 37, 23),
    Case(0, 1, -7, 43, 19),
    Case(1, 1, -7, 47, 23),
    Case(1, 1, -7, 59, 23),
    Case(-1, 1, -11, 29, 19),
    Case(-1, 1, -11, 37, 23),
    Case(1, 2, -3, 29, 13),
    Case(1, 2, -3, 41, 37),
    Case(1, 2, -3, 47, 19),
)
SMOKE_CASES = FULL_CASES[:2]


def inv_mod(value: int, p: int) -> int:
    return pow(value % p, -1, p)


def internal_coefficients(case: Case) -> tuple[int, int, int]:
    """Return coefficients for Y^2=X^3+a2*X^2+a4*X+a6, X=4x,Y=4y."""

    return 4 * case.B, 16 * case.C, 16 * case.D


def add_points(case: Case, left: Point, right: Point) -> Point:
    if left is None:
        return right
    if right is None:
        return left
    p = case.p
    a2, a4, _ = internal_coefficients(case)
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if left == right:
        if y1 % p == 0:
            return None
        slope = (3 * x1 * x1 + 2 * a2 * x1 + a4) * inv_mod(2 * y1, p) % p
    else:
        slope = (y2 - y1) * inv_mod(x2 - x1, p) % p
    x3 = (slope * slope - a2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    return x3, y3


def scalar_mul(case: Case, scalar: int, point: Point) -> Point:
    result: Point = None
    addend = point
    k = scalar
    while k:
        if k & 1:
            result = add_points(case, result, addend)
        addend = add_points(case, addend, addend)
        k >>= 1
    return result


def original_points(case: Case) -> list[tuple[int, int]]:
    points: list[tuple[int, int]] = []
    p = case.p
    for x in range(p):
        rhs = (4 * x * (x * x + case.B * x + case.C) + case.D) % p
        for y in range(p):
            if y * y % p == rhs:
                points.append((x, y))
    return points


def to_internal(case: Case, point: tuple[int, int]) -> tuple[int, int]:
    x, y = point
    return 4 * x % case.p, 4 * y % case.p


def to_original(case: Case, point: tuple[int, int]) -> tuple[int, int]:
    inverse_four = inv_mod(4, case.p)
    X, Y = point
    return X * inverse_four % case.p, Y * inverse_four % case.p


def is_nonsingular(case: Case) -> bool:
    p = case.p
    a2, a4, a6 = internal_coefficients(case)
    for x in range(p):
        value = (x**3 + a2 * x * x + a4 * x + a6) % p
        derivative = (3 * x * x + 2 * a2 * x + a4) % p
        if value == 0 and derivative == 0:
            return False
    return True


def find_generator(case: Case, affine_points: Iterable[tuple[int, int]]) -> tuple[Point, int]:
    internal_points = [to_internal(case, point) for point in affine_points]
    order = len(internal_points) + 1
    if order % case.r:
        raise ValueError(f"r={case.r} does not divide curve order {order} for {case.label}")
    cofactor = order // case.r
    for point in internal_points:
        candidate = scalar_mul(case, cofactor, point)
        if candidate is not None and scalar_mul(case, case.r, candidate) is None:
            return candidate, order
    raise ValueError(f"no order-{case.r} generator found for {case.label}")


def lifted_form_data(case: Case, point: tuple[int, int]) -> tuple[int, int, bool]:
    x, y = to_original(case, point)
    third = x * x + case.B * x + case.C
    discriminant = y * y - 4 * x * third
    primitive = math.gcd(math.gcd(abs(x), abs(y)), abs(third)) == 1
    return discriminant, (discriminant - case.D) // case.p, primitive


def analyze_case(case: Case) -> dict[str, object]:
    if not is_nonsingular(case):
        raise ValueError(f"singular reduction: {case.label}")
    affine = original_points(case)
    generator, curve_order = find_generator(case, affine)
    assert generator is not None
    discriminants: list[int] = []
    quotients: list[int] = []
    primitive_count = 0
    subgroup_points: list[tuple[int, int]] = []
    for scalar in range(1, case.r):
        point = scalar_mul(case, scalar, generator)
        if point is None:
            raise AssertionError("nonzero scalar reached the identity")
        subgroup_points.append(to_original(case, point))
        discriminant, quotient, primitive = lifted_form_data(case, point)
        if (discriminant - case.D) % case.p:
            raise AssertionError("lifted discriminant lost its model congruence")
        discriminants.append(discriminant)
        quotients.append(quotient)
        primitive_count += int(primitive)
    unique_discriminants = sorted(set(discriminants))
    generator_original = to_original(case, generator)
    return {
        "case": case.label,
        "B": case.B,
        "C": case.C,
        "D": case.D,
        "p": case.p,
        "curve_order": curve_order,
        "r": case.r,
        "generator_x": generator_original[0],
        "generator_y": generator_original[1],
        "nonzero_points": case.r - 1,
        "distinct_lifted_discriminants": len(unique_discriminants),
        "fixed_discriminant_points": sum(value == case.D for value in discriminants),
        "negative_discriminant_points": sum(value < 0 for value in discriminants),
        "primitive_form_points": primitive_count,
        "min_k": min(quotients),
        "max_k": max(quotients),
        "all_congruent_mod_p": all((value - case.D) % case.p == 0 for value in discriminants),
        "one_fixed_target": len(unique_discriminants) == 1 and unique_discriminants[0] == case.D,
        "lifted_discriminants": ";".join(str(value) for value in unique_discriminants),
        "subgroup_points": ";".join(f"{x}:{y}" for x, y in subgroup_points),
    }


def write_rows(rows: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="run two cases")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    args = parser.parse_args()
    profile = "smoke" if args.smoke else "full"
    cases = SMOKE_CASES if args.smoke else FULL_CASES
    rows = [analyze_case(case) for case in cases]
    output_path = args.output_dir / f"probe_buell_reduction_{profile}_{DATE_TAG}.csv"
    write_rows(rows, output_path)
    for row in rows:
        print(
            f"{row['case']} order={row['curve_order']} r={row['r']} "
            f"disc={row['distinct_lifted_discriminants']} "
            f"fixed={row['fixed_discriminant_points']} "
            f"one_target={row['one_fixed_target']}"
        )


if __name__ == "__main__":
    main()
