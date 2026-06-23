"""Summarize the exact quadratic curve/target variation tables.

Sub-goal: P1.3 / SG-08 and SG-09
Inputs: data/measure_quadratic_variants_q*_20260709.csv
Outputs: data/quadratic_family_summary_20260709.csv by default
Runtime: under one second
Validated against: per-row exact status and invariant assertions
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


FIELDS = [
    "q",
    "rows",
    "unique_curves",
    "unique_targets",
    "complete_rows",
    "verified_roots",
    "top_shape_verified_rows",
    "nonredundant_field_equation_rows",
    "first_fall_values",
    "regularity_values",
    "solving_degree_values",
    "core_solving_degree_values",
    "core_field_remainder_degree_values",
    "mutant_regularity_values",
    "mutant_solving_degree_values",
]


def _values(rows: list[dict[str, str]], field: str) -> str:
    return ";".join(sorted({row[field] for row in rows}, key=lambda item: int(item)))


def summarize(paths: list[Path]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                grouped[int(row["q"])].append(row)
    summaries: list[dict[str, object]] = []
    for q, rows in sorted(grouped.items()):
        summary = {
            "q": q,
            "rows": len(rows),
            "unique_curves": len(
                {
                    (row["curve_a_coordinates"], row["curve_b_coordinates"])
                    for row in rows
                }
            ),
            "unique_targets": len({row["target_coordinates"] for row in rows}),
            "complete_rows": sum(row["status"] == "complete" for row in rows),
            "verified_roots": sum(row["known_solution_verified"] == "True" for row in rows),
            "top_shape_verified_rows": sum(
                row["quadratic_top_shape_verified"] == "True" for row in rows
            ),
            "nonredundant_field_equation_rows": sum(
                row["core_field_equations_redundant"] == "False" for row in rows
            ),
            "first_fall_values": _values(rows, "first_fall_degree"),
            "regularity_values": _values(rows, "degree_of_regularity"),
            "solving_degree_values": _values(rows, "solving_degree"),
            "core_solving_degree_values": _values(rows, "core_solving_degree"),
            "core_field_remainder_degree_values": _values(
                rows, "core_field_remainder_max_degree"
            ),
            "mutant_regularity_values": _values(rows, "mutant_degree_of_regularity"),
            "mutant_solving_degree_values": _values(rows, "mutant_solving_degree"),
        }
        assert summary["complete_rows"] == len(rows)
        assert summary["verified_roots"] == len(rows)
        assert summary["top_shape_verified_rows"] == len(rows)
        assert summary["nonredundant_field_equation_rows"] == len(rows)
        assert summary["first_fall_values"] == "5"
        assert summary["regularity_values"] == str(q)
        assert summary["solving_degree_values"] == str(q)
        assert summary["core_solving_degree_values"] == "5"
        assert max(
            int(value)
            for value in str(summary["core_field_remainder_degree_values"]).split(";")
        ) <= 3
        assert max(
            int(value) for value in str(summary["mutant_regularity_values"]).split(";")
        ) <= 4
        assert max(
            int(value)
            for value in str(summary["mutant_solving_degree_values"]).split(";")
        ) <= 5
        summaries.append(summary)
    return summaries


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, nargs="*")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = Path(__file__).resolve().parents[1] / "data"
    inputs = args.inputs or sorted(
        path
        for path in data_dir.glob("measure_quadratic_variants_q*_*.csv")
        if "smoke" not in path.name
    )
    output = args.output or data_dir / f"quadratic_family_summary_{date.today():%Y%m%d}.csv"
    rows = summarize(inputs)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)
    print(f"wrote {len(rows)} summary rows to {output}")


if __name__ == "__main__":
    main()
