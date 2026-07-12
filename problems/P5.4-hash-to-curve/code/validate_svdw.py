"""
validate_svdw.py - Exhaustively validate the generic RFC SvdW fallback.
Sub-goal: P5.4 / SG-08a
Inputs:   --primes <csv> --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_svdw_<params>_<date>.csv
Runtime:  under 1 second for the default toy fields on Python 3.13
Validated against: a branch-using direct oracle for RFC 9380 Section 6.6.1
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
    find_svdw_z,
    inv0_mod,
    is_square_mod,
    map_to_curve_svdw,
    sgn0_prime,
    sqrt_mod,
    svdw_parameters_are_valid,
)

SVDW_CASES = {
    11: (("ordinary", 1, 1), ("j0", 0, 1), ("j1728", 1, 0)),
    13: (("ordinary", 1, 1), ("j0", 0, 1), ("j1728", 1, 0)),
    29: (("ordinary", 1, 1), ("j0", 0, 1), ("j1728", 1, 0)),
    37: (("ordinary", 1, 1), ("j0", 0, 1), ("j1728", 1, 0)),
}


def _g(curve: Curve, x: int) -> int:
    return (x * x * x + curve.a * x + curve.b) % curve.p


def _normalize_sign(root: int, sign: int, p: int) -> int:
    return (-root) % p if sgn0_prime(root, p) != sign else root


def svdw_oracle(curve: Curve, u: int, z: int) -> tuple[int, int]:
    """Return the SvdW image using explicit candidates and ordinary branches."""
    p = curve.p
    u %= p
    z %= p
    gz = _g(curve, z)
    numerator = (3 * z * z + 4 * curve.a) % p
    c2 = -z * inv0_mod(2, p) % p
    c3 = sqrt_mod(-gz * numerator, p)
    if c3 is None:
        raise ArithmeticError("invalid SvdW fixture: c3 is not square")
    c3 = _normalize_sign(c3, 0, p)
    c4 = -4 * gz * inv0_mod(numerator, p) % p

    t = u * u * gz % p
    left = (1 - t) % p
    right = (1 + t) % p
    inverse = inv0_mod(left * right, p)
    offset = u * left * inverse * c3 % p
    x1 = (c2 - offset) % p
    x2 = (c2 + offset) % p
    x3 = (right * right * inverse) % p
    x3 = (x3 * x3 * c4 + z) % p
    if is_square_mod(_g(curve, x1), p):
        x = x1
    elif is_square_mod(_g(curve, x2), p):
        x = x2
    else:
        x = x3
    y = sqrt_mod(_g(curve, x), p)
    if y is None:
        raise ArithmeticError("SvdW oracle selected a nonsquare ordinate")
    return x, _normalize_sign(y, sgn0_prime(u, p), p)


def _validate_case(
    p: int,
    family: str,
    a: int,
    b: int,
    seed: int,
) -> dict[str, int | str]:
    curve = Curve(p, a, b)
    z = find_svdw_z(curve)
    if not svdw_parameters_are_valid(curve, z):
        raise AssertionError(f"invalid SvdW fixture for p={p}, family={family}")
    schedules: set[tuple[str, ...]] = set()
    exception_count = 0
    candidate_counts = [0, 0, 0]
    for u in range(p):
        trace: list[str] = []
        actual = map_to_curve_svdw(curve, u, z, trace=trace)
        expected = svdw_oracle(curve, u, z)
        if actual != expected:
            raise AssertionError(
                f"SvdW mismatch p={p}, family={family}, u={u}: "
                f"{actual} != {expected}"
            )
        if not curve.contains(actual):
            raise AssertionError(f"SvdW off-curve output p={p}, u={u}")
        schedules.add(tuple(trace))

        gz = _g(curve, z)
        t = u * u * gz % p
        left = (1 - t) % p
        right = (1 + t) % p
        exception_count += left * right % p == 0
        c2 = -z * inv0_mod(2, p) % p
        numerator = (3 * z * z + 4 * a) % p
        c3 = sqrt_mod(-gz * numerator, p)
        assert c3 is not None
        c3 = _normalize_sign(c3, 0, p)
        offset = u * left * inv0_mod(left * right, p) * c3 % p
        x1 = (c2 - offset) % p
        x2 = (c2 + offset) % p
        if is_square_mod(_g(curve, x1), p):
            candidate_counts[0] += 1
        elif is_square_mod(_g(curve, x2), p):
            candidate_counts[1] += 1
        else:
            candidate_counts[2] += 1

    schedule = next(iter(schedules))
    return {
        "mapping": "svdw",
        "family": family,
        "p": p,
        "curve_parameters": f"a={a};b={b}",
        "z": z,
        "seed": seed,
        "inputs_tested": p,
        "on_curve": p,
        "oracle_matches": p,
        "exceptional_inputs": exception_count,
        "candidate_1": candidate_counts[0],
        "candidate_2": candidate_counts[1],
        "candidate_3": candidate_counts[2],
        "schedule_variants": len(schedules),
        "schedule_operations": len(schedule),
    }


def validate_primes(primes: list[int], seed: int) -> list[dict[str, int | str]]:
    """Return exhaustive SvdW validation rows for each requested family."""
    unknown = set(primes) - set(SVDW_CASES)
    if unknown:
        raise ValueError(f"no preregistered fixtures for primes {sorted(unknown)}")
    return [
        _validate_case(p, family, a, b, seed)
        for p in primes
        for family, a, b in SVDW_CASES[p]
    ]


def _parse_primes(value: str) -> list[int]:
    return [int(item) for item in value.split(",") if item]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=_parse_primes, default=[11, 13, 29, 37])
    parser.add_argument("--seed", type=int, default=5403)
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
            / f"validate_svdw_p{prime_label}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['inputs_tested']) for row in rows)} inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
