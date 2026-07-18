"""
lift_quartic_singular_primes.py - strong-Hensel audit of A021 exceptions.
Sub-goal: P4.2 / SG-23
Inputs:   --maximum-exponent <int> [--prime-bound <int>] [--smoke]
Outputs:  data/lift_quartic_singular_primes_<params>_<date>.csv
Runtime:  <30 s through exponent 8
Validated against: direct recursive residue lifting
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

from certify_quartic_odd_local import certify_odd_local  # noqa: E402
from classify_mixed_degree_pairs import PHI  # noqa: E402
from reduce_quartic_degree_pairs import C, _expression  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class SingularLiftRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    prime: int
    status: str
    certificate_exponent: int
    terminal_solution_count: int
    field_gap_residue: int | None
    field_p_residue: int | None
    function_valuation: int | None
    derivative_valuation: int | None


def _valuation(value: int, prime: int) -> int:
    if value == 0:
        return 10**9
    result = 0
    while value % prime == 0:
        result += 1
        value //= prime
    return result


def _expressions(degree_e1: int, degree_e2: int, h: int):
    first = _expression(PHI[degree_e1], negative=True)
    second = _expression(PHI[degree_e2])
    g = sympy.cancel((first - second) / C)
    field_p = sympy.Symbol("p")
    equation = sympy.expand(
        h * field_p**2 + (h * C + g) * field_p - second
    )
    return (
        equation,
        sympy.diff(equation, C),
        sympy.diff(equation, field_p),
        field_p,
    )


def _evaluate(expression, field_p_symbol, gap: int, field_p: int) -> int:
    return int(expression.subs({C: gap, field_p_symbol: field_p}))


def lift_singular_prime(
    degree_e1: int,
    degree_e2: int,
    h: int,
    prime: int,
    maximum_exponent: int,
) -> SingularLiftRow:
    """Lift all unit-field residues until obstruction or strong Hensel."""

    equation, derivative_c, derivative_p, field_p_symbol = _expressions(
        degree_e1, degree_e2, h
    )
    solutions = {
        (gap, field_p)
        for gap in range(prime)
        for field_p in range(1, prime)
        if (field_p + gap) % prime
        and _evaluate(equation, field_p_symbol, gap, field_p) % prime == 0
    }
    modulus = prime
    for exponent in range(1, maximum_exponent + 1):
        for gap, field_p in solutions:
            function_value = _evaluate(
                equation, field_p_symbol, gap, field_p
            )
            if function_value == 0:
                return SingularLiftRow(
                    degree_e1,
                    degree_e2,
                    h,
                    prime,
                    "exact_integer_solution_certificate",
                    exponent,
                    len(solutions),
                    gap,
                    field_p,
                    10**9,
                    min(
                        _valuation(
                            _evaluate(derivative_c, field_p_symbol, gap, field_p),
                            prime,
                        ),
                        _valuation(
                            _evaluate(derivative_p, field_p_symbol, gap, field_p),
                            prime,
                        ),
                    ),
                )
            function_valuation = _valuation(function_value, prime)
            derivative_valuation = min(
                _valuation(
                    _evaluate(derivative_c, field_p_symbol, gap, field_p), prime
                ),
                _valuation(
                    _evaluate(derivative_p, field_p_symbol, gap, field_p), prime
                ),
            )
            if function_valuation > 2 * derivative_valuation:
                return SingularLiftRow(
                    degree_e1,
                    degree_e2,
                    h,
                    prime,
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
        next_modulus = modulus * prime
        lifted: set[tuple[int, int]] = set()
        for gap, field_p in solutions:
            for gap_digit in range(prime):
                lifted_gap = gap + gap_digit * modulus
                for field_digit in range(prime):
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
            return SingularLiftRow(
                degree_e1,
                degree_e2,
                h,
                prime,
                "finite_power_obstruction",
                exponent + 1,
                0,
                None,
                None,
                None,
                None,
            )
    return SingularLiftRow(
        degree_e1,
        degree_e2,
        h,
        prime,
        "unresolved_at_exponent",
        maximum_exponent,
        len(solutions),
        None,
        None,
        None,
        None,
    )


def audit_singular_primes(
    maximum_exponent: int = 8,
    prime_bound: int = 251,
) -> list[SingularLiftRow]:
    """Audit all singular-only row/prime pairs emitted by A021."""

    if maximum_exponent < 2:
        raise ValueError("maximum_exponent must be at least 2")
    rows: list[SingularLiftRow] = []
    for source in certify_odd_local(prime_bound):
        if not source.singular_only_primes:
            continue
        for prime_text in source.singular_only_primes.split(","):
            rows.append(
                lift_singular_prime(
                    source.degree_e1,
                    source.degree_e2,
                    source.quotient_difference_h,
                    int(prime_text),
                    maximum_exponent,
                )
            )
    return rows


def write_rows(rows: list[SingularLiftRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(SingularLiftRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-exponent", type=int, default=8)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    maximum_exponent = 3 if args.smoke and args.maximum_exponent == 8 else args.maximum_exponent
    rows = audit_singular_primes(maximum_exponent, args.prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"lift_quartic_singular_primes_e{maximum_exponent}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    print(f"lifted {len(rows)} singular row/prime pairs; statuses={counts}")
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
