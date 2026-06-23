"""
measure_toy_degrees.py — verify four degree notions on a finite-field toy system.
Sub-goal: P1.3 / SG-01
Inputs:   --prime <odd prime>; --output <CSV path>; --smoke
Outputs:  data/measure_toy_degrees_q<q>_<date>.csv unless --output is supplied
Runtime:  under 1 second at q=5 on Python 3.13.4
Validated against: Caminata–Gorla, arXiv:2112.05579v2, Example 4.2
"""

from __future__ import annotations

import argparse
import csv
import itertools
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

import sympy


Monomial = tuple[int, ...]
Polynomial = dict[Monomial, int]


def monomial_degree(monomial: Monomial) -> int:
    return sum(monomial)


def grevlex_key(monomial: Monomial) -> tuple[int, ...]:
    """Key whose maximum is largest in graded reverse lexicographic order."""
    return (sum(monomial), *(-exponent for exponent in reversed(monomial)))


def monomials_exact_degree(nvars: int, degree: int) -> list[Monomial]:
    if nvars == 1:
        return [(degree,)]
    result: list[Monomial] = []
    for first in range(degree + 1):
        for suffix in monomials_exact_degree(nvars - 1, degree - first):
            result.append((first, *suffix))
    return result


def monomials_up_to_degree(nvars: int, degree: int) -> list[Monomial]:
    result = list(
        itertools.chain.from_iterable(
            monomials_exact_degree(nvars, value) for value in range(degree + 1)
        )
    )
    return sorted(result, key=grevlex_key, reverse=True)


def normalize(poly: Polynomial, prime: int) -> Polynomial:
    return {monomial: coefficient % prime for monomial, coefficient in poly.items() if coefficient % prime}


def add(left: Polynomial, right: Polynomial, prime: int, scale: int = 1) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = (result.get(monomial, 0) + scale * coefficient) % prime
    return normalize(result, prime)


def multiply_monomial(
    poly: Polynomial, monomial: Monomial, coefficient: int, prime: int
) -> Polynomial:
    return normalize(
        {
            tuple(a + b for a, b in zip(term, monomial, strict=True)): coefficient * value
            for term, value in poly.items()
        },
        prime,
    )


def polynomial_degree(poly: Polynomial) -> int:
    return max((monomial_degree(monomial) for monomial in poly), default=-1)


def leading_term(poly: Polynomial) -> tuple[Monomial, int]:
    monomial = max(poly, key=grevlex_key)
    return monomial, poly[monomial]


def divides(left: Monomial, right: Monomial) -> bool:
    return all(a <= b for a, b in zip(left, right, strict=True))


def quotient(right: Monomial, left: Monomial) -> Monomial:
    return tuple(a - b for a, b in zip(right, left, strict=True))


def lcm(left: Monomial, right: Monomial) -> Monomial:
    return tuple(max(a, b) for a, b in zip(left, right, strict=True))


def monic(poly: Polynomial, prime: int) -> Polynomial:
    _, coefficient = leading_term(poly)
    return multiply_monomial(poly, (0,) * len(next(iter(poly))), pow(coefficient, -1, prime), prime)


def reduce_polynomial(poly: Polynomial, basis: list[Polynomial], prime: int) -> Polynomial:
    remainder: Polynomial = {}
    work = normalize(poly, prime)
    while work:
        work_monomial, work_coefficient = leading_term(work)
        divisor = None
        for item in basis:
            item_monomial, item_coefficient = leading_term(item)
            if divides(item_monomial, work_monomial):
                divisor = (item, item_monomial, item_coefficient)
                break
        if divisor is None:
            term = {work_monomial: work_coefficient}
            remainder = add(remainder, term, prime)
            work = add(work, term, prime, scale=-1)
            continue
        item, item_monomial, item_coefficient = divisor
        multiplier = quotient(work_monomial, item_monomial)
        scale = work_coefficient * pow(item_coefficient, -1, prime)
        work = add(work, multiply_monomial(item, multiplier, scale, prime), prime, scale=-1)
    return normalize(remainder, prime)


@dataclass(frozen=True)
class BuchbergerTrace:
    basis: list[Polynomial]
    processed_pairs: int
    maximum_critical_pair_degree: int


