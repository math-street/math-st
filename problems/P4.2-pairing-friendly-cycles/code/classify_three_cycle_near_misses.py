"""
classify_three_cycle_near_misses.py - canonicalize two-target-edge near misses.
Sub-goal: P4.2 / SG-11
Inputs:   --candidates <csv> [--smoke]
Outputs:  data/classify_three_cycle_near_misses_<params>_<date>.csv
Runtime:  <1 s for the 22-bit 42-row ledger
Validated against: the x=480 MNT chain and the degree-483882 residual row
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter
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
from search_two_cycles import primes_below  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    PROBLEM_ROOT
    / "data"
    / "search_three_cycles_targeted_p5-4194303_k3-12_20260708_candidates.csv"
)


@dataclass(frozen=True, slots=True)
class ClassifiedNearMiss:
    source_field_e1: int
    source_field_e2: int
    source_field_e3: int
    canonical_field_p: int
    canonical_field_q: int
    canonical_field_r: int
    target_degree_p_to_q: int
    target_degree_q_to_r: int
    closing_degree_r_to_p: int
    signed_gap_q_minus_p: int
    signed_gap_r_minus_q: int
    maximum_field_prime: int
    first_appears_above_16bit: bool
    family: str
    parameter_x: int | None


def _bounded_degree(value: str) -> int | None:
    return int(value) if value.isdigit() and 3 <= int(value) <= 12 else None


def _mnt_parameter(
    p: int,
    q: int,
    r: int,
    degree_1: int,
    degree_2: int,
) -> int | None:
    gap_1 = q - p
    gap_2 = r - q
    if (degree_1, degree_2) != (4, 6) or gap_1 != gap_2 or gap_1 == 0:
        return None
    if abs(gap_1) % 2:
        return None
    x = abs(gap_1) // 2
    a = 4 * x * x - 2 * x + 1
    b = 4 * x * x + 1
    c = 4 * x * x + 2 * x + 1
    if (p, q, r) not in ((a, b, c), (c, b, a)):
        return None
    return x


def classify_rows(rows: list[dict[str, str]]) -> list[ClassifiedNearMiss]:
    """Rotate each row so the unique non-target edge is the closing edge."""

    near_misses = [row for row in rows if row["status"] == "two_of_three"]
    maximum_field = max(
        int(row[f"field_prime_e{position}"])
        for row in near_misses
        for position in (1, 2, 3)
    )
    factor_primes = primes_below(math.isqrt(maximum_field) + 2)
    classified: list[ClassifiedNearMiss] = []
    for row in near_misses:
        fields = tuple(int(row[f"field_prime_e{i}"]) for i in (1, 2, 3))
        bounded = tuple(_bounded_degree(row[f"embedding_degree_e{i}"]) for i in (1, 2, 3))
        missing = [index for index, degree in enumerate(bounded) if degree is None]
        if len(missing) != 1:
            raise ValueError(f"row does not have exactly two target edges: {fields}")
        exact = tuple(
            exact_multiplicative_order(fields[i], fields[(i + 1) % 3], factor_primes)
            for i in range(3)
        )
        start = (missing[0] + 1) % 3
        indices = (start, (start + 1) % 3, (start + 2) % 3)
        p, q, r = (fields[index] for index in indices)
        degree_1, degree_2, closing_degree = (exact[index] for index in indices)
        if not (3 <= degree_1 <= 12 and 3 <= degree_2 <= 12):
            raise AssertionError(f"canonical target edges failed for {fields}")
        parameter_x = _mnt_parameter(p, q, r, degree_1, degree_2)
        classified.append(
            ClassifiedNearMiss(
                source_field_e1=fields[0],
                source_field_e2=fields[1],
                source_field_e3=fields[2],
                canonical_field_p=p,
                canonical_field_q=q,
                canonical_field_r=r,
                target_degree_p_to_q=degree_1,
                target_degree_q_to_r=degree_2,
                closing_degree_r_to_p=closing_degree,
                signed_gap_q_minus_p=q - p,
                signed_gap_r_minus_q=r - q,
                maximum_field_prime=max(fields),
                first_appears_above_16bit=max(fields) >= 2**16,
                family=(
                    "consecutive_mnt_chain"
                    if parameter_x is not None
                    else "unclassified_residual"
                ),
                parameter_x=parameter_x,
            )
        )
    return classified


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_rows(rows: list[ClassifiedNearMiss], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(ClassifiedNearMiss.__dataclass_fields__),
        )
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
    rows = classify_rows(load_rows(args.candidates))
    if args.smoke:
        rows = rows[:10]
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"classify_three_cycle_near_misses_n{len(rows)}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    families = Counter(row.family for row in rows)
    high_residuals = sum(
        row.first_appears_above_16bit and row.family == "unclassified_residual"
        for row in rows
    )
    print(
        f"classified {len(rows)} rows; families={dict(families)}; "
        f"post-16-bit residuals={high_residuals}"
    )
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
