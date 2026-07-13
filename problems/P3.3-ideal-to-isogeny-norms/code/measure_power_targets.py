"""
measure_power_targets.py - certify minimum power-of-2 and power-of-3 norms.
Sub-goal: P3.3 / SG-08
Inputs:   --primes <p...> --trials-per-p <int> --seed <int> --max-box <int>
          --target-multiple <int>
Outputs:  data/measure_power_targets_<params>_<date>_{raw,summary}.csv and plots
Runtime:  measured after the first complete run; --smoke targets under 10 seconds
Validated against: target solver versus full exact spectrum in test_quaternion.py
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
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.quaternion import (  # noqa: E402
    MaximalOrder,
    exact_short_vector,
    first_represented_normalized_target,
)

from measure_shape_gap import near_p_primes  # noqa: E402


DEFAULT_PRIMES = [
    2203,
    2503,
    2803,
    3119,
    3467,
    3719,
    560083,
    640007,
    720019,
    800119,
    880027,
    960031,
    145000043,
    165000023,
    185000027,
    205000007,
    225000011,
    245000047,
]


def powers_through(base: int, limit: int) -> tuple[int, ...]:
    values = [1]
    while values[-1] * base <= limit:
        values.append(values[-1] * base)
    return tuple(values)


def run_instances(
    primes: Sequence[int],
    trials_per_p: int,
    seed: int,
    max_box: int,
    target_multiple: int = 4,
) -> list[dict[str, int | float | str]]:
    if trials_per_p < 1 or max_box < 1 or target_multiple < 1:
        raise ValueError("trials, max_box, and target_multiple must be positive")
    rng = random.Random(seed)
    rows: list[dict[str, int | float | str]] = []
    instance = 0
    for p in primes:
        order = MaximalOrder(p)
        ell_choices = near_p_primes(p)
        target_limit = target_multiple * p
        power2_targets = powers_through(2, target_limit)
        power3_targets = powers_through(3, target_limit)
        for local_trial in range(trials_per_p):
            ell = rng.choice(ell_choices)
            ideal, alpha = order.random_prime_ideal(ell, rng)
            exact = exact_short_vector(ideal)
            unconstrained_norm = exact.norm // ideal.norm
            power_results = {}
            for base, targets in ((2, power2_targets), (3, power3_targets)):
                started = time.perf_counter()
                try:
                    result = first_represented_normalized_target(
                        ideal, targets, max_box_candidates=max_box
                    )
                    error = ""
                except RuntimeError as exception:
                    result = None
                    error = str(exception)
                elapsed = time.perf_counter() - started
                if result is not None and result.normalized_norm is not None:
                    equivalent = ideal.equivalent_ideal_from_element(
                        result.order_coordinates
                    )
                    if (
                        equivalent.norm != result.normalized_norm
                        or not equivalent.verifies_left_closure()
                    ):
                        raise AssertionError("target equivalent ideal failed validation")
                power_results[base] = (result, error, elapsed)

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
                "unconstrained_norm": unconstrained_norm,
                "unconstrained_log_p_norm": math.log(unconstrained_norm, p),
                "unconstrained_over_sqrt_p": unconstrained_norm / math.sqrt(p),
                "max_box": max_box,
                "target_multiple": target_multiple,
                "target_limit": target_limit,
                "norm_convention": "q_I(x)=nrd(x)/N(I)=N(equivalent ideal)",
                "sampler": "near-p prime-neighbor; not proven class-group uniform",
            }
            for base in (2, 3):
                result, error, elapsed = power_results[base]
                norm = result.normalized_norm if result is not None else None
                row.update(
                    {
                        f"power{base}_norm": norm if norm is not None else "",
                        f"power{base}_log_p_norm": (
                            math.log(norm, p) if norm is not None else ""
                        ),
                        f"power{base}_over_unconstrained": (
                            norm / unconstrained_norm if norm is not None else ""
                        ),
                        f"power{base}_targets_tested": (
                            len(result.targets_tested) if result is not None else ""
                        ),
                        f"power{base}_coefficient_bounds": (
                            ";".join(str(value) for value in result.coefficient_bounds)
                            if result is not None
                            else ""
                        ),
                        f"power{base}_box_tuples_checked": (
                            result.box_tuples_checked if result is not None else ""
                        ),
                        f"power{base}_elimination_triples_checked": (
                            result.elimination_triples_checked
                            if result is not None
                            else ""
                        ),
                        f"power{base}_coefficient_box_size": (
                            result.coefficient_box_size if result is not None else ""
                        ),
                        f"power{base}_search_method": (
                            result.search_method if result is not None else ""
                        ),
                        f"power{base}_seconds": elapsed,
                        f"power{base}_censored": int(norm is None),
                        f"power{base}_error": error,
                    }
                )
            rows.append(row)
            instance += 1
    return rows


def _summary_row(
    family: str,
    value: str,
    rows: Sequence[dict[str, int | float | str]],
) -> dict[str, int | float | str]:
    result: dict[str, int | float | str] = {
        "group_family": family,
        "group_value": value,
        "n": len(rows),
        "unconstrained_log_p_norm_mean": statistics.fmean(
            float(row["unconstrained_log_p_norm"]) for row in rows
        ),
    }
    for base in (2, 3):
        observed = [row for row in rows if row[f"power{base}_norm"] != ""]
        exponents = [float(row[f"power{base}_log_p_norm"]) for row in observed]
        ratios = [float(row[f"power{base}_over_unconstrained"]) for row in observed]
        result.update(
            {
                f"power{base}_observed": len(observed),
                f"power{base}_censored_rate": 1 - len(observed) / len(rows),
                f"power{base}_log_p_norm_mean": (
                    statistics.fmean(exponents) if exponents else ""
                ),
                f"power{base}_log_p_norm_median": (
                    statistics.median(exponents) if exponents else ""
                ),
                f"power{base}_over_unconstrained_median": (
                    statistics.median(ratios) if ratios else ""
                ),
                f"power{base}_over_unconstrained_max": max(ratios) if ratios else "",
                f"power{base}_seconds_mean": statistics.fmean(
                    float(row[f"power{base}_seconds"]) for row in rows
                ),
                f"power{base}_box_tuples_max": (
                    max(int(row[f"power{base}_box_tuples_checked"]) for row in observed)
                    if observed
                    else ""
                ),
                f"power{base}_elimination_triples_max": (
                    max(
                        int(row[f"power{base}_elimination_triples_checked"])
                        for row in observed
                    )
                    if observed
                    else ""
                ),
                f"power{base}_coefficient_box_size_max": (
                    max(int(row[f"power{base}_coefficient_box_size"]) for row in observed)
                    if observed
                    else ""
                ),
            }
        )
    return result


def summarize_rows(
    rows: Sequence[dict[str, int | float | str]],
) -> list[dict[str, int | float | str]]:
    summaries = [_summary_row("overall", "all", rows)]
    groups: dict[int, list[dict[str, int | float | str]]] = defaultdict(list)
    for row in rows:
        groups[int(row["p_bits"])].append(row)
    for bits in sorted(groups):
        summaries.append(_summary_row("p_bits", str(bits), groups[bits]))
    return summaries


def write_csv(rows: Sequence[dict[str, int | float | str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_rows(rows: Sequence[dict[str, int | float | str]], output: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    matplotlib.rcParams["svg.hashsalt"] = "p3.3-power-targets"
    figure, axis = plt.subplots(figsize=(9.2, 5.5), constrained_layout=True)
    x_values = [math.log2(int(row["p"])) for row in rows]
    for key, label, color, marker in (
        ("unconstrained_log_p_norm", "Exact unconstrained", "#0f766e", "o"),
        ("power2_log_p_norm", r"Exact minimum $2^e$", "#b45309", "x"),
        ("power3_log_p_norm", r"Exact minimum $3^e$", "#7c3aed", "+"),
    ):
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
    axis.set_title("P3.3 exact pure-power targets across bit sizes")
    axis.grid(color="#d1d5db", linewidth=0.6, alpha=0.65)
    axis.legend(frameon=True, facecolor="white", framealpha=0.92, edgecolor="none")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, format="svg", metadata={"Date": None})
    figure.savefig(
        output.with_suffix(".png"),
        format="png",
        dpi=160,
        metadata={"Software": "P3.3 measure_power_targets.py"},
    )
    plt.close(figure)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primes", type=int, nargs="+", default=DEFAULT_PRIMES)
    parser.add_argument("--trials-per-p", type=int, default=6)
    parser.add_argument("--seed", type=int, default=33032028)
    parser.add_argument("--max-box", type=int, default=1_000_000_000)
    parser.add_argument(
        "--target-multiple",
        type=int,
        default=4,
        help="scan target powers through this multiple of p",
    )
    parser.add_argument("--date", default="20260713")
    parser.add_argument(
        "--output-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    primes = [2203, 560083] if args.smoke else args.primes
    trials = 1 if args.smoke else args.trials_per_p
    started = time.perf_counter()
    rows = run_instances(
        primes, trials, args.seed, args.max_box, args.target_multiple
    )
    summaries = summarize_rows(rows)
    prime_label = (
        "-".join(str(p) for p in primes)
        if len(primes) <= 4
        else f"{min(primes)}-{max(primes)}x{len(primes)}"
    )
    label = f"p{prime_label}_t{trials}_m{args.target_multiple}_s{args.seed}"
    raw_output = args.output_root / "data" / f"measure_power_targets_{label}_{args.date}_raw.csv"
    summary_output = args.output_root / "data" / f"measure_power_targets_{label}_{args.date}_summary.csv"
    figure_output = args.output_root / "figures" / f"measure_power_targets_{label}_{args.date}.svg"
    write_csv(rows, raw_output)
    write_csv(summaries, summary_output)
    plot_rows(rows, figure_output)
    overall = summaries[0]
    print(f"instances={len(rows)}")
    print(f"power2_censored_rate={float(overall['power2_censored_rate']):.6f}")
    print(f"power3_censored_rate={float(overall['power3_censored_rate']):.6f}")
    print(f"elapsed_seconds={time.perf_counter() - started:.3f}")
    print(f"raw={raw_output}")
    print(f"summary={summary_output}")
    print(f"figure={figure_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
