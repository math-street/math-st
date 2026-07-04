"""
measure_map_timing.py - Compare exceptional and ordinary toy-map timings.
Sub-goal: P5.4 / SG-06a
Inputs:   --p <prime> --samples <int> --batch <int> --seed <int> [--smoke]
Outputs:  data/measure_map_timing_<params>_<date>_{raw,summary}.csv
Runtime:  ~4 seconds at p=11, samples=240, batch=100
Validated against: timing groups from validate_rfc_maps.py exceptional predicates
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

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import (
    Curve,
    MontgomeryCurve,
    map_to_curve_elligator2,
    map_to_curve_simple_swu,
)
from validate_rfc_maps import ELLIGATOR2_CASES, SSWU_CASES


def percentile(values: list[float], probability: float) -> float:
    """Return a linearly interpolated percentile of a nonempty sample."""
    if not values:
        raise ValueError("percentile sample must be nonempty")
    if not 0 <= probability <= 1:
        raise ValueError("probability must be in [0, 1]")
    ordered = sorted(values)
    position = probability * (len(ordered) - 1)
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_mean_ratio(
    numerator: list[float],
    denominator: list[float],
    *,
    resamples: int,
    rng: Random,
) -> tuple[float, float, float]:
    """Return a mean ratio and percentile-bootstrap 95% interval."""
    if not numerator or not denominator:
        raise ValueError("bootstrap groups must be nonempty")
    if resamples < 1:
        raise ValueError("resamples must be positive")
    observed = statistics.fmean(numerator) / statistics.fmean(denominator)
    ratios = []
    for _ in range(resamples):
        sampled_numerator = [rng.choice(numerator) for _ in numerator]
        sampled_denominator = [rng.choice(denominator) for _ in denominator]
        ratios.append(
            statistics.fmean(sampled_numerator)
            / statistics.fmean(sampled_denominator)
        )
    return observed, percentile(ratios, 0.025), percentile(ratios, 0.975)


def bootstrap_paired_mean_ratio(
    numerator_by_round: list[float],
    denominator_by_round: list[float],
    *,
    resamples: int,
    rng: Random,
) -> tuple[float, float, float]:
    """Return a paired-round mean ratio and bootstrap 95% interval."""
    if not numerator_by_round or len(numerator_by_round) != len(denominator_by_round):
        raise ValueError("paired bootstrap groups must have equal nonzero length")
    if resamples < 1:
        raise ValueError("resamples must be positive")
    observed = statistics.fmean(numerator_by_round) / statistics.fmean(
        denominator_by_round
    )
    ratios = []
    population = range(len(numerator_by_round))
    for _ in range(resamples):
        indices = [rng.choice(population) for _ in population]
        ratios.append(
            statistics.fmean(numerator_by_round[index] for index in indices)
            / statistics.fmean(denominator_by_round[index] for index in indices)
        )
    return observed, percentile(ratios, 0.025), percentile(ratios, 0.975)


def _fixture_calls(p: int):
    if p not in SSWU_CASES or p not in ELLIGATOR2_CASES:
        raise ValueError(f"no preregistered timing fixture for p={p}")
    a, b, sswu_z = SSWU_CASES[p]
    sswu_curve = Curve(p, a, b)
    j, k, ell2_z = ELLIGATOR2_CASES[p]
    ell2_curve = MontgomeryCurve(p, j, k)

    def call_sswu(u: int) -> None:
        map_to_curve_simple_swu(sswu_curve, u, sswu_z)

    def call_ell2(u: int) -> None:
        map_to_curve_elligator2(ell2_curve, u, ell2_z)

    return (
        (
            "simple_swu",
            call_sswu,
            lambda u: (sswu_z * sswu_z * pow(u, 4, p) + sswu_z * u * u)
            % p
            == 0,
        ),
        (
            "elligator2",
            call_ell2,
            lambda u: ell2_z * u * u % p == p - 1,
        ),
    )


def measure_rows(
    *, p: int, samples: int, batch: int, seed: int
) -> list[dict[str, int | str | float]]:
    """Measure randomized input blocks and return raw timing rows."""
    if samples < 1 or batch < 1:
        raise ValueError("samples and batch must be positive")
    rng = Random(seed)
    fixtures = _fixture_calls(p)
    jobs = [
        (mapping, function, predicate, u)
        for mapping, function, predicate in fixtures
        for u in range(p)
    ]
    rows: list[dict[str, int | str | float]] = []

    for sample_index in range(samples):
        rng.shuffle(jobs)
        for mapping, function, predicate, u in jobs:
            started = perf_counter_ns()
            for _ in range(batch):
                function(u)
            elapsed = perf_counter_ns() - started
            rows.append(
                {
                    "mapping": mapping,
                    "p": p,
                    "u": u,
                    "exceptional": int(predicate(u)),
                    "sample": sample_index,
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
    """Summarize exceptional/ordinary timing ratios with bootstrap intervals."""
    rng = Random(seed ^ 0x9380)
    summaries: list[dict[str, int | str | float]] = []
    mappings = sorted({str(row["mapping"]) for row in rows})
    for mapping in mappings:
        mapping_rows = [row for row in rows if row["mapping"] == mapping]
        exceptional = [
            float(row["nanoseconds_per_call"])
            for row in mapping_rows
            if row["exceptional"] == 1
        ]
        ordinary = [
            float(row["nanoseconds_per_call"])
            for row in mapping_rows
            if row["exceptional"] == 0
        ]
        if not exceptional or not ordinary:
            raise ValueError(
                f"mapping {mapping} must have both timing classes in the fixture"
            )
        samples = sorted({int(row["sample"]) for row in mapping_rows})
        exceptional_by_round = [
            statistics.fmean(
                float(row["nanoseconds_per_call"])
                for row in mapping_rows
                if int(row["sample"]) == sample and row["exceptional"] == 1
            )
            for sample in samples
        ]
        ordinary_by_round = [
            statistics.fmean(
                float(row["nanoseconds_per_call"])
                for row in mapping_rows
                if int(row["sample"]) == sample and row["exceptional"] == 0
            )
            for sample in samples
        ]
        ratio, low, high = bootstrap_paired_mean_ratio(
            exceptional_by_round,
            ordinary_by_round,
            resamples=bootstrap_resamples,
            rng=rng,
        )
        summaries.append(
            {
                "mapping": mapping,
                "p": int(mapping_rows[0]["p"]),
                "seed": seed,
                "timing_rounds": len(samples),
                "exceptional_observations": len(exceptional),
                "ordinary_observations": len(ordinary),
                "exceptional_mean_ns": statistics.fmean(exceptional),
                "ordinary_mean_ns": statistics.fmean(ordinary),
                "exceptional_median_ns": statistics.median(exceptional),
                "ordinary_median_ns": statistics.median(ordinary),
                "exceptional_stdev_ns": statistics.stdev(exceptional),
                "ordinary_stdev_ns": statistics.stdev(ordinary),
                "mean_ratio_exceptional_over_ordinary": ratio,
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
    parser.add_argument("--p", type=int, default=11)
    parser.add_argument("--samples", type=int, default=240)
    parser.add_argument("--batch", type=int, default=100)
    parser.add_argument("--seed", type=int, default=5402)
    parser.add_argument("--bootstrap", type=int, default=2_000)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-prefix", type=Path)
    args = parser.parse_args()
    overall_started = perf_counter()
    samples = 10 if args.smoke else args.samples
    batch = 10 if args.smoke else args.batch
    bootstrap_resamples = 100 if args.smoke else args.bootstrap

    rows = measure_rows(p=args.p, samples=samples, batch=batch, seed=args.seed)
    summaries = summarize_rows(
        rows,
        bootstrap_resamples=bootstrap_resamples,
        seed=args.seed,
    )
    prefix = args.output_prefix
    if prefix is None:
        prefix = (
            Path(__file__).resolve().parents[1]
            / "data"
            / (
                f"measure_map_timing_p{args.p}_s{samples}_b{batch}_"
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
            f"{row['mapping']}: ratio="
            f"{float(row['mean_ratio_exceptional_over_ordinary']):.6f}, "
            f"ci95=[{float(row['ratio_ci95_low']):.6f}, "
            f"{float(row['ratio_ci95_high']):.6f}]"
        )
    print(f"elapsed_seconds={perf_counter() - overall_started:.6f}")


if __name__ == "__main__":
    main()
