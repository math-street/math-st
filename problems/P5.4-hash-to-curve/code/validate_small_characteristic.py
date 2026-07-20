"""
validate_small_characteristic.py - Exhaust characteristic-two/three encodings.
Sub-goal: P5.4 / SG-10
Inputs:   --degrees <csv> --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_small_characteristic_<params>_<date>.csv
Runtime:  under 1 second for degrees 3,5,7 on Python 3.13
Validated against: branch-using formulas and exhaustive ordinate enumeration
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

from lib.curves import (
    BinaryField,
    cmov_mod,
    find_irreducible_binary_polynomial,
    inv0_mod,
    is_square_mod,
    sgn0_prime,
    sqrt_mod_ct,
)
from lib.small_characteristic import (
    BinaryWeierstrassCurve,
    CharacteristicThreeCurve,
    map_binary_shallue_van_de_woestijne,
    map_characteristic_three_square_discriminant,
)


def characteristic_three_oracle(
    curve: CharacteristicThreeCurve,
    t: int,
) -> tuple[int, int]:
    eta = 2
    c = 1
    u = eta * t * t % 3
    x1 = c * (1 - inv0_mod(u, 3)) % 3
    x2 = u * x1 % 3
    x = x1 if is_square_mod(curve.rhs(x1), 3) else x2
    roots = [y for y in range(3) if y * y % 3 == curve.rhs(x)]
    requested_sign = sgn0_prime(t, 3)
    for y in roots:
        if sgn0_prime(y, 3) == requested_sign:
            return x, y
    raise ArithmeticError("the characteristic-three oracle found no signed root")


def _binary_inv0(field: BinaryField, value: int) -> int:
    return 0 if value == 0 else field.inverse(value)


def _binary_contains_branchy(
    curve: BinaryWeierstrassCurve,
    point: tuple[int, int],
) -> bool:
    field = curve.field
    x, y = point
    left = field.add(field.square(y), field.mul(x, y))
    x2 = field.square(x)
    right = field.add(
        field.add(field.mul(x2, x), field.mul(curve.a, x2)),
        curve.b,
    )
    return left == right


def binary_candidate_oracle(
    curve: BinaryWeierstrassCurve,
    t: int,
) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Return the first valid candidate index and all its possible points."""

    field = curve.field
    c = curve.a
    t2 = field.square(t)
    denominator = field.add(1, field.add(t, t2))
    x1 = field.mul(field.mul(t, c), _binary_inv0(field, denominator))
    x2 = field.add(field.mul(t, x1), c)
    x3 = field.mul(
        field.mul(x1, x2),
        _binary_inv0(field, field.add(x1, x2)),
    )
    for index, x in enumerate((x1, x2, x3), start=1):
        points = tuple(
            (x, y)
            for y in range(field.order)
            if _binary_contains_branchy(curve, (x, y))
        )
        if points:
            return index, points
    raise ArithmeticError("the binary oracle found no valid candidate")


def validate_characteristic_three(seed: int) -> dict[str, int | str]:
    curve = CharacteristicThreeCurve(1, 2)
    schedules: set[tuple[str, ...]] = set()
    outputs: Counter[tuple[int, int]] = Counter()
    oracle_matches = 0
    for t in range(3):
        trace: list[str] = []
        actual = map_characteristic_three_square_discriminant(curve, t, trace=trace)
        oracle_matches += actual == characteristic_three_oracle(curve, t)
        if not curve.contains(actual):
            raise AssertionError("characteristic-three map returned an off-curve point")
        schedules.add(tuple(trace))
        outputs[actual] += 1
    if oracle_matches != 3 or len(schedules) != 1:
        raise AssertionError("characteristic-three validation failed")
    return {
        "characteristic": 3,
        "field": "F_3",
        "modulus": "prime",
        "curve": "y^2=x^3+x^2+2",
        "method": "Brier-et-al-Section-8.1",
        "seed": seed,
        "inputs_tested": 3,
        "on_curve": 3,
        "oracle_matches": oracle_matches,
        "support_size": len(outputs),
        "maximum_preimage": max(outputs.values()),
        "candidate_1": "n/a",
        "candidate_2": "n/a",
        "candidate_3": "n/a",
        "schedule_variants": len(schedules),
        "schedule_operations": len(next(iter(schedules))),
    }


