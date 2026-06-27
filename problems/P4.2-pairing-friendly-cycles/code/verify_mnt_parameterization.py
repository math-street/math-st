"""
verify_mnt_parameterization.py - check every degree-(4,6) hit has MNT form.
Sub-goal: P4.2 / SG-04 extension
Inputs:   --candidates <csv> [--smoke]
Outputs:  data/verify_mnt_parameterization_<params>_<date>.csv
Runtime:  <1 s for the 22-bit ledger
Validated against: published x=3 fields 37 and 43
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    PROBLEM_ROOT
    / "data"
    / "search_two_cycles_targeted_p5-4194303_k3-12_20260708_candidates.csv"
)


@dataclass(frozen=True, slots=True)
class MntParameterRow:
    field_prime_e1: int
    field_prime_e2: int
    embedding_degree_e1: int
    embedding_degree_e2: int
    gap: int
    parameter_x: int
    orientation: str


def verify_mnt_pair(p: int, q: int, k1: int, k2: int) -> MntParameterRow:
    """Verify and return the MNT parameter for one degree-(4,6) hit."""

    if not 5 <= p < q:
        raise ValueError("expected primes ordered as 5 <= p < q")
    gap = q - p
    if gap % 2:
        raise AssertionError("the gap between odd primes must be even")
    x = gap // 2
    if (k1, k2) == (6, 4):
        expected = (4 * x * x + 1, 4 * x * x + 2 * x + 1)
        orientation = "MNT6-MNT4"
    elif (k1, k2) == (4, 6):
        expected = (4 * x * x - 2 * x + 1, 4 * x * x + 1)
        orientation = "MNT4-MNT6"
    else:
        raise ValueError("degree pair must be (6,4) or (4,6)")
    if (p, q) != expected:
        raise AssertionError(f"fields {(p, q)} do not match MNT parameter x={x}")
    return MntParameterRow(p, q, k1, k2, gap, x, orientation)


def verify_ledger(path: Path) -> list[MntParameterRow]:
    with path.open(newline="", encoding="utf-8") as handle:
        source = [row for row in csv.DictReader(handle) if row["status"] == "hit"]
    output = []
    for row in source:
        degrees = (int(row["embedding_degree_e1"]), int(row["embedding_degree_e2"]))
        if degrees not in {(6, 4), (4, 6)}:
            continue
        output.append(
            verify_mnt_pair(
                int(row["field_prime_e1"]),
                int(row["field_prime_e2"]),
                degrees[0],
                degrees[1],
            )
        )
    if not output:
        raise ValueError("ledger contains no degree-(4,6) hits")
    return output


def write_rows(rows: list[MntParameterRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MntParameterRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = verify_ledger(args.candidates)
    if args.smoke:
        rows = rows[:1]
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"verify_mnt_parameterization_n{len(rows)}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    print(f"verified MNT parameterization for {len(rows)} degree-(4,6) hits")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

