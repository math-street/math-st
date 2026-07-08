"""
search_three_cycles_targeted.py - complete hit-focused directed 3-cycle search.
Sub-goal: P4.2 / SG-05 extension
Inputs:   --limit <exclusive prime bound> --max-degree <int> [--smoke]
Outputs:  data/search_three_cycles_targeted_<params>_<date>_{candidates.csv,summary.json}
Runtime:  recorded in the summary; designed for bounds beyond 2^18
Validated against: exhaustive candidate ledgers at 2^16 and 2^18
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import date
from pathlib import Path
from time import perf_counter

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_three_cycles import (  # noqa: E402
    ThreeCycleCandidateRow,
    ThreeCycleSearchResult,
    write_result,
)
from search_two_cycles import (  # noqa: E402
    degree_label,
    fundamental_discriminant_and_conductor,
    multiplicative_order_up_to,
    primes_below,
    smallest_prime_factors,
)

PROBLEM_ROOT = Path(__file__).resolve().parents[1]


def canonical_rotation(
    fields: tuple[int, int, int],
    degrees: tuple[int | None, int | None, int | None],
) -> tuple[tuple[int, int, int], tuple[int | None, int | None, int | None]]:
    """Rotate a directed triple so its unique smallest field is first."""

    start = fields.index(min(fields))
    rotated_fields = fields[start:] + fields[:start]
    rotated_degrees = degrees[start:] + degrees[:start]
    return rotated_fields, rotated_degrees


def primitive_order_residues(prime: int, order: int) -> tuple[int, ...]:
    """Return every residue of exact multiplicative order modulo prime."""

    if order < 2 or (prime - 1) % order:
        return ()
    order_prime_divisors = [
        divisor
        for divisor in range(2, order + 1)
        if order % divisor == 0
        and all(divisor % trial for trial in range(2, math.isqrt(divisor) + 1))
    ]
    generator = None
    for base in range(2, prime):
        candidate = pow(base, (prime - 1) // order, prime)
        if candidate == 1:
            continue
        if all(
            pow(candidate, order // divisor, prime) != 1
            for divisor in order_prime_divisors
        ):
            generator = candidate
            break
    if generator is None:
        raise ArithmeticError(
            f"failed to find an element of order {order} modulo {prime}"
        )
    return tuple(
        sorted(
            {
                pow(generator, exponent, prime)
                for exponent in range(1, order + 1)
                if math.gcd(exponent, order) == 1
            }
        )
    )


def root_generated_target_graph(
    primes: list[int],
    max_degree: int,
) -> dict[int, list[tuple[int, int]]]:
    """Generate every target-degree Hasse edge from exact-order residues."""

    prime_set = set(primes)
    target_graph_sets: dict[int, set[tuple[int, int]]] = defaultdict(set)
    for order_prime in primes:
        for degree in range(3, max_degree + 1):
            for residue in primitive_order_residues(order_prime, degree):
                for field_prime in (residue, order_prime + residue):
                    if (
                        field_prime < 5
                        or field_prime not in prime_set
                        or field_prime == order_prime
                        or (field_prime + 1 - order_prime) ** 2 > 4 * field_prime
                    ):
                        continue
                    if multiplicative_order_up_to(
                        field_prime,
                        order_prime,
                        max_degree,
                    ) != degree:
                        raise AssertionError("generated residue has wrong exact order")
                    target_graph_sets[field_prime].add((order_prime, degree))
    return {
        field: sorted(edges)
        for field, edges in target_graph_sets.items()
    }


def search_three_cycles_targeted(
    *,
    limit: int,
    max_degree: int,
    edge_generator: str = "hasse_scan",
) -> ThreeCycleSearchResult:
    """Find every full hit and two-of-three near-miss without all triangles."""

    if limit <= 11:
        raise ValueError("limit must exceed 11")
    if not 3 <= max_degree <= 100:
        raise ValueError("max_degree must be in [3, 100]")
    if edge_generator not in {"hasse_scan", "cyclotomic_roots"}:
        raise ValueError("unknown edge generator")

    started = perf_counter()
    primes = [prime for prime in primes_below(limit) if prime >= 5]
    target_degrees = set(range(3, max_degree + 1))
    directed_hasse_edge_count: int | None
    if edge_generator == "cyclotomic_roots":
        target_graph = root_generated_target_graph(primes, max_degree)
        directed_hasse_edge_count = None
    else:
        target_graph = defaultdict(list)
        directed_hasse_edge_count = 0
        for field in primes:
            radius = math.isqrt(4 * field)
            start = bisect_left(primes, field + 1 - radius)
            stop = bisect_right(primes, field + 1 + radius)
            for order in primes[start:stop]:
                if order == field or (field + 1 - order) ** 2 > 4 * field:
                    continue
                directed_hasse_edge_count += 1
                degree = multiplicative_order_up_to(field, order, max_degree)
                if degree in target_degrees:
                    assert degree is not None
                    target_graph[field].append((order, degree))

    factor_table = smallest_prime_factors(4 * (limit - 1))
    candidate_data: dict[
        tuple[int, int, int],
        tuple[int | None, int | None, int | None],
    ] = {}

    for p1, first_edges in target_graph.items():
        for p2, k1 in first_edges:
            for p3, k2 in target_graph.get(p2, []):
                if p3 in (p1, p2) or (p3 + 1 - p1) ** 2 > 4 * p3:
                    continue
                k3 = multiplicative_order_up_to(p3, p1, max_degree)
                fields, degrees = canonical_rotation((p1, p2, p3), (k1, k2, k3))
                previous = candidate_data.get(fields)
                if previous is not None and previous != degrees:
                    raise ArithmeticError("inconsistent degree data for a directed cycle")
                candidate_data[fields] = degrees

    candidates: list[ThreeCycleCandidateRow] = []
    hit_degree_triples: Counter[tuple[int, int, int]] = Counter()
    for fields in sorted(candidate_data):
        degrees = candidate_data[fields]
        target_flags = tuple(degree in target_degrees for degree in degrees)
        target_count = sum(target_flags)
        if target_count < 2:
            raise ArithmeticError("targeted join produced fewer than two target edges")
        traces = tuple(
            fields[index] + 1 - fields[(index + 1) % 3]
            for index in range(3)
        )
        if sum(traces) != 3:
            raise ArithmeticError("3-cycle traces do not sum to 3")
        discriminant_data = [
            fundamental_discriminant_and_conductor(
                4 * field - trace * trace,
                factor_table,
            )
            for field, trace in zip(fields, traces)
        ]

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
            rejecting_condition = f"k{failed_position}_not_in_3_{max_degree}"

        rho_values = tuple(
            math.log(fields[index]) / math.log(fields[(index + 1) % 3])
            for index in range(3)
        )
        candidates.append(
            ThreeCycleCandidateRow(
                field_prime_e1=fields[0],
                field_prime_e2=fields[1],
                field_prime_e3=fields[2],
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
        "algorithm": (
            "cyclotomic-root target-edge join"
            if edge_generator == "cyclotomic_roots"
            else "target-edge join"
        ),
        "date": f"{date.today():%Y-%m-%d}",
        "limit_exclusive": limit,
        "minimum_prime": 5,
        "target_embedding_degrees": [3, max_degree],
        "prime_count": len(primes),
        "directed_hasse_edge_count": directed_hasse_edge_count,
        "target_edge_count": sum(len(edges) for edges in target_graph.values()),
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1 << 20)
    parser.add_argument("--max-degree", type=int, default=12)
    parser.add_argument(
        "--edge-generator",
        choices=("hasse_scan", "cyclotomic_roots"),
        default="hasse_scan",
    )
    parser.add_argument("--output-prefix", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    limit = 128 if args.smoke and args.limit == 1 << 20 else args.limit
    result = search_three_cycles_targeted(
        limit=limit,
        max_degree=args.max_degree,
        edge_generator=args.edge_generator,
    )
    prefix = args.output_prefix or (
        PROBLEM_ROOT
        / "data"
        / (
            f"search_three_cycles_targeted_{args.edge_generator}_"
            f"p5-{limit - 1}_k3-{args.max_degree}_"
            f"{date.today():%Y%m%d}"
        )
    )
    candidates_path = Path(f"{prefix}_candidates.csv")
    summary_path = Path(f"{prefix}_summary.json")
    write_result(result, candidates_path, summary_path)
    print(
        f"edge_generator={args.edge_generator}; "
        f"checked {result.summary['directed_hasse_edge_count']} directed Hasse edges; "
        f"target_edges={result.summary['target_edge_count']}; "
        f"hits={result.summary['hit_count']}; "
        f"two-of-three={result.summary['two_of_three_near_miss_count']}"
    )
    print(f"wrote {candidates_path} and {summary_path}")


if __name__ == "__main__":
    main()
