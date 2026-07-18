"""
audit_quartic_degenerate_cases.py - close non-genus-one quartic reductions.
Sub-goal: P4.2 / SG-17
Inputs:   --h-bound <int> [--smoke]
Outputs:  data/audit_quartic_degenerate_cases_<date>.csv
Runtime:  <1 s
Validated against: all 34 non-genus-one rows in the |h|<=24 reduction
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

from classify_mixed_degree_pairs import PHI  # noqa: E402
from reduce_quartic_degree_pairs import (  # noqa: E402
    C,
    _expression,
    reduce_quartic_pairs,
)
from lib.curves import is_prime  # noqa: E402
from search_two_cycles import multiplicative_order_up_to  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class DegenerateAuditRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    source_classification: str
    gap_c: int | None
    field_p: int | None
    field_q: int | None
    status: str
    rejection_reason: str


def _cauchy_bound(expression) -> int:
    polynomial = sympy.Poly(expression, C, domain=sympy.ZZ)
    if polynomial.is_zero or polynomial.degree() <= 0:
        return 2
    leading = abs(int(polynomial.LC()))
    other = [abs(int(value)) for value in polynomial.all_coeffs()[1:]]
    return 2 + max((value + leading - 1) // leading for value in other)


def _evaluate(expression, gap: int) -> int:
    return int(expression.subs(C, gap))


def _exact_cycle_status(
    degree_e1: int,
    degree_e2: int,
    gap: int,
    field_p: int,
    field_q: int,
) -> tuple[str, str]:
    if field_p < 5 or field_q - field_p != gap:
        return "candidate_rejected", "invalid ordered fields"
    if not is_prime(field_p) or not is_prime(field_q):
        return "candidate_rejected", "fields are not prime"
    if (gap - 1) ** 2 > 4 * field_p or (gap + 1) ** 2 > 4 * field_q:
        return "candidate_rejected", "Hasse inequality failed"
    exact = (
        multiplicative_order_up_to(field_p, field_q, 12),
        multiplicative_order_up_to(field_q, field_p, 12),
    )
    if exact != (degree_e1, degree_e2):
        return "candidate_rejected", f"exact degrees are {exact}"
    return "exact_cycle", "none"


def audit_degenerate_cases(h_bound: int = 24) -> list[DegenerateAuditRow]:
    """Audit every non-genus-one row in the requested quartic reduction."""

    source_rows = [
        row
        for row in reduce_quartic_pairs(h_bound)
        if row.classification != "genus_one_after_square_removal"
    ]
    output: list[DegenerateAuditRow] = []
    for row in source_rows:
        degree_e1 = row.degree_e1
        degree_e2 = row.degree_e2
        h = row.quotient_difference_h
        first = _expression(PHI[degree_e1], negative=True)
        second = _expression(PHI[degree_e2])
        g = sympy.cancel((first - second) / C)
        candidate_fields: set[tuple[int, int, int]] = set()

        if h == 0:
            if g == 0:
                output.append(
                    DegenerateAuditRow(
                        degree_e1,
                        degree_e2,
                        h,
                        row.classification,
                        None,
                        None,
                        None,
                        "audited_empty",
                        "G=0 makes H=G*p impossible",
                    )
                )
                continue
            quotient, remainder = sympy.div(
                sympy.Poly(second, C),
                sympy.Poly(g, C),
            )
            if remainder.is_zero:
                raise AssertionError("unexpected h=0 polynomial quotient")
            bound = max(
                _cauchy_bound(g),
                _cauchy_bound(g - remainder.as_expr()),
                _cauchy_bound(g + remainder.as_expr()),
            )
            for gap in range(2, bound + 1, 2):
                multiplier = _evaluate(g, gap)
                second_value = _evaluate(second, gap)
                if (
                    multiplier > 0
                    and second_value % multiplier == 0
                ):
                    field_p = second_value // multiplier
                    candidate_fields.add((gap, field_p, field_p + gap))
        elif row.classification == "constant_nonsquare_times_square":
            discriminant = sympy.expand((h * C + g) ** 2 + 4 * h * second)
            for root in sympy.ground_roots(discriminant):
                rational = Fraction(root)
                if rational.denominator == 1:
                    gap = rational.numerator
                    if gap >= 2 and gap % 2 == 0:
                        linear = h * gap + _evaluate(g, gap)
                        denominator = 2 * h
                        if (-linear) % denominator == 0:
                            field_p = (-linear) // denominator
                            candidate_fields.add((gap, field_p, field_p + gap))
        elif row.classification == "genus_zero_after_square_removal":
            discriminant = sympy.expand((h * C + g) ** 2 + 4 * h * second)
            polynomial = sympy.Poly(discriminant, C, domain=sympy.ZZ)
            if polynomial.LC() >= 0:
                raise AssertionError("unbounded genus-zero case requires analysis")
            bound = _cauchy_bound(discriminant)
            for gap in range(2, bound + 1, 2):
                value = _evaluate(discriminant, gap)
                if value < 0:
                    continue
                square_root = math.isqrt(value)
                if square_root * square_root != value:
                    continue
                for signed_root in {square_root, -square_root}:
                    numerator = -(h * gap + _evaluate(g, gap)) + signed_root
                    denominator = 2 * h
                    if numerator % denominator == 0:
                        field_p = numerator // denominator
                        candidate_fields.add((gap, field_p, field_p + gap))
        else:
            raise AssertionError(f"unexpected degenerate class {row.classification}")

        if not candidate_fields:
            output.append(
                DegenerateAuditRow(
                    degree_e1,
                    degree_e2,
                    h,
                    row.classification,
                    None,
                    None,
                    None,
                    "audited_empty",
                    "no allowable positive even-gap field candidate",
                )
            )
            continue
        for gap, field_p, field_q in sorted(candidate_fields):
            status, rejection = _exact_cycle_status(
                degree_e1,
                degree_e2,
                gap,
                field_p,
                field_q,
            )
            output.append(
                DegenerateAuditRow(
                    degree_e1,
                    degree_e2,
                    h,
                    row.classification,
                    gap,
                    field_p,
                    field_q,
                    status,
                    rejection,
                )
            )
    return output


def write_rows(rows: list[DegenerateAuditRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(DegenerateAuditRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--h-bound", type=int, default=24)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    h_bound = 4 if args.smoke and args.h_bound == 24 else args.h_bound
    rows = audit_degenerate_cases(h_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"audit_quartic_degenerate_cases_h{h_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    exact = sum(row.status == "exact_cycle" for row in rows)
    print(f"audited {len(rows)} certificate rows; exact cycles={exact}")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
