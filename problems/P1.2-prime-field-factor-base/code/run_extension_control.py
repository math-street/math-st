"""
run_extension_control.py — SG-02 cubic-extension positive control.
Sub-goal: P1.2 / SG-02
Inputs:   --q <prime> --secret <int> --max-attempts <int> --seed <int>
Outputs:  data/run_extension_control_q<q>_s<seed>_<YYYYMMDD>_{summary,relations}.csv
Runtime:  under one second for the default q=5 control.
Validated against: planted DLP secret and exhaustive field/group checks in lib/tests.
"""

from __future__ import annotations

import argparse
import csv
import random
import statistics
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.extension_curves import (
    ExtensionCurve,
    ExtensionPoint,
    find_prime_order_extension_curve,
    subfield_x_factor_base,
)
from lib.finite_fields import ExtensionElement, cubic_field


@dataclass(slots=True)
class ControlResult:
    summary: dict[str, Any]
    relations: list[dict[str, Any]]


def first_pair_table(
    curve: ExtensionCurve, factor_base: Sequence[ExtensionPoint]
) -> dict[ExtensionPoint, tuple[ExtensionPoint, ExtensionPoint]]:
    table: dict[ExtensionPoint, tuple[ExtensionPoint, ExtensionPoint]] = {}
    for left in factor_base:
        for right in factor_base:
            table.setdefault(curve.add(left, right), (left, right))
    return table


def decompose_three(
    curve: ExtensionCurve,
    factor_base: Sequence[ExtensionPoint],
    pair_table: dict[ExtensionPoint, tuple[ExtensionPoint, ExtensionPoint]],
    target: ExtensionPoint,
) -> tuple[ExtensionPoint, ExtensionPoint, ExtensionPoint] | None:
    for third in factor_base:
        needed = curve.add(target, curve.neg(third))
        pair = pair_table.get(needed)
        if pair is not None:
            return pair[0], pair[1], third
    return None


