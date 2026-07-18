"""
audit_quartic_small_gaps.py - exhaust quartic/quartic gaps below 108.
Sub-goal: P4.2 / SG-17
Inputs:   --maximum-gap <even int> [--smoke]
Outputs:  data/audit_quartic_small_gaps_<params>_<date>.csv
Runtime:  <1 s for gaps 2..106
Validated against: the exact (12,10) cycle over fields 11 and 13
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

from classify_mixed_degree_pairs import (  # noqa: E402
    PHI,
    QUARTIC_DEGREES,
    _at_negative,
    _evaluate,
)
from lib.curves import is_prime  # noqa: E402
from search_two_cycles import multiplicative_order_up_to  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class SmallGapAuditRow:
    degree_e1: int
    degree_e2: int
    gap_c: int
    field_p: int | None
    field_q: int | None
    status: str


def audit_small_gaps(maximum_gap: int) -> list[SmallGapAuditRow]:
    """Enumerate every divisor candidate for even gaps through maximum_gap."""

    if maximum_gap < 2 or maximum_gap % 2:
        raise ValueError("maximum_gap must be a positive even integer")
    rows: list[SmallGapAuditRow] = []
    for degree_e1 in QUARTIC_DEGREES:
        first = _at_negative(PHI[degree_e1])
        for degree_e2 in QUARTIC_DEGREES:
            second = PHI[degree_e2]
            for gap in range(2, maximum_gap + 1, 2):
                first_value = _evaluate(first, gap)
                second_value = _evaluate(second, gap)
                exact_fields: list[tuple[int, int]] = []
                for field_p in sympy.divisors(second_value):
                    field_p = int(field_p)
                    if field_p < 5 or not is_prime(field_p):
                        continue
                    field_q = field_p + gap
                    if (
                        not is_prime(field_q)
                        or first_value % field_q
                        or (gap - 1) ** 2 > 4 * field_p
                        or (gap + 1) ** 2 > 4 * field_q
                    ):
                        continue
                    exact = (
                        multiplicative_order_up_to(field_p, field_q, 12),
                        multiplicative_order_up_to(field_q, field_p, 12),
                    )
                    if exact == (degree_e1, degree_e2):
                        exact_fields.append((field_p, field_q))
                if exact_fields:
                    rows.extend(
                        SmallGapAuditRow(
                            degree_e1,
                            degree_e2,
                            gap,
                            field_p,
                            field_q,
                            "exact_cycle",
                        )
                        for field_p, field_q in exact_fields
                    )
                else:
                    rows.append(
                        SmallGapAuditRow(
                            degree_e1,
                            degree_e2,
                            gap,
                            None,
                            None,
                            "audited_empty",
                        )
                    )
    return rows


def write_rows(rows: list[SmallGapAuditRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(SmallGapAuditRow.__dataclass_fields__),
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-gap", type=int, default=106)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    maximum_gap = 10 if args.smoke and args.maximum_gap == 106 else args.maximum_gap
    rows = audit_small_gaps(maximum_gap)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"audit_quartic_small_gaps_c2-{maximum_gap}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    exact = sum(row.status == "exact_cycle" for row in rows)
    print(f"audited {len(rows)} case rows; exact cycles={exact}")
    print(f"sympy={sympy.__version__}; wrote {output_path}")


if __name__ == "__main__":
    main()
