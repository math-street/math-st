"""
measure_cm_coverage - Measure explicit-family and bounded-CM smooth-order coverage.
Sub-goal: P2.1 / SG-04 and SG-05
Inputs:   --bits <csv> --primes-per-bit <int> --exponents <csv> --disc-exponent <int>
Outputs:  data/measure_cm_coverage_<params>_<date>_{raw,summary}.csv
Runtime:  Recorded in the summary; --smoke targets under 10 seconds.
Validated against: exhaustive curve orders and brute CM traces in code/tests/test_measure_cm_coverage.py.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import math
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from sympy import factorint

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import is_prime, sqrt_mod
from measure_smooth_orders import parse_int_csv, wilson_interval


@dataclass(frozen=True, slots=True)
class CmHit:
    discriminant: int
    class_number: int
    conductor: int
    trace: int
    order: int
    largest_prime_factor: int


def is_squarefree(value: int) -> bool:
    return all(exponent == 1 for exponent in factorint(value).values())


def fundamental_discriminants(limit: int) -> list[int]:
    """Return negative fundamental discriminants ordered by absolute value."""
    squarefree = bytearray(b"\x01") * (limit + 1)
    squarefree[0] = 0
    for base in range(2, math.isqrt(limit) + 1):
        square = base * base
        squarefree[square : limit + 1 : square] = b"\x00" * (
            (limit - square) // square + 1
        )
    result: list[int] = []
    for absolute in range(3, limit + 1):
        discriminant = -absolute
        if discriminant % 4 == 1 and squarefree[absolute]:
            result.append(discriminant)
            continue
        if discriminant % 4 == 0:
            quotient = absolute // 4
            if quotient % 4 in (1, 2) and squarefree[quotient]:
                result.append(discriminant)
    return result


def cornacchia_prime(prime: int, coefficient: int) -> set[tuple[int, int]]:
    """Solve x^2 + coefficient*y^2 = prime by Cornacchia's algorithm."""
    root = sqrt_mod(-coefficient, prime)
    if root is None:
        return set()
    solutions: set[tuple[int, int]] = set()
    for candidate_root in {root, (-root) % prime}:
        left, right = prime, candidate_root
        if right > prime // 2:
            right = prime - right
        while right and right * right > prime:
            left, right = right, left % right
        if not right:
            continue
        remainder = prime - right * right
        if remainder < 0 or remainder % coefficient:
            continue
        y_squared = remainder // coefficient
        y = math.isqrt(y_squared)
        if y * y == y_squared:
            solutions.add((right, y))
    return solutions


def _cornacchia_composite(
    modulus: int,
    coefficient: int,
    roots: set[int],
) -> set[tuple[int, int]]:
    solutions: set[tuple[int, int]] = set()
    for candidate_root in roots:
        left, right = modulus, candidate_root % modulus
        if right > modulus // 2:
            right = modulus - right
        while right and right * right > modulus:
            left, right = right, left % right
        if not right:
            continue
        remainder = modulus - right * right
        if remainder < 0 or remainder % coefficient:
            continue
        y_squared = remainder // coefficient
        y = math.isqrt(y_squared)
        if y * y == y_squared:
            solutions.add((right, y))
    return solutions


def cm_trace_conductors(prime: int, discriminant: int) -> set[tuple[int, int]]:
    """Solve t^2 - discriminant*f^2 = 4*prime for fundamental D < 0."""
    if discriminant >= 0 or discriminant % 4 not in (0, 1):
        raise ValueError("discriminant must be a negative quadratic discriminant")
    absolute = -discriminant
    solutions: set[tuple[int, int]] = set()
    if discriminant % 4 == 0:
        coefficient = absolute // 4
        prime_solutions = cornacchia_prime(prime, coefficient)
        if discriminant == -4:
            prime_solutions |= {
                (y_coord, x_coord) for x_coord, y_coord in prime_solutions
            }
        for x_coord, conductor in prime_solutions:
            solutions.add((2 * x_coord, conductor))
    else:
        for x_coord, y_coord in cornacchia_prime(prime, absolute):
            solutions.add((2 * x_coord, 2 * y_coord))

        root = sqrt_mod(-absolute, prime)
        if root is not None:
            roots_mod_4p: set[int] = set()
            modulus = 4 * prime
            for root_mod_p in {root, (-root) % prime}:
                for offset in range(4):
                    candidate = root_mod_p + offset * prime
                    if (candidate * candidate + absolute) % modulus == 0:
                        roots_mod_4p.add(candidate)
            solutions.update(
                _cornacchia_composite(modulus, absolute, roots_mod_4p)
            )

    checked = {
        (trace, conductor)
        for trace, conductor in solutions
        if trace * trace + absolute * conductor * conductor == 4 * prime
    }
    return checked


