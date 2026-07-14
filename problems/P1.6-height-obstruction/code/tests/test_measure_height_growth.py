from __future__ import annotations

from fractions import Fraction
from random import Random
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from measure_height_growth import (  # noqa: E402
    corrected_curve,
    direct_short_lift,
    lift_solution_space,
    sample_curve_and_points,
    validate_reduction,
)
from reproduce_xedni_probability import reproduce  # noqa: E402
from analyze_lift_relations import bounded_relation, rational_neg  # noqa: E402
from lib.heights import WeierstrassCurveQ  # noqa: E402
from lib.curves import Curve  # noqa: E402
from reproduce_xedni_p17 import (  # noqa: E402
    coefficient_lattice,
    correction_from_coordinates,
    projective_lift_pool,
    run_experiment,
    standard_curve_and_points,
)


class HeightGrowthMeasurementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = 31
        self.finite_curve, self.points = sample_curve_and_points(self.p, Random(16062026))
        self.rational_points = [(Fraction(x), Fraction(y)) for x, y in self.points]

    def test_direct_single_point_lift(self) -> None:
        curve = direct_short_lift(self.p, self.finite_curve.a, self.points[0])
        validate_reduction(
            curve,
            self.rational_points[:1],
            self.p,
            self.finite_curve.a,
            self.finite_curve.b,
        )

    def test_four_point_general_lift(self) -> None:
        particular, nullspace = lift_solution_space(
            self.p, self.finite_curve.a, self.finite_curve.b, self.points
        )
        curve = corrected_curve(
            self.p,
            self.finite_curve.a,
            self.finite_curve.b,
            particular,
            nullspace,
            [0] * len(nullspace),
        )
        validate_reduction(
            curve,
            self.rational_points,
            self.p,
            self.finite_curve.a,
            self.finite_curve.b,
        )
        self.assertTrue(all(curve.contains(point) for point in self.rational_points))

    def test_published_xedni_probability(self) -> None:
        result = reproduce()
        self.assertEqual(result["group_order"], 263)
        self.assertEqual(result["eligible_second_points"], 260)
        self.assertEqual(result["favorable_points"], 4)
        self.assertEqual(result["measured_probability"], 1 / 65)

    def test_bounded_relation_is_minimal_on_37a1(self) -> None:
        curve = WeierstrassCurveQ.from_coefficients([0, 0, 1, -1, 0])
        point = (Fraction(0), Fraction(0))
        points = [curve.scalar_mul(index, point) for index in (1, 2)]
        result = bounded_relation(
            points,
            add=curve.add,
            neg=lambda item: rational_neg(curve, item),
            scalar_mul=curve.scalar_mul,
            identity=None,
            bound=8,
        )
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result[0], 2)
        self.assertEqual(curve.add(curve.scalar_mul(result[1][0], points[0]), curve.scalar_mul(result[1][1], points[1])), None)

    def test_no_small_relation_for_389a1_generators(self) -> None:
        curve = WeierstrassCurveQ.from_coefficients([0, 1, 1, -2, 0])
        points = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))]
        result = bounded_relation(
            points,
            add=curve.add,
            neg=lambda item: rational_neg(curve, item),
            scalar_mul=curve.scalar_mul,
            identity=None,
            bound=8,
        )
        self.assertIsNone(result)

    def test_p17_integer_lattice_and_standard_model(self) -> None:
        finite_curve = Curve(17, 2, 2)
        generator = (3, 1)
        finite_points = [generator, finite_curve.scalar_mul(5, generator)]
        projective_points = [projective_lift_pool(point, 17, 1)[0] for point in finite_points]
        lattice = coefficient_lattice(projective_points, 17, 2, 2)
        correction = correction_from_coordinates(lattice, [0] * len(lattice.reduced_basis_rows))
        curve, points = standard_curve_and_points(correction, projective_points, 17, 2, 2)
        self.assertTrue(all(curve.contains(point) for point in points))
        self.assertNotEqual(curve.discriminant, 0)

    def test_p17_smoke_experiment(self) -> None:
        raw, summary = run_experiment(
            trials=3,
            seed=17,
            projective_pool_size=3,
            curve_candidates=3,
            candidate_radius=1,
            relation_bound=8,
        )
        self.assertEqual(len(raw), 3)
        self.assertEqual(summary[0]["published_dependencies"], 317)


if __name__ == "__main__":
    unittest.main()
