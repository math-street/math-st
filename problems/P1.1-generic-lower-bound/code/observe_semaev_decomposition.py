"""
observe_semaev_decomposition.py — trace a toy Semaev f3 decomposition.
Sub-goal: P1.1 / SG-01
Inputs:   --p <prime> --trials <int> --seed <int>
Outputs:  data/observe_semaev_decomposition_p17_20260626.csv
Runtime:  under 1 second at p=17
Validated against: f3 identity in lib/tests/test_semaev.py and direct EC addition
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.curves import Curve
from lib.semaev import f3_value


def run() -> dict[str, int | str]:
    curve = Curve(17, 2, 2)
    generator = (5, 1)
    target = curve.scalar_mul(7, generator)
    assert target == (0, 6)
    factor_base = list(curve.affine_points(8))
    factor_x = sorted({point[0] for point in factor_base})

    polynomial_candidates = 0
    lifted_candidates = 0
    verified: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for x1 in factor_x:
        for x2 in factor_x:
            if f3_value(x1, x2, target[0], curve.a, curve.b, curve.p) != 0:
                continue
            polynomial_candidates += 1
            for point1 in curve.points_for_x(x1):
                for point2 in curve.points_for_x(x2):
                    lifted_candidates += 1
                    if curve.add(point1, point2) == target:
                        verified.append((point1, point2))

    if not verified:
        raise ArithmeticError("the known toy relation was not recovered")
    first = verified[0]
    return {
        "p": 17,
        "curve_a": 2,
        "curve_b": 2,
        "target_scalar": 7,
        "target": str(target),
        "factor_base_points": len(factor_base),
        "factor_base_x_values": len(factor_x),
        "polynomial_evaluations": len(factor_x) ** 2,
        "polynomial_zero_pairs": polynomial_candidates,
        "lifted_sign_candidates": lifted_candidates,
        "verified_ordered_decompositions": len(verified),
        "first_decomposition": str(first),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=17)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.p != 17 or args.trials != 1:
        raise ValueError("the validated fixture currently supports only --p 17 --trials 1")

    row = run()
    output = Path(__file__).resolve().parents[1] / "data" / "observe_semaev_decomposition_p17_20260626.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(output)
    print(row)


if __name__ == "__main__":
    main()
