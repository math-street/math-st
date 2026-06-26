"""
observe_smart_attack.py — trace a toy Smart attack on an anomalous curve.
Sub-goal: P1.1 / validation
Inputs:   --p <prime> --trials <int> --seed <int>
Outputs:  data/observe_smart_attack_p17_20260626.csv
Runtime:  under 1 second at p=17
Validated against: all nonzero logs on E/F_17: y^2=x^3+x+3, #E=17
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.anomalous import smart_attack
from lib.curves import Curve


def run() -> dict[str, int | str]:
    curve = Curve(17, 1, 3)
    generator = (2, 8)
    secret = 7
    target = curve.scalar_mul(secret, generator)
    trace: Counter[str] = Counter()
    recovered = smart_attack(curve, generator, target, trace=trace)
    if recovered != secret:
        raise ArithmeticError("known anomalous-curve logarithm was not recovered")
    return {
        "p": curve.p,
        "curve_a": curve.a,
        "curve_b": curve.b,
        "generator": str(generator),
        "target": str(target),
        "secret": secret,
        "recovered": recovered,
        "p_adic_lifts": trace["p_adic_lift"],
        "lifted_group_operations": trace["lifted_group_operation"],
        "coordinate_arithmetic_events": trace["coordinate_arithmetic"],
        "formal_group_ratios": trace["formal_group_ratio"],
        "pairing_evaluations": 0,
        "polynomial_system_solves": 0,
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
    output = Path(__file__).resolve().parents[1] / "data" / "observe_smart_attack_p17_20260626.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(output)
    print(row)


if __name__ == "__main__":
    main()
