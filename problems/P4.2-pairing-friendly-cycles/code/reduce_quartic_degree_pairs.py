"""
reduce_quartic_degree_pairs.py - audit quartic/quartic quotient discriminants.
Sub-goal: P4.2 / SG-17
Inputs:   --h-bound <int> [--smoke]
Outputs:  data/reduce_quartic_degree_pairs_<params>_<date>.csv
Runtime:  ~10 s for |h|<=552
Validated against: direct symbolic expansion and squarefree decomposition
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from datetime import date
from fractions import Fraction
from pathlib import Path

import sympy

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_mixed_degree_pairs import PHI, QUARTIC_DEGREES  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
C = sympy.Symbol("c")


@dataclass(frozen=True, slots=True)
class QuarticReductionRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    g_coefficients: str
    discriminant_coefficients: str
    discriminant_degree: int | None
    odd_squarefree_degree: int | None
    classification: str


def _expression(coefficients: tuple[int, ...], *, negative: bool = False):
    return sympy.expand(
        sum(
            coefficient * ((-C) if negative else C) ** exponent
            for exponent, coefficient in enumerate(coefficients)
        )
    )


def _coefficient_string(expression) -> str:
    polynomial = sympy.Poly(expression, C, domain=sympy.ZZ)
    return ",".join(str(value) for value in reversed(polynomial.all_coeffs()))


def _integer_square(value: int) -> bool:
    return value >= 0 and math.isqrt(value) ** 2 == value


def quotient_difference_bound(gap: int) -> Fraction:
    """Return the exact coarse Hasse upper bound for |h| at a gap."""

    if gap <= 1:
        raise ValueError("gap must exceed one")
    geometric_sum = gap**4 + gap**3 + gap**2 + gap + 1
    return Fraction(16 * geometric_sum, (gap - 1) ** 4) + Fraction(
        8 * (gap**2 + gap + 1),
        (gap - 1) ** 2,
    )


def _classify_discriminant(expression) -> tuple[int, int, str]:
    polynomial = sympy.Poly(expression, C, domain=sympy.ZZ)
    coefficient, factors = polynomial.sqf_list()
    odd_degree = sum(
        factor.degree() for factor, exponent in factors if exponent % 2
    )
    all_even = all(exponent % 2 == 0 for _factor, exponent in factors)
    if all_even and _integer_square(int(coefficient)):
        classification = "perfect_square_polynomial"
    elif odd_degree == 0:
        classification = "constant_nonsquare_times_square"
    elif odd_degree <= 2:
        classification = "genus_zero_after_square_removal"
    else:
        classification = "genus_one_after_square_removal"
    return polynomial.degree(), odd_degree, classification


def reduce_quartic_pairs(h_bound: int) -> list[QuarticReductionRow]:
    """Reduce all ordered quartic degree pairs for every bounded h."""

    if h_bound < 1:
        raise ValueError("h_bound must be positive")
    rows: list[QuarticReductionRow] = []
    for degree_e1 in QUARTIC_DEGREES:
        first = _expression(PHI[degree_e1], negative=True)
        for degree_e2 in QUARTIC_DEGREES:
            second = _expression(PHI[degree_e2])
            difference = sympy.expand(first - second)
            quotient, remainder = sympy.div(
                sympy.Poly(difference, C),
                sympy.Poly(C, C),
            )
            if not remainder.is_zero:
                raise AssertionError("quartic difference is not divisible by c")
            g = sympy.expand(quotient.as_expr())
            g_coefficients = _coefficient_string(g)
            for h in range(-h_bound, h_bound + 1):
                if h == 0:
                    if g == 0:
                        classification = "h0_impossible_zero_g"
                    else:
                        _quotient, h0_remainder = sympy.div(
                            sympy.Poly(second, C),
                            sympy.Poly(g, C),
                        )
                        classification = (
                            "h0_polynomial_quotient"
                            if h0_remainder.is_zero
                            else "h0_finite_divisibility"
                        )
                    rows.append(
                        QuarticReductionRow(
                            degree_e1,
                            degree_e2,
                            h,
                            g_coefficients,
                            "",
                            None,
                            None,
                            classification,
                        )
                    )
                    continue
                discriminant = sympy.expand((h * C + g) ** 2 + 4 * h * second)
                degree, odd_degree, classification = _classify_discriminant(
                    discriminant
                )
                rows.append(
                    QuarticReductionRow(
                        degree_e1,
                        degree_e2,
                        h,
                        g_coefficients,
                        _coefficient_string(discriminant),
                        degree,
                        odd_degree,
                        classification,
                    )
                )
    return rows


def write_rows(rows: list[QuarticReductionRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(QuarticReductionRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h-bound", type=int, default=552)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    h_bound = 4 if args.smoke and args.h_bound == 552 else args.h_bound
    rows = reduce_quartic_pairs(h_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"reduce_quartic_degree_pairs_h{h_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.classification] = counts.get(row.classification, 0) + 1
    print(f"reduced {len(rows)} (degree pair,h) cases; classes={counts}")
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
