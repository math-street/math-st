"""
measure_compiled_timing.py - Timing screen for the Rust p=11 pipeline.
Sub-goal: P5.4 / SG-11
Inputs:   --rounds --batch --resamples --seed [--smoke] [--output <path>]
Outputs:  data/measure_compiled_timing_<params>_<date>.csv and _summary.csv
Runtime:  under 10 seconds in smoke mode
Validated against: paired bootstrap interval and sign-permutation test
"""

from __future__ import annotations

import argparse
import csv
import platform
import shutil
import statistics
import subprocess
import tempfile
from datetime import date
from pathlib import Path
from random import Random

from measure_map_timing import bootstrap_paired_mean_ratio

SOURCE = Path(__file__).with_name("ct_backend_p11.rs")


def paired_sign_permutation_pvalue(
    left: list[float],
    right: list[float],
    *,
    resamples: int,
    rng: Random,
) -> float:
    """Two-sided random-sign permutation test for the paired mean difference."""

    if not left or len(left) != len(right):
        raise ValueError("paired samples must have equal nonzero length")
    differences = [left_value - right_value for left_value, right_value in zip(left, right)]
    observed = abs(statistics.fmean(differences))
    exceedances = 0
    for _ in range(resamples):
        permuted = statistics.fmean(
            difference if rng.getrandbits(1) else -difference
            for difference in differences
        )
        exceedances += abs(permuted) >= observed
    return (exceedances + 1) / (resamples + 1)


def measure(
    *,
    rounds: int,
    batch: int,
    resamples: int,
    seed: int,
) -> tuple[list[dict[str, int]], dict[str, int | float | str]]:
    if min(rounds, batch, resamples) < 1:
        raise ValueError("rounds, batch, and resamples must be positive")
    rustc = shutil.which("rustc")
    if rustc is None:
        raise RuntimeError("rustc is required for the compiled timing screen")
    with tempfile.TemporaryDirectory(prefix="p54-ct-timing-") as temporary:
        executable = Path(temporary) / "ct_backend_p11.exe"
        subprocess.run(
            [
                rustc,
                "-C",
                "opt-level=3",
                "-C",
                "target-cpu=native",
                "--emit",
                f"link={executable}",
                str(SOURCE),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        execution = subprocess.run(
            [str(executable), "--timing", str(rounds), str(batch)],
            check=True,
            capture_output=True,
            text=True,
        )
    raw_rows = [
        {key: int(value) for key, value in row.items()}
        for row in csv.DictReader(execution.stdout.splitlines())
    ]
    if len(raw_rows) != rounds:
        raise AssertionError("compiled harness emitted the wrong number of rounds")
    class_a = [row["class_a_ns"] / batch for row in raw_rows]
    class_b = [row["class_b_ns"] / batch for row in raw_rows]
    ratio, ci_low, ci_high = bootstrap_paired_mean_ratio(
        class_a,
        class_b,
        resamples=resamples,
        rng=Random(seed),
    )
    permutation_p = paired_sign_permutation_pvalue(
        class_a,
        class_b,
        resamples=resamples,
        rng=Random(seed + 1),
    )
    interval_intersects_band = int(ci_high >= 0.9 and ci_low <= 1.1)
    permutation_passes = int(permutation_p >= 0.01)
    summary: dict[str, int | float | str] = {
        "backend": "rust-u64-p11",
        "compiler": subprocess.run(
            [rustc, "--version"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "platform": platform.platform(),
        "class_a": "u0=0;u1=0",
        "class_b": "u0=1;u1=2",
        "rounds": rounds,
        "batch": batch,
        "resamples": resamples,
        "seed": seed,
        "class_a_mean_ns": statistics.fmean(class_a),
        "class_b_mean_ns": statistics.fmean(class_b),
        "mean_ratio_a_over_b": ratio,
        "paired_bootstrap_ci_low": ci_low,
        "paired_bootstrap_ci_high": ci_high,
        "sign_permutation_p": permutation_p,
        "interval_intersects_0.9_1.1": interval_intersects_band,
        "permutation_p_at_least_0.01": permutation_passes,
        "detector_passed": interval_intersects_band & permutation_passes,
    }
    return raw_rows, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rounds", type=int, default=400)
    parser.add_argument("--batch", type=int, default=1_000)
    parser.add_argument("--resamples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=5409)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rounds = 40 if args.smoke else args.rounds
    batch = 100 if args.smoke else args.batch
    resamples = 500 if args.smoke else args.resamples
    raw_rows, summary = measure(
        rounds=rounds,
        batch=batch,
        resamples=resamples,
        seed=args.seed,
    )
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / (
            f"measure_compiled_timing_p11_s{rounds}_b{batch}_seed{args.seed}_"
            f"{date.today():%Y%m%d}.csv"
        )
    )
    summary_output = output.with_name(f"{output.stem}_summary.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(raw_rows[0]))
        writer.writeheader()
        writer.writerows(raw_rows)
    with summary_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)
    print(f"wrote {len(raw_rows)} rows to {output}")
    print(f"wrote summary to {summary_output}")
    print(
        f"ratio={summary['mean_ratio_a_over_b']:.6f} "
        f"ci=[{summary['paired_bootstrap_ci_low']:.6f},"
        f"{summary['paired_bootstrap_ci_high']:.6f}] "
        f"permutation_p={summary['sign_permutation_p']:.6f}"
    )


if __name__ == "__main__":
    main()
