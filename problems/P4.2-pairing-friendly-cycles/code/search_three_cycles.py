"""
search_three_cycles.py - exhaust the frozen directed prime-order 3-cycle space.
Sub-goal: P4.2 / SG-05
Inputs:   --limit <exclusive prime bound> --max-degree <int> [--smoke]
Outputs:  data/search_three_cycles_<params>_<date>_{candidates.csv,summary.json}
Runtime:  recorded in the summary; intended bound is limit=65536
Validated against: direct permutation enumeration below 50
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from bisect import bisect_left, bisect_right
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from time import perf_counter

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_two_cycles import (  # noqa: E402
    degree_label,
    fundamental_discriminant_and_conductor,
    multiplicative_order_up_to,
    primes_below,
    smallest_prime_factors,
)

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, slots=True)
class ThreeCycleCandidateRow:
    field_prime_e1: int
    field_prime_e2: int
    field_prime_e3: int
    trace_e1: int
    trace_e2: int
    trace_e3: int
    cm_discriminant_e1: int
    cm_conductor_e1: int
    cm_discriminant_e2: int
    cm_conductor_e2: int
    cm_discriminant_e3: int
    cm_conductor_e3: int
    embedding_degree_e1: str
    embedding_degree_e2: str
    embedding_degree_e3: str
    target_position_count: int
    rho_max: str
    status: str
    first_rejecting_condition: str


@dataclass(frozen=True, slots=True)
class ThreeCycleSearchResult:
    candidates: list[ThreeCycleCandidateRow]
    summary: dict[str, object]


def build_directed_hasse_graph(primes: list[int]) -> dict[int, list[int]]:
    """Map each field prime to distinct prime orders in its Hasse interval."""

    graph: dict[int, list[int]] = {}
    for p in primes:
        radius = math.isqrt(4 * p)
        lower = p + 1 - radius
        upper = p + 1 + radius
        start = bisect_left(primes, lower)
        stop = bisect_right(primes, upper)
        graph[p] = [
            q
            for q in primes[start:stop]
            if q != p and (p + 1 - q) ** 2 <= 4 * p
        ]
    return graph


def search_three_cycles(*, limit: int, max_degree: int) -> ThreeCycleSearchResult:
    """Enumerate directed Hasse triangles once up to cyclic rotation."""

    if limit <= 11:
        raise ValueError("limit must exceed 11")
    if not 3 <= max_degree <= 100:
        raise ValueError("max_degree must be in [3, 100]")

    started = perf_counter()
    primes = [prime for prime in primes_below(limit) if prime >= 5]
    graph = build_directed_hasse_graph(primes)
    neighbor_sets = {prime: set(neighbors) for prime, neighbors in graph.items()}
    edge_degrees = {
        (p, q): multiplicative_order_up_to(p, q, max_degree)
        for p, neighbors in graph.items()
        for q in neighbors
    }
    target_degrees = set(range(3, max_degree + 1))
    factor_table = smallest_prime_factors(4 * (limit - 1))
    candidates: list[ThreeCycleCandidateRow] = []
    directed_cycle_count = 0
    target_count_distribution: Counter[int] = Counter()
    hit_degree_triples: Counter[tuple[int, int, int]] = Counter()

    for p1 in primes:
        for p2 in graph[p1]:
            if p2 == p1:
                continue
            for p3 in graph[p2]:
                if p3 in (p1, p2) or p1 not in neighbor_sets[p3]:
                    continue
                if p1 != min(p1, p2, p3):
                    continue
                directed_cycle_count += 1
                degrees = (
                    edge_degrees[(p1, p2)],
                    edge_degrees[(p2, p3)],
                    edge_degrees[(p3, p1)],
                )
                target_flags = tuple(degree in target_degrees for degree in degrees)
                target_count = sum(target_flags)
                target_count_distribution[target_count] += 1
                if target_count < 2:
                    continue

                traces = (p1 + 1 - p2, p2 + 1 - p3, p3 + 1 - p1)
                if sum(traces) != 3:
                    raise ArithmeticError("3-cycle traces do not sum to 3")
                discriminant_data = []
                for field_prime, trace in zip((p1, p2, p3), traces):
                    radicand = 4 * field_prime - trace * trace
                    discriminant_data.append(
                        fundamental_discriminant_and_conductor(
                            radicand,
                            factor_table,
                        )
                    )

                if target_count == 3:
                    status = "hit"
                    rejecting_condition = "none"
                    assert all(degree is not None for degree in degrees)
                    hit_degree_triples[
                        (int(degrees[0]), int(degrees[1]), int(degrees[2]))
                    ] += 1
                else:
                    status = "two_of_three"
                    failed_position = target_flags.index(False) + 1
                    rejecting_condition = (
                        f"k{failed_position}_not_in_3_{max_degree}"
                    )

                rho_values = (
                    math.log(p1) / math.log(p2),
                    math.log(p2) / math.log(p3),
                    math.log(p3) / math.log(p1),
                )
                candidates.append(
                    ThreeCycleCandidateRow(
                        field_prime_e1=p1,
                        field_prime_e2=p2,
                        field_prime_e3=p3,
                        trace_e1=traces[0],
                        trace_e2=traces[1],
                        trace_e3=traces[2],
                        cm_discriminant_e1=discriminant_data[0][0],
                        cm_conductor_e1=discriminant_data[0][1],
                        cm_discriminant_e2=discriminant_data[1][0],
                        cm_conductor_e2=discriminant_data[1][1],
                        cm_discriminant_e3=discriminant_data[2][0],
                        cm_conductor_e3=discriminant_data[2][1],
                        embedding_degree_e1=degree_label(degrees[0], max_degree),
                        embedding_degree_e2=degree_label(degrees[1], max_degree),
                        embedding_degree_e3=degree_label(degrees[2], max_degree),
                        target_position_count=target_count,
                        rho_max=f"{max(rho_values):.12f}",
                        status=status,
                        first_rejecting_condition=rejecting_condition,
                    )
                )

    hit_count = sum(hit_degree_triples.values())
    summary: dict[str, object] = {
        "schema_version": 1,
        "date": f"{date.today():%Y-%m-%d}",
        "limit_exclusive": limit,
        "minimum_prime": 5,
        "target_embedding_degrees": [3, max_degree],
        "prime_count": len(primes),
        "directed_hasse_edge_count": sum(len(neighbors) for neighbors in graph.values()),
        "directed_three_cycle_count": directed_cycle_count,
        "target_position_count_distribution": {
            str(count): frequency
            for count, frequency in sorted(target_count_distribution.items())
        },
        "candidate_row_count": len(candidates),
        "two_of_three_near_miss_count": len(candidates) - hit_count,
        "hit_count": hit_count,
        "hit_degree_triple_counts": {
            f"{first},{second},{third}": count
            for (first, second, third), count in sorted(hit_degree_triples.items())
        },
        "runtime_seconds": round(perf_counter() - started, 6),
    }
    return ThreeCycleSearchResult(candidates, summary)


def write_result(
    result: ThreeCycleSearchResult,
    candidates_path: Path,
    summary_path: Path,
) -> None:
    candidates_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(ThreeCycleCandidateRow.__dataclass_fields__)
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
    result = search_three_cycles(limit=limit, max_degree=args.max_degree)
    prefix = args.output_prefix or (
        PROBLEM_ROOT
        / "data"
        / (
            f"search_three_cycles_p5-{limit - 1}_k3-{args.max_degree}_"
            f"{date.today():%Y%m%d}"
        )
    )
    candidates_path = Path(f"{prefix}_candidates.csv")
    summary_path = Path(f"{prefix}_summary.json")
    write_result(result, candidates_path, summary_path)
    print(
        f"checked {result.summary['directed_three_cycle_count']} directed 3-cycles; "
        f"hits={result.summary['hit_count']}; "
        f"two-of-three={result.summary['two_of_three_near_miss_count']}"
    )
    print(f"wrote {candidates_path} and {summary_path}")


if __name__ == "__main__":
    main()

