"""
toy_deuring_roundtrip.py - a right-order-aware dual two-step Deuring round trip.
Sub-goal: P3.1 / SG-03c and SG-04b
Inputs:   --p <prime> --ell <prime> --trials <int> --seed <int>
Outputs:  data/toy_deuring_roundtrip_p11_ell3_20260711.csv
Runtime:  target under 10 seconds for the validated p=11, ell=3 fixture
Validated against: #E(F_(11^2))=144, four norm-3 neighbors, and I*conjugate(I)=3O
"""

from __future__ import annotations

import argparse
import csv
import sys
from itertools import product
from pathlib import Path
from random import Random
from time import perf_counter
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from lib.isogeny import (
    QuadraticExtensionCurve,
    deuring_curve_key,
    extension_velu_map,
    extension_velu_quotient,
    quadratic_curve_order,
    quadratic_field,
)
from lib.quaternion import IntegralIdeal, MaximalOrder


Point = tuple[object, object] | None


def point_key(point: Point) -> tuple[int, ...]:
    if point is None:
        return ()
    x, y = point
    return x + y  # type: ignore[operator]


def find_sqrt_minus_one(curve: QuadraticExtensionCurve):
    target = curve.field.constant(-1)
    for value in curve.field.elements():
        if curve.field.mul(value, value) == target:
            return value
    raise ArithmeticError("-1 had no square root in the quadratic field")


def iota(curve: QuadraticExtensionCurve, point: Point, sqrt_minus_one) -> Point:
    if point is None:
        return None
    x, y = point
    return curve.field.neg(x), curve.field.mul(sqrt_minus_one, y)


def frobenius(curve: QuadraticExtensionCurve, point: Point) -> Point:
    if point is None:
        return None
    x, y = point
    prime = curve.field.characteristic
    return curve.field.pow(x, prime), curve.field.pow(y, prime)


def add_scaled(
    curve: QuadraticExtensionCurve,
    accumulator: Point,
    coefficient: int,
    point: Point,
) -> Point:
    return curve.add(accumulator, curve.scalar_mul(coefficient, point))


def evaluate_order_element(
    curve: QuadraticExtensionCurve,
    point: Point,
    coordinates: Sequence[int],
    ell: int,
    sqrt_minus_one,
) -> Point:
    """Evaluate O0 coordinates on E[ell] via i->iota and j->Frobenius."""

    if len(coordinates) != 4:
        raise ValueError("order coordinates must have length four")
    half = pow(2, -1, ell)
    z0, z1, z2, z3 = (coordinate % ell for coordinate in coordinates)
    coefficients = (
        (z0 + half * z2) % ell,
        (z1 + half * z3) % ell,
        (half * z2) % ell,
        (half * z3) % ell,
    )
    i_point = iota(curve, point, sqrt_minus_one)
    j_point = frobenius(curve, point)
    ij_point = iota(curve, j_point, sqrt_minus_one)
    result: Point = None
    for coefficient, image in zip(coefficients, (point, i_point, j_point, ij_point)):
        result = add_scaled(curve, result, coefficient, image)
    return result


def ell_torsion_points(
    curve: QuadraticExtensionCurve, ell: int
) -> tuple[tuple[object, object], ...]:
    return tuple(
        point for point in curve.affine_points() if curve.scalar_mul(ell, point) is None
    )


def ideal_kernel(
    curve: QuadraticExtensionCurve,
    alpha: Sequence[int],
    ell: int,
    sqrt_minus_one,
) -> tuple[tuple[object, object], ...]:
    points = tuple(
        point
        for point in ell_torsion_points(curve, ell)
        if evaluate_order_element(curve, point, alpha, ell, sqrt_minus_one) is None
    )
    if len(points) != ell - 1:
        raise ArithmeticError(f"expected {ell - 1} nonzero kernel points, found {len(points)}")
    return tuple(sorted(points, key=point_key))


