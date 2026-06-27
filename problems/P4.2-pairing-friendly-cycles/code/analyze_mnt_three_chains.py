"""
analyze_mnt_three_chains.py - exhaust the finite MNT 3-chain remainder.
Sub-goal: P4.2 / SG-05 extension
Inputs:   --max-x <int> [--smoke]
Outputs:  data/analyze_mnt_three_chains_x1-<max>_<date>.csv
Runtime:  <1 s for max-x=1025
Validated against: x=3 and the x=480 20-bit near-miss
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from analyze_three_cycle_near_misses import exact_multiplicative_order  # noqa: E402
from lib.curves import is_prime  # noqa: E402
from search_two_cycles import primes_below  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class MntThreeChainRow:
    parameter_x: int
    field_a: int
    field_b: int
    field_c: int
    degree_a_to_b: int
    degree_b_to_c: int
    degree_c_to_a: int
    degree_a_to_c: int
    degree_c_to_b: int
    degree_b_to_a: int
    forward_closes_at_most_12: bool
    reverse_closes_at_most_12: bool


def power_remainder_coefficients(max_degree: int) -> list[tuple[int, int]]:
    """Return (a_k,b_k) with y^k = a_k*y+b_k modulo y^2-2y+4."""

    if max_degree < 1:
        raise ValueError("max_degree must be positive")
    coefficients = [(1, 0)]
    for _ in range(1, max_degree):
        a, b = coefficients[-1]
        coefficients.append((2 * a + b, -4 * a))
    return coefficients


def analyze_mnt_three_chains(max_x: int) -> list[MntThreeChainRow]:
    """Return every all-prime MNT triple through max_x with exact degrees."""

    if max_x < 1:
        raise ValueError("max_x must be positive")
    maximum_field = 4 * max_x * max_x + 2 * max_x + 1
    factor_primes = primes_below(math.isqrt(maximum_field) + 2)
    rows: list[MntThreeChainRow] = []
    for x in range(1, max_x + 1):
        a = 4 * x * x - 2 * x + 1
        b = 4 * x * x + 1
        c = 4 * x * x + 2 * x + 1
        if min(a, b, c) < 5 or not all(is_prime(value) for value in (a, b, c)):
            continue
        degrees = (
            exact_multiplicative_order(a, b, factor_primes),
            exact_multiplicative_order(b, c, factor_primes),
            exact_multiplicative_order(c, a, factor_primes),
            exact_multiplicative_order(a, c, factor_primes),
            exact_multiplicative_order(c, b, factor_primes),
            exact_multiplicative_order(b, a, factor_primes),
        )
        if (degrees[0], degrees[1], degrees[4], degrees[5]) != (4, 6, 4, 6):
            raise AssertionError(f"fixed MNT edge degree failed at x={x}")
        rows.append(
            MntThreeChainRow(
                parameter_x=x,
                field_a=a,
                field_b=b,
                field_c=c,
                degree_a_to_b=degrees[0],
                degree_b_to_c=degrees[1],
                degree_c_to_a=degrees[2],
                degree_a_to_c=degrees[3],
                degree_c_to_b=degrees[4],
                degree_b_to_a=degrees[5],
                forward_closes_at_most_12=3 <= degrees[2] <= 12,
                reverse_closes_at_most_12=3 <= degrees[3] <= 12,
            )
        )
    return rows


def write_rows(rows: list[MntThreeChainRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MntThreeChainRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-x", type=int, default=1025)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    max_x = 50 if args.smoke and args.max_x == 1025 else args.max_x
    rows = analyze_mnt_three_chains(max_x)
    if any(row.forward_closes_at_most_12 or row.reverse_closes_at_most_12 for row in rows):
        raise AssertionError("finite MNT 3-chain remainder contains a closing hit")
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"analyze_mnt_three_chains_x1-{max_x}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    print(f"checked x=1..{max_x}; all-prime triples={len(rows)}; closing hits=0")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

