"""
measure_norm_gap.py - measure exact and LLL ideal-lattice norm gaps.
Sub-goal: P3.3 / SG-02 through SG-05
Inputs:   --primes <p...> --trials-per-p <int> --ells <ell...> --seed <int>
Outputs:  data/measure_norm_gap_<params>_<date>_{raw,summary}.csv and an SVG
Runtime:  measured after the first complete run; --smoke targets under 10 seconds
Validated against: lib/tests/test_quaternion.py fixed relations and exhaustive SVP
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from sympy import nextprime  # noqa: E402

from lib.quaternion import (  # noqa: E402
    MaximalOrder,
    exact_short_vector,
    lll_short_vector,
    theta_series_prefix,
)


DEFAULT_PRIMES = [7, 11, 19, 23, 31, 43, 59, 71, 83, 103, 131, 151, 179, 223]
DEFAULT_ELLS = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]


def _format_tuple(values: Sequence[int]) -> str:
    return ";".join(str(value) for value in values)


def _fingerprint(p: int, theta: Sequence[int]) -> str:
    payload = json.dumps([p, list(theta)], separators=(",", ":")).encode("ascii")
    return hashlib.sha256(payload).hexdigest()[:16]


def run_instances(
    primes: Sequence[int],
    trials_per_p: int,
    ells: Sequence[int],
    seed: int,
    ell_policy: str = "listed",
) -> list[dict[str, int | float | str]]:
    if trials_per_p <= 0:
        raise ValueError("trials_per_p must be positive")
    if ell_policy not in {"listed", "near-p"}:
        raise ValueError("ell_policy must be 'listed' or 'near-p'")
    if ell_policy == "listed" and not ells:
        raise ValueError("at least one input ideal norm is required")
    rng = random.Random(seed)
    rows: list[dict[str, int | float | str]] = []
    instance = 0
    for p in primes:
        order = MaximalOrder(p)
        if ell_policy == "near-p":
            spacing = max(16, p // 100)
            admissible_ells = [
                int(nextprime(p + 2 + step * spacing)) for step in range(8)
            ]
        else:
            admissible_ells = [ell for ell in ells if ell != p]
        if not admissible_ells:
            raise ValueError(f"no admissible ell for p={p}")
        for local_trial in range(trials_per_p):
            ell = rng.choice(admissible_ells)
            ideal, alpha = order.random_prime_ideal(ell, rng)
            if ideal.index != ell * ell or not ideal.verifies_left_closure():
                raise AssertionError("sampled lattice failed the left-ideal checks")

            lll_started = time.perf_counter()
            lll = lll_short_vector(ideal)
            lll_seconds = time.perf_counter() - lll_started
            exact_started = time.perf_counter()
            exact = exact_short_vector(ideal)
            exact_seconds = time.perf_counter() - exact_started

            if lll.norm % ideal.norm or exact.norm % ideal.norm:
                raise AssertionError("element norm was not divisible by ideal norm")
            lll_equivalent = ideal.equivalent_ideal_from_element(lll.order_coordinates)
            exact_equivalent = ideal.equivalent_ideal_from_element(exact.order_coordinates)
            if not lll_equivalent.verifies_left_closure():
                raise AssertionError("LLL-derived equivalent ideal failed closure")
            if not exact_equivalent.verifies_left_closure():
                raise AssertionError("exact-derived equivalent ideal failed closure")

            lll_ideal_norm = lll.norm // ideal.norm
            exact_ideal_norm = exact.norm // ideal.norm
            if lll_equivalent.norm != lll_ideal_norm:
                raise AssertionError("LLL equivalent-ideal norm identity failed")
            if exact_equivalent.norm != exact_ideal_norm:
                raise AssertionError("exact equivalent-ideal norm identity failed")

            theta_cutoff = max(8, 2 * math.ceil(math.sqrt(p)))
            theta = theta_series_prefix(ideal, theta_cutoff)
            equivalent_theta = theta_series_prefix(exact_equivalent, theta_cutoff)
            if theta != equivalent_theta:
                raise AssertionError("theta-series equivalence check failed")
            theta_label = _fingerprint(p, theta)

            sqrt_p = math.sqrt(p)
            row: dict[str, int | float | str] = {
                "instance": instance,
                "local_trial": local_trial,
                "seed": seed,
                "p": p,
                "p_bits": p.bit_length(),
                "p_mod_8": p % 8,
                "ell": ell,
                "ell_mod_4": ell % 4,
                "alpha_order_coordinates": _format_tuple(alpha),
                "ideal_index": ideal.index,
                "input_ideal_norm": ideal.norm,
                "ideal_hnf": ideal.canonical_id,
                "theta_cutoff": theta_cutoff,
                "theta_fingerprint": theta_label,
                "theta_nonzero_coefficients": "|".join(
                    f"{norm}:{count}" for norm, count in enumerate(theta) if count
                ),
                "lll_element_coordinates": _format_tuple(lll.order_coordinates),
                "lll_element_reduced_norm": lll.norm,
                "lll_equivalent_ideal_norm": lll_ideal_norm,
                "lll_log_p_norm": math.log(lll_ideal_norm, p),
                "exact_element_coordinates": _format_tuple(exact.order_coordinates),
                "exact_element_reduced_norm": exact.norm,
                "exact_equivalent_ideal_norm": exact_ideal_norm,
                "exact_log_p_norm": math.log(exact_ideal_norm, p),
                "sqrt_p_reference": sqrt_p,
                "exact_norm_over_sqrt_p": exact_ideal_norm / sqrt_p,
                "lll_norm_over_sqrt_p": lll_ideal_norm / sqrt_p,
                "lll_approximation_factor": lll.norm / exact.norm,
                "lll_exact_hit": int(lll.norm == exact.norm),
                "exact_initial_norm_bound": exact.initial_norm_bound,
                "exact_coefficient_bounds": _format_tuple(exact.coefficient_bounds),
                "exact_candidates_checked": exact.candidates_checked,
                "lll_seconds": lll_seconds,
                "exact_seconds": exact_seconds,
                "norm_convention": "nrd(element)/N(input ideal)=N(equivalent ideal)",
                "sampler": (
                    "near-p prime-neighbor isotropic residue; not proven class-group uniform"
                    if ell_policy == "near-p"
                    else "small prime-neighbor isotropic residue; class-biased"
                ),
            }
            rows.append(row)
            instance += 1
    return rows


def _mean_ci(values: Sequence[float]) -> tuple[float, float]:
    mean = statistics.fmean(values)
    if len(values) < 2:
        return mean, 0.0
    return mean, 1.96 * statistics.stdev(values) / math.sqrt(len(values))


def _summary_row(
    family: str,
    value: str,
    group: Sequence[dict[str, int | float | str]],
) -> dict[str, int | float | str]:
    exponents = [float(row["exact_log_p_norm"]) for row in group]
    ratios = [float(row["exact_norm_over_sqrt_p"]) for row in group]
    approximations = [float(row["lll_approximation_factor"]) for row in group]
    exact_mean, exact_ci = _mean_ci(exponents)
    ratio_mean, ratio_ci = _mean_ci(ratios)
    lll_mean, lll_ci = _mean_ci(approximations)
    return {
        "group_family": family,
        "group_value": value,
        "n": len(group),
        "exact_log_p_norm_mean": exact_mean,
        "exact_log_p_norm_normal_95ci_halfwidth": exact_ci,
        "exact_log_p_norm_median": statistics.median(exponents),
        "exact_log_p_norm_min": min(exponents),
        "exact_log_p_norm_max": max(exponents),
        "exact_norm_over_sqrt_p_mean": ratio_mean,
        "exact_norm_over_sqrt_p_normal_95ci_halfwidth": ratio_ci,
        "exact_norm_over_sqrt_p_median": statistics.median(ratios),
        "lll_exact_hit_rate": statistics.fmean(
            float(row["lll_exact_hit"]) for row in group
        ),
        "lll_approximation_factor_mean": lll_mean,
        "lll_approximation_factor_normal_95ci_halfwidth": lll_ci,
        "lll_approximation_factor_max": max(approximations),
        "exact_candidates_mean": statistics.fmean(
            float(row["exact_candidates_checked"]) for row in group
        ),
        "exact_seconds_mean": statistics.fmean(
            float(row["exact_seconds"]) for row in group
        ),
    }


def summarize_rows(
    rows: Sequence[dict[str, int | float | str]],
) -> list[dict[str, int | float | str]]:
    if not rows:
        raise ValueError("cannot summarize an empty dataset")
    summaries = [_summary_row("overall", "all", rows)]
    group_specs = (
        ("p", "p"),
        ("p_bits", "p_bits"),
        ("p_mod_8", "p_mod_8"),
        ("input_ideal_norm", "ell"),
        ("ell_mod_4", "ell_mod_4"),
        ("theta_fingerprint", "theta_fingerprint"),
    )
    for family, key in group_specs:
        groups: dict[str, list[dict[str, int | float | str]]] = defaultdict(list)
        for row in rows:
            groups[str(row[key])].append(row)
        for value in sorted(groups, key=lambda item: (len(item), item)):
            summaries.append(_summary_row(family, value, groups[value]))
    return summaries


def scaling_rows(
    rows: Sequence[dict[str, int | float | str]],
) -> list[dict[str, int | float | str]]:
    groups: dict[int, list[dict[str, int | float | str]]] = defaultdict(list)
    for row in rows:
        groups[int(row["p_bits"])].append(row)
    if len(groups) < 2:
        return []
    points: list[dict[str, int | float | str]] = []
    for bits in sorted(groups):
        group = groups[bits]
        points.append(
            {
                "p_bits": bits,
                "n": len(group),
                "p_min": min(int(row["p"]) for row in group),
                "p_max": max(int(row["p"]) for row in group),
                "lll_exact_hit_rate": statistics.fmean(
                    float(row["lll_exact_hit"]) for row in group
                ),
                "exact_candidates_mean": statistics.fmean(
                    float(row["exact_candidates_checked"]) for row in group
                ),
                "exact_candidates_max": max(
                    int(row["exact_candidates_checked"]) for row in group
                ),
                "exact_seconds_mean": statistics.fmean(
                    float(row["exact_seconds"]) for row in group
                ),
                "exact_log_p_norm_mean": statistics.fmean(
                    float(row["exact_log_p_norm"]) for row in group
                ),
                "exact_norm_over_sqrt_p_mean": statistics.fmean(
                    float(row["exact_norm_over_sqrt_p"]) for row in group
                ),
            }
        )
    x_values = [float(point["p_bits"]) for point in points]
    y_values = [math.log2(float(point["exact_seconds_mean"])) for point in points]
    x_mean = statistics.fmean(x_values)
    y_mean = statistics.fmean(y_values)
    denominator = sum((value - x_mean) ** 2 for value in x_values)
    slope = sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values)
    ) / denominator
    intercept = y_mean - slope * x_mean
    for point, x_value, y_value in zip(points, x_values, y_values):
        fitted = intercept + slope * x_value
        point["log2_exact_seconds_fit"] = fitted
        point["log2_exact_seconds_residual"] = y_value - fitted
        point["log2_seconds_per_p_bit_slope"] = slope
        point["log2_seconds_fit_intercept"] = intercept
    return points


def write_csv(
    rows: Sequence[dict[str, int | float | str]], output: Path
) -> None:
    if not rows:
        raise ValueError("cannot write an empty dataset")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_distribution(
    rows: Sequence[dict[str, int | float | str]], output: Path
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["svg.hashsalt"] = "p3.3-norm-gap"
    x_values = [math.log2(int(row["p"])) for row in rows]
    exact_values = [float(row["exact_log_p_norm"]) for row in rows]
    lll_values = [float(row["lll_log_p_norm"]) for row in rows]
    hit_rate = statistics.fmean(float(row["lll_exact_hit"]) for row in rows)
    median_ratio = statistics.median(
        float(row["exact_norm_over_sqrt_p"]) for row in rows
    )

    fig, axis = plt.subplots(figsize=(9.2, 5.4), constrained_layout=True)
    axis.scatter(
        x_values,
        lll_values,
        s=24,
        color="#d97706",
        alpha=0.45,
        marker="x",
        linewidths=1.0,
        label="Norm-aware LLL basis minimum",
    )
    axis.scatter(
        x_values,
        exact_values,
        s=20,
        color="#0f766e",
        alpha=0.72,
        edgecolors="none",
        label="Certified exact minimum",
    )
    axis.axhline(
        0.5,
        color="#1f2937",
        linestyle="--",
        linewidth=1.2,
        label=r"Minkowski-scale exponent $1/2$",
    )
    axis.set_xlabel(r"Quaternion prime size $\log_2 p$")
    axis.set_ylabel(r"Equivalent-ideal exponent $\log_p N(J)$")
    axis.set_title("P3.3 toy ideal-lattice norm gap")
    axis.grid(color="#d1d5db", linewidth=0.6, alpha=0.65)
    axis.legend(
        frameon=True,
        facecolor="white",
        framealpha=0.92,
        edgecolor="none",
        loc="upper right",
    )
    axis.text(
        0.015,
        0.90,
        f"n={len(rows)}  |  LLL exact-hit={hit_rate:.1%}  |  "
        f"median exact N(J)/sqrt(p)={median_ratio:.3f}\n"
        "Convention: N(J)=nrd(x)/N(I); prime-neighbor sampler is not class-uniform",
        transform=axis.transAxes,
        fontsize=8.5,
        color="#374151",
        verticalalignment="top",
        bbox={"facecolor": "white", "alpha": 0.88, "edgecolor": "none", "pad": 3},
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, format="svg", metadata={"Date": None})
    fig.savefig(
        output.with_suffix(".png"),
        format="png",
        dpi=160,
        metadata={"Software": "P3.3 measure_norm_gap.py"},
    )
    plt.close(fig)


def _parameter_label(
    primes: Sequence[int], trials: int, seed: int, ell_policy: str
) -> str:
    if len(primes) <= 4:
        prime_label = "-".join(str(p) for p in primes)
    else:
        prime_label = f"{min(primes)}-{max(primes)}x{len(primes)}"
    policy_label = "_enearp" if ell_policy == "near-p" else ""
    return f"p{prime_label}_t{trials}_s{seed}{policy_label}"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=int, nargs="+", default=DEFAULT_PRIMES)
    parser.add_argument("--trials-per-p", type=int, default=10)
    parser.add_argument("--ells", type=int, nargs="+", default=DEFAULT_ELLS)
    parser.add_argument(
        "--ell-policy", choices=("listed", "near-p"), default="listed"
    )
    parser.add_argument("--seed", type=int, default=33032026)
    parser.add_argument("--date", default="20260701")
    parser.add_argument(
        "--output-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    primes = [11, 19] if args.smoke else args.primes
    trials = 2 if args.smoke else args.trials_per_p
    started = time.perf_counter()
    rows = run_instances(primes, trials, args.ells, args.seed, args.ell_policy)
    summaries = summarize_rows(rows)
    scaling = scaling_rows(rows)
    label = _parameter_label(primes, trials, args.seed, args.ell_policy)
    raw_output = args.output_root / "data" / f"measure_norm_gap_{label}_{args.date}_raw.csv"
    summary_output = (
        args.output_root / "data" / f"measure_norm_gap_{label}_{args.date}_summary.csv"
    )
    scaling_output = (
        args.output_root / "data" / f"measure_norm_gap_{label}_{args.date}_scaling.csv"
    )
    figure_output = (
        args.output_root / "figures" / f"measure_norm_gap_{label}_{args.date}.svg"
    )
    write_csv(rows, raw_output)
    write_csv(summaries, summary_output)
    if scaling:
        write_csv(scaling, scaling_output)
    plot_distribution(rows, figure_output)
    overall = summaries[0]
    elapsed = time.perf_counter() - started
    print(f"instances={len(rows)}")
    print(f"lll_exact_hit_rate={float(overall['lll_exact_hit_rate']):.6f}")
    print(
        "median_exact_norm_over_sqrt_p="
        f"{float(overall['exact_norm_over_sqrt_p_median']):.6f}"
    )
    print(f"elapsed_seconds={elapsed:.3f}")
    print(f"raw={raw_output}")
    print(f"summary={summary_output}")
    if scaling:
        print(f"scaling={scaling_output}")
    print(f"figure={figure_output}")
    print(f"figure_png={figure_output.with_suffix('.png')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
