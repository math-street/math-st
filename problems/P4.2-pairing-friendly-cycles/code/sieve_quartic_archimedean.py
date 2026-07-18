"""
sieve_quartic_archimedean.py - Hasse-bound sign sieve for A017 survivors.
Sub-goal: P4.2 / SG-19
Inputs:   --prime-bound <int> [--smoke]
Outputs:  data/sieve_quartic_archimedean_<params>_<date>.csv
Runtime:  <5 s for the 251-prime-bound survivor set
Validated against: sampled direct real-root evaluations above c=108
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import sympy

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_mixed_degree_pairs import PHI  # noqa: E402
from reduce_quartic_degree_pairs import C, _expression  # noqa: E402
from sieve_quartic_local_obstructions import sieve_local_obstructions  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
START_GAP = 108


@dataclass(frozen=True, slots=True)
class ArchimedeanSieveRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    status: str
    obstruction_reason: str
    discriminant_sign: int | None
    boundary_value_sign: int | None
    boundary_derivative_sign: int | None


def constant_sign_on_ray(expression, start: int = START_GAP) -> int | None:
    """Return the nonzero sign on [start,infinity), or None if not constant."""

    numerator, denominator = sympy.cancel(expression).as_numer_denom()
    if denominator.subs(C, start) <= 0:
        raise AssertionError("expected a positive constant denominator")
    polynomial = sympy.Poly(numerator, C, domain=sympy.QQ)
    value = polynomial.eval(start)
    if value == 0:
        return None
    if polynomial.count_roots(start, sympy.oo) != 0:
        return None
    return 1 if value > 0 else -1


def sieve_archimedean(prime_bound: int) -> list[ArchimedeanSieveRow]:
    """Apply sufficient exact real/Hasse obstructions to A017 survivors."""

    local_survivors = [
        row
        for row in sieve_local_obstructions(prime_bound)
        if row.status == "local_survivor"
    ]
    output: list[ArchimedeanSieveRow] = []
    hasse_boundary = (C - 1) ** 2 / 4
    for row in local_survivors:
        h = row.quotient_difference_h
        first = _expression(PHI[row.degree_e1], negative=True)
        second = _expression(PHI[row.degree_e2])
        g = sympy.cancel((first - second) / C)
        linear = h * C + g
        discriminant = sympy.expand(linear**2 + 4 * h * second)
        boundary_value = sympy.expand(
            h * hasse_boundary**2 + linear * hasse_boundary - second
        )
        boundary_derivative = sympy.expand(2 * h * hasse_boundary + linear)

        discriminant_sign = constant_sign_on_ray(discriminant)
        boundary_value_sign = constant_sign_on_ray(boundary_value)
        boundary_derivative_sign = constant_sign_on_ray(boundary_derivative)
        reason = "none"
        if discriminant_sign == -1:
            reason = "negative_discriminant_on_ray"
        elif (
            h > 0
            and boundary_value_sign == 1
            and boundary_derivative_sign == 1
        ):
            reason = "positive_and_increasing_above_hasse_boundary"
        elif (
            h < 0
            and boundary_value_sign == -1
            and boundary_derivative_sign == -1
        ):
            reason = "negative_and_decreasing_above_hasse_boundary"

        output.append(
            ArchimedeanSieveRow(
                row.degree_e1,
                row.degree_e2,
                h,
                "archimedean_obstructed" if reason != "none" else "survivor",
                reason,
                discriminant_sign,
                boundary_value_sign,
                boundary_derivative_sign,
            )
        )
    return output


def write_rows(rows: list[ArchimedeanSieveRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(ArchimedeanSieveRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prime_bound = 13 if args.smoke and args.prime_bound == 251 else args.prime_bound
    rows = sieve_archimedean(prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"sieve_quartic_archimedean_p{prime_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    obstructed = sum(row.status == "archimedean_obstructed" for row in rows)
    print(
        f"sieved {len(rows)} local survivors; obstructed={obstructed}; "
        f"survivors={len(rows) - obstructed}"
    )
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
