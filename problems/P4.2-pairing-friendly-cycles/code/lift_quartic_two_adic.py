"""
lift_quartic_two_adic.py - strong-Hensel two-adic audit after A022.
Sub-goal: P4.2 / SG-24
Inputs:   --maximum-exponent <int> [--prime-bound <int>] [--smoke]
Outputs:  data/lift_quartic_two_adic_<params>_<date>.csv
Runtime:  <10 s through exponent 12
Validated against: direct recursive residue lifting
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from lift_quartic_singular_primes import (  # noqa: E402
    _evaluate,
    _expressions,
    _valuation,
    audit_singular_primes,
)
from sieve_quartic_archimedean import sieve_archimedean  # noqa: E402

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class TwoAdicLiftRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    status: str
    certificate_exponent: int
    terminal_solution_count: int
    field_gap_residue: int | None
    field_p_residue: int | None
    function_valuation: int | None
    derivative_valuation: int | None


def lift_two_adic_row(
    degree_e1: int,
    degree_e2: int,
    h: int,
    maximum_exponent: int,
) -> TwoAdicLiftRow:
    """Lift even-gap, odd-field solutions through powers of two."""

    equation, derivative_c, derivative_p, field_p_symbol = _expressions(
        degree_e1, degree_e2, h
    )
    solutions = (
        {(0, 1)}
        if _evaluate(equation, field_p_symbol, 0, 1) % 2 == 0
        else set()
    )
    modulus = 2
    for exponent in range(1, maximum_exponent + 1):
        for gap, field_p in solutions:
            function_value = _evaluate(
                equation, field_p_symbol, gap, field_p
            )
            derivative_valuation = min(
                _valuation(
                    _evaluate(derivative_c, field_p_symbol, gap, field_p), 2
                ),
                _valuation(
                    _evaluate(derivative_p, field_p_symbol, gap, field_p), 2
                ),
            )
            if function_value == 0:
                return TwoAdicLiftRow(
                    degree_e1,
                    degree_e2,
                    h,
                    "exact_integer_solution_certificate",
                    exponent,
                    len(solutions),
                    gap,
                    field_p,
                    10**9,
                    derivative_valuation,
                )
            function_valuation = _valuation(function_value, 2)
            if function_valuation > 2 * derivative_valuation:
                return TwoAdicLiftRow(
                    degree_e1,
                    degree_e2,
                    h,
                    "strong_hensel_certificate",
                    exponent,
                    len(solutions),
                    gap,
                    field_p,
                    function_valuation,
                    derivative_valuation,
                )
        if exponent == maximum_exponent:
            break
        next_modulus = modulus * 2
        lifted: set[tuple[int, int]] = set()
        for gap, field_p in solutions:
            for gap_digit in (0, 1):
                lifted_gap = gap + gap_digit * modulus
                if lifted_gap % 2:
                    continue
                for field_digit in (0, 1):
                    lifted_field = field_p + field_digit * modulus
                    if (
                        _evaluate(
                            equation,
                            field_p_symbol,
                            lifted_gap,
                            lifted_field,
                        )
                        % next_modulus
                        == 0
                    ):
                        lifted.add((lifted_gap, lifted_field))
        solutions = lifted
        modulus = next_modulus
        if not solutions:
            return TwoAdicLiftRow(
                degree_e1,
                degree_e2,
                h,
                "finite_power_obstruction",
                exponent + 1,
                0,
                None,
                None,
                None,
                None,
            )
    return TwoAdicLiftRow(
        degree_e1,
        degree_e2,
        h,
        "unresolved_at_exponent",
        maximum_exponent,
        len(solutions),
        None,
        None,
        None,
        None,
    )


def audit_two_adic(
    maximum_exponent: int = 12,
    prime_bound: int = 251,
) -> list[TwoAdicLiftRow]:
    """Audit every A018 row not already eliminated by an odd prime power."""

    odd_obstructed = {
        (row.degree_e1, row.degree_e2, row.quotient_difference_h)
        for row in audit_singular_primes(8, prime_bound)
        if row.status == "finite_power_obstruction"
    }
    source = [
        row
        for row in sieve_archimedean(prime_bound)
        if row.status == "survivor"
        and (row.degree_e1, row.degree_e2, row.quotient_difference_h)
        not in odd_obstructed
    ]
    return [
        lift_two_adic_row(
            row.degree_e1,
            row.degree_e2,
            row.quotient_difference_h,
            maximum_exponent,
        )
        for row in source
    ]


def write_rows(rows: list[TwoAdicLiftRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(TwoAdicLiftRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-exponent", type=int, default=12)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    maximum_exponent = 5 if args.smoke and args.maximum_exponent == 12 else args.maximum_exponent
    rows = audit_two_adic(maximum_exponent, args.prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"lift_quartic_two_adic_e{maximum_exponent}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    print(f"lifted {len(rows)} final rows two-adically; statuses={counts}")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
