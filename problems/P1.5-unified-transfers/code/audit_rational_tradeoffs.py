"""Finite falsification checks for the P1.5 piecewise-rational constants.

This script is not a proof of the algebraic-geometric theorem. It exhausts
small cyclic subsets to catch sign, strict-inequality, and averaging mistakes
in the combinatorial reduction used by A010 and RATIONAL_TRANSFER_REVIEW.md.
"""

from __future__ import annotations

import argparse
import itertools
import math


def is_prime(integer: int) -> bool:
    """Return whether the integer is prime."""
    if integer < 2:
        return False
    return all(integer % divisor for divisor in range(2, math.isqrt(integer) + 1))


def overlap_counts(r: int, subset: frozenset[int]) -> tuple[int, ...]:
    """Return R(t)=|{x in S: x+t in S}| for every t in Z/rZ."""
    if not is_prime(r):
        raise ValueError("r must be prime")
    if any(value < 0 or value >= r for value in subset):
        raise ValueError("subset entries must be canonical residues modulo r")
    return tuple(
        sum((value + shift) % r in subset for value in subset)
        for shift in range(r)
    )


def verify_overlap_identity(r: int, subset: frozenset[int]) -> None:
    """Raise unless the exact ordered-difference identities hold."""
    counts = overlap_counts(r, subset)
    size = len(subset)
    if counts[0] != size:
        raise AssertionError("R(0) must equal |S|")
    if sum(counts) != size * size:
        raise AssertionError("sum_t R(t) must equal |S|^2")
    if sum(counts[1:]) != size * (size - 1):
        raise AssertionError("sum_{t != 0} R(t) must equal |S|(|S|-1)")


def minimum_peak_overlap(r: int, size: int) -> int:
    """Exhaust the least possible max_{t != 0} R(t) at fixed subset size."""
    if size < 1 or size > r:
        raise ValueError("size must lie between 1 and r")
    minimum = r
    for values in itertools.combinations(range(r), size):
        subset = frozenset(values)
        verify_overlap_identity(r, subset)
        minimum = min(minimum, max(overlap_counts(r, subset)[1:], default=0))
    return minimum


def certify_coarse_constant(r: int, branch_count: int, pole_degree: int) -> None:
    """Check the integer implication used to derive D_+ B^2 >= r/4."""
    if not is_prime(r):
        raise ValueError("r must be prime")
    if branch_count < 1 or branch_count > r:
        raise ValueError("branch_count must lie between 1 and r")
    if pole_degree < 0:
        raise ValueError("pole_degree must be nonnegative")
    if max(1, pole_degree) * branch_count**2 >= r / 4:
        return
    minimum_branch_size = (r + branch_count - 1) // branch_count
    if minimum_branch_size * (minimum_branch_size - 1) <= 2 * pole_degree * (r - 1):
        raise AssertionError(
            "the claimed coarse tradeoff does not follow from the exact overlap bound"
        )


def run_audit(primes: tuple[int, ...]) -> list[dict[str, object]]:
    """Exhaust subset profiles and every relevant small integer constant."""
    rows: list[dict[str, object]] = []
    for r in primes:
        if not is_prime(r):
            raise ValueError(f"{r} is not prime")
        for branch_count in range(1, r + 1):
            for pole_degree in range(r + 1):
                certify_coarse_constant(r, branch_count, pole_degree)
        profile = tuple(
            minimum_peak_overlap(r, size)
            for size in range(1, r + 1)
        )
        rows.append({"r": r, "minimum_peak_profile": profile})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--primes",
        type=int,
        nargs="+",
        default=(2, 3, 5, 7, 11, 13),
    )
    args = parser.parse_args()
    rows = run_audit(tuple(args.primes))
    for row in rows:
        print(
            f"r={row['r']:>2} "
            f"min_max_nonzero_overlap={row['minimum_peak_profile']}"
        )


if __name__ == "__main__":
    main()

