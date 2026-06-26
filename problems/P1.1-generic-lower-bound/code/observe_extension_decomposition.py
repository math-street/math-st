"""
observe_extension_decomposition.py — trace a Gaudry/Diem-style toy relation.
Sub-goal: P1.1 / validation
Inputs:   --q 5 --degree 3 --trials 1 --seed 12022026
Outputs:  data/observe_extension_decomposition_q5_n3_20260626.csv
Runtime:  under 1 second over F_(5^3)
Validated against: direct point lifting and group-law verification
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.extension_curves import ExtensionCurve, subfield_x_factor_base
from lib.finite_fields import ExtensionElement, cubic_field


def extension_f3(
    x1: ExtensionElement,
    x2: ExtensionElement,
    x3: ExtensionElement,
    a: ExtensionElement,
    b: ExtensionElement,
) -> ExtensionElement:
    """Evaluate Semaev's f3 in the ambient extension field."""
    return (
        (x1 - x2) ** 2 * x3**2
        - 2 * ((x1 + x2) * (x1 * x2 + a) + 2 * b) * x3
        + (x1 * x2 - a) ** 2
        - 4 * b * (x1 + x2)
    )


def run() -> dict[str, int | str]:
    field = cubic_field(5)
    curve = ExtensionCurve(
        field,
        field.element((0, 3, 4)),
        field.element((4, 3, 1)),
    )
    roots = curve.square_roots()
    factor_base = subfield_x_factor_base(curve, roots)
    source = factor_base[0]
    target = curve.add(source, source)
    if target is None or field.is_base_element(target[0]):
        raise ArithmeticError("fixture target must have a non-base-field x-coordinate")

    base_x_values = list(field.base_elements())
    zero_pairs: list[tuple[ExtensionElement, ExtensionElement]] = []
    for x1 in base_x_values:
        for x2 in base_x_values:
            if not extension_f3(x1, x2, target[0], curve.a, curve.b):
                zero_pairs.append((x1, x2))

    verified = []
    sign_candidates = 0
    for x1, x2 in zero_pairs:
        first_points = [point for point in factor_base if point[0] == x1]
        second_points = [point for point in factor_base if point[0] == x2]
        for first in first_points:
            for second in second_points:
                sign_candidates += 1
                if curve.add(first, second) == target:
                    verified.append((first, second))

    expected_pair = (source, source)
    if zero_pairs != [(source[0], source[0])]:
        raise ArithmeticError("unexpected f3 zero set in the fixed fixture")
    if verified != [expected_pair]:
        raise ArithmeticError("summation-polynomial relation failed point verification")

    return {
        "q": field.q,
        "extension_degree": field.degree,
        "field_modulus_ascending": str(field.modulus),
        "curve_a_basis": str(curve.a.coefficients),
        "curve_b_basis": str(curve.b.coefficients),
        "factor_base_points": len(factor_base),
        "factor_base_x_candidates": len(base_x_values),
        "target_x_basis": str(target[0].coefficients),
        "target_y_basis": str(target[1].coefficients),
        "basis_coefficient_equations": field.degree,
        "f3_evaluations": len(base_x_values) ** 2,
        "polynomial_zero_pairs": len(zero_pairs),
        "point_sign_candidates": sign_candidates,
        "group_relation_checks": sign_candidates,
        "verified_ordered_decompositions": len(verified),
        "polynomial_system_solves": 1,
        "subfield_structure_uses": 1,
        "pairing_evaluations": 0,
        "p_adic_lifts": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--degree", type=int, default=3)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--seed", type=int, default=12022026)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if (args.q, args.degree, args.trials, args.seed) != (5, 3, 1, 12022026):
        raise ValueError("the validated fixture supports q=5, degree=3, trials=1, seed=12022026")
    row = run()
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "observe_extension_decomposition_q5_n3_20260626.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(output)
    print(row)


if __name__ == "__main__":
    main()
