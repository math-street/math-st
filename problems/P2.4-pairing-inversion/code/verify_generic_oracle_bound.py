"""
verify_generic_oracle_bound.py -- audit the affine-collision core of A002.
Sub-goal: P2.4 / SG-09
Inputs:   --p <prime> --trials <int> --seed <int> [--smoke]
Outputs:  data/verify_generic_oracle_bound_<params>_<date>.csv
Runtime:  ~0.9 s for p=5,7,11, max_handles=4 on Python 3.13
Validated against: exact p=5 three-form fixture with three distinct roots
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import random
from datetime import date
from pathlib import Path
from statistics import fmean


AffineForm = tuple[int, int]


def collision_root(left: AffineForm, right: AffineForm, p: int) -> int | None:
    """Return c with left(c)=right(c), or None for distinct parallel forms."""
    left_alpha, left_beta = left
    right_alpha, right_beta = right
    if left == right:
        raise ValueError("collision_root expects distinct formal expressions")
    alpha_difference = (left_alpha - right_alpha) % p
    if alpha_difference == 0:
        return None
    return (right_beta - left_beta) * pow(alpha_difference, -1, p) % p


def informative_challenges(forms: tuple[AffineForm, ...], p: int) -> frozenset[int]:
    """Return every challenge causing equality of two distinct affine forms."""
    roots = {
        root
        for left, right in itertools.combinations(forms, 2)
        if (root := collision_root(left, right, p)) is not None
    }
    return frozenset(roots)


def known_fixture() -> tuple[AffineForm, ...]:
    """Give three F_5 forms whose pairwise collisions have distinct roots."""
    return (0, 0), (1, 0), (2, 1)


def audit_parameter(
    p: int,
    handles: int,
    trials: int,
    seed: int,
    exhaustive_limit: int = 300_000,
) -> dict[str, object]:
    """Exhaust or reproducibly sample distinct affine-form sets."""
    if p < 3 or any(p % divisor == 0 for divisor in range(2, math.isqrt(p) + 1)):
        raise ValueError("p must be prime")
    forms = tuple(itertools.product(range(p), repeat=2))
    if not 2 <= handles <= len(forms):
        raise ValueError("handles must be between 2 and p^2")
    combination_count = math.comb(len(forms), handles)
    exhaustive = combination_count <= exhaustive_limit
    if exhaustive:
        samples = itertools.combinations(forms, handles)
        sample_count = combination_count
    else:
        rng = random.Random(seed + 1_000_003 * p + handles)
        samples = (
            tuple(sorted(rng.sample(forms, handles)))
            for _ in range(trials)
        )
        sample_count = trials

    bad_sizes: list[int] = []
    violations = 0
    pair_bound = math.comb(handles, 2)
    for sample in samples:
        bad_size = len(informative_challenges(sample, p))
        bad_sizes.append(bad_size)
        violations += int(bad_size > pair_bound or bad_size > p)
    if violations:
        raise AssertionError("an affine set exceeded the collision union bound")
    return {
        "p": p,
        "handles_t": handles,
        "affine_form_count": len(forms),
        "all_subset_count": combination_count,
        "mode": "exhaustive" if exhaustive else "seeded_sample",
        "sets_checked": sample_count,
        "seed": seed,
        "pair_union_bound": pair_bound,
        "field_size_bound": p,
        "maximum_bad_challenges": max(bad_sizes),
        "mean_bad_challenges": round(fmean(bad_sizes), 9),
        "violations": violations,
    }


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    """Write deterministic audit rows."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, action="append", help="prime group order; may be repeated")
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=2404)
    parser.add_argument("--max-handles", type=int, default=4)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.trials <= 0:
        raise ValueError("trials must be positive")
    if args.max_handles < 2:
        raise ValueError("max_handles must be at least two")
    primes = args.p or [5, 7, 11]
    trials = args.trials
    max_handles = args.max_handles
    if args.smoke:
        primes = [5]
        trials = min(trials, 10)
        max_handles = min(max_handles, 3)
    if len(informative_challenges(known_fixture(), 5)) != 3:
        raise AssertionError("known tight three-form fixture failed")
    rows = [
        audit_parameter(p, handles, trials, args.seed)
        for p in primes
        for handles in range(2, max_handles + 1)
    ]
    parameter_label = "-".join(str(p) for p in primes)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"verify_generic_oracle_bound_p{parameter_label}_t{max_handles}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    print(output)


if __name__ == "__main__":
    main()
