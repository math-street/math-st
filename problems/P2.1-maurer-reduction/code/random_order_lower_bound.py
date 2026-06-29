"""
random_order_lower_bound - Exact adaptive-query bound in an iid order oracle.
Sub-goal: P2.1 / SG-06 and A003
Inputs:   --bits <csv> --exponent <int>
Outputs:  data/random_order_lower_bound_<params>_<date>.csv
Runtime:  Under 10 seconds in --smoke mode; recorded in the output.
Validated against: exhaustive finite sequence counts in code/tests/test_measure_smooth_orders.py.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from datetime import date
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from lib.curves import prime_below_power_of_two
from measure_smooth_orders import count_smooth_in_interval, parse_int_csv


def optimal_success_probability(smooth: int, total: int, queries: int) -> float:
    """Return the optimal success after distinct iid uniform order queries."""
    if total <= 0 or not 0 <= smooth <= total or queries < 0:
        raise ValueError("invalid oracle counts or query budget")
    if queries == 0 or smooth == 0:
        return 0.0
    if smooth == total:
        return 1.0
    return -math.expm1(queries * math.log1p(-smooth / total))


def exhaustive_sequence_success(smooth: int, total: int, queries: int) -> float:
    """Count successful length-q answer sequences exactly, then divide."""
    if total <= 0 or not 0 <= smooth <= total or queries < 0:
        raise ValueError("invalid sequence counts or query budget")
    sequence_count = total**queries
    failure_count = (total - smooth) ** queries
    return (sequence_count - failure_count) / sequence_count


def minimum_queries(
    smooth: int,
    total: int,
    target_success: float,
) -> int | None:
    """Return the least q attaining target success, or None if impossible."""
    if total <= 0 or not 0 <= smooth <= total:
        raise ValueError("invalid oracle counts")
    if not 0 < target_success < 1:
        raise ValueError("target success must lie strictly between zero and one")
    if smooth == 0:
        return None
    if smooth == total:
        return 1
    alpha = smooth / total
    estimate = math.ceil(math.log1p(-target_success) / math.log1p(-alpha))
    while optimal_success_probability(smooth, total, estimate - 1) >= target_success:
        estimate -= 1
    while optimal_success_probability(smooth, total, estimate) < target_success:
        estimate += 1
    return estimate


def measure(bits_values: list[int], exponent: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bits in bits_values:
        started = time.perf_counter()
        prime = prime_below_power_of_two(bits)
        radius = math.isqrt(4 * prime)
        lower = prime + 1 - radius
        upper = prime + 1 + radius
        bound = math.ceil(math.log2(prime) ** exponent)
        smooth = count_smooth_in_interval(lower, upper, bound)
        total = upper - lower + 1
        rows.append(
            {
                "bits": bits,
                "prime": prime,
                "smoothness_exponent": exponent,
                "bound": bound,
                "interval_lower": lower,
                "interval_upper": upper,
                "interval_size": total,
                "smooth_orders": smooth,
                "smooth_fraction": smooth / total,
                "queries_50_percent": minimum_queries(smooth, total, 0.5),
                "queries_95_percent": minimum_queries(smooth, total, 0.95),
                "queries_99_percent": minimum_queries(smooth, total, 0.99),
                "measurement_s": time.perf_counter() - started,
            }
        )
    return rows


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
    parser.add_argument("--exponent", type=int, default=3)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROBLEM_ROOT / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    if arguments.exponent <= 0:
        raise ValueError("exponent must be positive")
    bits_values = [10, 12] if arguments.smoke else arguments.bits
    rows = measure(bits_values, arguments.exponent)
    bit_label = "-".join(map(str, bits_values))
    output = arguments.output_dir / (
        f"random_order_lower_bound_b{bit_label}_e{arguments.exponent}_"
        f"{date.today():%Y%m%d}.csv"
    )
    write_csv(output, rows)
    print(output)


if __name__ == "__main__":
    main()