def naive_buchberger(generators: list[Polynomial], prime: int) -> BuchbergerTrace:
    """Buchberger without pair criteria or input interreduction, using FIFO pairs."""
    basis = [monic(poly, prime) for poly in generators if poly]
    pairs = [(left, right) for right in range(1, len(basis)) for left in range(right)]
    processed = 0
    maximum_pair_degree = 0
    cursor = 0
    while cursor < len(pairs):
        left_index, right_index = pairs[cursor]
        cursor += 1
        processed += 1
        left = basis[left_index]
        right = basis[right_index]
        left_monomial, left_coefficient = leading_term(left)
        right_monomial, right_coefficient = leading_term(right)
        pair_lcm = lcm(left_monomial, right_monomial)
        maximum_pair_degree = max(maximum_pair_degree, monomial_degree(pair_lcm))
        s_polynomial = add(
            multiply_monomial(
                left, quotient(pair_lcm, left_monomial), pow(left_coefficient, -1, prime), prime
            ),
            multiply_monomial(
                right, quotient(pair_lcm, right_monomial), pow(right_coefficient, -1, prime), prime
            ),
            prime,
            scale=-1,
        )
        reduced = reduce_polynomial(s_polynomial, basis, prime)
        if reduced:
            reduced = monic(reduced, prime)
            new_index = len(basis)
            basis.append(reduced)
            pairs.extend((index, new_index) for index in range(new_index))
    return BuchbergerTrace(basis, processed, maximum_pair_degree)


