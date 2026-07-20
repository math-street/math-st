"""
reproduce_cm_table.py -- reproduce Zywina's first published CM table row.
Sub-goal: P5.1 / SG-09
Inputs:   --limit <int> --checkpoints <csv> --seed <int>
Outputs:  data/reproduce_cm_table_x<limit>_s<seed>_<date>.csv and matching PNG
Runtime:  148.7 s wall time for all 50 checkpoints through x=1,000,000,000
Validated against: Walsh 2022 trace theorem and Zywina 2011, Table 3
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from datetime import date
from pathlib import Path

import mpmath

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from measure_corrected_cases import PUBLISHED_CM_CONSTANT


PUBLISHED_X = 20_000_000
PUBLISHED_ACTUAL = 49_847
PUBLISHED_EXPECTED_ROUNDED = 50_063

PUBLISHED_TABLE = {
    20_000_000: (49_847, 50_063),
    40_000_000: (91_074, 91_134),
    60_000_000: (129_660, 129_648),
    80_000_000: (166_429, 166_631),
    100_000_000: (202_316, 202_534),
    120_000_000: (237_402, 237_612),
    140_000_000: (271_865, 272_024),
    160_000_000: (305_749, 305_882),
    180_000_000: (338_987, 339_266),
    200_000_000: (372_142, 372_237),
    220_000_000: (404_768, 404_844),
    240_000_000: (437_027, 437_124),
    260_000_000: (469_002, 469_110),
    280_000_000: (500_848, 500_827),
    300_000_000: (532_345, 532_298),
    320_000_000: (563_613, 563_542),
    340_000_000: (594_570, 594_575),
    360_000_000: (625_409, 625_412),
    380_000_000: (656_138, 656_065),
    400_000_000: (686_710, 686_546),
    420_000_000: (716_542, 716_864),
    440_000_000: (746_751, 747_028),
    460_000_000: (776_709, 777_047),
    480_000_000: (806_405, 806_928),
    500_000_000: (836_080, 836_677),
    520_000_000: (865_909, 866_300),
    540_000_000: (895_323, 895_804),
    560_000_000: (924_773, 925_193),
    580_000_000: (954_215, 954_472),
    600_000_000: (983_415, 983_645),
    620_000_000: (1_012_618, 1_012_717),
    640_000_000: (1_041_478, 1_041_691),
    660_000_000: (1_070_519, 1_070_571),
    680_000_000: (1_099_310, 1_099_359),
    700_000_000: (1_127_947, 1_128_060),
    720_000_000: (1_156_596, 1_156_676),
    740_000_000: (1_185_077, 1_185_209),
    760_000_000: (1_213_434, 1_213_663),
    780_000_000: (1_241_996, 1_242_040),
    800_000_000: (1_270_215, 1_270_341),
    820_000_000: (1_298_419, 1_298_570),
    840_000_000: (1_326_489, 1_326_728),
    860_000_000: (1_354_726, 1_354_817),
    880_000_000: (1_382_946, 1_382_839),
    900_000_000: (1_410_787, 1_410_796),
    920_000_000: (1_438_522, 1_438_689),
    940_000_000: (1_466_143, 1_466_520),
    960_000_000: (1_493_786, 1_494_291),
    980_000_000: (1_521_276, 1_522_003),
    1_000_000_000: (1_548_766, 1_549_657),
}


def prime_flags(limit: int) -> bytearray:
    """Return an Eratosthenes primality table through limit."""
    if limit < 1:
        return bytearray(limit + 1)
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if flags[prime]:
            start = prime * prime
            flags[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return flags


def primes_from_flags(flags: bytearray) -> list[int]:
    """Extract the prime indices from a primality table."""
    return [value for value, flag in enumerate(flags) if flag]


def segmented_split_primes(limit: int, segment_size: int):
    """Yield primes 1 modulo 4 through limit with bounded working memory."""
    if segment_size < 1_000:
        raise ValueError("segment_size must be at least 1000")
    base_flags = prime_flags(math.isqrt(limit))
    base_primes = primes_from_flags(base_flags)
    for low in range(0, limit + 1, segment_size):
        high = min(limit + 1, low + segment_size)
        segment = bytearray(b"\x01") * (high - low)
        for prime in base_primes:
            if prime * prime >= high and prime > math.isqrt(high - 1):
                break
            start = max(prime * prime, ((low + prime - 1) // prime) * prime)
            if start >= high:
                continue
            segment[start - low : high - low : prime] = b"\x00" * (
                (high - 1 - start) // prime + 1
            )
        if low == 0:
            segment[0 : min(2, len(segment))] = b"\x00" * min(2, len(segment))
        first = low + ((1 - low) % 4)
        if first < 5:
            first += ((5 - first + 3) // 4) * 4
        for candidate in range(first, high, 4):
            if segment[candidate - low]:
                yield candidate


def _cornacchia_candidate(prime: int, root_minus_one: int) -> tuple[int, int] | None:
    """Try one square root of -1 in Cornacchia's algorithm."""
    previous, current = prime, root_minus_one
    while current * current > prime:
        previous, current = current, previous % current
    remainder = prime - current * current
    other = math.isqrt(remainder)
    if other * other != remainder:
        return None
    return abs(current), other


