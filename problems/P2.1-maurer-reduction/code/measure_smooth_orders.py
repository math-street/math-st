"""
measure_smooth_orders - Measure naive auxiliary-curve order smoothness.
Sub-goal: P2.1 / SG-02 and SG-03
Inputs:   --bits <csv> --trials <int> --seed <int> --exponents <csv>
Outputs:  data/measure_smooth_orders_<params>_<date>_{raw,summary}.csv
Runtime:  Measured in the generated summary; --smoke targets under 10 seconds.
Validated against: exhaustive point counts in code/tests/test_measure_smooth_orders.py.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from random import Random

import numpy as np
from sympy import factorint

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve, curve_order_bsgs, prime_below_power_of_two


@dataclass(frozen=True, slots=True)
class Trial:
    bits: int
    prime: int
    candidate: int
    a: int
    b: int
    order: int
    largest_prime_factor: int
    point_count_ms: float


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


def count_smooth_in_interval(lower: int, upper: int, bound: int) -> int:
    """Count exactly the bound-smooth integers in an inclusive interval."""
    if lower < 1 or upper < lower or bound < 1:
        raise ValueError("invalid smoothness interval or bound")
    remainders = np.arange(lower, upper + 1, dtype=np.uint64)
    for prime in primes_up_to(min(bound, upper)):
        offset = (-lower) % prime
        view = remainders[offset::prime]
        while True:
            divisible = view % prime == 0
            if not bool(np.any(divisible)):
                break
            view[divisible] //= prime
    return int(np.count_nonzero(remainders == 1))


def largest_prime_factor(integer: int) -> int:
    factors = factorint(integer)
    if not factors:
        return 1
    return max(int(prime) for prime in factors)


def wilson_interval(
    successes: int,
    trials: int,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    if trials <= 0 or not 0 <= successes <= trials:
        raise ValueError("invalid binomial counts")
    estimate = successes / trials
    denominator = 1 + z * z / trials
    center = (estimate + z * z / (2 * trials)) / denominator
    radius = (
        z
        * math.sqrt(
            estimate * (1 - estimate) / trials + z * z / (4 * trials**2)
        )
        / denominator
    )
    return center - radius, center + radius


def dickman_rho(argument: float, step: float = 0.0005) -> float:
    """Numerically approximate Dickman's rho via its delay equation."""
    if argument <= 1:
        return 1.0 if argument >= 0 else 0.0
    cells_per_unit = round(1 / step)
    step = 1 / cells_per_unit
    cell_count = math.ceil(argument / step)
    values = [1.0] * (cells_per_unit + 1)
    for index in range(cells_per_unit + 1, cell_count + 1):
        u = index * step
        derivative = -values[index - cells_per_unit] / u
        values.append(max(0.0, values[-1] + step * derivative))
    lower_index = math.floor(argument / step)
    if lower_index >= len(values) - 1:
        return values[-1]
    fraction = argument / step - lower_index
    return (
        values[lower_index] * (1 - fraction)
        + values[lower_index + 1] * fraction
    )


def sample_trials(bits_values: list[int], trials: int, seed: int) -> list[Trial]:
    rng = Random(seed)
    rows: list[Trial] = []
    for bits in bits_values:
        prime = prime_below_power_of_two(bits)
        for candidate in range(1, trials + 1):
            while True:
                a = rng.randrange(prime)
                b = rng.randrange(prime)
                try:
                    curve = Curve(prime, a, b)
                    break
                except ValueError:
                    continue
            started = time.perf_counter()
            order = curve_order_bsgs(curve, rng)
            elapsed_ms = (time.perf_counter() - started) * 1000
            rows.append(
                Trial(
                    bits=bits,
                    prime=prime,
                    candidate=candidate,
                    a=a,
                    b=b,
                    order=order,
                    largest_prime_factor=largest_prime_factor(order),
                    point_count_ms=elapsed_ms,
                )
            )
    return rows


