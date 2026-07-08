"""
search_two_cycles.py - exhaust the frozen toy prime-order 2-cycle space.
Sub-goal: P4.2 / SG-04
Inputs:   --limit <exclusive prime bound> --max-degree <int> [--smoke]
Outputs:  data/search_two_cycles_<params>_<date>_{candidates.csv,summary.json}
Runtime:  recorded in the summary; intended bound is limit=65536
Validated against: published MNT degree pairs (5,7,6,4) and (37,43,6,4)
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from bisect import bisect_right
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from time import perf_counter

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class CandidateRow:
    field_prime_e1: int
    field_prime_e2: int
    trace_e1: int
    trace_e2: int
    cm_fundamental_discriminant: int
    cm_conductor: int
    embedding_degree_e1: str
    embedding_degree_e2: str
    rho_max: str
    status: str
    first_rejecting_condition: str


@dataclass(frozen=True, slots=True)
class SearchResult:
    candidates: list[CandidateRow]
    summary: dict[str, object]


def primes_below(limit: int) -> list[int]:
    """Return all primes strictly below limit with an Eratosthenes sieve."""

    if limit <= 2:
        return []
    sieve = bytearray(b"\x01") * limit
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit - 1) + 1):
        if sieve[prime]:
            start = prime * prime
            count = (limit - 1 - start) // prime + 1
            sieve[start:limit:prime] = b"\x00" * count
    return [value for value in range(2, limit) if sieve[value]]


def smallest_prime_factors(limit: int) -> list[int]:
    """Return a smallest-prime-factor table for 0 through limit."""

    factors = list(range(limit + 1))
    if limit >= 1:
        factors[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if factors[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if factors[multiple] == multiple:
                factors[multiple] = prime
    return factors


def fundamental_discriminant_and_conductor(
    radicand: int,
    smallest_factors: list[int],
) -> tuple[int, int]:
    """Decompose -radicand as D_K*f^2 with D_K fundamental."""

    if radicand <= 0 or radicand >= len(smallest_factors):
        raise ValueError("radicand must be positive and covered by the factor table")
    remaining = radicand
    squarefree_part = 1
    while remaining > 1:
        prime = smallest_factors[remaining]
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent % 2:
            squarefree_part *= prime

    signed_squarefree_part = -squarefree_part
    fundamental = (
        signed_squarefree_part
        if signed_squarefree_part % 4 == 1
        else 4 * signed_squarefree_part
    )
    quotient = (-radicand) // fundamental
    conductor = math.isqrt(quotient)
    if fundamental * conductor * conductor != -radicand:
        raise ArithmeticError("invalid fundamental-discriminant decomposition")
    return fundamental, conductor


def multiplicative_order_up_to(base: int, modulus: int, maximum: int) -> int | None:
    """Return the exact order if at most maximum, otherwise None."""

    residue = 1
    for degree in range(1, maximum + 1):
        residue = residue * base % modulus
        if residue == 1:
            return degree
    return None


def degree_label(degree: int | None, maximum: int) -> str:
    return str(degree) if degree is not None else f">{maximum}"


def search_two_cycles(*, limit: int, max_degree: int) -> SearchResult:
    """Exhaust the space frozen in SEARCH_SPACE.md."""

    if limit <= 7:
        raise ValueError("limit must exceed 7")
    if not 3 <= max_degree <= 100:
        raise ValueError("max_degree must be in [3, 100]")

    started = perf_counter()
    primes = [prime for prime in primes_below(limit) if prime >= 5]
    smallest_factors = smallest_prime_factors(4 * (limit - 1))
    target_degrees = set(range(3, max_degree + 1))
    candidates: list[CandidateRow] = []
    hasse_valid_count = 0
    induced_discriminants: set[int] = set()
    hit_degree_pairs: Counter[tuple[int, int]] = Counter()
    non_mnt_degree_pattern_hits = 0

    for p_index, p in enumerate(primes):
        upper_q = min(limit - 1, p + 1 + math.isqrt(4 * p))
        stop = bisect_right(primes, upper_q, lo=p_index + 1)
        for q in primes[p_index + 1 : stop]:
            trace_e1 = p + 1 - q
            trace_e2 = q + 1 - p
            if trace_e1 * trace_e1 > 4 * p or trace_e2 * trace_e2 > 4 * q:
                continue
            hasse_valid_count += 1

            radicand_e1 = 4 * p - trace_e1 * trace_e1
            radicand_e2 = 4 * q - trace_e2 * trace_e2
            if radicand_e1 != radicand_e2:
                raise ArithmeticError("2-cycle CM-radicand identity failed")
            discriminant, conductor = fundamental_discriminant_and_conductor(
                radicand_e1,
                smallest_factors,
            )
            induced_discriminants.add(discriminant)

            degree_e1 = multiplicative_order_up_to(p, q, max_degree)
            degree_e2 = multiplicative_order_up_to(q, p, max_degree)
            e1_target = degree_e1 in target_degrees
            e2_target = degree_e2 in target_degrees
            if not (e1_target or e2_target):
                continue

            if e1_target and e2_target:
                status = "hit"
                rejecting_condition = "none"
                assert degree_e1 is not None and degree_e2 is not None
                hit_degree_pairs[(degree_e1, degree_e2)] += 1
                if (degree_e1, degree_e2) not in {(6, 4), (4, 6)}:
                    non_mnt_degree_pattern_hits += 1
            elif e1_target:
                status = "e1_only"
                rejecting_condition = f"k2_not_in_3_{max_degree}"
            else:
                status = "e2_only"
                rejecting_condition = f"k1_not_in_3_{max_degree}"

            candidates.append(
                CandidateRow(
                    field_prime_e1=p,
                    field_prime_e2=q,
                    trace_e1=trace_e1,
                    trace_e2=trace_e2,
                    cm_fundamental_discriminant=discriminant,
                    cm_conductor=conductor,
                    embedding_degree_e1=degree_label(degree_e1, max_degree),
                    embedding_degree_e2=degree_label(degree_e2, max_degree),
                    rho_max=f"{math.log(q) / math.log(p):.12f}",
                    status=status,
                    first_rejecting_condition=rejecting_condition,
                )
            )

    candidate_lookup = {
        (
            row.field_prime_e1,
            row.field_prime_e2,
            row.embedding_degree_e1,
            row.embedding_degree_e2,
        )
        for row in candidates
    }
    validations = {
        "5_7_6_4": (5, 7, "6", "4") in candidate_lookup,
        "37_43_6_4": (37, 43, "6", "4") in candidate_lookup,
    }
    if limit > 43 and max_degree >= 6 and not all(validations.values()):
        raise AssertionError("published MNT arithmetic validation pair was not recovered")

    hit_count = sum(hit_degree_pairs.values())
    summary: dict[str, object] = {
        "schema_version": 1,
        "date": f"{date.today():%Y-%m-%d}",
        "limit_exclusive": limit,
        "minimum_prime": 5,
        "target_embedding_degrees": [3, max_degree],
        "prime_count": len(primes),
        "unordered_prime_pair_count": len(primes) * (len(primes) - 1) // 2,
        "hasse_valid_pair_count": hasse_valid_count,
        "candidate_row_count": len(candidates),
        "hit_count": hit_count,
        "non_4_6_or_6_4_hit_count": non_mnt_degree_pattern_hits,
        "near_miss_count": len(candidates) - hit_count,
        "hit_degree_pair_counts": {
            f"{left},{right}": count
            for (left, right), count in sorted(hit_degree_pairs.items())
        },
        "induced_fundamental_discriminant_count": len(induced_discriminants),
        "minimum_fundamental_discriminant": min(induced_discriminants, default=None),
        "maximum_fundamental_discriminant": max(induced_discriminants, default=None),
        "published_pair_validations": validations,
        "runtime_seconds": round(perf_counter() - started, 6),
    }
    return SearchResult(candidates, summary)


def write_result(result: SearchResult, candidates_path: Path, summary_path: Path) -> None:
    """Write the candidate ledger and summary with stable schemas."""

    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(CandidateRow.__dataclass_fields__)
    with candidates_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in result.candidates)
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(result.summary, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1 << 16)
    parser.add_argument("--max-degree", type=int, default=12)
    parser.add_argument("--output-prefix", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    limit = 128 if args.smoke and args.limit == 1 << 16 else args.limit
    result = search_two_cycles(limit=limit, max_degree=args.max_degree)
    prefix = args.output_prefix or (
        PROBLEM_ROOT
        / "data"
        / (
            f"search_two_cycles_p5-{limit - 1}_k3-{args.max_degree}_"
            f"{date.today():%Y%m%d}"
        )
    )
    candidates_path = Path(f"{prefix}_candidates.csv")
    summary_path = Path(f"{prefix}_summary.json")
    write_result(result, candidates_path, summary_path)
    print(
        f"checked {result.summary['hasse_valid_pair_count']} Hasse-valid pairs; "
        f"hits={result.summary['hit_count']}; "
        "non-{(6,4),(4,6)} hits="
        f"{result.summary['non_4_6_or_6_4_hit_count']}"
    )
    print(f"wrote {candidates_path} and {summary_path}")


if __name__ == "__main__":
    main()
