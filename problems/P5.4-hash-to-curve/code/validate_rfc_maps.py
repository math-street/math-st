"""
validate_rfc_maps.py - Exhaustively compare RFC maps with direct toy oracles.
Sub-goal: P5.4 / SG-01a through SG-01c
Inputs:   --primes <csv> --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_rfc_maps_<params>_<date>.csv
Runtime:  ~1 second for the default toy fields on Python 3.13
Validated against: direct RFC 9380 Sections 6.6.2 and 6.7.1 formulas
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

from lib.curves import (
    Curve,
    MontgomeryCurve,
    inv0_mod,
    is_square_mod,
    map_to_curve_elligator2,
    map_to_curve_simple_swu,
    sgn0_prime,
    simple_swu_parameters_are_valid,
    sqrt_mod,
)

SSWU_CASES = {
    11: (1, 1, 6),
    13: (1, 1, 6),
    29: (1, 1, 8),
    37: (1, 1, 14),
}

ELLIGATOR2_CASES = {
    11: (1, 1, 2),
    13: (3, 1, 2),
    29: (1, 1, 2),
    37: (3, 1, 2),
}


def _normalize_sign(root: int, sign: int, p: int) -> int:
    return (-root) % p if sgn0_prime(root, p) != sign else root


def simple_swu_oracle(curve: Curve, u: int, z: int) -> tuple[int, int]:
    """Direct, branch-using transcription of RFC 9380 Section 6.6.2."""
    p = curve.p
    a = curve.a % p
    b = curve.b % p
    u %= p
    z %= p
    denominator = (z * z * pow(u, 4, p) + z * u * u) % p
    inverse = inv0_mod(denominator, p)
    x1 = (-b * inv0_mod(a, p) * (1 + inverse)) % p
    if inverse == 0:
        x1 = b * inv0_mod(z * a, p) % p
    gx1 = (x1 * x1 * x1 + a * x1 + b) % p
    x2 = z * u * u * x1 % p
    gx2 = (x2 * x2 * x2 + a * x2 + b) % p
    if is_square_mod(gx1, p):
        x, gx = x1, gx1
    else:
        x, gx = x2, gx2
    y = sqrt_mod(gx, p)
    if y is None:
        raise ArithmeticError("SSWU oracle selected a nonsquare ordinate")
    return x, _normalize_sign(y, sgn0_prime(u, p), p)


def elligator2_oracle(
    curve: MontgomeryCurve, u: int, z: int
) -> tuple[int, int]:
    """Direct, branch-using transcription of RFC 9380 Section 6.7.1."""
    p = curve.p
    u %= p
    z %= p
    c1 = curve.j * inv0_mod(curve.k, p) % p
    c2 = inv0_mod(curve.k * curve.k, p)
    x1 = -c1 * inv0_mod(1 + z * u * u, p) % p
    if x1 == 0:
        x1 = -c1 % p
    gx1 = (x1 * x1 * x1 + c1 * x1 * x1 + c2 * x1) % p
    x2 = (-x1 - c1) % p
    gx2 = (x2 * x2 * x2 + c1 * x2 * x2 + c2 * x2) % p
    if is_square_mod(gx1, p):
        x, gx, sign = x1, gx1, 1
    else:
        x, gx, sign = x2, gx2, 0
    y = sqrt_mod(gx, p)
    if y is None:
        raise ArithmeticError("Elligator 2 oracle selected a nonsquare ordinate")
    y = _normalize_sign(y, sign, p)
    return x * curve.k % p, y * curve.k % p


def _validate_sswu(p: int, seed: int) -> dict[str, int | str]:
    a, b, z = SSWU_CASES[p]
    curve = Curve(p, a, b)
    if not simple_swu_parameters_are_valid(curve, z):
        raise AssertionError(f"invalid SSWU fixture for p={p}")
    schedules: set[tuple[str, ...]] = set()
    exception_count = 0
    for u in range(p):
        trace: list[str] = []
        actual = map_to_curve_simple_swu(curve, u, z, trace=trace)
        expected = simple_swu_oracle(curve, u, z)
        if actual != expected:
            raise AssertionError(
                f"SSWU mismatch p={p}, u={u}: {actual} != {expected}"
            )
        if not curve.contains(actual):
            raise AssertionError(f"SSWU off-curve output p={p}, u={u}")
        schedules.add(tuple(trace))
        denominator = (z * z * pow(u, 4, p) + z * u * u) % p
        exception_count += denominator == 0
    schedule = next(iter(schedules))
    return {
        "mapping": "simple_swu",
        "p": p,
        "curve_parameters": f"a={a};b={b}",
        "z": z,
        "seed": seed,
        "inputs_tested": p,
        "on_curve": p,
        "oracle_matches": p,
        "exceptional_inputs": exception_count,
        "schedule_variants": len(schedules),
        "schedule_operations": len(schedule),
    }


def _validate_elligator2(p: int, seed: int) -> dict[str, int | str]:
    j, k, z = ELLIGATOR2_CASES[p]
    curve = MontgomeryCurve(p, j, k)
    if not curve.supports_elligator2():
        raise AssertionError(f"invalid Elligator 2 fixture for p={p}")
    schedules: set[tuple[str, ...]] = set()
    exception_count = 0
    for u in range(p):
        trace: list[str] = []
        actual = map_to_curve_elligator2(curve, u, z, trace=trace)
        expected = elligator2_oracle(curve, u, z)
        if actual != expected:
            raise AssertionError(
                f"Elligator 2 mismatch p={p}, u={u}: {actual} != {expected}"
            )
        if not curve.contains(actual):
            raise AssertionError(f"Elligator 2 off-curve output p={p}, u={u}")
        schedules.add(tuple(trace))
        exception_count += z * u * u % p == p - 1
    schedule = next(iter(schedules))
    return {
        "mapping": "elligator2",
        "p": p,
        "curve_parameters": f"j={j};k={k}",
        "z": z,
        "seed": seed,
        "inputs_tested": p,
        "on_curve": p,
        "oracle_matches": p,
        "exceptional_inputs": exception_count,
        "schedule_variants": len(schedules),
        "schedule_operations": len(schedule),
    }


def validate_primes(primes: list[int], seed: int) -> list[dict[str, int | str]]:
    """Return exhaustive validation summaries for the requested fixtures."""
    unknown = set(primes) - (set(SSWU_CASES) & set(ELLIGATOR2_CASES))
    if unknown:
        raise ValueError(f"no preregistered fixtures for primes {sorted(unknown)}")
    rows: list[dict[str, int | str]] = []
    for p in primes:
        rows.append(_validate_sswu(p, seed))
        rows.append(_validate_elligator2(p, seed))
    return rows


def _parse_primes(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=_parse_primes, default=[11, 13, 29, 37])
    parser.add_argument("--seed", type=int, default=5401)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    primes = [11, 13] if args.smoke else args.primes
    started = perf_counter()
    rows = validate_primes(primes, args.seed)
    elapsed = perf_counter() - started

    prime_label = "-".join(str(p) for p in primes)
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"validate_rfc_maps_p{prime_label}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['inputs_tested']) for row in rows)} inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
