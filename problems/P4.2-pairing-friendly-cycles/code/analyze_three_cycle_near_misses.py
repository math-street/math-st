"""
analyze_three_cycle_near_misses.py - compute exact degrees omitted by a bound.
Sub-goal: P4.2 / SG-06 extension
Inputs:   --candidates <csv> --minimum-field <int> [--smoke]
Outputs:  data/analyze_three_cycle_near_misses_<params>_<date>.csv
Runtime:  <1 s for the current candidate ledgers
Validated against: direct residue checks and fixed 20-bit near-miss degrees
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_two_cycles import primes_below  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    PROBLEM_ROOT
    / "data"
    / "search_three_cycles_targeted_p5-4194303_k3-12_20260708_candidates.csv"
)


@dataclass(frozen=True, slots=True)
class ExactNearMissRow:
    field_prime_e1: int
    field_prime_e2: int
    field_prime_e3: int
    bounded_degree_e1: str
    bounded_degree_e2: str
    bounded_degree_e3: str
    exact_degree_e1: int
    exact_degree_e2: int
    exact_degree_e3: int
    missing_positions: str
    maximum_field_prime: int


def exact_multiplicative_order(
    base: int,
    prime_modulus: int,
    factor_primes: list[int],
) -> int:
    """Return ord_modulus(base) by reducing the known multiple modulus-1."""

    if prime_modulus <= 2 or base % prime_modulus == 0:
        raise ValueError("modulus must be an odd prime coprime to the base")
    remaining = prime_modulus - 1
    prime_factors: list[int] = []
    for prime in factor_primes:
        if prime * prime > remaining:
            break
        if remaining % prime:
            continue
        prime_factors.append(prime)
        while remaining % prime == 0:
            remaining //= prime
    if remaining > 1:
        prime_factors.append(remaining)

    order = prime_modulus - 1
    for prime in prime_factors:
        while order % prime == 0 and pow(base, order // prime, prime_modulus) == 1:
            order //= prime
    if pow(base, order, prime_modulus) != 1:
        raise ArithmeticError("computed multiplicative order does not annihilate the base")
    return order


def analyze_near_misses(
    candidate_path: Path,
    *,
    minimum_field: int,
) -> list[ExactNearMissRow]:
    """Compute all three exact degrees for extension near-miss rows."""

    with candidate_path.open(newline="", encoding="utf-8") as handle:
        source_rows = [
            row
            for row in csv.DictReader(handle)
            if row["status"] == "two_of_three"
            and max(int(row[f"field_prime_e{index}"]) for index in (1, 2, 3))
            >= minimum_field
        ]
    if not source_rows:
        raise ValueError("no two-of-three row reaches the requested minimum field")

    maximum_modulus = max(
        int(row[f"field_prime_e{index}"])
        for row in source_rows
        for index in (1, 2, 3)
    )
    factor_primes = primes_below(int(maximum_modulus**0.5) + 2)
    output: list[ExactNearMissRow] = []
    for row in source_rows:
        fields = tuple(int(row[f"field_prime_e{index}"]) for index in (1, 2, 3))
        bounded = tuple(row[f"embedding_degree_e{index}"] for index in (1, 2, 3))
        exact = tuple(
            exact_multiplicative_order(
                fields[index],
                fields[(index + 1) % 3],
                factor_primes,
            )
            for index in range(3)
        )
        for bounded_value, exact_value in zip(bounded, exact):
            if not bounded_value.startswith(">") and int(bounded_value) != exact_value:
                raise AssertionError("bounded and exact embedding degrees disagree")
        missing_positions = ";".join(
            str(index + 1)
            for index, bounded_value in enumerate(bounded)
            if bounded_value.startswith(">")
        )
        output.append(
            ExactNearMissRow(
                field_prime_e1=fields[0],
                field_prime_e2=fields[1],
                field_prime_e3=fields[2],
                bounded_degree_e1=bounded[0],
                bounded_degree_e2=bounded[1],
                bounded_degree_e3=bounded[2],
                exact_degree_e1=exact[0],
                exact_degree_e2=exact[1],
                exact_degree_e3=exact[2],
                missing_positions=missing_positions,
                maximum_field_prime=max(fields),
            )
        )
    return output


def write_rows(rows: list[ExactNearMissRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(ExactNearMissRow.__dataclass_fields__)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--minimum-field", type=int, default=1 << 20)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    minimum_field = 1 if args.smoke else args.minimum_field
    rows = analyze_near_misses(args.candidates, minimum_field=minimum_field)
    if args.smoke:
        rows = rows[:1]
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / (
            f"analyze_three_cycle_near_misses_min{minimum_field}_n{len(rows)}_"
            f"{date.today():%Y%m%d}.csv"
        )
    )
    write_rows(rows, output_path)
    print(f"computed exact degrees for {len(rows)} near-miss rows")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

