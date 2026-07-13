"""
measure_shape_gap.py - certify the cost of power and smooth norm constraints.
Sub-goal: P3.3 / SG-05 and SG-07
Inputs:   --primes <p...> --trials-per-p <int> --seed <int> --limit-multiplier <int>
Outputs:  data/measure_shape_gap_<params>_<date>_{raw,summary}.csv and SVG/PNG
Runtime:  measured after the first complete run; --smoke targets under 10 seconds
Validated against: exact spectrum/theta support equality in test_quaternion.py
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sympy import nextprime  # noqa: E402

from lib.quaternion import (  # noqa: E402
    IntegralIdeal,
    MaximalOrder,
    exact_short_vector,
    normalized_norm_spectrum,
)


DEFAULT_PRIMES = [7, 11, 19, 23, 31, 43, 59, 71, 83, 103, 131, 151, 179, 223]


def is_prime_power(value: int, prime: int) -> bool:
    if value < 1 or prime < 2:
        return False
    while value % prime == 0:
        value //= prime
    return value == 1


def is_b_smooth(value: int, bound: int) -> bool:
    if value < 1 or bound < 2:
        return False
    divisor = 2
    while divisor <= bound:
        while value % divisor == 0:
            value //= divisor
        divisor += 1
    return value == 1


def near_p_primes(p: int) -> list[int]:
    spacing = max(16, p // 100)
    return [int(nextprime(p + 2 + step * spacing)) for step in range(8)]


def _minimum_matching(
    witnesses: dict[int, tuple[int, ...]], predicate: Callable[[int], bool]
) -> tuple[int | None, tuple[int, ...] | None]:
    matches = [norm for norm in witnesses if predicate(norm)]
    if not matches:
        return None, None
    norm = min(matches)
    return norm, witnesses[norm]


def _validate_witness(
    ideal: IntegralIdeal, norm: int | None, vector: tuple[int, ...] | None
) -> None:
    if norm is None or vector is None:
        return
    equivalent = ideal.equivalent_ideal_from_element(vector)
    if equivalent.norm != norm or not equivalent.verifies_left_closure():
        raise AssertionError("constrained equivalent-ideal validation failed")


def run_instances(
    primes: Sequence[int],
    trials_per_p: int,
    seed: int,
    limit_multiplier: int,
    smooth_bound: int,
) -> list[dict[str, int | float | str]]:
    if trials_per_p < 1 or limit_multiplier < 1 or smooth_bound < 2:
        raise ValueError("trials and bounds must be positive")
    rng = random.Random(seed)
    rows: list[dict[str, int | float | str]] = []
    instance = 0
    for p in primes:
        order = MaximalOrder(p)
        ell_choices = near_p_primes(p)
        for local_trial in range(trials_per_p):
            ell = rng.choice(ell_choices)
            ideal, alpha = order.random_prime_ideal(ell, rng)
            if not ideal.verifies_left_closure():
                raise AssertionError("sampled ideal failed left closure")
            exact = exact_short_vector(ideal)
            exact_norm = exact.norm // ideal.norm
            actual_multiplier = 1
            spectrum_seconds = 0.0
            spectrum_candidates_total = 0
            while True:
                cutoff = actual_multiplier * p
                started = time.perf_counter()
                spectrum = normalized_norm_spectrum(
                    ideal, cutoff, max_candidates=5_000_000
                )
                spectrum_seconds += time.perf_counter() - started
                spectrum_candidates_total += spectrum.candidates_checked
                power2_norm, power2_vector = _minimum_matching(
                    spectrum.witnesses, lambda value: is_prime_power(value, 2)
                )
                power3_norm, power3_vector = _minimum_matching(
                    spectrum.witnesses, lambda value: is_prime_power(value, 3)
                )
                smooth_norm, smooth_vector = _minimum_matching(
                    spectrum.witnesses,
                    lambda value: is_b_smooth(value, smooth_bound),
                )
                if (
                    power2_norm is not None
                    and power3_norm is not None
                    and smooth_norm is not None
                ) or actual_multiplier == limit_multiplier:
                    break
                actual_multiplier = min(2 * actual_multiplier, limit_multiplier)
            _validate_witness(ideal, power2_norm, power2_vector)
            _validate_witness(ideal, power3_norm, power3_vector)
            _validate_witness(ideal, smooth_norm, smooth_vector)

            row: dict[str, int | float | str] = {
                "instance": instance,
                "local_trial": local_trial,
                "seed": seed,
                "p": p,
                "p_bits": p.bit_length(),
                "p_mod_8": p % 8,
                "ell": ell,
                "alpha_order_coordinates": ";".join(str(value) for value in alpha),
                "input_ideal_norm": ideal.norm,
                "search_limit": cutoff,
                "max_limit_multiplier": limit_multiplier,
                "actual_limit_multiplier": actual_multiplier,
                "smooth_bound": smooth_bound,
                "unconstrained_norm": exact_norm,
                "unconstrained_log_p_norm": math.log(exact_norm, p),
                "unconstrained_over_sqrt_p": exact_norm / math.sqrt(p),
                "power2_norm": power2_norm if power2_norm is not None else "",
                "power2_log_p_norm": (
                    math.log(power2_norm, p) if power2_norm is not None else ""
                ),
                "power2_over_unconstrained": (
                    power2_norm / exact_norm if power2_norm is not None else ""
                ),
                "power2_censored": int(power2_norm is None),
                "power3_norm": power3_norm if power3_norm is not None else "",
                "power3_log_p_norm": (
                    math.log(power3_norm, p) if power3_norm is not None else ""
                ),
                "power3_over_unconstrained": (
                    power3_norm / exact_norm if power3_norm is not None else ""
                ),
                "power3_censored": int(power3_norm is None),
                "smooth_norm": smooth_norm if smooth_norm is not None else "",
                "smooth_log_p_norm": (
                    math.log(smooth_norm, p) if smooth_norm is not None else ""
                ),
                "smooth_over_unconstrained": (
                    smooth_norm / exact_norm if smooth_norm is not None else ""
                ),
                "smooth_censored": int(smooth_norm is None),
                "represented_positive_norms": len(spectrum.witnesses),
                "spectrum_coefficient_bounds": ";".join(
                    str(value) for value in spectrum.coefficient_bounds
                ),
                "spectrum_candidates_checked": spectrum.candidates_checked,
                "spectrum_candidates_total": spectrum_candidates_total,
                "spectrum_seconds": spectrum_seconds,
                "norm_convention": "q_I(x)=nrd(x)/N(I)=N(equivalent ideal)",
                "sampler": "near-p prime-neighbor; not proven class-group uniform",
            }
            rows.append(row)
            instance += 1
    return rows


def _mean_ci(values: Sequence[float]) -> tuple[float | str, float | str]:
    if not values:
        return "", ""
    mean = statistics.fmean(values)
    if len(values) < 2:
        return mean, 0.0
    return mean, 1.96 * statistics.stdev(values) / math.sqrt(len(values))


def _summary_row(
    family: str,
    value: str,
    rows: Sequence[dict[str, int | float | str]],
) -> dict[str, int | float | str]:
    result: dict[str, int | float | str] = {
        "group_family": family,
        "group_value": value,
        "n": len(rows),
    }
    for label in ("unconstrained", "power2", "power3", "smooth"):
        exponent_key = f"{label}_log_p_norm"
        exponents = [float(row[exponent_key]) for row in rows if row[exponent_key] != ""]
        mean, ci = _mean_ci(exponents)
        result[f"{label}_observed"] = len(exponents)
        result[f"{label}_log_p_norm_mean"] = mean
        result[f"{label}_log_p_norm_normal_95ci_halfwidth"] = ci
        result[f"{label}_log_p_norm_median"] = (
            statistics.median(exponents) if exponents else ""
        )
    for label in ("power2", "power3", "smooth"):
        ratios = [
            float(row[f"{label}_over_unconstrained"])
            for row in rows
            if row[f"{label}_over_unconstrained"] != ""
        ]
        result[f"{label}_over_unconstrained_median"] = (
            statistics.median(ratios) if ratios else ""
        )
        result[f"{label}_censored_rate"] = statistics.fmean(
            float(row[f"{label}_censored"]) for row in rows
        )
    result["spectrum_candidates_mean"] = statistics.fmean(
        float(row["spectrum_candidates_checked"]) for row in rows
    )
    result["spectrum_candidates_max"] = max(
        int(row["spectrum_candidates_checked"]) for row in rows
    )
    result["spectrum_seconds_mean"] = statistics.fmean(
        float(row["spectrum_seconds"]) for row in rows
    )
    return result


def summarize_rows(
    rows: Sequence[dict[str, int | float | str]],
) -> list[dict[str, int | float | str]]:
    if not rows:
        raise ValueError("cannot summarize empty rows")
    summaries = [_summary_row("overall", "all", rows)]
    for family, key in (("p", "p"), ("p_mod_8", "p_mod_8")):
        groups: dict[str, list[dict[str, int | float | str]]] = defaultdict(list)
        for row in rows:
            groups[str(row[key])].append(row)
        for value in sorted(groups, key=int):
            summaries.append(_summary_row(family, value, groups[value]))
    return summaries


def write_csv(
    rows: Sequence[dict[str, int | float | str]], output: Path
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_shape_gap(
    rows: Sequence[dict[str, int | float | str]], output: Path, smooth_bound: int
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["svg.hashsalt"] = "p3.3-shape-gap"
    figure, axis = plt.subplots(figsize=(9.2, 5.5), constrained_layout=True)
    series = (
        ("unconstrained_log_p_norm", "Exact unconstrained", "#0f766e", "o"),
        ("power2_log_p_norm", r"Exact $2^e$", "#b45309", "x"),
        ("power3_log_p_norm", r"Exact $3^e$", "#7c3aed", "+"),
        ("smooth_log_p_norm", f"Exact {smooth_bound}-smooth", "#2563eb", "s"),
    )
    x_values = [math.log2(int(row["p"])) for row in rows]
    for key, label, color, marker in series:
        points = [
            (x, float(row[key]))
            for x, row in zip(x_values, rows)
            if row[key] != ""
        ]
        axis.scatter(
            [point[0] for point in points],
            [point[1] for point in points],
            s=26,
            alpha=0.68,
            color=color,
            marker=marker,
            label=label,
        )
    axis.axhline(0.5, color="#1f2937", linestyle="--", linewidth=1.1, label="Exponent 1/2")
    axis.axhline(1.0, color="#6b7280", linestyle=":", linewidth=1.1, label="Exponent 1")
    axis.set_xlabel(r"Quaternion prime size $\log_2 p$")
    axis.set_ylabel(r"Equivalent-ideal exponent $\log_p N(J)$")
    axis.set_title("P3.3 exact norm-shape penalty")
    axis.grid(color="#d1d5db", linewidth=0.6, alpha=0.65)
    axis.legend(frameon=True, facecolor="white", framealpha=0.92, edgecolor="none")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, format="svg", metadata={"Date": None})
    figure.savefig(
        output.with_suffix(".png"),
        format="png",
        dpi=160,
        metadata={"Software": "P3.3 measure_shape_gap.py"},
    )
    plt.close(figure)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=int, nargs="+", default=DEFAULT_PRIMES)
    parser.add_argument("--trials-per-p", type=int, default=5)
    parser.add_argument("--seed", type=int, default=33032030)
    parser.add_argument("--limit-multiplier", type=int, default=16)
    parser.add_argument("--smooth-bound", type=int, default=5)
    parser.add_argument("--date", default="20260713")
    parser.add_argument(
        "--output-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    primes = [11, 19] if args.smoke else args.primes
    trials = 1 if args.smoke else args.trials_per_p
    started = time.perf_counter()
    rows = run_instances(
        primes, trials, args.seed, args.limit_multiplier, args.smooth_bound
    )
    summaries = summarize_rows(rows)
    prime_label = (
        "-".join(str(p) for p in primes)
        if len(primes) <= 4
        else f"{min(primes)}-{max(primes)}x{len(primes)}"
    )
    label = (
        f"p{prime_label}_t{trials}_m{args.limit_multiplier}_"
        f"b{args.smooth_bound}_s{args.seed}"
    )
    raw_output = args.output_root / "data" / f"measure_shape_gap_{label}_{args.date}_raw.csv"
    summary_output = args.output_root / "data" / f"measure_shape_gap_{label}_{args.date}_summary.csv"
    figure_output = args.output_root / "figures" / f"measure_shape_gap_{label}_{args.date}.svg"
    write_csv(rows, raw_output)
    write_csv(summaries, summary_output)
    plot_shape_gap(rows, figure_output, args.smooth_bound)
    overall = summaries[0]
    print(f"instances={len(rows)}")
    print(f"power2_censored_rate={float(overall['power2_censored_rate']):.6f}")
    print(f"power3_censored_rate={float(overall['power3_censored_rate']):.6f}")
    print(f"smooth_censored_rate={float(overall['smooth_censored_rate']):.6f}")
    print(f"elapsed_seconds={time.perf_counter() - started:.3f}")
    print(f"raw={raw_output}")
    print(f"summary={summary_output}")
    print(f"figure={figure_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
