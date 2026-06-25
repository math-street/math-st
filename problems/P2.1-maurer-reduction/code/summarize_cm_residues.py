"""
summarize_cm_residues - Aggregate CM coverage by the input prime modulo 12.
Sub-goal: P2.1 / SG-05
Inputs:   --raw <measure_cm_coverage raw CSV> [--output <CSV>]
Outputs:  data/<raw-stem>_residues.csv, or a dated smoke CSV
Runtime:  Under one second for the recorded 4,096-prime files.
Validated against: fixed hand-counted rows in code/tests/test_measure_cm_coverage.py.
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from measure_smooth_orders import wilson_interval


def summarize_residues(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    keys = sorted(
        {
            (
                int(row["bits"]),
                int(row["smoothness_exponent"]),
                int(row["discriminant_bound"]),
                int(row["prime_mod_12"]),
            )
            for row in rows
        }
    )
    summaries: list[dict[str, object]] = []
    for bits, exponent, discriminant_bound, residue in keys:
        selected = [
            row
            for row in rows
            if int(row["bits"]) == bits
            and int(row["smoothness_exponent"]) == exponent
            and int(row["discriminant_bound"]) == discriminant_bound
            and int(row["prime_mod_12"]) == residue
        ]
        count = len(selected)
        explicit = sum(int(row["explicit_success"]) for row in selected)
        bounded = sum(int(row["bounded_cm_success"]) for row in selected)
        explicit_low, explicit_high = wilson_interval(explicit, count)
        bounded_low, bounded_high = wilson_interval(bounded, count)
        summaries.append(
            {
                "bits": bits,
                "smoothness_exponent": exponent,
                "discriminant_bound": discriminant_bound,
                "prime_mod_12": residue,
                "primes": count,
                "explicit_successes": explicit,
                "explicit_rate": explicit / count,
                "explicit_wilson_95_low": explicit_low,
                "explicit_wilson_95_high": explicit_high,
                "bounded_cm_successes": bounded,
                "bounded_cm_rate": bounded / count,
                "bounded_cm_wilson_95_low": bounded_low,
                "bounded_cm_wilson_95_high": bounded_high,
            }
        )
    return summaries


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def smoke_rows() -> list[dict[str, str]]:
    return [
        {
            "bits": "10",
            "smoothness_exponent": "2",
            "discriminant_bound": "1000",
            "prime_mod_12": residue,
            "explicit_success": explicit,
            "bounded_cm_success": bounded,
        }
        for residue, explicit, bounded in ((1, "1", "1"), (11, "0", "1"))
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    if arguments.smoke:
        rows = smoke_rows()
        default_output = (
            PROBLEM_ROOT
            / "data"
            / f"summarize_cm_residues_smoke_{date.today():%Y%m%d}.csv"
        )
    else:
        if arguments.raw is None:
            raise ValueError("--raw is required unless --smoke is used")
        rows = read_csv(arguments.raw)
        default_output = arguments.raw.with_name(
            arguments.raw.name.removesuffix("_raw.csv") + "_residues.csv"
        )
    output = arguments.output or default_output
    write_csv(output, summarize_residues(rows))
    print(output)


if __name__ == "__main__":
    main()
