"""Exhaustively search small q for redundant quadratic Semaev field equations.

The fast filter counts F_q-rational core zeros.  The universal core quotient
has dimension eight, so redundancy requires eight distinct rational zeros.
For prime q, every surviving candidate is then checked by exact Groebner
normal forms.  A dedicated table implementation covers the smallest
non-prime odd prime power q=9.

Sub-goal: P1.3 / SG-11
Inputs: --q values from 5, 7, 9
Outputs: data/search_quadratic_redundancy_<date>.json unless overridden
Runtime: about 70 seconds for q=5,7,9 on Python 3.13.4
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import date
from pathlib import Path

from measure_quadratic_variants import analyze_core
from sparse_weil import FiniteField, curve_is_nonsingular, find_irreducible_modulus


def scan_prime(q: int) -> dict[str, object]:
    field = FiniteField(q, find_irreducible_modulus(q, 2))
    elements = list(field.elements())
    base = [field.element(value) for value in range(q)]
    squares = {field.mul(value, value) for value in elements}
    two = field.element(2)
    four = field.element(4)
    checked = 0
    eligible = 0
    histogram: Counter[int] = Counter()
    candidates: list[dict[str, object]] = []
    started = time.perf_counter()
    for curve_a in elements:
        for curve_b in elements:
            if not curve_is_nonsingular(field, curve_a, curve_b):
                continue
            for target in elements:
                if target[1] == 0:
                    continue
                checked += 1
                target_squared = field.mul(target, target)
                target_rhs = field.add(
                    field.add(
                        field.mul(target_squared, target),
                        field.mul(curve_a, target),
                    ),
                    curve_b,
                )
                if target_rhs not in squares:
                    continue
                eligible += 1
                zeros: list[tuple[int, int]] = []
                for value_x, point_x in enumerate(base):
                    for value_y, point_y in enumerate(base):
                        difference = field.sub(point_x, point_y)
                        total = field.add(point_x, point_y)
                        product = field.mul(point_x, point_y)
                        semaev = field.mul(
                            field.mul(difference, difference), target_squared
                        )
                        bracket = field.add(
                            field.mul(total, field.add(product, curve_a)),
                            field.mul(two, curve_b),
                        )
                        semaev = field.sub(
                            semaev, field.mul(two, field.mul(bracket, target))
                        )
                        shifted_product = field.sub(product, curve_a)
                        semaev = field.add(
                            semaev, field.mul(shifted_product, shifted_product)
                        )
                        semaev = field.sub(
                            semaev, field.mul(four, field.mul(curve_b, total))
                        )
                        if semaev == field.zero:
                            zeros.append((value_x, value_y))
                histogram[len(zeros)] += 1
                if len(zeros) == 8:
                    analysis = analyze_core(q, curve_a, curve_b, target)
                    assert analysis["core_field_equations_redundant"] is True
                    candidates.append(
                        {
                            "curve_a": list(curve_a),
                            "curve_b": list(curve_b),
                            "target_x": list(target),
                            "rational_zeros": [list(point) for point in zeros],
                            "field_equation_normal_forms": analysis[
                                "core_field_equation_remainders"
                            ],
                        }
                    )
    return {
        "q": q,
        "base_field_model": f"prime field F_{q}",
        "quadratic_modulus": list(field.modulus),
        "candidates_checked": checked,
        "eligible_on_curve_targets": eligible,
        "rational_core_zero_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "redundant_cases": len(candidates),
        "candidates": candidates,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "verification": "eight-zero filter plus exact Groebner normal forms",
    }


def _q9_tables() -> tuple[
    list[list[int]], list[list[int]], list[int], list[list[int]], list[list[int]], list[int], int
]:
    # F_9 = F_3[v]/(v^2+1), encoded by a+3b.  Its quadratic extension
    # is F_9[u]/(u^2-D), encoded by a+9b, with D the first nonsquare.
    base_order = 9

    def base_pair(value: int) -> tuple[int, int]:
        return value % 3, value // 3

    def base_id(first: int, second: int) -> int:
        return first % 3 + 3 * (second % 3)

    base_add = [[0] * base_order for _ in range(base_order)]
    base_mul = [[0] * base_order for _ in range(base_order)]
    base_neg = [0] * base_order
    for left in range(base_order):
        a, b = base_pair(left)
        base_neg[left] = base_id(-a, -b)
        for right in range(base_order):
            c, d = base_pair(right)
            base_add[left][right] = base_id(a + c, b + d)
            base_mul[left][right] = base_id(a * c - b * d, a * d + b * c)
    base_squares = {base_mul[value][value] for value in range(base_order)}
    nonsquare = next(value for value in range(1, base_order) if value not in base_squares)

    extension_order = 81

    def extension_pair(value: int) -> tuple[int, int]:
        return value % base_order, value // base_order

    def extension_id(first: int, second: int) -> int:
        return first + base_order * second

    extension_add = [[0] * extension_order for _ in range(extension_order)]
    extension_mul = [[0] * extension_order for _ in range(extension_order)]
    extension_neg = [0] * extension_order
    for left in range(extension_order):
        a, b = extension_pair(left)
        extension_neg[left] = extension_id(base_neg[a], base_neg[b])
        for right in range(extension_order):
            c, d = extension_pair(right)
            extension_add[left][right] = extension_id(
                base_add[a][c], base_add[b][d]
            )
            extension_mul[left][right] = extension_id(
                base_add[base_mul[a][c]][base_mul[nonsquare][base_mul[b][d]]],
                base_add[base_mul[a][d]][base_mul[b][c]],
            )
    return (
        base_add,
        base_mul,
        base_neg,
        extension_add,
        extension_mul,
        extension_neg,
        nonsquare,
    )


def scan_q9() -> dict[str, object]:
    (
        _,
        _,
        _,
        add,
        multiply,
        negate,
        nonsquare,
    ) = _q9_tables()
    q = 9
    extension_order = 81
    base = [value for value in range(q)]
    nonbase = [value for value in range(extension_order) if value // q != 0]
    squares = {multiply[value][value] for value in range(extension_order)}
    subtract = lambda left, right: add[left][negate[right]]
    two = 2
    four = 1  # characteristic 3
    checked = 0
    eligible = 0
    histogram: Counter[int] = Counter()
    candidates: list[dict[str, int]] = []
    started = time.perf_counter()
    for curve_a in range(extension_order):
        curve_a_cubed = multiply[multiply[curve_a][curve_a]][curve_a]
        for curve_b in range(extension_order):
            # 4*A^3+27*B^2 = A^3 in characteristic three.
            if curve_a_cubed == 0:
                continue
            for target in nonbase:
                checked += 1
                target_squared = multiply[target][target]
                target_rhs = add[add[multiply[target_squared][target]][multiply[curve_a][target]]][
                    curve_b
                ]
                if target_rhs not in squares:
                    continue
                eligible += 1
                zero_count = 0
                for point_x in base:
                    for point_y in base:
                        difference = subtract(point_x, point_y)
                        total = add[point_x][point_y]
                        product = multiply[point_x][point_y]
                        semaev = multiply[multiply[difference][difference]][target_squared]
                        bracket = add[multiply[total][add[product][curve_a]]][multiply[two][curve_b]]
                        semaev = subtract(
                            semaev, multiply[two][multiply[bracket][target]]
                        )
                        shifted = subtract(product, curve_a)
                        semaev = add[semaev][multiply[shifted][shifted]]
                        semaev = subtract(
                            semaev, multiply[four][multiply[curve_b][total]]
                        )
                        zero_count += semaev == 0
                histogram[zero_count] += 1
                if zero_count == 8:
                    candidates.append(
                        {"curve_a_id": curve_a, "curve_b_id": curve_b, "target_x_id": target}
                    )
    assert not candidates
    return {
        "q": q,
        "base_field_model": "F_3[v]/(v^2+1)",
        "quadratic_extension_nonsquare_id": nonsquare,
        "candidates_checked": checked,
        "eligible_on_curve_targets": eligible,
        "rational_core_zero_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "redundant_cases": 0,
        "candidates": candidates,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "verification": "exhaustive eight-zero necessary-condition filter",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", nargs="+", type=int, default=[5, 7, 9])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    unsupported = set(args.q) - {5, 7, 9}
    if unsupported:
        raise ValueError(f"supported exhaustive values are 5, 7, and 9, got {unsupported}")
    rows = [scan_q9() if q == 9 else scan_prime(q) for q in args.q]
    result = {
        "status": "exhaustive small-field search complete",
        "scope": "all nonsingular short-Weierstrass curves and nonbase on-curve target x-coordinates",
        "results": rows,
    }
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"search_quadratic_redundancy_{date.today():%Y%m%d}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"wrote search result to {output}")


if __name__ == "__main__":
    main()