def solve_full_rank(rows: Sequence[Sequence[int]], right_sides: Sequence[int], modulus: int) -> list[int] | None:
    """Solve an overdetermined linear system over F_modulus, or return None below full rank."""
    if not rows:
        return None
    columns = len(rows[0])
    matrix = [
        [entry % modulus for entry in row] + [right_side % modulus]
        for row, right_side in zip(rows, right_sides)
    ]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], modulus - 2, modulus)
        matrix[pivot_row] = [value * inverse % modulus for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % modulus
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    for row in matrix:
        if all(value == 0 for value in row[:-1]) and row[-1] != 0:
            raise ArithmeticError("relation system is inconsistent")
    if len(pivots) < columns:
        return None
    solution = [0] * columns
    for row, column in enumerate(pivots):
        solution[column] = matrix[row][-1]
    return solution


def _element_text(value: ExtensionElement) -> str:
    return ":".join(str(coefficient) for coefficient in value.coefficients)


def _point_text(point: ExtensionPoint) -> str:
    if point is None:
        return "O"
    return f"({_element_text(point[0])};{_element_text(point[1])})"


def run_control(q: int, secret: int, max_attempts: int, seed: int) -> ControlResult:
    started = time.perf_counter()
    field = cubic_field(q)
    rng = random.Random(seed)
    curve, points, curve_attempts = find_prime_order_extension_curve(field, rng)
    order = len(points)
    generator = next(point for point in points if point is not None)
    if curve.scalar_mul(order, generator) is not None:
        raise ArithmeticError("generator failed the prime-order check")
    secret %= order
    if secret == 0:
        secret = 1
    target_point = curve.scalar_mul(secret, generator)
    roots = curve.square_roots()
    factor_base = subfield_x_factor_base(curve, roots)
    if not factor_base:
        raise RuntimeError("subfield-x factor base is empty")
    if any(point is None or point[0] ** q != point[0] for point in factor_base):
        raise ArithmeticError("factor base failed Frobenius membership")
    base_index = {point: index for index, point in enumerate(factor_base)}
    if len(base_index) != len(factor_base):
        raise ArithmeticError("factor base contains duplicates")
    pair_table = first_pair_table(curve, factor_base)

    relation_rows: list[list[int]] = []
    right_sides: list[int] = []
    relation_records: list[dict[str, Any]] = []
    solution: list[int] | None = None
    decomposable_attempts = 0
    for attempt in range(1, max_attempts + 1):
        alpha = rng.randrange(order)
        beta = rng.randrange(order)
        relation_target = curve.add(
            curve.scalar_mul(alpha, generator), curve.scalar_mul(beta, target_point)
        )
        triple = decompose_three(curve, factor_base, pair_table, relation_target)
        if triple is None:
            continue
        decomposable_attempts += 1
        if curve.add(curve.add(triple[0], triple[1]), triple[2]) != relation_target:
            raise ArithmeticError("invalid extension-field decomposition")
        multiplicities = Counter(triple)
        row = [multiplicities.get(point, 0) % order for point in factor_base]
        row.append((-beta) % order)
        relation_rows.append(row)
        right_sides.append(alpha)
        relation_records.append(
            {
                "attempt": attempt,
                "alpha": alpha,
                "beta": beta,
                "target": _point_text(relation_target),
                "p1": _point_text(triple[0]),
                "p2": _point_text(triple[1]),
                "p3": _point_text(triple[2]),
                "row": ":".join(str(value) for value in row),
                "rhs": alpha,
            }
        )
        if len(relation_rows) >= len(factor_base) + 1:
            solution = solve_full_rank(relation_rows, right_sides, order)
            if solution is not None:
                break
    if solution is None:
        raise RuntimeError(f"relation system did not reach full rank in {max_attempts} attempts")
    recovered = solution[-1]
    if curve.scalar_mul(recovered, generator) != target_point:
        raise ArithmeticError("recovered logarithm does not reproduce the target")
    if recovered != secret:
        raise ArithmeticError("recovered logarithm differs from the planted secret")

    # Validate factor-base log variables only after solving; they were not used to construct rows.
    scalar_lookup = {curve.scalar_mul(scalar, generator): scalar for scalar in range(order)}
    actual_base_logs = [scalar_lookup[point] for point in factor_base]
    if solution[:-1] != actual_base_logs:
        raise ArithmeticError("solved factor-base logarithms failed exhaustive validation")
    attempts_used = relation_records[-1]["attempt"]
    summary = {
        "date": date.today().isoformat(),
        "seed": seed,
        "q": q,
        "extension_degree": field.degree,
        "field_order": field.order,
        "modulus": ":".join(str(value) for value in field.modulus),
        "curve_a": _element_text(curve.a),
        "curve_b": _element_text(curve.b),
        "curve_order": order,
        "curve_attempts": curve_attempts,
        "factor_base_size": len(factor_base),
        "factor_base": "|".join(_point_text(point) for point in factor_base),
        "expected_ordered_triples_per_target": f"{len(factor_base) ** 3 / order:.12g}",
        "pair_sum_targets": len(pair_table),
        "planted_secret": secret,
        "recovered_secret": recovered,
        "relations_used": len(relation_rows),
        "attempts_used": attempts_used,
        "decomposable_attempts": decomposable_attempts,
        "decomposition_success_rate": f"{decomposable_attempts / attempts_used:.12g}",
        "full_rank": 1,
        "elapsed_s": f"{time.perf_counter() - started:.9f}",
    }
    return ControlResult(summary, relation_records)


def write_result(result: ControlResult, prefix: Path) -> None:
    prefix.parent.mkdir(parents=True, exist_ok=True)
    summary_path = Path(f"{prefix}_summary.csv")
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.summary))
        writer.writeheader()
        writer.writerow(result.summary)
    relations_path = Path(f"{prefix}_relations.csv")
    with relations_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.relations[0]))
        writer.writeheader()
        writer.writerows(result.relations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--secret", type=int, default=37)
    parser.add_argument("--max-attempts", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=12022027)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-prefix", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    max_attempts = 1000 if args.smoke else args.max_attempts
    result = run_control(args.q, args.secret, max_attempts, args.seed)
    stamp = date.today().strftime("%Y%m%d")
    default_prefix = Path(__file__).resolve().parents[1] / "data" / (
        f"run_extension_control_q{args.q}_s{args.seed}_{stamp}"
    )
    prefix = args.output_prefix or default_prefix
    write_result(result, prefix)
    for key, value in result.summary.items():
        print(f"{key}={value}")
    print(f"output_prefix={prefix}")


if __name__ == "__main__":
    main()
