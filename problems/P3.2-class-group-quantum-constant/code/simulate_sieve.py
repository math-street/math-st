"""
simulate_sieve.py — simulate fixed-batch Kuperberg-style sieve counters.
Sub-goal: P3.2 / SG-02
Inputs:   --bits <csv> --trials <int> --seed <int> --block-width-scale <float>
Outputs:  data/simulate_sieve_n<MIN>-<MAX>_seed<SEED>_<YYYYMMDD>.csv
Runtime:  about 2 seconds for seven sizes and 100 trials in the recorded environment
Validated against: exact occupancy-pair counts and seeded reproducibility tests
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

import numpy as np


@dataclass(frozen=True, slots=True)
class SieveTrial:
    """One abstract sieve-counter observation."""

    seed: int
    trial: int
    n_bits: int
    log_natural_N: float
    block_width: int
    block_width_scale: float
    stages: int
    list_size: int
    list_multiplier: int
    combination_success_probability: float
    target_probability: float
    query_count: float
    combination_attempts: float
    successful_combinations: float
    final_candidate_states: float


def stage_widths(n_bits: int, block_width: int) -> tuple[int, ...]:
    """Partition the lowest n-1 label bits into sieve stages."""
    if n_bits < 3:
        raise ValueError("n_bits must be at least 3")
    if block_width < 1:
        raise ValueError("block_width must be positive")
    remaining = n_bits - 1
    widths = []
    while remaining:
        width = min(block_width, remaining)
        widths.append(width)
        remaining -= width
    return tuple(widths)


def occupancy_pairs(counts: np.ndarray) -> int:
    """Return the exact number of disjoint same-bucket pairs."""
    if counts.ndim != 1 or np.any(counts < 0):
        raise ValueError("counts must be a one-dimensional nonnegative array")
    return int(np.sum(counts // 2))


def simulate_trial(
    n_bits: int,
    list_multiplier: int,
    block_width_scale: float,
    combination_success_probability: float,
    target_probability: float,
    rng: np.random.Generator,
    *,
    seed: int,
    trial: int,
) -> SieveTrial:
    """Simulate occupancy losses and back-propagate the abstract work."""
    if list_multiplier < 1:
        raise ValueError("list_multiplier must be positive")
    if block_width_scale <= 0:
        raise ValueError("block_width_scale must be positive")
    if not 0.0 < combination_success_probability <= 1.0:
        raise ValueError("combination success probability must be in (0, 1]")
    if not 0.0 < target_probability <= 1.0:
        raise ValueError("target probability must be in (0, 1]")

    block_width = max(1, round(block_width_scale * math.sqrt(n_bits - 1)))
    widths = stage_widths(n_bits, block_width)
    list_size = list_multiplier * (1 << block_width)
    pair_rates: list[float] = []
    success_rates: list[float] = []

    for width in widths:
        bucket_count = 1 << width
        probabilities = np.full(bucket_count, 1.0 / bucket_count)
        counts = rng.multinomial(list_size, probabilities)
        pairs = occupancy_pairs(counts)
        successes = int(rng.binomial(pairs, combination_success_probability))
        if successes == 0:
            raise ArithmeticError("a sieve stage produced no successful combinations")
        pair_rates.append(pairs / list_size)
        success_rates.append(successes / list_size)

    useful_targets = int(rng.binomial(list_size, target_probability))
    if useful_targets == 0:
        raise ArithmeticError("the final batch contained no useful target labels")
    target_rate = useful_targets / list_size

    required_output = list_size / target_rate
    final_candidate_states = required_output
    combination_attempts = 0.0
    successful_combinations = 0.0
    for pair_rate, success_rate in reversed(tuple(zip(pair_rates, success_rates))):
        required_input = required_output / success_rate
        combination_attempts += required_input * pair_rate
        successful_combinations += required_output
        required_output = required_input

    return SieveTrial(
        seed=seed,
        trial=trial,
        n_bits=n_bits,
        log_natural_N=n_bits * math.log(2.0),
        block_width=block_width,
        block_width_scale=block_width_scale,
        stages=len(widths),
        list_size=list_size,
        list_multiplier=list_multiplier,
        combination_success_probability=combination_success_probability,
        target_probability=target_probability,
        query_count=required_output,
        combination_attempts=combination_attempts,
        successful_combinations=successful_combinations,
        final_candidate_states=final_candidate_states,
    )


def simulate(
    bits: tuple[int, ...],
    trials: int,
    seed: int,
    list_multiplier: int = 8,
    block_width_scale: float = math.sqrt(2.0),
    combination_success_probability: float = 0.5,
    target_probability: float = 0.5,
) -> list[SieveTrial]:
    """Run a deterministic seeded grid of abstract sieve trials."""
    if len(bits) < 1 or trials < 1:
        raise ValueError("at least one size and one trial are required")
    rng = np.random.default_rng(seed)
    return [
        simulate_trial(
            n_bits,
            list_multiplier,
            block_width_scale,
            combination_success_probability,
            target_probability,
            rng,
            seed=seed,
            trial=trial,
        )
        for n_bits in bits
        for trial in range(trials)
    ]


def parse_bits(value: str) -> tuple[int, ...]:
    bits = tuple(int(part) for part in value.split(",") if part)
    if not bits or any(n_bits < 3 for n_bits in bits):
        raise argparse.ArgumentTypeError("bits must be comma-separated integers of at least 3")
    return bits


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=parse_bits, default=(24, 32, 40, 48, 56, 64, 72))
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260722)
    parser.add_argument("--list-multiplier", type=int, default=8)
    parser.add_argument("--block-width-scale", type=float, default=math.sqrt(2.0))
    parser.add_argument("--combination-success-probability", type=float, default=0.5)
    parser.add_argument("--target-probability", type=float, default=0.5)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    bits = (12, 16) if args.smoke else args.bits
    trials = 2 if args.smoke else args.trials
    rows = simulate(
        bits,
        trials,
        args.seed,
        args.list_multiplier,
        args.block_width_scale,
        args.combination_success_probability,
        args.target_probability,
    )
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"simulate_sieve_n{min(bits)}-{max(bits)}_seed{args.seed}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    print(f"rows={len(rows)} sizes={len(bits)} seed={args.seed}")
    print(output)


if __name__ == "__main__":
    main()
