"""
observe_coordinate_bypass.py — compare oracle-charged and coordinate-compiled BSGS.
Sub-goal: P1.1 / SG-03
Inputs:   --p <prime> --trials <int> --seed <int> (only p=17 is a known-answer fixture)
Outputs:  data/observe_coordinate_bypass_p17_20260624.csv
Runtime:  under 1 second at p=17
Validated against: E(F_17): y^2=x^3+2x+2, #E=19, [7](5,1)=(0,6)
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.curves import ShortWeierstrassCurve
from lib.dlog import bsgs


def run() -> list[dict[str, int | str]]:
    curve = ShortWeierstrassCurve(17, 2, 2)
    generator = curve.point(5, 1)
    target = curve.scalar_mul(7, generator)
    rows: list[dict[str, int | str]] = []
    for mode, charge in (("charged_group_oracle", True), ("free_coordinate_formula", False)):
        curve.reset_trace()
        recovered = bsgs(curve, generator, target, 19, charge=charge)
        rows.append(
            {
                "mode": mode,
                "p": 17,
                "order": 19,
                "secret": 7,
                "recovered": recovered,
                "group_operations": curve.trace["group_operation"],
                "coordinate_arithmetic_events": curve.trace["coordinate_arithmetic"],
                "equality_tests": curve.trace["equality_test"],
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=17)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.p != 17 or args.trials != 1:
        raise ValueError("the validated fixture currently supports only --p 17 --trials 1")

    rows = run()
    output = Path(__file__).resolve().parents[1] / "data" / "observe_coordinate_bypass_p17_20260624.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(output)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
