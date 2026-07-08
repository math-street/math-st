"""
construct_three_cycle_hits.py - instantiate every full SG-05 directed hit.
Sub-goal: P4.2 / SG-05
Inputs:   --candidates <csv> --seed <int> --max-attempts <int> [--smoke]
Outputs:  data/construct_three_cycle_hits_<params>_<date>.csv
Runtime:  recorded per curve; intended input is the frozen 16-bit hit ledger
Validated against: the target order, CM data, and degree in every search row
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from construct_hit_cycles import (  # noqa: E402
    ConstructedCurveRow,
    find_curve_with_order,
)
from lib.curves import curve_order, embedding_degree  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    PROBLEM_ROOT
    / "data"
    / "search_three_cycles_p5-65535_k3-12_20260708_candidates.csv"
)


def load_hits(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        hits = [row for row in csv.DictReader(handle) if row["status"] == "hit"]
    if not hits:
        raise ValueError(f"candidate ledger has no hit rows: {path}")
    return hits


def construct_three_cycle_hits(
    hits: list[dict[str, str]],
    *,
    seed: int,
    max_attempts: int,
) -> list[ConstructedCurveRow]:
    """Construct and independently verify all three positions of every hit."""

    output: list[ConstructedCurveRow] = []
    for cycle_index, hit in enumerate(hits):
        fields = tuple(int(hit[f"field_prime_e{index}"]) for index in (1, 2, 3))
        degrees = tuple(int(hit[f"embedding_degree_e{index}"]) for index in (1, 2, 3))
        discriminants = tuple(int(hit[f"cm_discriminant_e{index}"]) for index in (1, 2, 3))
        conductors = tuple(int(hit[f"cm_conductor_e{index}"]) for index in (1, 2, 3))
        cycle_name = "-".join(str(field) for field in fields)
        cycle_rows: list[ConstructedCurveRow] = []
        for position_index in range(3):
            field = fields[position_index]
            order = fields[(position_index + 1) % 3]
            expected_degree = degrees[position_index]
            expected_radicand = -discriminants[position_index] * conductors[position_index] ** 2
            curve_seed = seed + 3 * cycle_index + position_index
            curve, bsgs_order, attempts, isolation_failures, elapsed = find_curve_with_order(
                field,
                order,
                seed=curve_seed,
                max_attempts=max_attempts,
            )
            exhaustive_order = curve_order(curve)
            trace = field + 1 - exhaustive_order
            cm_radicand = 4 * field - trace * trace
            computed_degree = embedding_degree(
                field,
                order,
                max_degree=expected_degree,
            )
            if computed_degree != expected_degree:
                raise AssertionError(
                    f"{cycle_name}/E{position_index + 1}: degree mismatch"
                )
            if cm_radicand != expected_radicand:
                raise AssertionError(
                    f"{cycle_name}/E{position_index + 1}: CM mismatch"
                )
            cycle_rows.append(
                ConstructedCurveRow(
                    cycle=cycle_name,
                    position=f"E{position_index + 1}",
                    field_prime=field,
                    a=curve.a % field,
                    b=curve.b % field,
                    expected_order=order,
                    bsgs_order=bsgs_order,
                    exhaustive_order=exhaustive_order,
                    trace=trace,
                    cm_radicand=cm_radicand,
                    embedding_degree=computed_degree,
                    coefficient_attempts=attempts,
                    bsgs_isolation_failures=isolation_failures,
                    seed=curve_seed,
                    elapsed_seconds=f"{elapsed:.6f}",
                )
            )
        if sum(row.trace for row in cycle_rows) != 3:
            raise AssertionError(f"{cycle_name}: traces do not sum to 3")
        if any(
            cycle_rows[index].exhaustive_order != cycle_rows[(index + 1) % 3].field_prime
            for index in range(3)
        ):
            raise AssertionError(f"{cycle_name}: an order does not close the cycle")
        output.extend(cycle_rows)
    return output


def write_rows(rows: list[ConstructedCurveRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(ConstructedCurveRow.__dataclass_fields__)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--seed", type=int, default=4303)
    parser.add_argument("--max-attempts", type=int, default=20_000)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hits = load_hits(args.candidates)
    if args.smoke:
        hits = hits[:1]
    rows = construct_three_cycle_hits(
        hits,
        seed=args.seed,
        max_attempts=args.max_attempts,
    )
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / (
            f"construct_three_cycle_hits_n{len(hits)}_s{args.seed}_"
            f"{date.today():%Y%m%d}.csv"
        )
    )
    write_rows(rows, output_path)
    print(f"constructed and independently verified {len(rows) // 3} directed 3-cycles")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()

