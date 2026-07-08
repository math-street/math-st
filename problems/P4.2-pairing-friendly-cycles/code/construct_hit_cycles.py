"""
construct_hit_cycles.py - instantiate and verify every SG-04 arithmetic hit.
Sub-goal: P4.2 / SG-04
Inputs:   --candidates <csv> --seed <int> --max-attempts <int>
          [--minimum-field <int>] [--smoke]
Outputs:  data/construct_hit_cycles_<params>_<date>.csv
Runtime:  recorded per curve; intended input is the frozen 16-bit hit ledger
Validated against: the target order and degree in each exhaustive-search row
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import date
from math import isqrt
from pathlib import Path
from random import Random
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.curves import (  # noqa: E402
    Curve,
    curve_order,
    curve_order_bsgs,
    embedding_degree,
    is_prime,
    quadratic_twist,
)

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    PROBLEM_ROOT
    / "data"
    / "search_two_cycles_p5-65535_k3-12_20260708_candidates.csv"
)


@dataclass(frozen=True, slots=True)
class ConstructedCurveRow:
    cycle: str
    position: str
    field_prime: int
    a: int
    b: int
    expected_order: int
    bsgs_order: int
    exhaustive_order: int | None
    trace: int
    cm_radicand: int
    embedding_degree: int
    coefficient_attempts: int
    bsgs_isolation_failures: int
    seed: int
    elapsed_seconds: str
    verification_method: str = "exhaustive_enumeration"
    independently_verified_order: int | None = None
    witness_x: int | None = None
    witness_y: int | None = None


def verify_prime_order_in_hasse_interval(
    curve: Curve,
    target_order: int,
    *,
    exhaustive_limit: int,
) -> tuple[int, str, tuple[int, int] | None]:
    """Verify an exact order by enumeration or a prime-order Hasse certificate."""

    if curve.p <= exhaustive_limit:
        exhaustive_order = curve_order(curve)
        if exhaustive_order != target_order:
            raise AssertionError(
                f"exhaustive order {exhaustive_order} != target {target_order}"
            )
        return exhaustive_order, "exhaustive_enumeration", None
    if not is_prime(target_order):
        raise ValueError("Hasse certificate requires a prime target order")
    radius = isqrt(4 * curve.p)
    lower = curve.p + 1 - radius
    upper = curve.p + 1 + radius
    first_multiple = (lower + target_order - 1) // target_order
    last_multiple = upper // target_order
    if (first_multiple, last_multiple) != (1, 1):
        raise AssertionError(
            f"target {target_order} is not the unique positive multiple "
            f"in the Hasse interval [{lower}, {upper}]"
        )
    witness = curve.first_affine_point()
    if not curve.contains(witness) or curve.scalar_mul(target_order, witness) is not None:
        raise AssertionError("prime-order Hasse witness does not have target order")
    return target_order, "prime_point_hasse_certificate", witness


def find_curve_with_order(
    field_prime: int,
    target_order: int,
    *,
    seed: int,
    max_attempts: int,
    exhaustive_limit: int = (1 << 22) - 1,
) -> tuple[Curve, int, int, int, float]:
    """Find by BSGS, then independently verify the exact group order."""

    rng = Random(seed)
    started = perf_counter()
    bsgs_isolation_failures = 0
    for attempt in range(1, max_attempts + 1):
        a = rng.randrange(field_prime)
        b = rng.randrange(field_prime)
        try:
            curve = Curve(field_prime, a, b)
        except ValueError as error:
            if str(error) != "singular curve":
                raise
            continue
        try:
            bsgs_order = curve_order_bsgs(curve, rng)
        except RuntimeError as error:
            if not str(error).startswith("point orders did not isolate the curve order"):
                raise
            bsgs_isolation_failures += 1
            continue
        if bsgs_order != target_order:
            if 2 * field_prime + 2 - bsgs_order != target_order:
                continue
            curve = quadratic_twist(curve)
            bsgs_order = curve_order_bsgs(curve, rng)
            if bsgs_order != target_order:
                raise AssertionError(
                    "quadratic-twist complement predicted the target order, "
                    f"but BSGS returned {bsgs_order} instead of {target_order}"
                )
        verify_prime_order_in_hasse_interval(
            curve,
            target_order,
            exhaustive_limit=exhaustive_limit,
        )
        return (
            curve,
            bsgs_order,
            attempt,
            bsgs_isolation_failures,
            perf_counter() - started,
        )
    raise RuntimeError(
        f"no curve of order {target_order} over F_{field_prime} in "
        f"{max_attempts} attempts"
    )


def load_hits(path: Path) -> list[dict[str, str]]:
    """Load only full arithmetic hits from the SG-04 candidate ledger."""

    with path.open(newline="", encoding="utf-8") as handle:
        hits = [row for row in csv.DictReader(handle) if row["status"] == "hit"]
    if not hits:
        raise ValueError(f"candidate ledger has no hit rows: {path}")
    return hits


def filter_hits_by_minimum_field(
    hits: list[dict[str, str]],
    minimum_field: int,
) -> list[dict[str, str]]:
    """Keep cycles whose largest field prime reaches the requested boundary."""

    if minimum_field < 0:
        raise ValueError("minimum_field must be nonnegative")
    filtered = [
        hit
        for hit in hits
        if max(int(hit["field_prime_e1"]), int(hit["field_prime_e2"]))
        >= minimum_field
    ]
    if not filtered:
        raise ValueError(f"no hit reaches minimum_field={minimum_field}")
    return filtered


def construct_hit_cycles(
    hits: list[dict[str, str]],
    *,
    seed: int,
    max_attempts: int,
    exhaustive_limit: int = (1 << 22) - 1,
) -> list[ConstructedCurveRow]:
    """Construct and validate both curves for every supplied hit row."""

    output: list[ConstructedCurveRow] = []
    for cycle_index, hit in enumerate(hits):
        p = int(hit["field_prime_e1"])
        q = int(hit["field_prime_e2"])
        expected_radicand = int(hit["cm_fundamental_discriminant"])
        conductor = int(hit["cm_conductor"])
        expected_cm_radicand = -expected_radicand * conductor * conductor
        cycle_name = f"{p}-{q}"
        specifications = (
            ("E1", p, q, int(hit["embedding_degree_e1"])),
            ("E2", q, p, int(hit["embedding_degree_e2"])),
        )
        cycle_rows: list[ConstructedCurveRow] = []
        for position_index, (position, field, order, expected_degree) in enumerate(
            specifications
        ):
            curve_seed = seed + 2 * cycle_index + position_index
            curve, bsgs_order, attempts, isolation_failures, elapsed = find_curve_with_order(
                field,
                order,
                seed=curve_seed,
                max_attempts=max_attempts,
                exhaustive_limit=exhaustive_limit,
            )
            (
                independently_verified_order,
                verification_method,
                witness,
            ) = verify_prime_order_in_hasse_interval(
                curve,
                order,
                exhaustive_limit=exhaustive_limit,
            )
            exhaustive_order = (
                independently_verified_order
                if verification_method == "exhaustive_enumeration"
                else None
            )
            trace = field + 1 - independently_verified_order
            cm_radicand = 4 * field - trace * trace
            computed_degree = embedding_degree(
                field,
                order,
                max_degree=expected_degree,
            )
            if computed_degree != expected_degree:
                raise AssertionError(
                    f"{cycle_name}/{position}: degree {computed_degree} != {expected_degree}"
                )
            if cm_radicand != expected_cm_radicand:
                raise AssertionError(
                    f"{cycle_name}/{position}: CM radicand {cm_radicand} != "
                    f"{expected_cm_radicand}"
                )
            cycle_rows.append(
                ConstructedCurveRow(
                    cycle=cycle_name,
                    position=position,
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
                    verification_method=verification_method,
                    independently_verified_order=independently_verified_order,
                    witness_x=None if witness is None else witness[0],
                    witness_y=None if witness is None else witness[1],
                )
            )
        if (
            cycle_rows[0].independently_verified_order
            != cycle_rows[1].field_prime
        ):
            raise AssertionError(f"{cycle_name}: E1 order does not close the cycle")
        if (
            cycle_rows[1].independently_verified_order
            != cycle_rows[0].field_prime
        ):
            raise AssertionError(f"{cycle_name}: E2 order does not close the cycle")
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
    parser.add_argument("--seed", type=int, default=4203)
    parser.add_argument("--max-attempts", type=int, default=20_000)
    parser.add_argument(
        "--minimum-field",
        type=int,
        default=0,
        help="construct only cycles whose largest field reaches this value",
    )
    parser.add_argument(
        "--exhaustive-limit",
        type=int,
        default=(1 << 22) - 1,
        help=(
            "enumerate equations through this field; use a prime-point Hasse "
            "certificate above it"
        ),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    hits = load_hits(args.candidates)
    hits = filter_hits_by_minimum_field(hits, args.minimum_field)
    if args.smoke:
        hits = hits[:1]
    rows = construct_hit_cycles(
        hits,
        seed=args.seed,
        max_attempts=args.max_attempts,
        exhaustive_limit=args.exhaustive_limit,
    )
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / (
            f"construct_hit_cycles_n{len(hits)}_s{args.seed}_"
            f"{date.today():%Y%m%d}.csv"
        )
    )
    write_rows(rows, output_path)
    print(f"constructed and independently verified {len(rows) // 2} cycles")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
