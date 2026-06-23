"""Merge repeated Weil-degree runs into one canonical experiment table.

Sub-goals: P1.3 / SG-04 through SG-07
Inputs: data/measure_weil_degrees*.csv
Output: data/first_fall_vs_solving_20260701.csv by default
Selection rule: for each (q,n,m,target_mode), retain the row that reached the
latest pipeline stage; break ties in favour of complete and later input files.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


STAGES = {
    "": 0,
    "target_selection": 1,
    "system_build": 2,
    "first_fall": 3,
    "degree_of_regularity": 4,
    "groebner_basis": 5,
    "solving_degree": 6,
}


def inferred_stage(row: dict[str, str]) -> str:
    """Infer the last stage for legacy rows that predate stage logging."""

    if row.get("solving_degree"):
        return "solving_degree"
    if row.get("gb_size"):
        return "groebner_basis"
    if row.get("degree_of_regularity"):
        return "degree_of_regularity"
    if row.get("first_fall_degree"):
        return "first_fall"
    if row.get("core_equation_count"):
        return "system_build"
    if row.get("target_coordinates"):
        return "target_selection"
    return ""


def row_score(row: dict[str, str], input_index: int) -> tuple[int, int, int]:
    stage = row.get("stage_completed") or inferred_stage(row)
    complete = int(row.get("status") == "complete")
    return STAGES.get(stage, 0), complete, input_index


def merge_rows(paths: Iterable[Path]) -> list[dict[str, str]]:
    """Return one best row per deterministic parameter tuple."""

    selected: dict[tuple[int, int, int, str], tuple[tuple[int, int, int], dict[str, str]]] = {}
    for input_index, path in enumerate(paths):
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for source_row in csv.DictReader(handle):
                row = dict(source_row)
                row["stage_completed"] = row.get("stage_completed") or inferred_stage(row)
                row["source_file"] = path.name
                key = (
                    int(row["q"]),
                    int(row["n"]),
                    int(row["m"]),
                    row["target_mode"],
                )
                score = row_score(row, input_index)
                if key not in selected or score >= selected[key][0]:
                    selected[key] = score, row
    return [
        item[1]
        for _, item in sorted(
            selected.items(),
            key=lambda pair: (pair[0][0], pair[0][1], pair[0][2], pair[0][3]),
        )
    ]


def write_rows(rows: list[dict[str, str]], output: Path) -> None:
    if not rows:
        raise ValueError("no experiment rows found")
    preferred = [
        "q", "n", "m", "target_mode", "status", "stage_completed",
        "first_fall_degree", "degree_of_regularity", "solving_degree",
        "solving_minus_first_fall", "known_solution_verified",
    ]
    remaining = sorted({key for row in rows for key in row} - set(preferred))
    fieldnames = preferred + remaining
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "data"
        / "first_fall_vs_solving_20260701.csv",
    )
    args = parser.parse_args()
    data_dir = Path(__file__).resolve().parents[1] / "data"
    inputs = args.inputs or sorted(data_dir.glob("measure_weil_degrees*.csv"))
    rows = merge_rows(path for path in inputs if path.resolve() != args.output.resolve())
    write_rows(rows, args.output)
    print(f"wrote {len(rows)} canonical rows to {args.output}")


if __name__ == "__main__":
    main()