def dual_kernel(
    curve: QuadraticExtensionCurve,
    generator: Point,
    ell: int,
) -> tuple[tuple[object, object], ...]:
    """Recover the nonzero dual kernel as the image of E[ell]."""

    images: dict[tuple[int, ...], tuple[object, object]] = {}
    for point in ell_torsion_points(curve, ell):
        image = extension_velu_map(curve, point, generator, ell)
        if image is not None:
            images[point_key(image)] = image
    if len(images) != ell - 1:
        raise ArithmeticError(
            f"expected {ell - 1} nonzero dual-kernel points, found {len(images)}"
        )
    return tuple(images[key] for key in sorted(images))


def kernel_key(points: Sequence[Point]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((point_key(point) for point in points)))


def points_from_kernel_key(
    curve: QuadraticExtensionCurve, key: Sequence[Sequence[int]]
) -> tuple[tuple[object, object], ...]:
    degree = curve.field.degree
    return tuple(
        (tuple(encoded[:degree]), tuple(encoded[degree:])) for encoded in key
    )


def enumerate_neighbor_ideals(
    order: MaximalOrder,
    curve: QuadraticExtensionCurve,
    ell: int,
    sqrt_minus_one,
) -> dict[tuple[tuple[int, ...], ...], IntegralIdeal]:
    neighbors: dict[tuple[tuple[int, ...], ...], IntegralIdeal] = {}
    seen_ideals: set[str] = set()
    for alpha in product(range(ell), repeat=4):
        if not any(alpha) or order.norm(alpha) % ell:
            continue
        try:
            ideal = order.prime_ideal(ell, alpha)
        except ValueError:
            continue
        if ideal.canonical_id in seen_ideals:
            continue
        seen_ideals.add(ideal.canonical_id)
        key = kernel_key(ideal_kernel(curve, alpha, ell, sqrt_minus_one))
        if key in neighbors and neighbors[key].canonical_id != ideal.canonical_id:
            raise ArithmeticError("two distinct ideals produced the same kernel")
        neighbors[key] = ideal
    if len(neighbors) != ell + 1:
        raise ArithmeticError(f"expected {ell + 1} neighbors, found {len(neighbors)}")
    return neighbors


def right_order_target_dictionary(
    order: MaximalOrder,
    curve: QuadraticExtensionCurve,
    ell: int,
    neighbors: dict[tuple[tuple[int, ...], ...], IntegralIdeal],
) -> tuple[dict[str, tuple[str, int]], dict[str, str]]:
    """Associate exact embedded right orders to quotient Deuring keys."""

    ideal_orders: dict[str, tuple[str, int]] = {}
    order_targets: dict[str, str] = {}
    for key, ideal in neighbors.items():
        kernel = points_from_kernel_key(curve, key)
        quotient = extension_velu_quotient(curve, kernel[0], ell)
        target_key = ";".join(map(str, deuring_curve_key(quotient)))
        right_order = ideal.right_order()
        order_id = right_order.canonical_id
        if order_id in order_targets and order_targets[order_id] != target_key:
            raise ArithmeticError("one embedded right order maps to two curve keys")
        order_targets[order_id] = target_key
        ideal_orders[ideal.canonical_id] = (
            order_id,
            abs(right_order.trace_discriminant()),
        )
    return ideal_orders, order_targets


