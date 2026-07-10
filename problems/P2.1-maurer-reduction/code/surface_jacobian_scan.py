"""
surface_jacobian_scan - Exhaust ordinary surface Weil polynomials and HNR obstructions.
Sub-goal: P2.1 / SG-14
Inputs:   --bits <csv> --exponent <int>; deterministic, with no randomness.
Outputs:  data/surface_jacobian_scan_<params>_<date>.csv
Runtime:  Recorded in each output row; --smoke targets under 10 seconds.
Validated against: split trace products and published HNR exception families in tests.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import numpy as np
from sympy import factorint

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import prime_below_power_of_two


@dataclass(frozen=True, slots=True)
class ScanRow:
    bits: int
    prime: int
    smoothness_exponent: int
    smoothness_bound: int
    interval_lower: int
    interval_upper: int
    interval_size: int
    ordinary_surface_orders: int
    jacobian_admissible_orders: int
    smooth_integers: int
    smooth_surface_orders: int
    smooth_jacobian_admissible_orders: int
    elapsed_seconds: float


def parse_int_csv(value: str) -> list[int]:
    parsed = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not parsed or any(item <= 0 for item in parsed):
        raise argparse.ArgumentTypeError("expected comma-separated positive integers")
    return parsed


def primes_up_to(limit: int) -> list[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value, is_prime_value in enumerate(sieve) if is_prime_value]


def smooth_mask(lower: int, upper: int, bound: int) -> np.ndarray:
    """Return the exact bound-smooth mask on an inclusive positive interval."""
    if lower < 1 or upper < lower or bound < 1:
        raise ValueError("invalid smoothness interval or bound")
    remainders = np.arange(lower, upper + 1, dtype=np.uint64)
    for prime in primes_up_to(min(bound, upper)):
        view = remainders[(-lower) % prime :: prime]
        while True:
            divisible = view % prime == 0
            if not bool(np.any(divisible)):
                break
            view[divisible] //= prime
    return remainders == 1


def is_ordinary_surface_weil_polynomial(prime: int, a: int, b: int) -> bool:
    """Check the degree-four ordinary prime-field Weil inequalities exactly."""
    if prime <= 2:
        raise ValueError("the scan requires an odd prime field")
    if a * a > 16 * prime:
        return False
    if 4 * b > a * a + 8 * prime:
        return False
    shifted = b + 2 * prime
    if shifted < 0 or shifted * shifted < 4 * a * a * prime:
        return False
    return b % prime != 0


def split_traces(prime: int, a: int, b: int) -> tuple[int, int] | None:
    """Return elliptic traces when the surface Weil polynomial splits over Z."""
    discriminant = a * a - 4 * (b - 2 * prime)
    if discriminant < 0:
        return None
    root = math.isqrt(discriminant)
    if root * root != discriminant:
        return None
    if (-a + root) % 2 or (-a - root) % 2:
        return None
    return (-a + root) // 2, (-a - root) // 2


def all_prime_divisors_are_one_mod_three(integer: int) -> bool:
    if integer <= 1:
        return False
    return all(int(prime) % 3 == 1 for prime in factorint(integer))


def hnr_contains_jacobian(prime: int, a: int, b: int) -> bool:
    """Apply the ordinary cases of Howe--Nart--Ritzenthaler Theorem 1.2."""
    if not is_ordinary_surface_weil_polynomial(prime, a, b):
        raise ValueError("HNR classification requires an ordinary Weil polynomial")
    traces = split_traces(prime, a, b)
    if traces is not None:
        first, second = traces
        if abs(first - second) == 1:
            return False
        if first == second and first * first - 4 * prime in {-3, -4, -7}:
            return False
        return True

    if a * a - b == prime and b < 0:
        if all_prime_divisors_are_one_mod_three(-b):
            return False
    if a == 0 and b in {1 - 2 * prime, 2 - 2 * prime}:
        return False
    return True


def coefficient_bounds(prime: int, a: int) -> tuple[int, int]:
    """Return the exact inclusive b-range for degree-four Weil polynomials."""
    radicand = 4 * a * a * prime
    root = math.isqrt(radicand)
    shifted_minimum = root if root * root == radicand else root + 1
    return shifted_minimum - 2 * prime, (a * a + 8 * prime) // 4


def scan_prime(prime: int, bits: int, exponent: int) -> ScanRow:
    started = time.perf_counter()
    half_width = math.isqrt(prime**3)
    lower = prime * prime - half_width
    upper = prime * prime + half_width
    interval_size = upper - lower + 1
    surface = np.zeros(interval_size, dtype=np.bool_)
    jacobian = np.zeros(interval_size, dtype=np.bool_)

    a_limit = math.isqrt(16 * prime)
    for a in range(-a_limit, a_limit + 1):
        b_lower, b_upper = coefficient_bounds(prime, a)
        for b in range(b_lower, b_upper + 1):
            if not is_ordinary_surface_weil_polynomial(prime, a, b):
                continue
            order = prime * prime + 1 + a * (prime + 1) + b
            if not lower <= order <= upper:
                continue
            offset = order - lower
            surface[offset] = True
            if hnr_contains_jacobian(prime, a, b):
                jacobian[offset] = True

    bound = max(2, math.floor(math.log2(prime) ** exponent))
    smooth = smooth_mask(lower, upper, bound)
    return ScanRow(
        bits=bits,
        prime=prime,
        smoothness_exponent=exponent,
        smoothness_bound=bound,
        interval_lower=lower,
        interval_upper=upper,
        interval_size=interval_size,
        ordinary_surface_orders=int(np.count_nonzero(surface)),
        jacobian_admissible_orders=int(np.count_nonzero(jacobian)),
        smooth_integers=int(np.count_nonzero(smooth)),
        smooth_surface_orders=int(np.count_nonzero(smooth & surface)),
        smooth_jacobian_admissible_orders=int(np.count_nonzero(smooth & jacobian)),
        elapsed_seconds=time.perf_counter() - started,
    )


def output_path(bits_values: list[int], exponent: int) -> Path:
    bits_label = "-".join(str(value) for value in bits_values)
    filename = (
        f"surface_jacobian_scan_b{bits_label}_e{exponent}_{date.today():%Y%m%d}.csv"
    )
    return Path(__file__).resolve().parents[1] / "data" / filename


def write_rows(path: Path, rows: list[ScanRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=parse_int_csv, default=[8, 10, 12])
    parser.add_argument("--exponent", type=int, default=3)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.exponent <= 0:
        parser.error("--exponent must be positive")
    bits_values = [8] if args.smoke else args.bits
    rows = [
        scan_prime(prime_below_power_of_two(bits), bits, args.exponent)
        for bits in bits_values
        for prime in [prime_below_power_of_two(bits)]
    ]
    path = output_path(bits_values, args.exponent)
    write_rows(path, rows)
    print(path)
    for row in rows:
        print(asdict(row))


if __name__ == "__main__":
    main()