def rref_mod_prime(rows: list[list[int]], prime: int) -> list[list[int]]:
    if not rows:
        return []
    matrix = [[value % prime for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (value - scale * pivot_value) % prime
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return [row for row in matrix if any(row)]


def vector(poly: Polynomial, columns: list[Monomial], prime: int) -> list[int]:
    return [poly.get(monomial, 0) % prime for monomial in columns]


def polynomial(row: list[int], columns: list[Monomial], prime: int) -> Polynomial:
    return normalize(dict(zip(columns, row, strict=True)), prime)


def in_rowspace(poly: Polynomial, basis_rows: list[list[int]], columns: list[Monomial], prime: int) -> bool:
    return len(rref_mod_prime([*basis_rows, vector(poly, columns, prime)], prime)) == len(basis_rows)


@dataclass(frozen=True)
class MacaulaySpace:
    degree: int
    initial_rows: int
    rank: int
    rows: list[list[int]]
    columns: list[Monomial]


def closed_macaulay_space(
    generators: list[Polynomial], nvars: int, degree: int, prime: int
) -> MacaulaySpace:
    columns = monomials_up_to_degree(nvars, degree)
    rows: list[list[int]] = []
    for generator in generators:
        remaining_degree = degree - polynomial_degree(generator)
        if remaining_degree < 0:
            continue
        for multiplier in monomials_up_to_degree(nvars, remaining_degree):
            rows.append(vector(multiply_monomial(generator, multiplier, 1, prime), columns, prime))
    initial_rows = len(rows)
    rows = rref_mod_prime(rows, prime)

    changed = True
    while changed:
        current_polynomials = [polynomial(row, columns, prime) for row in rows]
        candidates: list[list[int]] = []
        for item in current_polynomials:
            remaining_degree = degree - polynomial_degree(item)
            if remaining_degree <= 0:
                continue
            for multiplier in monomials_up_to_degree(nvars, remaining_degree):
                product = multiply_monomial(item, multiplier, 1, prime)
                candidates.append(vector(product, columns, prime))
        enlarged = rref_mod_prime([*rows, *candidates], prime)
        changed = len(enlarged) > len(rows)
        rows = enlarged
    return MacaulaySpace(degree, initial_rows, len(rows), rows, columns)


def top_homogeneous_part(poly: Polynomial) -> Polynomial:
    degree = polynomial_degree(poly)
    return {monomial: coefficient for monomial, coefficient in poly.items() if sum(monomial) == degree}


def first_fall_degree(generators: list[Polynomial], nvars: int, prime: int, ceiling: int) -> int:
    """Detect the first non-Koszul homogeneous syzygy; sufficient for this degree-3 witness."""
    tops = [top_homogeneous_part(poly) for poly in generators]
    input_degrees = [polynomial_degree(poly) for poly in tops]
    for degree in range(min(input_degrees), ceiling + 1):
        rows: list[list[int]] = []
        output_columns = [
            monomial
            for monomial in monomials_exact_degree(nvars, degree)
            if all(exponent < prime for exponent in monomial)
        ]
        domain_size = 0
        for item, item_degree in zip(tops, input_degrees, strict=True):
            if item_degree > degree:
                continue
            for multiplier in monomials_exact_degree(nvars, degree - item_degree):
                domain_size += 1
                product = multiply_monomial(item, multiplier, 1, prime)
                product = {
                    monomial: coefficient
                    for monomial, coefficient in product.items()
                    if all(exponent < prime for exponent in monomial)
                }
                rows.append(vector(product, output_columns, prime))
        rank = len(rref_mod_prime(rows, prime))
        nullity = domain_size - rank
        # All Koszul syzygies have degree at least the sum of the two smallest
        # generator degrees, which is 4 for the checked toy system. Thus any
        # degree-3 kernel is nontrivial in the first-fall sense.
        minimum_koszul_degree = sum(sorted(input_degrees)[:2])
        if nullity > 0 and degree < minimum_koszul_degree:
            return degree
    raise ValueError(f"no first fall detected through degree {ceiling}")


def degree_of_regularity(generators: list[Polynomial], nvars: int, ceiling: int) -> int:
    """Compute d_reg when every top part is a monomial."""
    top_monomials = [next(iter(top_homogeneous_part(poly))) for poly in generators]
    for degree in range(ceiling + 1):
        monomials = monomials_exact_degree(nvars, degree)
        if monomials and all(any(divides(generator, monomial) for generator in top_monomials) for monomial in monomials):
            return degree
    raise ValueError(f"degree of regularity exceeds {ceiling}")


def toy_generators(prime: int) -> list[Polynomial]:
    if prime <= 3 or prime % 2 == 0:
        raise ValueError("the cited family requires an odd prime q > 3")
    return [
        {(1, 1, 0): 1, (0, 1, 0): 1},
        {(0, 2, 0): 1, (0, 0, 0): -1},
        {(0, 0, prime - 1): 1, (0, 0, 0): -1},
        {(prime, 0, 0): 1, (1, 0, 0): -1},
    ]


def sympy_groebner_basis(prime: int) -> list[sympy.Poly]:
    x1, x2, x3 = sympy.symbols("x1 x2 x3")
    basis = sympy.groebner(
        [x1 * x2 + x2, x2**2 - 1, x3 ** (prime - 1) - 1, x1**prime - x1],
        x1,
        x2,
        x3,
        order="grevlex",
        modulus=prime,
    )
    return list(basis.polys)


def sympy_poly_to_dict(item: sympy.Poly, prime: int) -> Polynomial:
    return normalize({tuple(monomial): int(coefficient) for monomial, coefficient in item.terms()}, prime)


def measure(prime: int) -> dict[str, int | str]:
    generators = toy_generators(prime)
    first_fall = first_fall_degree(generators, 3, prime, ceiling=3)
    regularity = degree_of_regularity(generators, 3, ceiling=2 * prime)
    groebner_basis = sympy_groebner_basis(prime)
    target_basis = [sympy_poly_to_dict(item, prime) for item in groebner_basis]

    macaulay_spaces = [closed_macaulay_space(generators, 3, degree, prime) for degree in range(prime)]
    solving_degree = next(
        space.degree
        for space in macaulay_spaces
        if all(
            polynomial_degree(item) <= space.degree
            and in_rowspace(item, space.rows, space.columns, prime)
            for item in target_basis
        )
    )

    trace = naive_buchberger(generators, prime)
    return {
        "prime": prime,
        "system": "{x1*x2+x2, x2^2-1, x3^(q-1)-1, x1^q-x1}",
        "order": "grevlex(x1>x2>x3)",
        "first_fall_degree": first_fall,
        "degree_of_regularity": regularity,
        "solving_degree": solving_degree,
        "algorithm": "naive Buchberger; FIFO; no pair criteria; no input interreduction",
        "algorithm_max_critical_pair_degree": trace.maximum_critical_pair_degree,
        "buchberger_pairs_processed": trace.processed_pairs,
        "groebner_basis": "; ".join(str(item.as_expr()) for item in groebner_basis),
        "sympy_version": sympy.__version__,
    }


def write_csv(measurement: dict[str, int | str], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(measurement))
        writer.writeheader()
        writer.writerow(measurement)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime", type=int, default=5)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    measurement = measure(5 if args.smoke else args.prime)
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"measure_toy_degrees_q{measurement['prime']}_{date.today():%Y%m%d}.csv"
        )
    write_csv(measurement, output)
    for key, value in measurement.items():
        print(f"{key}: {value}")
    print(f"output: {output}")


if __name__ == "__main__":
    main()
