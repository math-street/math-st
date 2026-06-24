"""
analyze_miller_function.py — expand a fixed-P Miller function in F_p[x,y]/(E).
Sub-goal: P2.4 / SG-03
Inputs:   --p <prime> --trials <int> --seed <int> --orders <odd integers> [--smoke]
Outputs:  data/analyze_miller_function_<params>_<date>.csv
Runtime:  <1 s for p=43, r=11 and the default degree-growth sequence
Validated against: lib.pairing.miller_loop at every nonidentity point of G2
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import TypeAlias

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve  # noqa: E402
from lib.extension_curves import ExtensionCurve  # noqa: E402
from lib.finite_fields import ExtensionElement, ExtensionField  # noqa: E402
from lib.pairing import j1728_distortion_map, lift_base_point, miller_loop  # noqa: E402


Polynomial: TypeAlias = tuple[int, ...]
CoordinateElement: TypeAlias = tuple[Polynomial, Polynomial]
FactorCounts: TypeAlias = Counter[CoordinateElement]


def trim(values: list[int], p: int) -> Polynomial:
    normalized = [value % p for value in values]
    while len(normalized) > 1 and normalized[-1] == 0:
        normalized.pop()
    return tuple(normalized or [0])


def poly_add(left: Polynomial, right: Polynomial, p: int) -> Polynomial:
    length = max(len(left), len(right))
    values = [0] * length
    for index in range(length):
        values[index] = (left[index] if index < len(left) else 0) + (
            right[index] if index < len(right) else 0
        )
    return trim(values, p)


def poly_mul(left: Polynomial, right: Polynomial, p: int) -> Polynomial:
    values = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            values[left_index + right_index] += left_value * right_value
    return trim(values, p)


def coordinate_mul(
    left: CoordinateElement,
    right: CoordinateElement,
    curve_polynomial: Polynomial,
    p: int,
) -> CoordinateElement:
    left_a, left_b = left
    right_a, right_b = right
    constant = poly_add(
        poly_mul(left_a, right_a, p),
        poly_mul(poly_mul(left_b, right_b, p), curve_polynomial, p),
        p,
    )
    y_coefficient = poly_add(
        poly_mul(left_a, right_b, p),
        poly_mul(left_b, right_a, p),
        p,
    )
    return constant, y_coefficient


def coordinate_pow(
    value: CoordinateElement,
    exponent: int,
    curve_polynomial: Polynomial,
    p: int,
) -> CoordinateElement:
    result: CoordinateElement = ((1,), (0,))
    base = value
    while exponent:
        if exponent & 1:
            result = coordinate_mul(result, base, curve_polynomial, p)
        base = coordinate_mul(base, base, curve_polynomial, p)
        exponent >>= 1
    return result


def evaluate_polynomial(
    coefficients: Polynomial,
    value: ExtensionElement,
) -> ExtensionElement:
    result = value.field.zero
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def evaluate_coordinate(value: CoordinateElement, point: tuple[ExtensionElement, ExtensionElement]) -> ExtensionElement:
    x, y = point
    return evaluate_polynomial(value[0], x) + evaluate_polynomial(value[1], x) * y


def vertical_factor(x_coordinate: int, p: int) -> CoordinateElement:
    return (trim([-x_coordinate, 1], p), (0,))


def line_factors(
    curve: Curve,
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[CoordinateElement, CoordinateElement | None, tuple[int, int] | None]:
    p = curve.p
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % p == 0:
        return vertical_factor(x1, p), None, None
    if left == right:
        if y1 == 0:
            return vertical_factor(x1, p), None, None
        slope = (3 * x1 * x1 + curve.a) * pow(2 * y1, p - 2, p) % p
    else:
        slope = (y2 - y1) * pow((x2 - x1) % p, p - 2, p) % p
    numerator: CoordinateElement = (
        trim([-y1 + slope * x1, -slope], p),
        (1,),
    )
    result = curve.add(left, right)
    denominator = None if result is None else vertical_factor(result[0], p)
    return numerator, denominator, result


def double_counts(counts: FactorCounts) -> FactorCounts:
    return Counter({factor: 2 * exponent for factor, exponent in counts.items()})


def factorized_miller(
    curve: Curve,
    order: int,
    point: tuple[int, int],
) -> tuple[FactorCounts, FactorCounts]:
    numerator: FactorCounts = Counter()
    denominator: FactorCounts = Counter()
    running = point
    for bit in bin(order)[3:]:
        numerator = double_counts(numerator)
        denominator = double_counts(denominator)
        line, vertical, doubled = line_factors(curve, running, running)
        numerator[line] += 1
        if vertical is not None:
            denominator[vertical] += 1
        if doubled is None and bit == "1":
            raise ArithmeticError("unexpected infinity before an addition step")
        running = doubled
        if bit == "1":
            assert running is not None
            line, vertical, added = line_factors(curve, running, point)
            numerator[line] += 1
            if vertical is not None:
                denominator[vertical] += 1
            running = added

    if running != curve.scalar_mul(order, point):
        raise ArithmeticError("symbolic Miller scalar trace is inconsistent")
    for factor in set(numerator) & set(denominator):
        cancellation = min(numerator[factor], denominator[factor])
        numerator[factor] -= cancellation
        denominator[factor] -= cancellation
        if numerator[factor] == 0:
            del numerator[factor]
        if denominator[factor] == 0:
            del denominator[factor]
    return numerator, denominator


def expand_factors(
    factors: FactorCounts,
    curve_polynomial: Polynomial,
    p: int,
) -> CoordinateElement:
    result: CoordinateElement = ((1,), (0,))
    for factor, exponent in sorted(factors.items(), key=lambda item: repr(item[0])):
        result = coordinate_mul(
            result,
            coordinate_pow(factor, exponent, curve_polynomial, p),
            curve_polynomial,
            p,
        )
    return result


def polynomial_degree(value: Polynomial) -> int:
    return -1 if value == (0,) else len(value) - 1


def factorization_json(factors: FactorCounts) -> str:
    records = [
        {
            "A": list(factor[0]),
            "B": list(factor[1]),
            "exponent": exponent,
        }
        for factor, exponent in sorted(factors.items(), key=lambda item: repr(item[0]))
    ]
    return json.dumps(records, separators=(",", ":"))


def factor_degree_growth(order: int) -> tuple[int, int]:
    if order < 3 or order % 2 == 0:
        raise ValueError("growth orders must be odd integers at least three")
    numerator_degree = 0
    denominator_degree = 0
    scalar = 1
    for bit in bin(order)[3:]:
        numerator_degree = 2 * numerator_degree + 1
        denominator_degree *= 2
        scalar = 2 * scalar % order
        if scalar:
            denominator_degree += 1
        if bit == "1":
            numerator_degree += 1
            scalar = (scalar + 1) % order
            if scalar:
                denominator_degree += 1
    if scalar != 0:
        raise ArithmeticError("the loop did not finish at the identity")
    # The last vertical numerator cancels the vertical denominator introduced
    # by the immediately preceding doubling step.
    return numerator_degree - 1, denominator_degree - 1


def exact_row(p: int, order: int, point: tuple[int, int], seed: int, trials: int) -> dict[str, object]:
    curve = Curve(p, 1, 0)
    numerator_factors, denominator_factors = factorized_miller(curve, order, point)
    curve_polynomial = (0, 1, 0, 1)
    numerator = expand_factors(numerator_factors, curve_polynomial, p)
    denominator = expand_factors(denominator_factors, curve_polynomial, p)

    field = ExtensionField(p, (1, 0, 1))
    extension_curve = ExtensionCurve(field, field.element(1), field.zero)
    lifted_point = lift_base_point(field, point)
    q_generator = j1728_distortion_map(field, point, field.element((0, 1)))
    validated = 0
    for scalar in range(1, order):
        evaluation_point = extension_curve.scalar_mul(scalar, q_generator)
        assert evaluation_point is not None
        symbolic_value = evaluate_coordinate(numerator, evaluation_point) / evaluate_coordinate(
            denominator, evaluation_point
        )
        if symbolic_value != miller_loop(extension_curve, order, lifted_point, evaluation_point):
            raise AssertionError("symbolic function disagrees with the numeric Miller loop")
        validated += 1

    return {
        "row_type": "exact_fixed_P",
        "p": p,
        "order_r": order,
        "point_x": point[0],
        "point_y": point[1],
        "numerator_factor_degree": sum(numerator_factors.values()),
        "denominator_factor_degree": sum(denominator_factors.values()),
        "numerator_A_x_degree": polynomial_degree(numerator[0]),
        "numerator_B_x_degree": polynomial_degree(numerator[1]),
        "denominator_A_x_degree": polynomial_degree(denominator[0]),
        "denominator_B_x_degree": polynomial_degree(denominator[1]),
        "numerator_term_count": sum(coefficient != 0 for polynomial in numerator for coefficient in polynomial),
        "denominator_term_count": sum(coefficient != 0 for polynomial in denominator for coefficient in polynomial),
        "numerator_factorization_A_plus_B_y": factorization_json(numerator_factors),
        "denominator_factorization_A_plus_B_y": factorization_json(denominator_factors),
        "numerator_A_coefficients_ascending": json.dumps(numerator[0], separators=(",", ":")),
        "numerator_B_coefficients_ascending": json.dumps(numerator[1], separators=(",", ":")),
        "denominator_A_coefficients_ascending": json.dumps(denominator[0], separators=(",", ":")),
        "denominator_B_coefficients_ascending": json.dumps(denominator[1], separators=(",", ":")),
        "validated_G2_points": validated,
        "trials": trials,
        "seed": seed,
    }


def growth_row(order: int, seed: int, trials: int) -> dict[str, object]:
    numerator_degree, denominator_degree = factor_degree_growth(order)
    return {
        "row_type": "generic_degree_growth",
        "p": "",
        "order_r": order,
        "point_x": "",
        "point_y": "",
        "numerator_factor_degree": numerator_degree,
        "denominator_factor_degree": denominator_degree,
        "numerator_A_x_degree": "",
        "numerator_B_x_degree": "",
        "denominator_A_x_degree": "",
        "denominator_B_x_degree": "",
        "numerator_term_count": "",
        "denominator_term_count": "",
        "numerator_factorization_A_plus_B_y": "",
        "denominator_factorization_A_plus_B_y": "",
        "numerator_A_coefficients_ascending": "",
        "numerator_B_coefficients_ascending": "",
        "denominator_A_coefficients_ascending": "",
        "denominator_B_coefficients_ascending": "",
        "validated_G2_points": "",
        "trials": trials,
        "seed": seed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=43)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--seed", type=int, default=2404)
    parser.add_argument("--orders", type=int, nargs="+", default=[3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 41])
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.p != 43:
        raise ValueError("the exact fixed-P vector currently supports p=43")
    orders = [3, 5, 7] if args.smoke else args.orders
    rows = [exact_row(43, 11, (23, 8), args.seed, args.trials)]
    rows.extend(growth_row(order, args.seed, args.trials) for order in orders)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"analyze_miller_function_p43_r11_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(output)


if __name__ == "__main__":
    main()
