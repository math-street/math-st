"""Audit the finite-set support bound for translate-probe decomposers."""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve


FIELDS = (
    "date",
    "group_order",
    "base_size",
    "probe_count",
    "shift_schedules",
    "union_bound",
    "minimum_support",
    "maximum_support",
    "strict_schedules",
    "violations",
)


def translated_support(
    curve: Curve,
    factor_base: tuple[AffinePoint, ...],
    shifts: tuple[AffinePoint, ...],
) -> set[AffinePoint]:
    return {
        curve.add(shift, point)
        for shift in shifts
        for point in factor_base
    }


def audit_order_19(max_probes: int = 4) -> list[dict[str, int | str]]:
    curve = Curve(17, 2, 2)
    generator = (5, 1)
    order = 19
    factor_base = tuple(curve.scalar_mul(index, generator) for index in (1, 4, 7, 11))
    group = tuple(curve.scalar_mul(index, generator) for index in range(order))
    rows: list[dict[str, int | str]] = []
    for probe_count in range(1, max_probes + 1):
        sizes: list[int] = []
        bound = probe_count * len(factor_base)
        strict_schedules = 0
        violations = 0
        schedule_count = 0
        for shifts in itertools.combinations(group, probe_count):
            schedule_count += 1
            support_size = len(translated_support(curve, factor_base, shifts))
            sizes.append(support_size)
            strict_schedules += support_size < bound
            violations += support_size > bound
        if schedule_count != math.comb(order, probe_count):
            raise ArithmeticError("shift schedule enumeration was incomplete")
        rows.append(
            {
                "date": date.today().isoformat(),
                "group_order": order,
                "base_size": len(factor_base),
                "probe_count": probe_count,
                "shift_schedules": schedule_count,
                "union_bound": bound,
                "minimum_support": min(sizes),
                "maximum_support": max(sizes),
                "strict_schedules": strict_schedules,
                "violations": violations,
            }
        )
    return rows


def write_rows(path: Path, rows: list[dict[str, int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-probes", type=int, default=4)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    max_probes = 2 if args.smoke else args.max_probes
    rows = audit_order_19(max_probes=max_probes)
    for row in rows:
        print(" ".join(f"{field}={row[field]}" for field in FIELDS))
    if args.smoke:
        return
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"audit_translate_probe_r19_s4_t1-{max_probes}_{date.today().strftime('%Y%m%d')}.csv"
    )
    write_rows(output, rows)
    print(f"output={output}")


if __name__ == "__main__":
    main()
