"""
validate_extension_pipeline.py - Exhaust the F_(7^3) complete pipeline.
Sub-goal: P5.4 / SG-10
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_extension_pipeline_<params>_<date>.csv
Runtime:  under 10 seconds in smoke mode; about 15 seconds full
Validated against: exhaustive roots, branch-using group law, and pipeline oracle
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.finite_fields import (
    ExtensionMaskedPoint,
    FieldElement,
    add_complete_extension_weierstrass,
    map_to_curve_svdw_extension,
)
from validate_extension_svdw import CURVE, FIELD, Z, svdw_extension_oracle

AffinePoint = tuple[FieldElement, FieldElement] | None


def _masked(point: AffinePoint) -> ExtensionMaskedPoint:
    return (FIELD.zero, FIELD.zero, 1) if point is None else (point[0], point[1], 0)


def _affine(point: ExtensionMaskedPoint) -> AffinePoint:
    return None if point[2] else (point[0], point[1])


def extension_add_oracle(left: AffinePoint, right: AffinePoint) -> AffinePoint:
    field = FIELD
    curve = CURVE
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2:
        if field.add(y1, y2) == field.zero:
            return None
        slope = field.mul(
            field.add(
                field.mul(field.constant(3), field.square(x1)),
                curve.a,
            ),
            field.inv0(field.mul(field.constant(2), y1)),
        )
    else:
        slope = field.mul(field.sub(y2, y1), field.inv0(field.sub(x2, x1)))
    x3 = field.sub(field.sub(field.square(slope), x1), x2)
    y3 = field.sub(field.mul(slope, field.sub(x1, x3)), y1)
    return x3, y3


def _scalar_table(scalar: int, point: int, table: list[list[int]], identity: int) -> int:
    result = identity
    addend = point
    while scalar:
        if scalar & 1:
            result = table[result][addend]
        addend = table[addend][addend]
        scalar >>= 1
    return result


def validate(seed: int, *, smoke: bool = False) -> dict[str, int | str]:
    field = FIELD
    curve = CURVE
    square_roots: dict[FieldElement, list[FieldElement]] = {}
    for y in field.elements():
        square_roots.setdefault(field.square(y), []).append(y)
    points: list[AffinePoint] = [
        *(
            (x, y)
            for x in field.elements()
            for y in square_roots.get(curve.rhs(x), ())
        ),
        None,
    ]
    if len(points) != 320:
        raise AssertionError("registered extension curve order changed")
    point_indices = {point: index for index, point in enumerate(points)}
    identity = point_indices[None]
    point_limit = 32 if smoke else len(points)
    complete_table = [[identity] * len(points) for _ in points]
    oracle_table = [[identity] * len(points) for _ in points]
    group_matches = 0
    add_schedules: set[tuple[str, ...]] = set()
    for left_index, left in enumerate(points):
        for right_index, right in enumerate(points):
            if smoke and (left_index >= point_limit or right_index >= point_limit):
                continue
            trace: list[str] = []
            actual = _affine(
                add_complete_extension_weierstrass(
                    curve,
                    _masked(left),
                    _masked(right),
                    trace=trace.append,
                )
            )
            expected = extension_add_oracle(left, right)
            group_matches += actual == expected
            complete_table[left_index][right_index] = point_indices[actual]
            oracle_table[left_index][right_index] = point_indices[expected]
            add_schedules.add(tuple(trace))
    group_pairs = point_limit**2 if smoke else len(points) ** 2
    if group_matches != group_pairs or len(add_schedules) != 1:
        raise AssertionError("extension complete group law failed")
    if smoke:
        return {
            "field": "F_(7^3)",
            "curve": "y^2=x^3+X^2*x+X^2",
            "seed": seed,
            "group_order": 320,
            "subgroup_order": 5,
            "cofactor": 64,
            "map_inputs": 0,
            "map_oracle_matches": 0,
            "group_pairs": group_pairs,
            "group_law_matches": group_matches,
            "field_pairs": 0,
            "pipeline_oracle_matches": 0,
            "subgroup_checks": 0,
            "subgroup_support": 0,
            "schedule_variants": len(add_schedules),
        }

    map_indices: list[int] = []
    map_schedules: set[tuple[str, ...]] = set()
    map_matches = 0
    for u in field.elements():
        trace: list[str] = []
        actual = map_to_curve_svdw_extension(curve, Z, u, trace=trace.append)
        expected = svdw_extension_oracle(curve, Z, u)
        map_matches += actual == expected
        map_indices.append(point_indices[actual])
        map_schedules.add(tuple(trace))
    if map_matches != field.order or len(map_schedules) != 1:
        raise AssertionError("extension map validation failed")

    killed_by_five = [
        _scalar_table(5, index, oracle_table, identity) == identity
        for index in range(len(points))
    ]
    support: set[int] = set()
    pipeline_matches = 0
    subgroup_checks = 0
    for left in map_indices:
        for right in map_indices:
            actual = complete_table[left][right]
            expected = oracle_table[left][right]
            for _ in range(6):
                actual = complete_table[actual][actual]
                expected = oracle_table[expected][expected]
            pipeline_matches += actual == expected
            subgroup_checks += killed_by_five[actual]
            support.add(actual)
    field_pairs = field.order**2
    schedule_variants = int(len(map_schedules) == 1 and len(add_schedules) == 1)
    if (
        pipeline_matches != field_pairs
        or subgroup_checks != field_pairs
        or len(support) != 5
        or schedule_variants != 1
    ):
        raise AssertionError("extension two-map pipeline failed")
    return {
        "field": "F_(7^3)",
        "curve": "y^2=x^3+X^2*x+X^2",
        "seed": seed,
        "group_order": 320,
        "subgroup_order": 5,
        "cofactor": 64,
        "map_inputs": field.order,
        "map_oracle_matches": map_matches,
        "group_pairs": group_pairs,
        "group_law_matches": group_matches,
        "field_pairs": field_pairs,
        "pipeline_oracle_matches": pipeline_matches,
        "subgroup_checks": subgroup_checks,
        "subgroup_support": len(support),
        "schedule_variants": schedule_variants,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5411)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = perf_counter()
    row = validate(args.seed, smoke=args.smoke)
    elapsed = perf_counter() - started
    mode = "smoke" if args.smoke else "full"
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"validate_extension_pipeline_{mode}_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(f"wrote 1 row to {output}")
    print(f"validated {row['group_pairs']} group pairs and {row['field_pairs']} field pairs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
