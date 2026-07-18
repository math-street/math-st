"""
canonicalize_quartic_survivors.py - deduplicate the final A018 quartics.
Sub-goal: P4.2 / SG-21
Inputs:   --prime-bound <int> [--smoke]
Outputs:  data/canonicalize_quartic_survivors_<params>_<date>.csv
Runtime:  <5 s
Validated against: exact square-content and squarefree-twist equality in SymPy
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
from reduce_quartic_degree_pairs import C, _expression  # noqa: E402
from sieve_quartic_archimedean import sieve_archimedean  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class CanonicalQuarticRow:
    canonical_curve_id: str
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    square_content: int
    squarefree_twist: int
    normalized_coefficients: str
    multiplicity: int


def canonicalize_survivors(
    prime_bound: int = 251,
    *,
    exclude_odd_obstructions: bool = False,
) -> list[CanonicalQuarticRow]:
    """Map surviving rows to quartics after square-content removal."""

    source_rows = [
        row
        for row in sieve_archimedean(prime_bound)
        if row.status == "survivor"
    ]
    if exclude_odd_obstructions:
        from lift_quartic_singular_primes import audit_singular_primes

        obstructed = {
            (row.degree_e1, row.degree_e2, row.quotient_difference_h)
            for row in audit_singular_primes(8, prime_bound)
            if row.status == "finite_power_obstruction"
        }
        source_rows = [
            row
            for row in source_rows
            if (row.degree_e1, row.degree_e2, row.quotient_difference_h)
            not in obstructed
        ]
    raw: list[tuple[tuple[int, ...], int, int, int, int, int]] = []
    for row in source_rows:
        h = row.quotient_difference_h
        first = _expression(PHI[row.degree_e1], negative=True)
        second = _expression(PHI[row.degree_e2])
        g = sympy.cancel((first - second) / C)
        discriminant = sympy.Poly(
            sympy.expand((h * C + g) ** 2 + 4 * h * second),
            C,
            domain=sympy.ZZ,
        )
        content, primitive = discriminant.primitive()
        factorization = sympy.factorint(int(content))
        square_content = math.prod(
            prime ** (exponent // 2)
            for prime, exponent in factorization.items()
        )
        squarefree_twist = int(content) // square_content**2
        normalized = tuple(
            squarefree_twist * int(value) for value in primitive.all_coeffs()
        )
        raw.append(
            (
                normalized,
                row.degree_e1,
                row.degree_e2,
                h,
                square_content,
                squarefree_twist,
            )
        )
    keys = sorted({entry[0] for entry in raw})
    identifiers = {key: f"QG{index:03d}" for index, key in enumerate(keys, 1)}
    multiplicities = {key: sum(entry[0] == key for entry in raw) for key in keys}
    return [
        CanonicalQuarticRow(
            identifiers[key],
            degree_e1,
            degree_e2,
            h,
            square_content,
            squarefree_twist,
            ",".join(str(value) for value in key),
            multiplicities[key],
        )
        for key, degree_e1, degree_e2, h, square_content, squarefree_twist in raw
    ]


def write_rows(rows: list[CanonicalQuarticRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(CanonicalQuarticRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime-bound", type=int, default=251)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--exclude-odd-obstructions", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prime_bound = 13 if args.smoke and args.prime_bound == 251 else args.prime_bound
    rows = canonicalize_survivors(
        prime_bound,
        exclude_odd_obstructions=args.exclude_odd_obstructions,
    )
    suffix = "_odd_survivors" if args.exclude_odd_obstructions else ""
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"canonicalize_quartic_survivors_p{prime_bound}{suffix}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    curves = len({row.canonical_curve_id for row in rows})
    duplicates = sum(row.multiplicity > 1 for row in rows)
    print(f"canonicalized {len(rows)} rows to {curves} curves; duplicate mappings={duplicates}")
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
