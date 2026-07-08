"""
search_two_cycles_targeted.py - candidate-complete low-memory 2-cycle search.
Sub-goal: P4.2 / SG-04 extension
Inputs:   --limit <exclusive prime bound> --max-degree <int> [--smoke]
Outputs:  data/search_two_cycles_targeted_<params>_<date>_{candidates.csv,summary.json}
Runtime:  recorded in the summary; designed for bounds beyond 2^20
Validated against: exhaustive candidate ledgers at prior bounds
"""

from __future__ import annotations

import argparse
import math
import sys
from bisect import bisect_right
from collections import Counter
from datetime import date
from pathlib import Path
from time import perf_counter

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_two_cycles import (  # noqa: E402
    CandidateRow,
    SearchResult,
    degree_label,
    multiplicative_order_up_to,
    primes_below,
    write_result,
)
from search_three_cycles_targeted import root_generated_target_graph  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


def fundamental_discriminant_trial(
    radicand: int,
    factor_primes: list[int],
) -> tuple[int, int]:
    """Decompose -radicand as D_K*f^2 using trial division."""

    if radicand <= 0:
        raise ValueError("radicand must be positive")
    remaining = radicand
    squarefree_part = 1
    for prime in factor_primes:
        if prime * prime > remaining:
            break
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        if exponent % 2:
            squarefree_part *= prime
    if remaining > 1:
        squarefree_part *= remaining

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


def search_two_cycles_targeted(
    *,
    limit: int,
    max_degree: int,
    pair_generator: str = "hasse_scan",
) -> SearchResult:
    """Enumerate every full hit and one-sided near-miss at low memory cost."""

    if limit <= 7:
        raise ValueError("limit must exceed 7")
    if not 3 <= max_degree <= 100:
        raise ValueError("max_degree must be in [3, 100]")
    if pair_generator not in {"hasse_scan", "cyclotomic_roots"}:
        raise ValueError("unknown pair generator")

    started = perf_counter()
    primes = [prime for prime in primes_below(limit) if prime >= 5]
    factor_primes = primes_below(math.isqrt(4 * (limit - 1)) + 2)
    target_degrees = set(range(3, max_degree + 1))
    candidates: list[CandidateRow] = []
    hasse_valid_count: int | None = 0
    hit_degree_pairs: Counter[tuple[int, int]] = Counter()
    exceptional_hits = 0

    if pair_generator == "cyclotomic_roots":
        target_graph = root_generated_target_graph(primes, max_degree)
        pair_iterator = iter(
            sorted(
                {
                    (min(field, order), max(field, order))
                    for field, edges in target_graph.items()
                    for order, _degree in edges
                }
            )
        )
        hasse_valid_count = None
    else:
        def hasse_pairs():
            for p_index, p in enumerate(primes):
                upper_q = min(limit - 1, p + 1 + math.isqrt(4 * p))
                stop = bisect_right(primes, upper_q, lo=p_index + 1)
                for q in primes[p_index + 1 : stop]:
                    trace_e1 = p + 1 - q
                    trace_e2 = q + 1 - p
                    if (
                        trace_e1 * trace_e1 <= 4 * p
                        and trace_e2 * trace_e2 <= 4 * q
                    ):
                        yield p, q

        pair_iterator = hasse_pairs()

    for p, q in pair_iterator:
        trace_e1 = p + 1 - q
        trace_e2 = q + 1 - p
        if trace_e1 * trace_e1 > 4 * p or trace_e2 * trace_e2 > 4 * q:
            raise AssertionError("pair generator produced a non-Hasse pair")
        if hasse_valid_count is not None:
            hasse_valid_count += 1
        degree_e1 = multiplicative_order_up_to(p, q, max_degree)
        degree_e2 = multiplicative_order_up_to(q, p, max_degree)
        e1_target = degree_e1 in target_degrees
        e2_target = degree_e2 in target_degrees
        if not (e1_target or e2_target):
            continue

        radicand = 4 * p - trace_e1 * trace_e1
        if radicand != 4 * q - trace_e2 * trace_e2:
            raise ArithmeticError("2-cycle CM-radicand identity failed")
        discriminant, conductor = fundamental_discriminant_trial(
            radicand,
            factor_primes,
        )

        if e1_target and e2_target:
            status = "hit"
            rejecting_condition = "none"
            assert degree_e1 is not None and degree_e2 is not None
            hit_degree_pairs[(degree_e1, degree_e2)] += 1
            if (degree_e1, degree_e2) not in {(6, 4), (4, 6)}:
                exceptional_hits += 1
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

    hit_count = sum(hit_degree_pairs.values())
    summary: dict[str, object] = {
        "schema_version": 1,
        "algorithm": (
            "cyclotomic-root candidate-targeted"
            if pair_generator == "cyclotomic_roots"
            else "candidate-targeted"
        ),
        "date": f"{date.today():%Y-%m-%d}",
        "limit_exclusive": limit,
        "minimum_prime": 5,
        "target_embedding_degrees": [3, max_degree],
        "prime_count": len(primes),
        "unordered_prime_pair_count": len(primes) * (len(primes) - 1) // 2,
        "hasse_valid_pair_count": hasse_valid_count,
        "candidate_row_count": len(candidates),
        "hit_count": hit_count,
        "non_4_6_or_6_4_hit_count": exceptional_hits,
        "near_miss_count": len(candidates) - hit_count,
        "hit_degree_pair_counts": {
            f"{left},{right}": count
            for (left, right), count in sorted(hit_degree_pairs.items())
        },
        "runtime_seconds": round(perf_counter() - started, 6),
    }
    return SearchResult(candidates, summary)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1 << 22)
    parser.add_argument("--max-degree", type=int, default=12)
    parser.add_argument(
        "--pair-generator",
        choices=("hasse_scan", "cyclotomic_roots"),
        default="hasse_scan",
    )
    parser.add_argument("--output-prefix", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    limit = 128 if args.smoke and args.limit == 1 << 22 else args.limit
    result = search_two_cycles_targeted(
        limit=limit,
        max_degree=args.max_degree,
        pair_generator=args.pair_generator,
    )
    prefix = args.output_prefix or (
        PROBLEM_ROOT
        / "data"
        / (
            f"search_two_cycles_targeted_{args.pair_generator}_"
            f"p5-{limit - 1}_k3-{args.max_degree}_"
            f"{date.today():%Y%m%d}"
        )
    )
    candidates_path = Path(f"{prefix}_candidates.csv")
    summary_path = Path(f"{prefix}_summary.json")
    write_result(result, candidates_path, summary_path)
    print(
        f"pair_generator={args.pair_generator}; "
        f"checked {result.summary['hasse_valid_pair_count']} Hasse-valid pairs; "
        f"hits={result.summary['hit_count']}; "
        "non-{(6,4),(4,6)} hits="
        f"{result.summary['non_4_6_or_6_4_hit_count']}"
    )
    print(f"wrote {candidates_path} and {summary_path}")


if __name__ == "__main__":
    main()
