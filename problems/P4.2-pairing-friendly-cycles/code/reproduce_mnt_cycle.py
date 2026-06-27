"""
reproduce_mnt_cycle.py - verify the published x=3 MNT6/MNT4 cycle.
Sub-goal: P4.2 / SG-02
Inputs:   --seed <int> [--smoke]
Outputs:  data/reproduce_mnt_cycle_x3_s<seed>_<date>.csv
Runtime:  <1 s for the fixed two-curve regression on Python 3.13.4
Validated against: Chiesa--Chua--Weidner 2019, Example 4.9
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from random import Random
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.curves import Curve, curve_order, curve_order_bsgs, embedding_degree  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class PublishedCurve:
    name: str
    family: str
    field_prime: int
    a: int
    b: int
    expected_order: int
    expected_embedding_degree: int


@dataclass(frozen=True, slots=True)
class VerificationRow:
    name: str
    family: str
    parameter: int
    field_prime: int
    a: int
    b: int
    expected_order: int
    exhaustive_order: int
    bsgs_order: int
    trace: int
    cm_radicand: int
    expected_embedding_degree: int
    computed_embedding_degree: int
    lower_degree_residues: str
    target_degree_residue: int
    rho: str
    seed: int
    elapsed_seconds: str


PUBLISHED_X3 = (
    PublishedCurve("E1", "MNT6", 37, 24, 16, 43, 6),
    PublishedCurve("E2", "MNT4", 43, 36, 5, 37, 4),
)


def verify_curve(spec: PublishedCurve, *, seed: int) -> VerificationRow:
    """Verify one published curve using two exact point-counting methods."""

    started = perf_counter()
    curve = Curve(spec.field_prime, spec.a, spec.b)
    exhaustive_order = curve_order(curve)
    bsgs_order = curve_order_bsgs(curve, Random(seed))
    computed_degree = embedding_degree(
        spec.field_prime,
        spec.expected_order,
        max_degree=spec.expected_embedding_degree,
    )
    residues = [
        pow(spec.field_prime, exponent, spec.expected_order)
        for exponent in range(1, spec.expected_embedding_degree + 1)
    ]

    if exhaustive_order != spec.expected_order:
        raise AssertionError(
            f"{spec.name}: exhaustive order {exhaustive_order} != {spec.expected_order}"
        )
    if bsgs_order != spec.expected_order:
        raise AssertionError(
            f"{spec.name}: BSGS order {bsgs_order} != {spec.expected_order}"
        )
    if computed_degree != spec.expected_embedding_degree:
        raise AssertionError(
            f"{spec.name}: embedding degree {computed_degree} != "
            f"{spec.expected_embedding_degree}"
        )
    if any(residue == 1 for residue in residues[:-1]) or residues[-1] != 1:
        raise AssertionError(f"{spec.name}: exact embedding-degree residues failed")

    trace = spec.field_prime + 1 - exhaustive_order
    return VerificationRow(
        name=spec.name,
        family=spec.family,
        parameter=3,
        field_prime=spec.field_prime,
        a=spec.a,
        b=spec.b,
        expected_order=spec.expected_order,
        exhaustive_order=exhaustive_order,
        bsgs_order=bsgs_order,
        trace=trace,
        cm_radicand=4 * spec.field_prime - trace * trace,
        expected_embedding_degree=spec.expected_embedding_degree,
        computed_embedding_degree=computed_degree,
        lower_degree_residues=";".join(str(value) for value in residues[:-1]),
        target_degree_residue=residues[-1],
        rho=f"{math.log(spec.field_prime) / math.log(spec.expected_order):.12f}",
        seed=seed,
        elapsed_seconds=f"{perf_counter() - started:.6f}",
    )


def reconstruct_cycle(seed: int) -> list[VerificationRow]:
    """Return verified rows for the published x=3 MNT6/MNT4 2-cycle."""

    rows = [
        verify_curve(spec, seed=seed + index)
        for index, spec in enumerate(PUBLISHED_X3)
    ]
    if rows[0].exhaustive_order != rows[1].field_prime:
        raise AssertionError("E1 order does not equal E2 field characteristic")
    if rows[1].exhaustive_order != rows[0].field_prime:
        raise AssertionError("E2 order does not equal E1 field characteristic")
    if sum(row.trace for row in rows) != 2:
        raise AssertionError("2-cycle traces do not sum to 2")
    if len({row.cm_radicand for row in rows}) != 1:
        raise AssertionError("2-cycle CM radicands disagree")
    return rows


def write_rows(rows: list[VerificationRow], output_path: Path) -> None:
    """Write deterministic-column CSV output."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]))
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=4202)
    parser.add_argument(
        "--output",
        type=Path,
        help="override the dated CSV destination",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run the same fixed regression; it is already sub-second",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = reconstruct_cycle(args.seed)
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"reproduce_mnt_cycle_x3_s{args.seed}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    print(f"verified {len(rows)} curves; wrote {output_path}")


if __name__ == "__main__":
    main()

