"""
sieve_quartic_local_obstructions.py - locally sieve A016 genus-one rows.
Sub-goal: P4.2 / SG-18
Inputs:   --prime-bound <int> [--smoke]
Outputs:  data/sieve_quartic_local_obstructions_<params>_<date>.csv
Runtime:  <5 s for odd primes through 251 and moduli 8,16,32
Validated against: direct residue enumeration for selected small moduli
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
from reduce_quartic_degree_pairs import (  # noqa: E402
    C,
    _expression,
    reduce_quartic_pairs,
)

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
TWO_POWER_MODULI = (8, 16, 32)


@dataclass(frozen=True, slots=True)
class LocalSieveRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    status: str
    obstruction_modulus: int | None
    obstruction_kind: str
    moduli_tested: int


def _evaluate_mod(expression, value: int, modulus: int) -> int:
    return int(expression.subs(C, value)) % modulus


def _has_two_power_solution(g, second, h: int, modulus: int) -> bool:
    """Test the necessary equation with even c and odd p modulo 2^a."""

    for gap in range(0, modulus, 2):
        g_value = _evaluate_mod(g, gap, modulus)
        second_value = _evaluate_mod(second, gap, modulus)
        for field_p in range(1, modulus, 2):
            value = (
                h * field_p * field_p
                + (h * gap + g_value) * field_p
                - second_value
            ) % modulus
            if value == 0:
                return True
    return False


def _square_roots(prime: int) -> dict[int, tuple[int, ...]]:
    roots: dict[int, list[int]] = {}
    for value in range(prime):
        roots.setdefault(value * value % prime, []).append(value)
    return {residue: tuple(values) for residue, values in roots.items()}


def _has_odd_prime_solution(
    g,
    second,
    h: int,
    prime: int,
    square_roots: dict[int, tuple[int, ...]],
) -> bool:
    """Test equation plus necessary nonzero prime-field residues modulo l."""

    h_mod = h % prime
    for gap in range(prime):
        g_value = _evaluate_mod(g, gap, prime)
        second_value = _evaluate_mod(second, gap, prime)
        linear = (h_mod * gap + g_value) % prime
        if h_mod == 0:
            if linear == 0:
                if second_value != 0:
                    continue
                candidates = range(1, prime)
            else:
                candidates = ((second_value * pow(linear, -1, prime)) % prime,)
        else:
            discriminant = (linear * linear + 4 * h_mod * second_value) % prime
            roots = square_roots.get(discriminant)
            if roots is None:
                continue
            inverse = pow(2 * h_mod, -1, prime)
            candidates = (
                ((-linear + root) * inverse) % prime for root in roots
            )
        for field_p in candidates:
            if field_p != 0 and (field_p + gap) % prime != 0:
                return True
    return False


def sieve_local_obstructions(prime_bound: int) -> list[LocalSieveRow]:
    """Return the first local obstruction, if any, for all 750 A016 rows."""

    if prime_bound < 3:
        raise ValueError("prime_bound must be at least 3")
    primes = [int(value) for value in sympy.primerange(3, prime_bound + 1)]
    root_tables = {prime: _square_roots(prime) for prime in primes}
    source_rows = [
        row
        for row in reduce_quartic_pairs(24)
        if row.classification == "genus_one_after_square_removal"
    ]
    output: list[LocalSieveRow] = []
    for row in source_rows:
        first = _expression(PHI[row.degree_e1], negative=True)
        second = _expression(PHI[row.degree_e2])
        g = sympy.cancel((first - second) / C)
        tested = 0
        obstruction: tuple[int, str] | None = None
        for modulus in TWO_POWER_MODULI:
            tested += 1
            if not _has_two_power_solution(
                g,
                second,
                row.quotient_difference_h,
                modulus,
            ):
                obstruction = (modulus, "two_power_parity")
                break
        if obstruction is None:
            for prime in primes:
                tested += 1
                if not _has_odd_prime_solution(
                    g,
                    second,
                    row.quotient_difference_h,
                    prime,
                    root_tables[prime],
                ):
                    obstruction = (prime, "odd_prime_with_prime_fields")
                    break
        output.append(
            LocalSieveRow(
                row.degree_e1,
                row.degree_e2,
                row.quotient_difference_h,
                "locally_obstructed" if obstruction else "local_survivor",
                obstruction[0] if obstruction else None,
                obstruction[1] if obstruction else "none",
                tested,
            )
        )
    return output


def write_rows(rows: list[LocalSieveRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(LocalSieveRow.__dataclass_fields__),
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
    rows = sieve_local_obstructions(prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"sieve_quartic_local_obstructions_p{prime_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    obstructed = sum(row.status == "locally_obstructed" for row in rows)
    print(
        f"sieved {len(rows)} genus-one rows; obstructed={obstructed}; "
        f"survivors={len(rows) - obstructed}"
    )
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