def sum_of_two_squares_prime(prime: int) -> tuple[int, int]:
    """Return positive coordinates whose squares sum to a prime 1 modulo 4."""
    if prime <= 2 or prime % 4 != 1:
        raise ValueError("prime must be an odd prime congruent to 1 modulo 4")
    nonresidue = 2
    while pow(nonresidue, (prime - 1) // 2, prime) != prime - 1:
        nonresidue += 1
    root_minus_one = pow(nonresidue, (prime - 1) // 4, prime)
    for root in (root_minus_one, prime - root_minus_one):
        result = _cornacchia_candidate(prime, root)
        if result is not None:
            return result
    raise ArithmeticError(f"Cornacchia failed for p={prime}")


def cm_trace_j1728_minus_one(prime: int) -> int:
    """Return the Frobenius trace of y^2=x^3-x at an odd prime."""
    if prime <= 2:
        raise ValueError("prime must be odd")
    if prime % 4 == 3:
        return 0
    first, second = sum_of_two_squares_prime(prime)
    if first % 2 == 1:
        odd_coordinate = first
    elif second % 2 == 1:
        odd_coordinate = second
    else:
        raise ArithmeticError(f"no odd coordinate for p={prime}")
    if odd_coordinate % 4 != 1:
        odd_coordinate = -odd_coordinate
    if prime % 8 == 1:
        return 2 * odd_coordinate
    return -2 * odd_coordinate


def cm_curve_order(prime: int) -> int:
    """Return #E(F_p) for E: y^2=x^3-x."""
    return prime + 1 - cm_trace_j1728_minus_one(prime)


def published_integral_prediction(cutoff: int) -> float:
    """Evaluate Zywina's equation (7.1) with his published constant."""
    if cutoff < 9:
        return 0.0
    mpmath.mp.dps = 40
    upper = mpmath.mpf(cutoff)
    integrand = lambda value: 1 / (
        mpmath.log(value) * (mpmath.log(value + 1) - mpmath.log(8))
    )
    breakpoints = [mpmath.mpf(9)]
    for point in (100, 10_000, 1_000_000):
        if point < cutoff:
            breakpoints.append(mpmath.mpf(point))
    breakpoints.append(upper)
    integral = mpmath.quad(integrand, breakpoints)
    return float(mpmath.mpf(str(PUBLISHED_CM_CONSTANT)) * integral / 2)


def refined_weight(prime: int) -> float:
    """Return the direct split-prime refined weight for quotient t=8."""
    if prime + 1 <= 8:
        return 0.0
    return 1.0 / (math.log(prime + 1.0) - math.log(8.0))


def parse_checkpoints(raw: str, limit: int) -> list[int]:
    """Parse increasing checkpoints and include the final limit."""
    checkpoints = sorted({int(value.strip()) for value in raw.split(",") if value})
    checkpoints = [value for value in checkpoints if 5 <= value <= limit]
    if not checkpoints or checkpoints[-1] != limit:
        checkpoints.append(limit)
    return checkpoints


def measure(
    limit: int,
    checkpoints: list[int],
    seed: int,
    *,
    segmented: bool = False,
    segment_size: int = 10_000_000,
) -> list[dict[str, object]]:
    """Count split-prime CM quotient events at all requested checkpoints."""
    started = time.perf_counter()
    maximum_quotient = (limit + 1 + 2 * math.isqrt(limit) + 7) // 8
    quotient_flags = prime_flags(maximum_quotient)
    if segmented:
        split_primes = segmented_split_primes(limit, segment_size)
    else:
        flags = prime_flags(limit)
        split_primes = (
            prime for prime in range(5, limit + 1, 4) if flags[prime]
        )
    sieve_seconds = time.perf_counter() - started
    rows: list[dict[str, object]] = []
    split_prime_count = 0
    quotient_prime_count = 0
    direct_baseline = 0.0
    checkpoint_position = 0

    for prime in split_primes:
        while (
            checkpoint_position < len(checkpoints)
            and checkpoints[checkpoint_position] < prime
        ):
            cutoff = checkpoints[checkpoint_position]
            integral_prediction = published_integral_prediction(cutoff)
            rows.append(
                _result_row(
                    cutoff,
                    split_prime_count,
                    quotient_prime_count,
                    direct_baseline,
                    integral_prediction,
                    sieve_seconds,
                    time.perf_counter() - started,
                    seed,
                )
            )
            checkpoint_position += 1

        split_prime_count += 1
        order = cm_curve_order(prime)
        if order % 8 != 0:
            raise AssertionError(f"split-prime order not divisible by 8 at p={prime}")
        quotient = order // 8
        quotient_prime_count += quotient < len(quotient_flags) and bool(
            quotient_flags[quotient]
        )
        direct_baseline += refined_weight(prime)

    while checkpoint_position < len(checkpoints):
        cutoff = checkpoints[checkpoint_position]
        integral_prediction = published_integral_prediction(cutoff)
        rows.append(
            _result_row(
                cutoff,
                split_prime_count,
                quotient_prime_count,
                direct_baseline,
                integral_prediction,
                sieve_seconds,
                time.perf_counter() - started,
                seed,
            )
        )
        checkpoint_position += 1
    return rows


def _result_row(
    cutoff: int,
    split_prime_count: int,
    quotient_prime_count: int,
    direct_baseline: float,
    integral_prediction: float,
    sieve_seconds: float,
    elapsed_seconds: float,
    seed: int,
) -> dict[str, object]:
    """Construct one deterministic output row."""
    direct_prediction = PUBLISHED_CM_CONSTANT * direct_baseline
    published = PUBLISHED_TABLE.get(cutoff)
    return {
        "cutoff": cutoff,
        "split_prime_count": split_prime_count,
        "quotient_prime_count": quotient_prime_count,
        "published_cm_constant": f"{PUBLISHED_CM_CONSTANT:.12f}",
        "integral_predicted_count": f"{integral_prediction:.12f}",
        "integral_predicted_rounded": round(integral_prediction),
        "observed_over_integral_predicted": (
            f"{quotient_prime_count / integral_prediction:.12f}"
        ),
        "direct_prime_sum_baseline": f"{direct_baseline:.12f}",
        "direct_prime_sum_predicted": f"{direct_prediction:.12f}",
        "observed_over_direct_predicted": (
            f"{quotient_prime_count / direct_prediction:.12f}"
        ),
        "published_actual": "" if published is None else published[0],
        "published_actual_difference": (
            "" if published is None else quotient_prime_count - published[0]
        ),
        "published_expected_rounded": "" if published is None else published[1],
        "published_expected_difference": (
            "" if published is None else round(integral_prediction) - published[1]
        ),
        "sieve_seconds": f"{sieve_seconds:.6f}",
        "elapsed_seconds": f"{elapsed_seconds:.6f}",
        "seed": seed,
        "point_counter": "cornacchia_walsh_j1728_exact_trace",
    }


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    """Write deterministic CSV output."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_rows(rows: list[dict[str, object]], output: Path) -> None:
    """Plot convergence of the two refined predictors across the full table."""
    import matplotlib.pyplot as plt

    cutoffs = [int(row["cutoff"]) for row in rows]
    integral_ratios = [
        float(row["observed_over_integral_predicted"]) for row in rows
    ]
    direct_ratios = [float(row["observed_over_direct_predicted"]) for row in rows]
    figure, axis = plt.subplots(figsize=(9.4, 4.8))
    axis.plot(
        cutoffs,
        integral_ratios,
        color="#0b6e69",
        linewidth=2,
        marker="o",
        markersize=3.2,
        label="Zywina integral predictor",
    )
    axis.plot(
        cutoffs,
        direct_ratios,
        color="#735aa6",
        linewidth=1.6,
        linestyle="--",
        label="direct split-prime sum",
    )
    axis.axhline(1.0, color="#d2553d", linestyle=":", linewidth=1.5)
    axis.set_xlabel("Prime cutoff x")
    axis.set_ylabel("Observed / predicted")
    axis.set_title("CM Koblitz quotient: complete reproduction of Zywina Table 3")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=PUBLISHED_X)
    parser.add_argument(
        "--checkpoints", default="131072,1000000,5000000,10000000,20000000"
    )
    parser.add_argument("--seed", type=int, default=51012026)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--figure", type=Path)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--segmented", action="store_true")
    parser.add_argument("--segment-size", type=int, default=10_000_000)
    parser.add_argument("--full-published-table", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.smoke:
        args.limit = 10_000
        args.checkpoints = "1000,5000,10000"
    if args.full_published_table:
        args.limit = max(PUBLISHED_TABLE)
        args.checkpoints = ",".join(str(value) for value in PUBLISHED_TABLE)
        args.segmented = True
    if args.limit < 9:
        raise ValueError("limit must be at least 9")
    if args.limit.bit_length() > 60:
        raise ValueError("limit exceeds the scaffold's 60-bit toy ceiling")

    checkpoints = parse_checkpoints(args.checkpoints, args.limit)
    segmented = args.segmented or args.limit > 50_000_000
    rows = measure(
        args.limit,
        checkpoints,
        args.seed,
        segmented=segmented,
        segment_size=args.segment_size,
    )
    stamp = date.today().strftime("%Y%m%d")
    stem = f"reproduce_cm_table_x{args.limit}_s{args.seed}_{stamp}"
    output = args.output or (Path(__file__).parents[1] / "data" / f"{stem}.csv")
    figure = args.figure or (Path(__file__).parents[1] / "figures" / f"{stem}.png")
    write_csv(rows, output)
    if not args.no_plot:
        plot_rows(rows, figure)
    final = rows[-1]
    print(f"quotient_prime_count={final['quotient_prime_count']}")
    print(f"integral_predicted_count={final['integral_predicted_count']}")
    print(f"integral_predicted_rounded={final['integral_predicted_rounded']}")
    print(f"observed_over_integral_predicted={final['observed_over_integral_predicted']}")
    if args.limit == PUBLISHED_X:
        print(
            "published_actual_difference="
            f"{int(final['quotient_prime_count']) - PUBLISHED_ACTUAL}"
        )
        print(
            "published_expected_difference="
            f"{int(final['integral_predicted_rounded']) - PUBLISHED_EXPECTED_ROUNDED}"
        )
    published_rows = [row for row in rows if row["published_actual"] != ""]
    if published_rows:
        actual_mismatches = sum(
            int(row["published_actual_difference"]) != 0 for row in published_rows
        )
        expected_mismatches = sum(
            int(row["published_expected_difference"]) != 0 for row in published_rows
        )
        print(f"published_rows_compared={len(published_rows)}")
        print(f"published_actual_mismatches={actual_mismatches}")
        print(f"published_expected_mismatches={expected_mismatches}")
    print(f"elapsed_seconds={final['elapsed_seconds']}")
    print(f"csv={output}")
    if not args.no_plot:
        print(f"figure={figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
