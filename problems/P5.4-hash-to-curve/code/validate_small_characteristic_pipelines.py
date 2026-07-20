"""
validate_small_characteristic_pipelines.py - Exhaust complete two-map pipelines.
Sub-goal: P5.4 / SG-10
Inputs:   --degrees <csv> --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_small_characteristic_pipelines_<params>_<date>.csv
Runtime:  under 10 seconds in smoke mode
Validated against: exhaustive branch-using group and scalar-multiplication oracles
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import BinaryField, find_irreducible_binary_polynomial
from lib.small_characteristic import (
    BinaryWeierstrassCurve,
    CharacteristicThreeCurve,
    MaskedPoint,
    add_complete_binary,
    add_complete_characteristic_three,
    map_binary_shallue_van_de_woestijne,
    map_characteristic_three_square_discriminant,
)

AffinePoint = tuple[int, int] | None


def _masked(point: AffinePoint) -> MaskedPoint:
    return (0, 0, 1) if point is None else (point[0], point[1], 0)


def _affine(point: MaskedPoint) -> AffinePoint:
    return None if point[2] else (point[0], point[1])


def characteristic_three_add_oracle(
    curve: CharacteristicThreeCurve,
    left: AffinePoint,
    right: AffinePoint,
) -> AffinePoint:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2:
        if (y1 + y2) % 3 == 0:
            return None
        slope = 2 * curve.a * x1 * pow(2 * y1, -1, 3) % 3
    else:
        slope = (y2 - y1) * pow((x2 - x1) % 3, -1, 3) % 3
    x3 = (slope * slope - curve.a - x1 - x2) % 3
    y3 = (slope * (x1 - x3) - y1) % 3
    return x3, y3


def binary_add_oracle(
    curve: BinaryWeierstrassCurve,
    left: AffinePoint,
    right: AffinePoint,
) -> AffinePoint:
    if left is None:
        return right
    if right is None:
        return left
    field = curve.field
    x1, y1 = left
    x2, y2 = right
    if x1 == x2:
        if y2 == field.add(y1, x1) or x1 == 0:
            return None
        slope = field.add(x1, field.div(y1, x1))
        x3 = field.add(field.add(field.square(slope), slope), curve.a)
        y3 = field.add(
            field.square(x1),
            field.mul(field.add(slope, 1), x3),
        )
        return x3, y3
    slope = field.div(field.add(y1, y2), field.add(x1, x2))
    x3 = field.add(
        field.add(field.square(slope), slope),
        field.add(field.add(x1, x2), curve.a),
    )
    y3 = field.add(
        field.add(field.mul(slope, field.add(x1, x3)), x3),
        y1,
    )
    return x3, y3


def _scalar_mul(
    scalar: int,
    point: AffinePoint,
    add,
) -> AffinePoint:
    result: AffinePoint = None
    addend = point
    while scalar:
        if scalar & 1:
            result = add(result, addend)
        addend = add(addend, addend)
        scalar >>= 1
    return result


def validate_characteristic_three(seed: int) -> dict[str, int | str]:
    curve = CharacteristicThreeCurve(1, 2)
    points: list[AffinePoint] = [
        *((x, y) for x in range(3) for y in range(3) if curve.contains((x, y))),
        None,
    ]
    add = lambda left, right: characteristic_three_add_oracle(curve, left, right)
    group_matches = 0
    for left in points:
        for right in points:
            group_matches += _affine(
                add_complete_characteristic_three(curve, _masked(left), _masked(right))
            ) == add(left, right)
    if len(points) != 3 or group_matches != 9:
        raise AssertionError("characteristic-three complete group law failed")

    schedules: set[tuple[str, ...]] = set()
    support: Counter[AffinePoint] = Counter()
    oracle_matches = 0
    subgroup_checks = 0
    for u0 in range(3):
        for u1 in range(3):
            trace: list[str] = []
            q0 = map_characteristic_three_square_discriminant(curve, u0, trace=trace)
            q1 = map_characteristic_three_square_discriminant(curve, u1, trace=trace)
            actual = _affine(
                add_complete_characteristic_three(
                    curve,
                    _masked(q0),
                    _masked(q1),
                    trace=trace,
                )
            )
            expected = add(q0, q1)
            oracle_matches += actual == expected
            subgroup_checks += _scalar_mul(3, actual, add) is None
            support[actual] += 1
            schedules.add(tuple(trace))
    if (oracle_matches, subgroup_checks, len(schedules), len(support)) != (9, 9, 1, 3):
        raise AssertionError("characteristic-three two-map pipeline failed")
    return {
        "characteristic": 3,
        "field": "F_3",
        "curve": "y^2=x^3+x^2+2",
        "seed": seed,
        "group_order": 3,
        "subgroup_order": 3,
        "cofactor": 1,
        "group_pairs": 9,
        "group_law_matches": group_matches,
        "field_pairs": 9,
        "pipeline_oracle_matches": oracle_matches,
        "subgroup_checks": subgroup_checks,
        "subgroup_support": len(support),
        "schedule_variants": len(schedules),
    }


def validate_binary_degree(degree: int, seed: int) -> dict[str, int | str]:
    field = BinaryField(degree, find_irreducible_binary_polynomial(degree))
    curve = BinaryWeierstrassCurve(field, 1, 1)
    points: list[AffinePoint] = [
        *(
            (x, y)
            for x in range(field.order)
            for y in range(field.order)
            if curve.contains((x, y))
        ),
        None,
    ]
    expected_orders = {3: (14, 7), 5: (22, 11), 7: (142, 71)}
    group_order, subgroup_order = expected_orders[degree]
    if len(points) != group_order:
        raise AssertionError("binary fixture group order changed")
    add = lambda left, right: binary_add_oracle(curve, left, right)
    group_matches = 0
    for left in points:
        for right in points:
            group_matches += _affine(
                add_complete_binary(curve, _masked(left), _masked(right))
            ) == add(left, right)
    if group_matches != group_order**2:
        raise AssertionError("binary complete group law failed")

    schedules: set[tuple[str, ...]] = set()
    support: Counter[AffinePoint] = Counter()
    oracle_matches = 0
    subgroup_checks = 0
    for u0 in range(field.order):
        for u1 in range(field.order):
            trace: list[str] = []
            q0 = map_binary_shallue_van_de_woestijne(curve, u0, trace=trace)
            q1 = map_binary_shallue_van_de_woestijne(curve, u1, trace=trace)
            summed = add_complete_binary(
                curve,
                _masked(q0),
                _masked(q1),
                trace=trace,
            )
            cleared = add_complete_binary(curve, summed, summed, trace=trace)
            actual = _affine(cleared)
            expected = _scalar_mul(2, add(q0, q1), add)
            oracle_matches += actual == expected
            subgroup_checks += _scalar_mul(subgroup_order, actual, add) is None
            support[actual] += 1
            schedules.add(tuple(trace))
    field_pairs = field.order**2
    if (
        oracle_matches != field_pairs
        or subgroup_checks != field_pairs
        or len(schedules) != 1
        or len(support) != subgroup_order
    ):
        raise AssertionError("binary two-map pipeline failed")
    return {
        "characteristic": 2,
        "field": f"F_(2^{degree})",
        "curve": "y^2+xy=x^3+x^2+1",
        "seed": seed,
        "group_order": group_order,
        "subgroup_order": subgroup_order,
        "cofactor": 2,
        "group_pairs": group_order**2,
        "group_law_matches": group_matches,
        "field_pairs": field_pairs,
        "pipeline_oracle_matches": oracle_matches,
        "subgroup_checks": subgroup_checks,
        "subgroup_support": len(support),
        "schedule_variants": len(schedules),
    }


def validate(degrees: list[int], seed: int) -> list[dict[str, int | str]]:
    if any(degree not in (3, 5, 7) for degree in degrees):
        raise ValueError("registered binary degrees are 3, 5, and 7")
    return [
        validate_characteristic_three(seed),
        *(validate_binary_degree(degree, seed) for degree in degrees),
    ]


def _parse_degrees(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--degrees", type=_parse_degrees, default=[3, 5, 7])
    parser.add_argument("--seed", type=int, default=5410)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    degrees = [3] if args.smoke else args.degrees
    started = perf_counter()
    rows = validate(degrees, args.seed)
    elapsed = perf_counter() - started
    degree_label = "-".join(str(degree) for degree in degrees)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"validate_small_characteristic_pipelines_n{degree_label}_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['field_pairs']) for row in rows)} field pairs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