def summarize(rows: list[Trial], exponents: list[int]) -> list[dict[str, object]]:
    summary: list[dict[str, object]] = []
    for bits in sorted({row.bits for row in rows}):
        selected = [row for row in rows if row.bits == bits]
        prime = selected[0].prime
        radius = math.isqrt(4 * prime)
        lower = prime + 1 - radius
        upper = prime + 1 + radius
        interval_size = upper - lower + 1
        timings = [row.point_count_ms for row in selected]
        for exponent in exponents:
            bound = math.ceil(math.log2(prime) ** exponent)
            successes = sum(
                row.largest_prime_factor <= bound for row in selected
            )
            ci_low, ci_high = wilson_interval(successes, len(selected))
            integer_successes = count_smooth_in_interval(lower, upper, bound)
            integer_rate = integer_successes / interval_size
            curve_rate = successes / len(selected)
            first_success = next(
                (
                    row.candidate
                    for row in selected
                    if row.largest_prime_factor <= bound
                ),
                "",
            )
            u = math.log(prime) / math.log(bound) if bound > 1 else math.inf
            summary.append(
                {
                    "bits": bits,
                    "prime": prime,
                    "trials": len(selected),
                    "smoothness_exponent": exponent,
                    "bound": bound,
                    "successes": successes,
                    "curve_rate": curve_rate,
                    "wilson_95_low": ci_low,
                    "wilson_95_high": ci_high,
                    "first_success_candidate": first_success,
                    "hasse_lower": lower,
                    "hasse_upper": upper,
                    "integer_successes": integer_successes,
                    "integer_rate": integer_rate,
                    "curve_to_integer_ratio": (
                        curve_rate / integer_rate if integer_rate else ""
                    ),
                    "dickman_u": u,
                    "dickman_rho": dickman_rho(u),
                    "mean_point_count_ms": statistics.fmean(timings),
                    "median_point_count_ms": statistics.median(timings),
                    "total_point_count_s": sum(timings) / 1000,
                }
            )
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bits",
        type=parse_int_csv,
        default=parse_int_csv("12,16,20,24,28,32,36,40"),
    )
    parser.add_argument("--trials", type=int, default=128)
    parser.add_argument("--seed", type=int, default=21012026)
    parser.add_argument(
        "--exponents", type=parse_int_csv, default=parse_int_csv("2,3")
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    if arguments.trials <= 0:
        raise ValueError("trials must be positive")
    bits_values = [10, 12] if arguments.smoke else arguments.bits
    trials = 6 if arguments.smoke else arguments.trials
    exponents = [2] if arguments.smoke else arguments.exponents
    started = time.perf_counter()
    trials_rows = sample_trials(bits_values, trials, arguments.seed)
    summary_rows = summarize(trials_rows, exponents)
    runtime_s = time.perf_counter() - started
    for row in summary_rows:
        row["full_runtime_s"] = runtime_s

    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(map(str, bits_values))
    exponent_label = "-".join(map(str, exponents))
    stem = (
        f"measure_smooth_orders_b{bit_label}_t{trials}_e{exponent_label}_"
        f"s{arguments.seed}_{stamp}"
    )
    raw_path = arguments.output_dir / f"{stem}_raw.csv"
    summary_path = arguments.output_dir / f"{stem}_summary.csv"
    raw_dicts = [
        {
            "bits": row.bits,
            "prime": row.prime,
            "candidate": row.candidate,
            "a": row.a,
            "b": row.b,
            "order": row.order,
            "largest_prime_factor": row.largest_prime_factor,
            "point_count_ms": row.point_count_ms,
            "seed": arguments.seed,
        }
        for row in trials_rows
    ]
    write_csv(raw_path, raw_dicts)
    write_csv(summary_path, summary_rows)
    print(raw_path)
    print(summary_path)
    print(f"runtime_s={runtime_s:.6f}")


if __name__ == "__main__":
    main()
