"""
validate_hash_pipeline.py - Exhaust the two-map sum and cofactor pipeline.
Sub-goals: P5.4 / SG-05a and SG-07a
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_hash_pipeline_<params>_<date>.csv
Runtime:  under 1 second on Python 3.13
Checks:   RFC XMD vectors, all field pairs, exact subgroup distributions
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from datetime import date
from fractions import Fraction
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from hash_pipeline import TOY_SUITES, ToyHashToCurveSuite, expand_message_xmd_sha256

RFC_XMD_DST = b"QUUX-V01-CS02-with-expander-SHA256-128"
RFC_XMD_VECTORS = (
    (
        b"",
        32,
        "68a985b87eb6b46952128911f2a4412bbc302a9d759667f8"
        "7f7a21d803f07235",
    ),
    (
        b"abc",
        32,
        "d8ccab23b5985ccea865c6c97b6e5b8350e794e603b4b979"
        "02f53a8a0d605615",
    ),
)


def validate_xmd_vectors() -> None:
    """Check the two compact RFC 9380 Appendix K.1 anchors."""
    for message, length, expected_hex in RFC_XMD_VECTORS:
        actual = expand_message_xmd_sha256(message, RFC_XMD_DST, length)
        if actual.hex() != expected_hex:
            raise AssertionError(f"RFC XMD vector mismatch for msg={message!r}")


def _point_label(point: tuple[int, int] | None) -> str:
    return "identity" if point is None else f"x={point[0]};y={point[1]}"


def _validate_suite(suite: ToyHashToCurveSuite, seed: int) -> dict[str, int | str]:
    subgroup = {
        point
        for point in (None, *suite.curve.affine_points())
        if suite.curve.scalar_mul(suite.subgroup_order, point) is None
    }
    if len(subgroup) != suite.subgroup_order:
        raise AssertionError("declared subgroup does not have the requested order")
    counts: Counter[tuple[int, int] | None] = Counter()
    map_schedules: set[tuple[str, ...]] = set()
    for u in range(suite.curve.p):
        trace: list[str] = []
        mapped = suite.map_field_element(u, trace=trace)
        if not suite.curve.contains(mapped):
            raise AssertionError(f"off-curve map output in {suite.suite_id}")
        map_schedules.add(tuple(trace))
    for u0 in range(suite.curve.p):
        for u1 in range(suite.curve.p):
            output = suite.hash_field_pair(u0, u1)
            if output not in subgroup:
                raise AssertionError(f"subgroup failure in {suite.suite_id}")
            counts[output] += 1

    total = suite.curve.p**2
    uniform = Fraction(1, suite.subgroup_order)
    tv_distance = sum(
        abs(Fraction(counts[point], total) - uniform) for point in subgroup
    ) / 2
    abc_output = suite.hash_to_curve(b"abc")
    if abc_output not in subgroup:
        raise AssertionError("message pipeline output is outside the subgroup")
    return {
        "suite_id": suite.suite_id,
        "method": suite.method,
        "seed": seed,
        "p": suite.curve.p,
        "curve": f"a={suite.curve.a};b={suite.curve.b}",
        "subgroup_order": suite.subgroup_order,
        "cofactor": suite.cofactor,
        "field_pairs": total,
        "subgroup_checks": total,
        "support_size": len(counts),
        "minimum_preimages": min(counts.values()),
        "maximum_preimages": max(counts.values()),
        "tv_distance_fraction": f"{tv_distance.numerator}/{tv_distance.denominator}",
        "tv_distance_decimal": f"{float(tv_distance):.8f}",
        "map_schedule_variants": len(map_schedules),
        "abc_output": _point_label(abc_output),
    }


def validate(seed: int, smoke: bool = False) -> list[dict[str, int | str]]:
    """Validate RFC expansion and every pair for the selected toy suites."""
    validate_xmd_vectors()
    suites = TOY_SUITES[:2] if smoke else TOY_SUITES
    if len({suite.dst for suite in suites}) != len(suites):
        raise AssertionError("suite DSTs are not unique")
    return [_validate_suite(suite, seed) for suite in suites]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5406)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = perf_counter()
    rows = validate(args.seed, smoke=args.smoke)
    elapsed = perf_counter() - started

    label = "smoke" if args.smoke else "full"
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"validate_hash_pipeline_{label}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['field_pairs']) for row in rows)} field pairs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
