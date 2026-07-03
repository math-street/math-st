"""reproduce_xedni_p17 - failed A002 diagnostic, not a reproduction.

Sub-goal: P1.6 / SG-09
Attempt status: dead/failed; generated rates are not accepted as evidence.
Inputs:   --trials <int> --seed <int> --curve-candidates <int> --relation-bound <int>
Outputs:  data/reproduce_xedni_p17_<params>_20260714_{raw,summary}.csv
Runtime:  three-row unit smoke takes about 0.1 s locally; no full rate run accepted.
Validated against: the published p=17 curve order/generator/restrictions and
                   exact containment/reduction/relation checks on every row.

This is a documented variant because the paper does not specify tie-breaking
or a probability distribution over short projective vectors and nearby
coefficient-lattice vectors. It must not be represented as an exact replay of
the authors' LiDIA/SIMATH implementation.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, log, sqrt
from pathlib import Path
from random import Random
import sys
from typing import Sequence

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_decomp

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analyze_lift_relations import bounded_relation, rational_neg  # noqa: E402
from lib.curves import AffinePoint, Curve, curve_order  # noqa: E402
from lib.heights import RationalPoint, WeierstrassCurveQ, rational_log_height  # noqa: E402
from measure_height_growth import balanced, fraction_mod, write_csv  # noqa: E402

DATE_STAMP = "20260714"
PUBLISHED_TRIALS = 100_000
PUBLISHED_DEPENDENCIES = 317


@dataclass(frozen=True, slots=True)
class CoefficientLattice:
    particular: tuple[int, ...]
    reduced_basis_rows: tuple[tuple[int, ...], ...]


def primitive_projective(coordinates: Sequence[int]) -> tuple[int, int, int]:
    common = 0
    for value in coordinates:
        common = gcd(common, abs(value))
    if common == 0:
        raise ValueError("zero projective vector")
    result = tuple(value // common for value in coordinates)
    first_nonzero = next(value for value in result if value)
    if first_nonzero < 0:
        result = tuple(-value for value in result)
    return result  # type: ignore[return-value]


def projective_lift_pool(
    point: tuple[int, int], p: int, pool_size: int
) -> list[tuple[int, int, int]]:
    candidates: dict[tuple[int, int, int], int] = {}
    x, y = point
    for scalar in range(1, p):
        vector = primitive_projective(
            (balanced(scalar * x, p), balanced(scalar * y, p), balanced(scalar, p))
        )
        if vector[2] % p == 0:
            continue
        candidates[vector] = sum(value * value for value in vector)
    return [
        vector
        for vector, _ in sorted(candidates.items(), key=lambda item: (item[1], item[0]))[:pool_size]
    ]


def constraint_row(point: tuple[int, int, int]) -> tuple[int, ...]:
    x, y, z = point
    return (
        y * y * z,
        x * y * z,
        y * z * z,
        -x**3,
        -x * x * z,
        -x * z * z,
        -z**3,
    )


def coefficient_lattice(
    points: Sequence[tuple[int, int, int]], p: int, a: int, b: int
) -> CoefficientLattice:
    rows = [constraint_row(point) for point in points]
    right: list[int] = []
    for x, y, z in points:
        base = y * y * z - x**3 - a * x * z * z - b * z**3
        if base % p:
            raise AssertionError("projective lift does not satisfy the finite equation")
        right.append(-base // p)
    matrix = Matrix(rows)
    rhs = Matrix(right)
    diagonal, left_transform, right_transform = smith_normal_decomp(matrix, domain=ZZ)
    if diagonal != left_transform * matrix * right_transform:
        raise AssertionError("Smith decomposition identity failed")
    transformed_rhs = left_transform * rhs
    rank = matrix.rank()
    if rank != len(points):
        raise ValueError("constraint matrix lacks full row rank")
    smith_coordinates = [0] * matrix.cols
    for index in range(rank):
        divisor = int(diagonal[index, index])
        value = int(transformed_rhs[index])
        if divisor == 0 or value % divisor:
            raise ValueError("no integral coefficient correction exists")
        smith_coordinates[index] = value // divisor
    particular_matrix = right_transform * Matrix(smith_coordinates)
    particular = tuple(int(value) for value in particular_matrix)
    homogeneous_rows = right_transform[:, rank:].T
    reduced = homogeneous_rows.lll()
    if matrix * Matrix(particular) != rhs:
        raise AssertionError("particular coefficient solution failed")
    if matrix * reduced.T != Matrix.zeros(matrix.rows, reduced.rows):
        raise AssertionError("homogeneous coefficient basis failed")
    return CoefficientLattice(
        particular,
        tuple(tuple(int(value) for value in reduced.row(row)) for row in range(reduced.rows)),
    )


def nearest_lattice_coordinates(lattice: CoefficientLattice) -> tuple[int, ...]:
    basis = np.asarray(lattice.reduced_basis_rows, dtype=float).T
    target = -np.asarray(lattice.particular, dtype=float)
    coordinates = np.linalg.lstsq(basis, target, rcond=None)[0]
    return tuple(int(round(value)) for value in coordinates)


def correction_from_coordinates(
    lattice: CoefficientLattice, coordinates: Sequence[int]
) -> tuple[int, ...]:
    correction = list(lattice.particular)
    for coefficient, basis_row in zip(coordinates, lattice.reduced_basis_rows, strict=True):
        correction = [
            left + coefficient * right
            for left, right in zip(correction, basis_row, strict=True)
        ]
    return tuple(correction)


def original_projective_contains(
    correction: Sequence[int], point: tuple[int, int, int], p: int, a: int, b: int
) -> bool:
    u1, u2, u3, u4, u5, u6, u7 = correction
    x, y, z = point
    return (
        (1 + p * u1) * y * y * z
        + p * u2 * x * y * z
        + p * u3 * y * z * z
        - (1 + p * u4) * x**3
        - p * u5 * x * x * z
        - (a + p * u6) * x * z * z
        - (b + p * u7) * z**3
        == 0
    )


def standard_curve_and_points(
    correction: Sequence[int],
    projective_points: Sequence[tuple[int, int, int]],
    p: int,
    a: int,
    b: int,
) -> tuple[WeierstrassCurveQ, list[RationalPoint]]:
    u1, u2, u3, u4, u5, u6, u7 = correction
    alpha = 1 + p * u1
    beta = 1 + p * u4
    if alpha == 0 or beta == 0:
        raise ValueError("leading coefficient vanished")
    ratio = Fraction(beta, alpha)
    curve = WeierstrassCurveQ.from_coefficients(
        [
            Fraction(p * u2, alpha),
            Fraction(p * u5, alpha),
            Fraction(p * u3, alpha) * ratio,
            Fraction(a + p * u6, alpha) * ratio,
            Fraction(b + p * u7, alpha) * ratio * ratio,
        ]
    )
    points: list[RationalPoint] = []
    for projective in projective_points:
        if not original_projective_contains(correction, projective, p, a, b):
            raise AssertionError("projective point is not on the constructed curve")
        x, y, z = projective
        if z == 0:
            raise ValueError("affine conversion received a point at infinity")
        point = ratio * Fraction(x, z), ratio * Fraction(y, z)
        if not curve.contains(point):
            raise AssertionError("standard-model point containment failed")
        points.append(point)
    if curve.discriminant == 0 or fraction_mod(curve.discriminant, p) == 0:
        raise ValueError("constructed curve lacks good reduction")
    if [fraction_mod(value, p) for value in (curve.a1, curve.a2, curve.a3, curve.a4, curve.a6)] != [
        0,
        0,
        0,
        a % p,
        b % p,
    ]:
        raise AssertionError("constructed curve has the wrong reduction")
    return curve, points


def choose_small_discriminant_curve(
    lattice: CoefficientLattice,
    projective_points: Sequence[tuple[int, int, int]],
    *,
    p: int,
    a: int,
    b: int,
    rng: Random,
    candidates: int,
    radius: int,
) -> tuple[tuple[int, ...], WeierstrassCurveQ, list[RationalPoint]]:
    center = nearest_lattice_coordinates(lattice)
    coordinate_candidates = {center}
    for _ in range(max(0, candidates - 1)):
        coordinate_candidates.add(
            tuple(value + rng.randint(-radius, radius) for value in center)
        )
    measured: list[
        tuple[float, int, tuple[int, ...], WeierstrassCurveQ, list[RationalPoint]]
    ] = []
    for coordinates in coordinate_candidates:
        correction = correction_from_coordinates(lattice, coordinates)
        try:
            curve, points = standard_curve_and_points(correction, projective_points, p, a, b)
        except ValueError:
            continue
        measured.append(
            (
                rational_log_height(curve.discriminant),
                max(abs(value) for value in correction),
                correction,
                curve,
                points,
            )
        )
    if not measured:
        raise RuntimeError("no nonsingular nearby coefficient solution")
    _, _, correction, curve, points = min(measured, key=lambda item: (item[0], item[1], item[2]))
    return correction, curve, points


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    proportion = successes / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    half = z * sqrt(proportion * (1 - proportion) / trials + z * z / (4 * trials * trials)) / denominator
    return center - half, center + half


def run_experiment(
    *,
    trials: int,
    seed: int,
    projective_pool_size: int,
    curve_candidates: int,
    candidate_radius: int,
    relation_bound: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    p, a, b = 17, 2, 2
    finite_curve = Curve(p, a, b)
    generator = (3, 1)
    if curve_order(finite_curve) != 19 or not finite_curve.contains(generator):
        raise AssertionError("published p=17 finite input was not reproduced")
    rng = Random(seed)
    first_finite = generator
    first_pool = projective_lift_pool(first_finite, p, projective_pool_size)
    second_pools = {
        scalar: projective_lift_pool(
            finite_curve.scalar_mul(scalar, generator), p, projective_pool_size
        )
        for scalar in range(2, 18)
    }
    lattice_cache: dict[
        tuple[tuple[int, int, int], tuple[int, int, int]], CoefficientLattice
    ] = {}
    raw: list[dict[str, object]] = []
    for trial in range(trials):
        second_scalar = rng.randint(2, 17)
        projective_points = [rng.choice(first_pool), rng.choice(second_pools[second_scalar])]
        key = projective_points[0], projective_points[1]
        lattice = lattice_cache.get(key)
        if lattice is None:
            lattice = coefficient_lattice(projective_points, p, a, b)
            lattice_cache[key] = lattice
        correction, curve, points = choose_small_discriminant_curve(
            lattice,
            projective_points,
            p=p,
            a=a,
            b=b,
            rng=rng,
            candidates=curve_candidates,
            radius=candidate_radius,
        )
        relation = bounded_relation(
            points,
            add=curve.add,
            neg=lambda point: rational_neg(curve, point),
            scalar_mul=curve.scalar_mul,
            identity=None,
            bound=relation_bound,
        )
        discriminant_height = rational_log_height(curve.discriminant)
        raw.append(
            {
                "trial": trial,
                "seed": seed,
                "p": p,
                "second_scalar": second_scalar,
                "projective_point_1": ";".join(map(str, projective_points[0])),
                "projective_point_2": ";".join(map(str, projective_points[1])),
                "correction_u1_u2_u3_u4_u5_u6_u7": ";".join(map(str, correction)),
                "discriminant_log_height": discriminant_height,
                "discriminant_bit_height": max(1, int(discriminant_height / log(2.0)) + 1),
                "dependent_through_bound": int(relation is not None),
                "relation_bound": relation_bound,
                "relation_min_linf": "" if relation is None else relation[0],
                "relation": "" if relation is None else ";".join(map(str, relation[1])),
            }
        )
        if (trial + 1) % 500 == 0:
            print(f"completed {trial + 1}/{trials} trials", flush=True)

    dependencies = sum(int(row["dependent_through_bound"]) for row in raw)
    lower, upper = wilson_interval(dependencies, trials)
    all_discriminants = [float(row["discriminant_log_height"]) for row in raw]
    dependent_discriminants = [
        float(row["discriminant_log_height"])
        for row in raw
        if int(row["dependent_through_bound"])
    ]
    summary = [
        {
            "experiment": "seeded-projective-p17-variant",
            "trials": trials,
            "seed": seed,
            "projective_pool_size": projective_pool_size,
            "curve_candidates": curve_candidates,
            "candidate_radius": candidate_radius,
            "relation_bound": relation_bound,
            "dependencies": dependencies,
            "dependency_rate": dependencies / trials,
            "wilson95_low": lower,
            "wilson95_high": upper,
            "published_trials": PUBLISHED_TRIALS,
            "published_dependencies": PUBLISHED_DEPENDENCIES,
            "published_rate": PUBLISHED_DEPENDENCIES / PUBLISHED_TRIALS,
            "expected_dependencies_at_published_rate": trials * PUBLISHED_DEPENDENCIES / PUBLISHED_TRIALS,
            "mean_discriminant_log_height": sum(all_discriminants) / trials,
            "min_discriminant_log_height": min(all_discriminants),
            "max_discriminant_log_height": max(all_discriminants),
            "mean_dependent_discriminant_log_height": ""
            if not dependent_discriminants
            else sum(dependent_discriminants) / len(dependent_discriminants),
            "algorithmic_caveat": "tie-breaking and sampling differ from unspecified LiDIA/SIMATH implementation",
        }
    ]
    return raw, summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=17002000)
    parser.add_argument("--projective-pool-size", type=int, default=8)
    parser.add_argument("--curve-candidates", type=int, default=24)
    parser.add_argument("--candidate-radius", type=int, default=1)
    parser.add_argument("--relation-bound", type=int, default=8)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(
        "WARNING: A002 is a failed diagnostic variant, not a reproduction; "
        "do not compare its rate with Table 3.",
        flush=True,
    )
    if args.smoke:
        args.trials = 25
        args.curve_candidates = min(args.curve_candidates, 6)
    raw, summary = run_experiment(
        trials=args.trials,
        seed=args.seed,
        projective_pool_size=args.projective_pool_size,
        curve_candidates=args.curve_candidates,
        candidate_radius=args.candidate_radius,
        relation_bound=args.relation_bound,
    )
    tag = (
        f"t{args.trials}_s{args.seed}_pp{args.projective_pool_size}"
        f"_cc{args.curve_candidates}_r{args.candidate_radius}_B{args.relation_bound}_{DATE_STAMP}"
    )
    raw_path = args.output_dir / f"reproduce_xedni_p17_{tag}_raw.csv"
    summary_path = args.output_dir / f"reproduce_xedni_p17_{tag}_summary.csv"
    write_csv(raw_path, raw)
    write_csv(summary_path, summary)
    print(f"wrote {len(raw)} rows to {raw_path}")
    print(f"wrote summary to {summary_path}")


if __name__ == "__main__":
    main()
