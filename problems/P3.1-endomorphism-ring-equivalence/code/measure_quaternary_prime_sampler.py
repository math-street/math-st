"""
measure_quaternary_prime_sampler.py - enumerate the A003 residue norm lattice.
Sub-goal: P3.1 / SG-02d
Inputs:   --max-p <prime bound> --ells <csv> --cutoff <int> --trials <int> --seed <int>
Outputs:  data/measure_quaternary_prime_sampler_<params>_20260711.csv
Runtime:  target under 2 minutes for p <= 59, ell <= 7, cutoff 5000
Validated against: det(q_I)=p^2 and det(q_Lambda)=(8 ell)^6 p^2
"""

from __future__ import annotations

import argparse
import csv
import sys
from fractions import Fraction
from itertools import product
from math import isqrt, log
from pathlib import Path
from random import Random
from typing import Iterable, Sequence

from sympy import Matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.quaternion import IntegralIdeal, MaximalOrder


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def linear_combination(
    coefficients: Sequence[int], rows: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    return tuple(
        sum(coefficients[row] * rows[row][column] for row in range(4))
        for column in range(4)
    )


def normalized_norm(ideal: IntegralIdeal, coordinates: Sequence[int]) -> int:
    numerator = ideal.order.norm(coordinates)
    if numerator % ideal.norm:
        raise ArithmeticError("ideal norm form was not integral")
    return numerator // ideal.norm


def find_residue_vector(ideal: IntegralIdeal, ell: int) -> tuple[tuple[int, ...], int]:
    """Find x with first ideal coordinate one and the A003 residue conditions."""

    modulus = 8 * ell
    for tail in product(range(modulus), repeat=3):
        relative = (1, *tail)
        ambient = linear_combination(relative, ideal.basis)
        value = normalized_norm(ideal, ambient)
        if value % 8 != 1 or value % ideal.order.p == 0:
            continue
        if value % ell and pow(value % ell, (ell - 1) // 2, ell) == ell - 1:
            return ambient, value % modulus
    raise RuntimeError("no residue vector was found")


def residue_lattice_basis(
    ideal: IntegralIdeal, ell: int
) -> tuple[tuple[tuple[int, ...], ...], int]:
    modulus = 8 * ell
    vector, residue = find_residue_vector(ideal, ell)
    basis = (vector,) + tuple(
        tuple(modulus * coordinate for coordinate in ideal.basis[index])
        for index in range(1, 4)
    )
    return basis, residue


def normalized_doubled_gram(
    ideal: IntegralIdeal, basis: Sequence[Sequence[int]]
) -> Matrix:
    ambient_gram = Matrix(ideal.order.doubled_norm_gram)
    basis_matrix = Matrix(basis)
    gram = basis_matrix * ambient_gram * basis_matrix.T / ideal.norm
    if any(entry.q != 1 for entry in gram):
        raise ArithmeticError("residue lattice Gram matrix was not integral")
    return gram


def coefficient_bounds(gram: Matrix, cutoff: int) -> tuple[int, ...]:
    inverse = gram.inv()
    bounds: list[int] = []
    for index in range(4):
        bound_squared = Fraction(
            2 * cutoff * int(inverse[index, index].p),
            int(inverse[index, index].q),
        )
        bounds.append(isqrt(bound_squared.numerator // bound_squared.denominator))
    return tuple(bounds)


def enumerate_norms(
    ideal: IntegralIdeal,
    basis: Sequence[Sequence[int]],
    cutoff: int,
) -> tuple[list[int], tuple[int, ...], int]:
    gram = normalized_doubled_gram(ideal, basis)
    bounds = coefficient_bounds(gram, cutoff)
    values: list[int] = []
    candidates = 0
    gram_rows = tuple(
        tuple(int(gram[row, column]) for column in range(4))
        for row in range(4)
    )
    ranges: Iterable[range] = (range(-bound, bound + 1) for bound in bounds)
    for coefficients in product(*ranges):
        candidates += 1
        doubled = sum(
            coefficients[row] * gram_rows[row][column] * coefficients[column]
            for row in range(4)
            for column in range(4)
        )
        if doubled > 2 * cutoff:
            continue
        vector = linear_combination(coefficients, basis)
        value = normalized_norm(ideal, vector)
        if 0 < value <= cutoff:
            values.append(value)
    return values, bounds, candidates


def choose_neighbor_prime(p: int, ell: int) -> int:
    for candidate in (3, 5, 7, 11, 13, 17, 19):
        if candidate not in (p, ell):
            return candidate
    raise RuntimeError("no neighbor prime is available")


def measure_case(
    p: int,
    ell: int,
    cutoff: int,
    ideal: IntegralIdeal,
    ideal_label: str,
) -> dict[str, int | float | str]:
    modulus = 8 * ell
    basis, residue = residue_lattice_basis(ideal, ell)
    gram = normalized_doubled_gram(ideal, basis)
    expected_discriminant = p * p * modulus**6
    discriminant = int(gram.det())
    if discriminant != expected_discriminant:
        raise ArithmeticError(
            f"unexpected discriminant {discriminant}, expected {expected_discriminant}"
        )

    values, bounds, candidates = enumerate_norms(ideal, basis, cutoff)
    represented = set(values)
    prime_values = [value for value in values if is_prime(value)]
    eligible_prime_vectors = [
        value for value in prime_values if value not in (ell, p) and value > 2
    ]
    reciprocity_violations = [
        value
        for value in eligible_prime_vectors
        if pow(ell % value, (value - 1) // 2, value) != value - 1
    ]
    if reciprocity_violations:
        raise ArithmeticError(
            f"quadratic-nonresidue invariant failed: {reciprocity_violations[:3]}"
        )

    progression_primes = [
        value
        for value in range(residue, cutoff + 1, modulus)
        if value >= 2 and is_prime(value) and value != p
    ]
    represented_progression = [
        value for value in progression_primes if value in represented
    ]
    missing = [value for value in progression_primes if value not in represented]
    prime_probability = len(prime_values) / len(values) if values else 0.0
    scaled_probability = prime_probability * log(cutoff) if cutoff > 1 else 0.0

    return {
        "p": p,
        "ell": ell,
        "ideal": ideal_label,
        "ideal_norm": ideal.norm,
        "cutoff": cutoff,
        "modulus": modulus,
        "residue": residue,
        "discriminant": discriminant,
        "coefficient_bounds": ";".join(str(bound) for bound in bounds),
        "box_candidates": candidates,
        "ellipsoid_vectors": len(values),
        "prime_vectors": len(prime_values),
        "prime_probability": prime_probability,
        "prime_probability_times_log_cutoff": scaled_probability,
        "progression_primes": len(progression_primes),
        "represented_progression_primes": len(represented_progression),
        "progression_coverage": (
            len(represented_progression) / len(progression_primes)
            if progression_primes
            else 0.0
        ),
        "least_missing_progression_prime": missing[0] if missing else 0,
        "reciprocity_violations": len(reciprocity_violations),
    }


def run_grid(
    max_p: int,
    ells: Sequence[int],
    cutoff: int,
    trials: int,
    seed: int,
) -> list[dict[str, int | float | str]]:
    rng = Random(seed)
    rows: list[dict[str, int | float | str]] = []
    primes = [p for p in range(3, max_p + 1) if p % 4 == 3 and is_prime(p)]
    for p in primes:
        order = MaximalOrder(p)
        identity = IntegralIdeal(
            order,
            tuple(tuple(1 if row == column else 0 for column in range(4)) for row in range(4)),
        )
        for ell in ells:
            if ell == p or ell == 2 or not is_prime(ell):
                continue
            rows.append(measure_case(p, ell, cutoff, identity, "maximal_order"))
            neighbor_prime = choose_neighbor_prime(p, ell)
            for trial in range(trials):
                ideal, _ = order.random_prime_ideal(neighbor_prime, rng)
                rows.append(
                    measure_case(
                        p,
                        ell,
                        cutoff,
                        ideal,
                        f"prime_ideal_{neighbor_prime}_trial_{trial}",
                    )
                )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-p", type=int, default=59)
    parser.add_argument("--ells", default="3,5,7")
    parser.add_argument("--cutoff", type=int, default=5000)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--seed", type=int, default=3102)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.max_p = 11
        args.ells = "3"
        args.cutoff = 1000
        args.trials = 1
    ells = tuple(int(value) for value in args.ells.split(",") if value)
    rows = run_grid(args.max_p, ells, args.cutoff, args.trials, args.seed)
    if not rows:
        raise RuntimeError("the parameter grid produced no cases")

    label = f"p{args.max_p}_ells{'-'.join(map(str, ells))}_x{args.cutoff}"
    output = Path(__file__).resolve().parents[1] / "data" / (
        f"measure_quaternary_prime_sampler_{label}_20260711.csv"
    )
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
