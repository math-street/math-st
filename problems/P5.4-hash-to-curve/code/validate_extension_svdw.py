"""
validate_extension_svdw.py - Exhaustive SvdW validation over F_(7^3).
Sub-goal: P5.4 / SG-10
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_extension_svdw_<params>_<date>.csv
Runtime:  under 1 second on Python 3.13
Validated against: branch-using direct candidate oracle plus exhaustive roots
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
    ExtensionWeierstrassCurve,
    FieldElement,
    PrimePolynomialField,
    find_svdw_z_extension,
    map_to_curve_svdw_extension,
)

FIELD = PrimePolynomialField(7, (2, 0, 0, 1))
CURVE = ExtensionWeierstrassCurve(FIELD, (0, 0, 1), (0, 0, 1))
Z = (0, 0, 3)


def _normalize_sign(
    field: PrimePolynomialField,
    root: FieldElement,
    sign: int,
) -> FieldElement:
    return field.neg(root) if field.sgn0(root) != sign else root


def svdw_extension_oracle(
    curve: ExtensionWeierstrassCurve,
    z: FieldElement,
    u: FieldElement,
) -> tuple[FieldElement, FieldElement]:
    """Evaluate the three candidates with branches and enumerate the root."""

    field = curve.field
    one = field.one
    two = field.constant(2)
    three = field.constant(3)
    four = field.constant(4)
    gz = curve.rhs(z)
    numerator = field.add(field.mul(three, field.square(z)), field.mul(four, curve.a))
    c2 = field.neg(field.mul(z, field.inv0(two)))
    c3 = field.sqrt(field.neg(field.mul(gz, numerator)))
    c3 = _normalize_sign(field, c3, 0)
    c4 = field.neg(field.mul(field.mul(four, gz), field.inv0(numerator)))

    t = field.mul(field.square(u), gz)
    left = field.sub(one, t)
    right = field.add(one, t)
    inverse = field.inv0(field.mul(left, right))
    offset = field.mul(field.mul(field.mul(u, left), inverse), c3)
    x1 = field.sub(c2, offset)
    x2 = field.add(c2, offset)
    x3 = field.mul(field.square(right), inverse)
    x3 = field.add(field.mul(field.square(x3), c4), z)
    if field.is_square(curve.rhs(x1)):
        x = x1
    elif field.is_square(curve.rhs(x2)):
        x = x2
    else:
        x = x3

    roots = [value for value in field.elements() if field.square(value) == curve.rhs(x)]
    if not roots:
        raise ArithmeticError("the SvdW oracle selected a nonsquare")
    requested_sign = field.sgn0(u)
    for root in roots:
        if field.sgn0(root) == requested_sign:
            return x, root
    raise ArithmeticError("no square root has the requested sign")


def validate(seed: int) -> dict[str, int | str]:
    field = FIELD
    curve = CURVE
    if find_svdw_z_extension(curve) != Z:
        raise AssertionError("the preregistered extension-field Z changed")
    schedules: set[tuple[str, ...]] = set()
    oracle_matches = 0
    on_curve = 0
    inverse_checks = 0
    for value in field.elements():
        if value != field.zero:
            inverse_checks += field.mul(value, field.inv0(value)) == field.one
        trace: list[str] = []
        actual = map_to_curve_svdw_extension(curve, Z, value, trace=trace.append)
        expected = svdw_extension_oracle(curve, Z, value)
        oracle_matches += actual == expected
        on_curve += curve.contains(actual)
        schedules.add(tuple(trace))
    if inverse_checks != field.order:
        # Exactly q - 1 nonzero elements should have passed.
        if inverse_checks != field.order - 1:
            raise AssertionError("extension-field inversion check failed")
    if oracle_matches != field.order or on_curve != field.order:
        raise AssertionError("extension-field SvdW validation failed")
    if len(schedules) != 1:
        raise AssertionError("input-dependent mapping schedule")
    schedule = next(iter(schedules))
    return {
        "mapping": "svdw",
        "field": "F_(7^3)",
        "modulus": "x^3+2",
        "curve_a": str(curve.a),
        "curve_b": str(curve.b),
        "z": str(Z),
        "seed": seed,
        "inputs_tested": field.order,
        "inverse_checks": inverse_checks,
        "on_curve": on_curve,
        "oracle_matches": oracle_matches,
        "schedule_variants": len(schedules),
        "schedule_operations": len(schedule),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5404)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = perf_counter()
    row = validate(args.seed)
    elapsed = perf_counter() - started
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"validate_extension_svdw_q343_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(f"wrote 1 row to {output}")
    print(f"validated {row['inputs_tested']} extension-field inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
