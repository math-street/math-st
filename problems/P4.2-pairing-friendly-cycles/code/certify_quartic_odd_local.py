"""
certify_quartic_odd_local.py - complete critical odd-prime audit for A018.
Sub-goal: P4.2 / SG-22
Inputs:   --prime-bound <int> [--smoke]
Outputs:  data/certify_quartic_odd_local_<params>_<date>.csv
Runtime:  <10 s
Validated against: direct equation and partial-derivative enumeration
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
from sieve_quartic_archimedean import sieve_archimedean  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
SMALL_ODD_PRIMES = (3, 5, 7, 11, 13, 17)


@dataclass(frozen=True, slots=True)
class OddLocalCertificateRow:
    degree_e1: int
    degree_e2: int
    quotient_difference_h: int
    critical_primes: str
    maximum_critical_prime: int
    status: str
    failed_primes: str
    singular_only_primes: str


def _value(expression, c_value: int, modulus: int) -> int:
    return int(expression.subs(C, c_value)) % modulus


def _prime_status(g, second, h: int, prime: int) -> str:
    """Return nonsingular, singular_only, or no_solution for one prime."""

    g_derivative = sympy.diff(g, C)
    second_derivative = sympy.diff(second, C)
    singular_found = False
    for gap in range(prime):
        g_value = _value(g, gap, prime)
        second_value = _value(second, gap, prime)
        g_derivative_value = _value(g_derivative, gap, prime)
        second_derivative_value = _value(second_derivative, gap, prime)
        for field_p in range(1, prime):
            if (field_p + gap) % prime == 0:
                continue
            equation = (
                h * field_p * field_p
                + (h * gap + g_value) * field_p
                - second_value
            ) % prime
            if equation:
                continue
            derivative_p = (
                2 * h * field_p + h * gap + g_value
            ) % prime
            derivative_c = (
                (h + g_derivative_value) * field_p
                - second_derivative_value
            ) % prime
            if derivative_p or derivative_c:
                return "nonsingular"
            singular_found = True
    return "singular_only" if singular_found else "no_solution"


def certify_odd_local(prime_bound: int = 251) -> list[OddLocalCertificateRow]:
    """Audit all primes not covered uniformly by the good-prime argument."""

    survivors = [
        row
        for row in sieve_archimedean(prime_bound)
        if row.status == "survivor"
    ]
    output: list[OddLocalCertificateRow] = []
    for row in survivors:
        h = row.quotient_difference_h
        first = _expression(PHI[row.degree_e1], negative=True)
        second = _expression(PHI[row.degree_e2])
        g = sympy.cancel((first - second) / C)
        discriminant_polynomial = sympy.expand((h * C + g) ** 2 + 4 * h * second)
        curve_discriminant = abs(int(sympy.discriminant(discriminant_polynomial, C)))
        critical = set(SMALL_ODD_PRIMES)
        critical.update(
            int(prime)
            for prime in sympy.factorint(abs(h))
            if int(prime) != 2
        )
        critical.update(
            int(prime)
            for prime in sympy.factorint(curve_discriminant)
            if int(prime) != 2
        )
        statuses = {
            prime: _prime_status(g, second, h, prime)
            for prime in sorted(critical)
        }
        failed = [prime for prime, status in statuses.items() if status == "no_solution"]
        singular = [
            prime for prime, status in statuses.items() if status == "singular_only"
        ]
        if failed:
            status = "odd_local_obstruction"
        elif singular:
            status = "higher_power_required"
        else:
            status = "all_odd_primes_certified"
        output.append(
            OddLocalCertificateRow(
                row.degree_e1,
                row.degree_e2,
                h,
                ",".join(str(prime) for prime in sorted(critical)),
                max(critical),
                status,
                ",".join(str(prime) for prime in failed),
                ",".join(str(prime) for prime in singular),
            )
        )
    return output


def write_rows(rows: list[OddLocalCertificateRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(OddLocalCertificateRow.__dataclass_fields__),
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
    rows = certify_odd_local(prime_bound)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"certify_quartic_odd_local_p{prime_bound}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    print(f"audited {len(rows)} rows at every critical odd prime; statuses={counts}")
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