def run(p: int, ell: int, trials: int, seed: int) -> list[dict[str, int | str | float]]:
    if p % 4 != 3:
        raise ValueError("the current special-curve dictionary requires p == 3 mod 4")
    field = quadratic_field(p)
    curve = QuadraticExtensionCurve(field, field.constant(-1), field.zero)
    expected_order = (p + 1) ** 2
    actual_order = quadratic_curve_order(curve)
    if actual_order != expected_order:
        raise ArithmeticError(f"unexpected source curve order {actual_order}")
    if expected_order % (ell * ell):
        raise ValueError("the validated round trip requires full rational ell-torsion")

    order = MaximalOrder(p)
    sqrt_minus_one = find_sqrt_minus_one(curve)
    torsion = ell_torsion_points(curve, ell)
    if len(torsion) != ell * ell - 1:
        raise ArithmeticError("the full nonzero ell-torsion was not rational")
    neighbors = enumerate_neighbor_ideals(order, curve, ell, sqrt_minus_one)
    ideal_orders, order_targets = right_order_target_dictionary(
        order, curve, ell, neighbors
    )
    rows: list[dict[str, int | str | float]] = []
    for trial in range(trials):
        trial_seed = seed + trial
        rng = Random(trial_seed)
        ideal, alpha = order.random_prime_ideal(ell, rng)
        kernel = ideal_kernel(curve, alpha, ell, sqrt_minus_one)
        recovered = neighbors[kernel_key(kernel)]
        if recovered.canonical_id != ideal.canonical_id:
            raise ArithmeticError("ideal-kernel-ideal round trip failed")
        generator = kernel[0]
        quotient = extension_velu_quotient(curve, generator, ell)
        if quadratic_curve_order(quotient) != actual_order:
            raise ArithmeticError("Velu quotient changed the point count")
        second_kernel = dual_kernel(curve, generator, ell)
        terminal_curve = extension_velu_quotient(quotient, second_kernel[0], ell)
        source_deuring_key = ";".join(map(str, deuring_curve_key(curve)))
        terminal_deuring_key = ";".join(map(str, deuring_curve_key(terminal_curve)))
        if terminal_deuring_key != source_deuring_key:
            raise ArithmeticError("dual two-step path did not return the source class")
        if not ideal.verifies_dual_product_identity():
            raise ArithmeticError("ideal times its conjugate did not equal ell times O")
        right_order_id, right_order_discriminant = ideal_orders[ideal.canonical_id]
        target_deuring_key = ";".join(map(str, deuring_curve_key(quotient)))
        if order_targets[right_order_id] != target_deuring_key:
            raise ArithmeticError("right-order dictionary recovered the wrong curve key")
        rows.append(
            {
                "p": p,
                "ell": ell,
                "trial": trial,
                "seed": trial_seed,
                "source_order": actual_order,
                "torsion_points": len(torsion),
                "neighbor_ideals": len(neighbors),
                "alpha": ";".join(str(value) for value in alpha),
                "ideal_id": ideal.canonical_id,
                "recovered_ideal_id": recovered.canonical_id,
                "roundtrip_match": 1,
                "kernel_nonzero_points": len(kernel),
                "source_deuring_key": source_deuring_key,
                "target_deuring_key": target_deuring_key,
                "target_order": quadratic_curve_order(quotient),
                "right_order_id": right_order_id,
                "right_order_discriminant": right_order_discriminant,
                "right_order_lookup_match": 1,
                "embedded_right_orders": len(order_targets),
                "target_curve_classes": len(set(order_targets.values())),
                "dual_kernel_nonzero_points": len(second_kernel),
                "terminal_deuring_key": terminal_deuring_key,
                "dual_roundtrip_match": 1,
                "dual_ideal_product_match": 1,
                "chain_degree": ell * ell,
                "ideal_candidates": ell**4 - 1,
                "velu_steps": 2,
                "oracle_queries": 0,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=11)
    parser.add_argument("--ell", type=int, default=3)
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--seed", type=int, default=3103)
    parser.add_argument(
        "--output-name",
        type=str,
        help="optional data-directory filename for a separately recorded run",
    )
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        args.p = 11
        args.ell = 3
        args.trials = 1
    started = perf_counter()
    rows = run(args.p, args.ell, args.trials, args.seed)
    elapsed = perf_counter() - started
    for row in rows:
        row["batch_wall_seconds"] = elapsed
        row["seconds_per_trial"] = elapsed / len(rows)
    default_output_name = (
        "toy_deuring_roundtrip_smoke_20260711.csv"
        if args.smoke
        else f"toy_deuring_roundtrip_p{args.p}_ell{args.ell}_20260711.csv"
    )
    output_name = args.output_name or default_output_name
    if Path(output_name).name != output_name or not output_name.endswith(".csv"):
        raise ValueError("output-name must be a CSV filename without a directory")
    output = Path(__file__).resolve().parents[1] / "data" / output_name
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(output)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
