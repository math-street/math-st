"""
observe_ghs_transfer.py -- trace an exact genus-one GHS transfer fixture.
Sub-goal: P1.1 / remaining GHS end-to-end validation
Inputs:   --q 4 --degree 5 --secret 2 --seed 0
Outputs:  data/observe_ghs_transfer_q4_n5_r3_20260629.csv
Runtime:  under 1 second over F_(2^10)/F_(2^2)
Validated against: the odd-degree m=1 fixed-field equation and exhaustive
                   scalar preservation on the order-three source subgroup
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.binary_curves import BinaryEllipticCurve, BinaryPoint
from lib.curves import BinaryField, find_irreducible_binary_polynomial
from lib.ghs_transfer import (
    GenusOneGHSTransfer,
    fixed_subfield_elements,
    is_in_subfield,
)


def format_point(point: BinaryPoint) -> str:
    if point is None:
        return "infinity"
    return f"[{point[0]},{point[1]}]"


def run() -> dict[str, int | str]:
    field = BinaryField(10, find_irreducible_binary_polynomial(10))
    source = BinaryEllipticCurve(field, a=234, b=236)
    descent = GenusOneGHSTransfer.from_source(source, 2, twist=3)
    base_values = fixed_subfield_elements(field, 2)

    target_preimage = (237, 0)
    source_generator = descent.inverse_isomorphism(target_preimage)
    image_generator = descent.transfer(source_generator)
    subgroup_order = source.point_order(source_generator)
    if subgroup_order != 3 or descent.target.point_order(image_generator) != subgroup_order:
        raise ArithmeticError("the transfer did not preserve the fixed prime subgroup")
    if is_in_subfield(field, source.a, 2):
        raise ArithmeticError("the source coefficient must be genuinely outside the base field")
    if source_generator is None or all(
        is_in_subfield(field, coordinate, 2) for coordinate in source_generator
    ):
        raise ArithmeticError("the source generator must be genuinely extension-field-valued")

    for scalar in range(subgroup_order):
        source_multiple = source.scalar_mul(scalar, source_generator)
        if descent.transfer(source_multiple) != descent.target.scalar_mul(
            scalar,
            image_generator,
        ):
            raise ArithmeticError("the transfer failed exhaustive scalar preservation")

    secret = 2
    source_target = source.scalar_mul(secret, source_generator)
    image_target = descent.transfer(source_target)
    recovered = next(
        scalar
        for scalar in range(subgroup_order)
        if descent.target.scalar_mul(scalar, image_generator) == image_target
    )
    target_points = descent.target.points(base_values)
    if len(target_points) != 6 or recovered != secret:
        raise ArithmeticError("the fixed auxiliary-curve DLP fixture changed")

    return {
        "base_field_order": 4,
        "relative_extension_degree": descent.extension_degree,
        "ambient_absolute_degree": field.degree,
        "ambient_modulus_binary": bin(field.modulus),
        "source_a": source.a,
        "source_b": source.b,
        "source_a_in_base_field": 0,
        "target_a_relative_trace": descent.target.a,
        "target_b": descent.target.b,
        "artin_schreier_twist": descent.twist,
        "source_generator": format_point(source_generator),
        "source_target": format_point(source_target),
        "image_generator": format_point(image_generator),
        "image_target": format_point(image_target),
        "source_subgroup_order": subgroup_order,
        "auxiliary_curve_points": len(target_points),
        "frobenius_conjugates_summed": descent.extension_degree,
        "scalar_relations_checked": subgroup_order,
        "secret": secret,
        "recovered": recovered,
        "auxiliary_dlp_solves": 1,
        "conorm_norm_transfers": subgroup_order + 2,
        "higher_genus_claims": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=4)
    parser.add_argument("--degree", type=int, default=5)
    parser.add_argument("--secret", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if (args.q, args.degree, args.secret, args.seed) != (4, 5, 2, 0):
        raise ValueError("the validated fixture supports q=4, degree=5, secret=2, seed=0")

    row = run()
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "observe_ghs_transfer_q4_n5_r3_20260629.csv"
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
