"""
measure_extended_timing.py - Compare input classes on the extended toy maps.
Sub-goal: P5.4 / SG-06a
Inputs:   --samples <int> --batch <int> --seed <int> [--smoke]
Outputs:  data/measure_extended_timing_<params>_<date>_{raw,summary}.csv
Runtime:  roughly 10 seconds at 160 rounds and batch 80 on Python 3.13
Validated against: fixed fixtures from the exhaustive validators
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from datetime import date
from pathlib import Path
from random import Random
from time import perf_counter, perf_counter_ns
from typing import Callable

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from hash_pipeline import TOY_EDWARDS_SUITE
from lib.curves import (
    Curve,
    MontgomeryCurve,
    map_to_curve_elligator2_edwards,
    map_to_curve_svdw,
    map_to_curve_svdw_montgomery,
)
from measure_map_timing import bootstrap_paired_mean_ratio
from validate_isogeny_workarounds import FIXTURES, map_via_isogeny

TimingCall = Callable[[int], object]
Predicate = Callable[[int], bool]


def _svdw_exception(curve: Curve, z: int, u: int) -> bool:
    gz = (z**3 + curve.a * z + curve.b) % curve.p
    t = u * u * gz % curve.p
    return (1 - t) * (1 + t) % curve.p == 0


def timing_fixtures() -> tuple[tuple[str, int, TimingCall, Predicate, str], ...]:
    """Return public map fixtures and their preregistered input partitions."""
    j0_curve = Curve(11, 0, 1)
    j1728_curve = Curve(11, 1, 0)
    montgomery = MontgomeryCurve(11, 3, 1)
    montgomery_model = Curve(11, 9, 1)
    return (
        (
            "svdw_j0",
            11,
            lambda u: map_to_curve_svdw(j0_curve, u, 1),
            lambda u: _svdw_exception(j0_curve, 1, u),
            "exceptional_over_ordinary",
        ),
        (
            "svdw_j1728",
            11,
            lambda u: map_to_curve_svdw(j1728_curve, u, 10),
            lambda u: _svdw_exception(j1728_curve, 10, u),
            "exceptional_over_ordinary",
        ),
        (
            "sswu_isogeny_j0",
            FIXTURES[0].source.p,
            lambda u: map_via_isogeny(FIXTURES[0], u),
            lambda u: u == 0,
            "zero_over_nonzero",
        ),
        (
            "sswu_isogeny_j1728",
            FIXTURES[1].source.p,
            lambda u: map_via_isogeny(FIXTURES[1], u),
            lambda u: u == 0,
            "zero_over_nonzero",
        ),
        (
            "elligator2_edwards",
            TOY_EDWARDS_SUITE.curve.p,
            lambda u: map_to_curve_elligator2_edwards(
                TOY_EDWARDS_SUITE.montgomery_curve,
                u,
                TOY_EDWARDS_SUITE.z,
            ),
            lambda u: TOY_EDWARDS_SUITE.z * u * u
            % TOY_EDWARDS_SUITE.curve.p
            == TOY_EDWARDS_SUITE.curve.p - 1,
            "exceptional_over_ordinary",
        ),
        (
            "svdw_montgomery_transport",
            11,
            lambda u: map_to_curve_svdw_montgomery(montgomery, u, 9),
            lambda u: _svdw_exception(montgomery_model, 9, u),
            "exceptional_over_ordinary",
        ),
    )


def measure_rows(
    *, samples: int, batch: int, seed: int
) -> list[dict[str, int | str | float]]:
    """Measure randomized full-field rounds for every extended fixture."""
    if samples < 1 or batch < 1:
        raise ValueError("samples and batch must be positive")
    rng = Random(seed)
    jobs = [
        (mapping, p, function, predicate, ratio_label, u)
        for mapping, p, function, predicate, ratio_label in timing_fixtures()
        for u in range(p)
    ]
    rows: list[dict[str, int | str | float]] = []
    for sample in range(samples):
        rng.shuffle(jobs)
        for mapping, p, function, predicate, ratio_label, u in jobs:
            started = perf_counter_ns()
            for _ in range(batch):
                function(u)
            elapsed = perf_counter_ns() - started
            rows.append(
                {
                    "mapping": mapping,
                    "p": p,
                    "u": u,
                    "class_a": int(predicate(u)),
                    "ratio_label": ratio_label,
                    "sample": sample,
                    "batch": batch,
                    "seed": seed,
                    "nanoseconds_per_call": elapsed / batch,
                }
            )
    return rows


def summarize_rows(
    rows: list[dict[str, int | str | float]],
    *,
    bootstrap_resamples: int,
    seed: int,
) -> list[dict[str, int | str | float]]:
    """Return paired-round class-A/class-B mean ratios and 95% intervals."""
    rng = Random(seed ^ 0x5407)
    summaries: list[dict[str, int | str | float]] = []
    for mapping in sorted({str(row["mapping"]) for row in rows}):
        mapping_rows = [row for row in rows if row["mapping"] == mapping]
        if {int(row["class_a"]) for row in mapping_rows} != {0, 1}:
            raise ValueError(f"fixture {mapping} does not contain both classes")
        samples = sorted({int(row["sample"]) for row in mapping_rows})
        by_class = {
            class_a: [
                statistics.fmean(
                    float(row["nanoseconds_per_call"])
                    for row in mapping_rows
                    if int(row["sample"]) == sample
                    and int(row["class_a"]) == class_a
                )
                for sample in samples
            ]
            for class_a in (0, 1)
        }
        ratio, low, high = bootstrap_paired_mean_ratio(
            by_class[1],
            by_class[0],
            resamples=bootstrap_resamples,
            rng=rng,
        )
        summaries.append(
            {
                "mapping": mapping,
                "p": int(mapping_rows[0]["p"]),
                "seed": seed,
                "timing_rounds": len(samples),
                "batch": int(mapping_rows[0]["batch"]),
                "ratio_label": str(mapping_rows[0]["ratio_label"]),
                "class_a_mean_ns": statistics.fmean(by_class[1]),
                "class_b_mean_ns": statistics.fmean(by_class[0]),
                "mean_ratio_a_over_b": ratio,
                "ratio_ci95_low": low,
                "ratio_ci95_high": high,
                "bootstrap_resamples": bootstrap_resamples,
            }
        )
    return summaries


def _write_csv(path: Path, rows: list[dict[str, int | str | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=160)
    parser.add_argument("--batch", type=int, default=80)
    parser.add_argument("--seed", type=int, default=5408)
    parser.add_argument("--bootstrap", type=int, default=2_000)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-prefix", type=Path)
    args = parser.parse_args()
    started = perf_counter()
    samples = 8 if args.smoke else args.samples
    batch = 8 if args.smoke else args.batch
    bootstrap = 100 if args.smoke else args.bootstrap
    rows = measure_rows(samples=samples, batch=batch, seed=args.seed)
    summaries = summarize_rows(
        rows,
        bootstrap_resamples=bootstrap,
        seed=args.seed,
    )
    prefix = args.output_prefix
    if prefix is None:
        prefix = (
            Path(__file__).resolve().parents[1]
            / "data"
            / (
                f"measure_extended_timing_s{samples}_b{batch}_"
                f"seed{args.seed}_{date.today():%Y%m%d}"
            )
        )
    raw_path = Path(f"{prefix}_raw.csv")
    summary_path = Path(f"{prefix}_summary.csv")
    _write_csv(raw_path, rows)
    _write_csv(summary_path, summaries)
    print(f"wrote {len(rows)} raw rows to {raw_path}")
    print(f"wrote {len(summaries)} summaries to {summary_path}")
    for row in summaries:
        print(
            f"{row['mapping']}: ratio={float(row['mean_ratio_a_over_b']):.6f}, "
            f"ci95=[{float(row['ratio_ci95_low']):.6f}, "
            f"{float(row['ratio_ci95_high']):.6f}]"
        )
    print(f"elapsed_seconds={perf_counter() - started:.6f}")


if __name__ == "__main__":
    main()
