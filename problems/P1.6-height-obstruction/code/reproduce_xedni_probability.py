"""reproduce_xedni_probability - reproduce a probability in Jacobson et al.

Sub-goal: P1.6 / SG-05
Inputs:   none (the published p=257 Experiment C parameters are fixed)
Outputs:  data/reproduce_xedni_probability_p257_20260703.csv
Runtime:  under 0.1 s.
Validated against: Jacobson--Koblitz--Silverman--Stein--Teske (2000),
                   Section 5.4.1, which reports 4/(N-3)=1/65.
"""

from __future__ import annotations

import csv
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import Curve, curve_order  # noqa: E402

DATE_STAMP = "20260703"


def reproduce() -> dict[str, int | float]:
    p = 257
    curve = Curve(p, 88, -41)
    generator = (2, 20)
    if not curve.contains(generator):
        raise AssertionError("published generator is not on the published curve")
    order = curve_order(curve)
    if order != 263:
        raise AssertionError(f"published order 263 was not reproduced: got {order}")

    first = generator
    excluded = {None, first, curve.neg(first)}
    eligible = [
        curve.scalar_mul(scalar, generator)
        for scalar in range(order)
        if curve.scalar_mul(scalar, generator) not in excluded
    ]
    favorable = 0
    for second in eligible:
        has_relation = any(
            curve.add(curve.scalar_mul(left, first), curve.scalar_mul(right, second)) is None
            for left in (-2, -1, 1, 2)
            for right in (-2, -1, 1, 2)
        )
        favorable += int(has_relation)
    return {
        "p": p,
        "curve_a": 88,
        "curve_b": -41,
        "group_order": order,
        "eligible_second_points": len(eligible),
        "favorable_points": favorable,
        "measured_probability": favorable / len(eligible),
        "published_numerator": 4,
        "published_denominator": 260,
        "published_probability": 1 / 65,
    }


def main() -> None:
    row = reproduce()
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"reproduce_xedni_probability_p257_{DATE_STAMP}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(f"wrote {output}")


if __name__ == "__main__":
    main()

