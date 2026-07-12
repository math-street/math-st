"""
validate_curve_transports.py - Exhaust Montgomery and Edwards form transports.
Sub-goals: P5.4 / SG-02a, SG-05a, and SG-07a
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_curve_transports_<params>_<date>.csv
Runtime:  under 1 second on Python 3.13
Checks:   direct oracles, schedules, group laws, subgroup-cleared pair sums
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from hash_pipeline import TOY_EDWARDS_SUITE, TOY_MONTGOMERY_SUITE
from lib.curves import (
    MontgomeryCurve,
    inv0_mod,
    map_to_curve_elligator2,
    map_to_curve_elligator2_edwards,
    map_to_curve_svdw_montgomery,
    montgomery_to_twisted_edwards,
    montgomery_weierstrass_curve,
    twisted_edwards_from_montgomery,
    weierstrass_to_montgomery,
)
from validate_rfc_maps import elligator2_oracle
from validate_svdw import svdw_oracle


def montgomery_to_edwards_oracle(
    curve: MontgomeryCurve,
    point: tuple[int, int],
) -> tuple[int, int]:
    """Use ordinary branches and inversions for the Appendix D.1 map."""
    s, t = point
    p = curve.p
    if t == 0 or s == p - 1:
        return 0, 1
    return (
        s * inv0_mod(t, p) % p,
        (s - 1) * inv0_mod(s + 1, p) % p,
    )


def _montgomery_points(curve: MontgomeryCurve) -> tuple[tuple[int, int] | None, ...]:
    affine = tuple(
        (s, t)
        for s in range(curve.p)
        for t in range(curve.p)
        if curve.contains((s, t))
    )
    return None, *affine


def _validate_montgomery_elligator(seed: int) -> dict[str, int | str]:
    suite = TOY_MONTGOMERY_SUITE
    curve = suite.curve
    points = _montgomery_points(curve)
    weierstrass = montgomery_weierstrass_curve(curve)
    weierstrass_points = (None, *weierstrass.affine_points())
    transported = {
        None
        if point is None
        else weierstrass_to_montgomery(curve, point)
        for point in weierstrass_points
    }
    if transported != set(points):
        raise AssertionError("Weierstrass-to-Montgomery transport is not bijective")
    for left in points:
        for right in points:
            result = suite.add(left, right)
            if not curve.contains(result):
                raise AssertionError("Montgomery addition left the curve")
    for left in points:
        for middle in points:
            for right in points:
                if suite.add(suite.add(left, middle), right) != suite.add(
                    left, suite.add(middle, right)
                ):
                    raise AssertionError("Montgomery associativity failure")

    schedules: set[tuple[str, ...]] = set()
    for u in range(curve.p):
        trace: list[str] = []
        actual = map_to_curve_elligator2(curve, u, suite.z, trace=trace)
        if actual != elligator2_oracle(curve, u, suite.z):
            raise AssertionError(f"Montgomery Elligator mismatch at u={u}")
        schedules.add(tuple(trace))

    subgroup = {suite.scalar_mul(suite.cofactor, point) for point in points}
    if len(subgroup) != suite.subgroup_order:
        raise AssertionError("Montgomery cofactor image has wrong order")
    outputs = {
        suite.hash_field_pair(u0, u1)
        for u0 in range(curve.p)
        for u1 in range(curve.p)
    }
    if not outputs <= subgroup:
        raise AssertionError("Montgomery pair sum escaped the subgroup")
    return {
        "form": "montgomery",
        "mapping": "elligator2",
        "seed": seed,
        "p": curve.p,
        "curve_parameters": f"j={curve.j};k={curve.k}",
        "inputs_tested": curve.p,
        "on_curve": curve.p,
        "oracle_matches": curve.p,
        "schedule_variants": len(schedules),
        "group_order": len(points),
        "group_law_checks": len(points) ** 2 + len(points) ** 3,
        "pipeline_field_pairs": curve.p**2,
        "subgroup_order": suite.subgroup_order,
        "subgroup_support": len(outputs),
    }


def _validate_edwards_elligator(seed: int) -> dict[str, int | str]:
    suite = TOY_EDWARDS_SUITE
    curve = suite.curve
    montgomery = suite.montgomery_curve
    points = tuple(curve.points())
    schedules: set[tuple[str, ...]] = set()
    for u in range(curve.p):
        trace: list[str] = []
        actual = map_to_curve_elligator2_edwards(
            montgomery,
            u,
            suite.z,
            trace=trace,
        )
        source = elligator2_oracle(montgomery, u, suite.z)
        expected = montgomery_to_edwards_oracle(montgomery, source)
        if actual != expected or not curve.contains(actual):
            raise AssertionError(f"twisted-Edwards transport mismatch at u={u}")
        schedules.add(tuple(trace))

    denominator_failures = 0
    for left in points:
        for right in points:
            product = curve.d * left[0] * right[0] * left[1] * right[1] % curve.p
            denominator_failures += (1 + product) % curve.p == 0
            denominator_failures += (1 - product) % curve.p == 0
            result = curve.add(left, right)
            if not curve.contains(result):
                raise AssertionError("twisted-Edwards addition left the curve")
    for left in points:
        for middle in points:
            for right in points:
                if curve.add(curve.add(left, middle), right) != curve.add(
                    left, curve.add(middle, right)
                ):
                    raise AssertionError("twisted-Edwards associativity failure")
    if denominator_failures:
        raise AssertionError("selected Edwards addition law had a zero denominator")

    subgroup = {curve.scalar_mul(suite.cofactor, point) for point in points}
    outputs = {
        suite.hash_field_pair(u0, u1)
        for u0 in range(curve.p)
        for u1 in range(curve.p)
    }
    if len(subgroup) != suite.subgroup_order or not outputs <= subgroup:
        raise AssertionError("twisted-Edwards subgroup clearing failed")
    return {
        "form": "twisted_edwards",
        "mapping": "elligator2_transport",
        "seed": seed,
        "p": curve.p,
        "curve_parameters": f"a={curve.a};d={curve.d}",
        "inputs_tested": curve.p,
        "on_curve": curve.p,
        "oracle_matches": curve.p,
        "schedule_variants": len(schedules),
        "group_order": len(points),
        "group_law_checks": len(points) ** 2 + len(points) ** 3,
        "pipeline_field_pairs": curve.p**2,
        "subgroup_order": suite.subgroup_order,
        "subgroup_support": len(outputs),
    }


def _validate_montgomery_svdw(seed: int) -> dict[str, int | str]:
    curve = MontgomeryCurve(11, 3, 1)
    weierstrass = montgomery_weierstrass_curve(curve)
    z = 9
    schedules: set[tuple[str, ...]] = set()
    for u in range(curve.p):
        trace: list[str] = []
        actual = map_to_curve_svdw_montgomery(curve, u, z, trace=trace)
        expected = weierstrass_to_montgomery(
            curve,
            svdw_oracle(weierstrass, u, z),
        )
        if actual != expected or not curve.contains(actual):
            raise AssertionError(f"SvdW-to-Montgomery mismatch at u={u}")
        schedules.add(tuple(trace))
    return {
        "form": "montgomery",
        "mapping": "svdw_transport",
        "seed": seed,
        "p": curve.p,
        "curve_parameters": f"j={curve.j};k={curve.k}",
        "inputs_tested": curve.p,
        "on_curve": curve.p,
        "oracle_matches": curve.p,
        "schedule_variants": len(schedules),
        "group_order": len(_montgomery_points(curve)),
        "group_law_checks": 0,
        "pipeline_field_pairs": 0,
        "subgroup_order": 0,
        "subgroup_support": 0,
    }


def validate(seed: int, smoke: bool = False) -> list[dict[str, int | str]]:
    """Validate all form transports, or the compact Elligator anchors."""
    rows = [_validate_montgomery_elligator(seed), _validate_edwards_elligator(seed)]
    if not smoke:
        rows.append(_validate_montgomery_svdw(seed))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5407)
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
            / f"validate_curve_transports_{label}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['inputs_tested']) for row in rows)} map inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