def fundamental_discriminant_and_conductor(
    prime: int,
    trace: int,
) -> tuple[int, int]:
    delta = trace * trace - 4 * prime
    if delta >= 0:
        raise ValueError("trace is outside the ordinary Hasse range")
    absolute = -delta
    factors = factorint(absolute)
    squarefree_absolute = math.prod(
        int(factor) for factor, exponent in factors.items() if exponent % 2
    )
    square_part = math.isqrt(absolute // squarefree_absolute)
    squarefree_negative = -squarefree_absolute
    if squarefree_negative % 4 == 1:
        discriminant = squarefree_negative
        conductor = square_part
    else:
        if square_part % 2:
            raise ArithmeticError("invalid discriminant square decomposition")
        discriminant = 4 * squarefree_negative
        conductor = square_part // 2
    if discriminant * conductor * conductor != delta:
        raise ArithmeticError("CM discriminant reconstruction failed")
    return discriminant, conductor


def class_number(discriminant: int) -> int:
    """Count reduced primitive positive binary quadratic forms of D < 0."""
    if discriminant >= 0 or discriminant % 4 not in (0, 1):
        raise ValueError("invalid negative discriminant")
    count = 0
    bound = math.isqrt((-discriminant) // 3) + 1
    for leading in range(1, bound + 1):
        for middle in range(-leading, leading + 1):
            numerator = middle * middle - discriminant
            denominator = 4 * leading
            if numerator % denominator:
                continue
            trailing = numerator // denominator
            if leading > trailing:
                continue
            if math.gcd(leading, math.gcd(abs(middle), trailing)) != 1:
                continue
            if (abs(middle) == leading or leading == trailing) and middle < 0:
                continue
            count += 1
    return count


def representation_by_x2_plus_dy2(prime: int, coefficient: int) -> tuple[int, int]:
    solutions = cornacchia_prime(prime, coefficient)
    if not solutions:
        raise ArithmeticError(
            f"no representation of {prime} by x^2+{coefficient}y^2"
        )
    return min(solutions)


def explicit_order_families(prime: int) -> dict[int, set[str]]:
    """Return orders reachable by the j=0 and j=1728 twist families."""
    orders: dict[int, set[str]] = {}

    def add(order: int, family: str) -> None:
        orders.setdefault(order, set()).add(family)

    if prime % 4 == 3:
        add(prime + 1, "j1728")
    else:
        x_coord, y_coord = representation_by_x2_plus_dy2(prime, 1)
        for trace in {2 * x_coord, -2 * x_coord, 2 * y_coord, -2 * y_coord}:
            add(prime + 1 - trace, "j1728")

    if prime % 3 == 2:
        add(prime + 1, "j0")
    else:
        x_coord, y_coord = representation_by_x2_plus_dy2(prime, 3)
        traces = {
            2 * x_coord,
            -2 * x_coord,
            x_coord + 3 * y_coord,
            -x_coord - 3 * y_coord,
            x_coord - 3 * y_coord,
            -x_coord + 3 * y_coord,
        }
        for trace in traces:
            add(prime + 1 - trace, "j0")
    return orders


def largest_prime_factor(integer: int) -> int:
    return max((int(prime) for prime in factorint(integer)), default=1)


def prime_ensemble(bits: int, count: int) -> list[int]:
    candidate = (1 << bits) - 1
    if candidate % 2 == 0:
        candidate -= 1
    primes: list[int] = []
    while candidate >= 5 and len(primes) < count:
        if is_prime(candidate):
            primes.append(candidate)
        candidate -= 2
    if len(primes) != count:
        raise RuntimeError(f"could not find {count} primes below 2^{bits}")
    return primes


def bounded_cm_hits(
    prime: int,
    order_bounds: dict[int, int],
    discriminants: list[int],
) -> dict[int, CmHit | None]:
    hits: dict[int, CmHit | None] = {exponent: None for exponent in order_bounds}
    factor_cache: dict[int, int] = {}
    class_cache: dict[int, int] = {}
    for discriminant in discriminants:
        for absolute_trace, conductor in cm_trace_conductors(prime, discriminant):
            for trace in {absolute_trace, -absolute_trace}:
                order = prime + 1 - trace
                largest = factor_cache.setdefault(order, largest_prime_factor(order))
                for exponent, bound in order_bounds.items():
                    if hits[exponent] is None and largest <= bound:
                        degree = class_cache.setdefault(
                            discriminant, class_number(discriminant)
                        )
                        hits[exponent] = CmHit(
                            discriminant=discriminant,
                            class_number=degree,
                            conductor=conductor,
                            trace=trace,
                            order=order,
                            largest_prime_factor=largest,
                        )
        if all(hit is not None for hit in hits.values()):
            break
    return hits


def _measure_prime_task(
    task: tuple[int, int, int, list[int], int, list[int]],
) -> list[dict[str, object]]:
    bits, prime_index, prime, exponents, disc_exponent, discriminants = task
    discriminant_bound = bits**disc_exponent
    started = time.perf_counter()
    explicit = explicit_order_families(prime)
    explicit_factors = {order: largest_prime_factor(order) for order in explicit}
    order_bounds = {
        exponent: math.ceil(math.log2(prime) ** exponent)
        for exponent in exponents
    }
    hits = bounded_cm_hits(prime, order_bounds, discriminants)
    elapsed_ms = (time.perf_counter() - started) * 1000
    rows: list[dict[str, object]] = []
    for exponent, order_bound in order_bounds.items():
        smooth_explicit = [
            order
            for order, largest in explicit_factors.items()
            if largest <= order_bound
        ]
        best_explicit_order = min(
            explicit,
            key=lambda order: (explicit_factors[order], order),
        )
        hit = hits[exponent]
        rows.append(
            {
                "bits": bits,
                "prime_index": prime_index,
                "prime": prime,
                "prime_mod_12": prime % 12,
                "smoothness_exponent": exponent,
                "order_bound": order_bound,
                "discriminant_exponent": disc_exponent,
                "discriminant_bound": discriminant_bound,
                "explicit_order_count": len(explicit),
                "explicit_success": int(bool(smooth_explicit)),
                "explicit_smooth_count": len(smooth_explicit),
                "explicit_best_order": best_explicit_order,
                "explicit_best_lpf": explicit_factors[best_explicit_order],
                "explicit_first_smooth_order": (
                    min(smooth_explicit) if smooth_explicit else ""
                ),
                "bounded_cm_success": int(hit is not None),
                "cm_discriminant": hit.discriminant if hit else "",
                "cm_class_number": hit.class_number if hit else "",
                "cm_conductor": hit.conductor if hit else "",
                "cm_trace": hit.trace if hit else "",
                "cm_order": hit.order if hit else "",
                "cm_lpf": hit.largest_prime_factor if hit else "",
                "measurement_ms": elapsed_ms,
            }
        )
    return rows


def run_measurement(
    bits_values: list[int],
    primes_per_bit: int,
    exponents: list[int],
    disc_exponent: int,
    workers: int = 1,
) -> list[dict[str, object]]:
    maximum_disc = max(bits_values) ** disc_exponent
    all_discriminants = fundamental_discriminants(maximum_disc)
    tasks: list[tuple[int, int, int, list[int], int, list[int]]] = []
    for bits in bits_values:
        discriminant_bound = bits**disc_exponent
        discriminants = [
            value for value in all_discriminants if -value <= discriminant_bound
        ]
        for prime_index, prime in enumerate(prime_ensemble(bits, primes_per_bit), 1):
            tasks.append(
                (bits, prime_index, prime, exponents, disc_exponent, discriminants)
            )
    rows: list[dict[str, object]] = []
    if workers == 1:
        for task in tasks:
            rows.extend(_measure_prime_task(task))
    else:
        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
            for task_rows in pool.map(_measure_prime_task, tasks, chunksize=1):
                rows.extend(task_rows)
    rows.sort(
        key=lambda row: (
            int(row["bits"]),
            int(row["prime_index"]),
            int(row["smoothness_exponent"]),
        )
    )
    return rows


def summarize(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    keys = sorted(
        {
            (int(row["bits"]), int(row["smoothness_exponent"]))
            for row in rows
        }
    )
    for bits, exponent in keys:
        selected = [
            row
            for row in rows
            if row["bits"] == bits and row["smoothness_exponent"] == exponent
        ]
        explicit_successes = sum(int(row["explicit_success"]) for row in selected)
        cm_successes = sum(int(row["bounded_cm_success"]) for row in selected)
        explicit_low, explicit_high = wilson_interval(explicit_successes, len(selected))
        cm_low, cm_high = wilson_interval(cm_successes, len(selected))
        discriminants = [
            abs(int(row["cm_discriminant"]))
            for row in selected
            if row["cm_discriminant"] != ""
        ]
        class_numbers = [
            int(row["cm_class_number"])
            for row in selected
            if row["cm_class_number"] != ""
        ]
        output.append(
            {
                "bits": bits,
                "smoothness_exponent": exponent,
                "order_bound": selected[0]["order_bound"],
                "discriminant_bound": selected[0]["discriminant_bound"],
                "primes": len(selected),
                "explicit_successes": explicit_successes,
                "explicit_rate": explicit_successes / len(selected),
                "explicit_wilson_95_low": explicit_low,
                "explicit_wilson_95_high": explicit_high,
                "bounded_cm_successes": cm_successes,
                "bounded_cm_rate": cm_successes / len(selected),
                "bounded_cm_wilson_95_low": cm_low,
                "bounded_cm_wilson_95_high": cm_high,
                "median_min_discriminant": (
                    statistics.median(discriminants) if discriminants else ""
                ),
                "max_min_discriminant": max(discriminants, default=""),
                "median_class_number": (
                    statistics.median(class_numbers) if class_numbers else ""
                ),
                "max_class_number": max(class_numbers, default=""),
                "mean_measurement_ms": statistics.fmean(
                    float(row["measurement_ms"]) for row in selected
                ),
                "total_measurement_s": sum(
                    float(row["measurement_ms"]) for row in selected
                )
                / 1000,
            }
        )
    return output


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
    parser.add_argument("--primes-per-bit", type=int, default=32)
    parser.add_argument(
        "--exponents", type=parse_int_csv, default=parse_int_csv("2,3")
    )
    parser.add_argument("--disc-exponent", type=int, default=3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    if (
        arguments.primes_per_bit <= 0
        or arguments.disc_exponent <= 0
        or arguments.workers <= 0
    ):
        raise ValueError("prime count, discriminant exponent, and workers must be positive")
    bits_values = [10, 12] if arguments.smoke else arguments.bits
    primes_per_bit = 3 if arguments.smoke else arguments.primes_per_bit
    exponents = [2] if arguments.smoke else arguments.exponents
    started = time.perf_counter()
    raw_rows = run_measurement(
        bits_values,
        primes_per_bit,
        exponents,
        arguments.disc_exponent,
        arguments.workers,
    )
    summary_rows = summarize(raw_rows)
    runtime_s = time.perf_counter() - started
    for row in summary_rows:
        row["full_runtime_s"] = runtime_s

    stamp = date.today().strftime("%Y%m%d")
    bit_label = "-".join(map(str, bits_values))
    exponent_label = "-".join(map(str, exponents))
    stem = (
        f"measure_cm_coverage_b{bit_label}_p{primes_per_bit}_e{exponent_label}_"
        f"d{arguments.disc_exponent}_w{arguments.workers}_{stamp}"
    )
    raw_path = arguments.output_dir / f"{stem}_raw.csv"
    summary_path = arguments.output_dir / f"{stem}_summary.csv"
    write_csv(raw_path, raw_rows)
    write_csv(summary_path, summary_rows)
    print(raw_path)
    print(summary_path)
    print(f"runtime_s={runtime_s:.6f}")


if __name__ == "__main__":
    main()
