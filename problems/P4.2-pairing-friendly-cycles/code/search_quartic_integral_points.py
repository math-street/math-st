"""
search_quartic_integral_points.py - finite square search on A018 survivors.
Sub-goal: P4.2 / SG-20
Inputs:   --maximum-gap <even int> [--prime-bound <int>] [--smoke]
Outputs:  data/search_quartic_integral_points_<params>_<date>.csv
Runtime:  target <60 s through c=10,000,000
Validated against: a direct unfiltered scan on short ranges
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import sympy

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from classify_mixed_degree_pairs import PHI  # noqa: E402
from lib.curves import is_prime  # noqa: E402
from reduce_quartic_degree_pairs import C, _expression  # noqa: E402
from search_two_cycles import multiplicative_order_up_to  # noqa: E402
from sieve_quartic_archimedean import sieve_archimedean  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
MINIMUM_GAP = 108
WHEEL_PRIMES = (3, 5, 7, 11, 13)


@dataclass(frozen=True, slots=True)
class IntegralPointSearchRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    maximum_gap: int
    wheel_candidate_gaps: int
    gap_c: int | None
    field_p: int | None
    field_q: int | None
    status: str
    rejection_reason: str


def _coefficients(expression) -> tuple[int, ...]:
    return tuple(int(value) for value in sympy.Poly(expression, C).all_coeffs())


def _evaluate(coefficients: tuple[int, ...], value: int) -> int:
    result = 0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def _allowed_gap_classes(g, second, h: int, prime: int) -> set[int]:
    g_coefficients = _coefficients(g)
    second_coefficients = _coefficients(second)
    allowed: set[int] = set()
    for gap in range(prime):
        g_value = _evaluate(g_coefficients, gap)
        second_value = _evaluate(second_coefficients, gap)
        for field_p in range(1, prime):
            if (field_p + gap) % prime == 0:
                continue
            if (
                h * field_p * field_p
                + (h * gap + g_value) * field_p
                - second_value
            ) % prime == 0:
                allowed.add(gap)
                break
    return allowed


def _wheel_residues(g, second, h: int) -> tuple[int, tuple[int, ...]]:
    modulus = 2 * math.prod(WHEEL_PRIMES)
    allowed = {
        prime: _allowed_gap_classes(g, second, h, prime)
        for prime in WHEEL_PRIMES
    }
    residues = tuple(
        gap
        for gap in range(0, modulus, 2)
        if all(gap % prime in allowed[prime] for prime in WHEEL_PRIMES)
    )
    return modulus, residues


def _candidate_gaps(
    modulus: int,
    residues: tuple[int, ...],
    maximum_gap: int,
):
    for residue in residues:
        first = MINIMUM_GAP + (residue - MINIMUM_GAP) % modulus
        yield from range(first, maximum_gap + 1, modulus)


def _point_status(
    degree_e1: int,
    degree_e2: int,
    gap: int,
    field_p: int,
    first_value: int,
    second_value: int,
) -> tuple[str, str]:
    field_q = field_p + gap
    if field_p < 5:
        return "integral_point_rejected", "nonpositive or tiny first field"
    if first_value % field_q or second_value % field_p:
        return "integral_point_rejected", "cyclotomic divisibility failed"
    if (gap - 1) ** 2 > 4 * field_p:
        return "integral_point_rejected", "Hasse inequality failed"
    if not is_prime(field_p) or not is_prime(field_q):
        return "integral_point_rejected", "one or both fields are composite"
    exact_degrees = (
        multiplicative_order_up_to(field_p, field_q, 12),
        multiplicative_order_up_to(field_q, field_p, 12),
    )
    if exact_degrees != (degree_e1, degree_e2):
        return "integral_point_rejected", f"exact degrees are {exact_degrees}"
    return "exact_cycle", "none"


def search_integral_points(
    maximum_gap: int,
    prime_bound: int = 251,
) -> list[IntegralPointSearchRow]:
    """Search every wheel-admissible gap on the 51 A018 survivors."""

    if maximum_gap < MINIMUM_GAP or maximum_gap % 2:
        raise ValueError("maximum_gap must be even and at least 108")
    survivors = [
        row
        for row in sieve_archimedean(prime_bound)
        if row.status == "survivor"
    ]
    output: list[IntegralPointSearchRow] = []
    for row in survivors:
        h = row.quotient_difference_h
        first = _expression(PHI[row.degree_e1], negative=True)
        second = _expression(PHI[row.degree_e2])
        g = sympy.cancel((first - second) / C)
        linear = sympy.expand(h * C + g)
        discriminant = sympy.expand(linear**2 + 4 * h * second)
        first_coefficients = _coefficients(first)
        second_coefficients = _coefficients(second)
        linear_coefficients = _coefficients(linear)
        discriminant_coefficients = _coefficients(discriminant)
        modulus, residues = _wheel_residues(g, second, h)
        tested = 0
        retained: list[tuple[int, int, int, str, str]] = []
        for gap in _candidate_gaps(modulus, residues, maximum_gap):
            tested += 1
            discriminant_value = _evaluate(discriminant_coefficients, gap)
            if discriminant_value < 0:
                continue
            square_root = math.isqrt(discriminant_value)
            if square_root * square_root != discriminant_value:
                continue
            linear_value = _evaluate(linear_coefficients, gap)
            denominator = 2 * h
            first_value = _evaluate(first_coefficients, gap)
            second_value = _evaluate(second_coefficients, gap)
            for signed_root in {square_root, -square_root}:
                numerator = -linear_value + signed_root
                if numerator % denominator:
                    continue
                field_p = numerator // denominator
                field_q = field_p + gap
                status, rejection = _point_status(
                    row.degree_e1,
                    row.degree_e2,
                    gap,
                    field_p,
                    first_value,
                    second_value,
                )
                retained.append((gap, field_p, field_q, status, rejection))
        if not retained:
            output.append(
                IntegralPointSearchRow(
                    row.degree_e1,
                    row.degree_e2,
                    h,
                    maximum_gap,
                    tested,
                    None,
                    None,
                    None,
                    "no_integral_point_in_range",
                    "none",
                )
            )
        else:
            output.extend(
                IntegralPointSearchRow(
                    row.degree_e1,
                    row.degree_e2,
                    h,
                    maximum_gap,
                    tested,
                    gap,
                    field_p,
                    field_q,
                    status,
                    rejection,
                )
                for gap, field_p, field_q, status, rejection in retained
            )
    return output


def write_rows(rows: list[IntegralPointSearchRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(IntegralPointSearchRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-gap", type=int, default=10_000_000)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    maximum_gap = 10_000 if args.smoke and args.maximum_gap == 10_000_000 else args.maximum_gap
    rows = search_integral_points(maximum_gap, args.prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"search_quartic_integral_points_c{MINIMUM_GAP}-{maximum_gap}_p{args.prime_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    points = sum(row.gap_c is not None for row in rows)
    exact = sum(row.status == "exact_cycle" for row in rows)
    tested = sum(row.wheel_candidate_gaps for row in rows)
    print(
        f"searched 51 curves through c={maximum_gap}; wheel candidates={tested}; "
        f"integral points={points}; exact cycles={exact}"
    )
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
