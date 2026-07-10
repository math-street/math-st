"""Census toy discriminants whose class number is divisible by a prime.

Sub-goal: P1.5 / SG-28
Inputs:   [--limit INT] [--smoke] [--output-dir PATH]
Outputs:  data/probe_exact_order_targets_<profile>_<date>.csv
Runtime:  smoke under 10 seconds; full runtime recorded after execution
Validated against: h(-3)=h(-4)=1, h(-15)=h(-20)=2, h(-23)=3,
                   h(-47)=5, and h(-71)=7
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.isogeny import (  # noqa: E402
    class_number_from_reduced_forms,
    reduced_positive_forms,
)


SMOKE_PRIMES = (3, 5, 7)
FULL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
KNOWN_CLASS_NUMBERS = {-3: 1, -4: 1, -15: 2, -20: 2, -23: 3, -47: 5, -71: 7}


def class_numbers_through(limit: int) -> dict[int, int]:
    """Count primitive reduced positive forms for every negative D to limit."""
    if limit < 3:
        raise ValueError("limit must be at least 3")
    counts: dict[int, int] = {}
    maximum_a = math.isqrt(limit // 3) + 1
    for a in range(1, maximum_a + 1):
        for b in range(-a, a + 1):
            maximum_c = (b * b + limit) // (4 * a)
            for c in range(a, maximum_c + 1):
                discriminant = b * b - 4 * a * c
                if discriminant >= 0 or -discriminant > limit:
                    continue
                if discriminant % 4 not in (0, 1):
                    continue
                if b < 0 and (abs(b) == a or a == c):
                    continue
                if math.gcd(math.gcd(a, abs(b)), c) != 1:
                    continue
                counts[discriminant] = counts.get(discriminant, 0) + 1
    return counts


def validate_known_answers(counts: dict[int, int]) -> None:
    """Raise if any known class-number fixture is absent or incorrect."""
    for discriminant, expected in KNOWN_CLASS_NUMBERS.items():
        actual = counts.get(discriminant, 0)
        if actual != expected:
            raise AssertionError(
                f"h({discriminant})={actual}, expected known value {expected}"
            )
        if actual != class_number_from_reduced_forms(discriminant):
            raise AssertionError(f"batch and shared enumerators disagree at {discriminant}")


def least_divisible_rows(limit: int, primes: tuple[int, ...]) -> list[dict[str, object]]:
    """Return the least-magnitude D in range with r dividing h(D)."""
    counts = class_numbers_through(limit)
    validate_known_answers(counts)
    ordered = sorted(counts.items(), key=lambda item: -item[0])
    rows: list[dict[str, object]] = []
    for r in primes:
        match = next(((d, h) for d, h in ordered if h % r == 0), None)
        if match is None:
            rows.append(
                {
                    "r": r,
                    "search_limit": limit,
                    "found": False,
                    "discriminant": "",
                    "class_number": "",
                    "class_number_equals_r": "",
                    "form_a": "",
                    "form_b": "",
                    "form_c": "",
                    "discriminant_bits": "",
                    "a019_bits": r + 2,
                    "abs_delta_over_r_squared": "",
                }
            )
            continue
        discriminant, class_number = match
        nonprincipal = next(form for form in reduced_positive_forms(discriminant) if form[0] > 1)
        rows.append(
            {
                "r": r,
                "search_limit": limit,
                "found": True,
                "discriminant": discriminant,
                "class_number": class_number,
                "class_number_equals_r": class_number == r,
                "form_a": nonprincipal[0],
                "form_b": nonprincipal[1],
                "form_c": nonprincipal[2],
                "discriminant_bits": (-discriminant).bit_length(),
                "a019_bits": r + 2,
                "abs_delta_over_r_squared": round((-discriminant) / (r * r), 6),
            }
        )
    return rows


def write_rows(rows: list[dict[str, object]], path: Path) -> None:
    """Write deterministic census rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=200_000)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parents[1] / "data")
    args = parser.parse_args()
    limit = min(args.limit, 1_000) if args.smoke else args.limit
    primes = SMOKE_PRIMES if args.smoke else FULL_PRIMES
    rows = least_divisible_rows(limit, primes)
    profile = "smoke" if args.smoke else "full"
    output = args.output_dir / f"probe_exact_order_targets_{profile}_{date.today():%Y%m%d}.csv"
    write_rows(rows, output)
    for row in rows:
        print(row)
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