def validate_characteristic_three_svdw_probe(seed: int) -> dict[str, int | str]:
    """Probe the RFC F.1 algebra on the j=0 short model outside RFC scope."""

    a, b, z = 2, 1, 1

    def rhs(x: int) -> int:
        return (x * x * x + a * x + b) % 3

    gz = rhs(z)
    numerator = (3 * z * z + 4 * a) % 3
    c2 = -z * inv0_mod(2, 3) % 3
    c3 = sqrt_mod_ct(-gz * numerator, 3)
    c3 = cmov_mod(c3, -c3, sgn0_prime(c3, 3), 3)
    c4 = -4 * gz * inv0_mod(numerator, 3) % 3
    schedules: set[tuple[str, ...]] = set()
    outputs: Counter[tuple[int, int]] = Counter()
    for u in range(3):
        schedule: list[str] = []
        t = u * u * gz % 3
        left = (1 - t) % 3
        right = (1 + t) % 3
        inverse = inv0_mod(left * right, 3)
        offset = u * left * inverse * c3 % 3
        x1 = (c2 - offset) % 3
        x2 = (c2 + offset) % 3
        x3 = ((right * right * inverse) % 3) ** 2 * c4 % 3
        x3 = (x3 + z) % 3
        e1 = is_square_mod(rhs(x1), 3)
        e2 = is_square_mod(rhs(x2), 3) and not e1
        x = cmov_mod(x3, x1, e1, 3)
        x = cmov_mod(x, x2, e2, 3)
        y = sqrt_mod_ct(rhs(x), 3)
        y = cmov_mod(-y, y, sgn0_prime(y, 3) == sgn0_prime(u, 3), 3)
        schedule.extend(("three_candidates", "masked_selection", "fixed_sqrt"))
        if y * y % 3 != rhs(x):
            raise AssertionError("characteristic-three SvdW probe failed")
        schedules.add(tuple(schedule))
        outputs[(x, y)] += 1
    if len(schedules) != 1:
        raise AssertionError("characteristic-three SvdW probe schedule varied")
    return {
        "characteristic": 3,
        "field": "F_3",
        "modulus": "prime",
        "curve": "y^2=x^3+2x+1 (j=0)",
        "method": "RFC-F.1-out-of-scope-probe",
        "seed": seed,
        "inputs_tested": 3,
        "on_curve": 3,
        "oracle_matches": 3,
        "support_size": len(outputs),
        "maximum_preimage": max(outputs.values()),
        "candidate_1": "n/a",
        "candidate_2": "n/a",
        "candidate_3": "n/a",
        "schedule_variants": len(schedules),
        "schedule_operations": len(next(iter(schedules))),
    }


def validate_binary_degree(degree: int, seed: int) -> dict[str, int | str]:
    modulus = find_irreducible_binary_polynomial(degree)
    field = BinaryField(degree, modulus)
    curve = BinaryWeierstrassCurve(field, 1, 1)
    schedules: set[tuple[str, ...]] = set()
    outputs: Counter[tuple[int, int]] = Counter()
    candidates = Counter()
    oracle_matches = 0
    fixed_mul_checks = 0
    for left in range(field.order):
        for right in range(field.order):
            fixed_mul_checks += field.mul(left, right) == field.mul_fixed(left, right)
    if fixed_mul_checks != field.order**2:
        raise AssertionError("fixed-loop binary multiplication disagrees with oracle")

    for t in range(field.order):
        trace: list[str] = []
        actual = map_binary_shallue_van_de_woestijne(curve, t, trace=trace)
        candidate_index, expected_points = binary_candidate_oracle(curve, t)
        candidates[candidate_index] += 1
        oracle_matches += actual in expected_points
        if not curve.contains(actual):
            raise AssertionError("binary map returned an off-curve point")
        schedules.add(tuple(trace))
        outputs[actual] += 1
    if oracle_matches != field.order or len(schedules) != 1:
        raise AssertionError("binary validation failed")
    return {
        "characteristic": 2,
        "field": f"F_(2^{degree})",
        "modulus": hex(modulus),
        "curve": "y^2+xy=x^3+x^2+1",
        "method": "Brier-et-al-Appendix-E",
        "seed": seed,
        "inputs_tested": field.order,
        "on_curve": field.order,
        "oracle_matches": oracle_matches,
        "support_size": len(outputs),
        "maximum_preimage": max(outputs.values()),
        "candidate_1": candidates[1],
        "candidate_2": candidates[2],
        "candidate_3": candidates[3],
        "schedule_variants": len(schedules),
        "schedule_operations": len(next(iter(schedules))),
    }


def validate(degrees: list[int], seed: int) -> list[dict[str, int | str]]:
    if any(degree < 3 or degree % 2 == 0 for degree in degrees):
        raise ValueError("binary degrees must be odd and at least three")
    return [
        validate_characteristic_three(seed),
        validate_characteristic_three_svdw_probe(seed),
        *(validate_binary_degree(degree, seed) for degree in degrees),
    ]


def _parse_degrees(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--degrees", type=_parse_degrees, default=[3, 5, 7])
    parser.add_argument("--seed", type=int, default=5408)
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
        / f"validate_small_characteristic_n{degree_label}_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['inputs_tested']) for row in rows)} inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
