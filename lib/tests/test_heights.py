from fractions import Fraction
import unittest

from lib.heights import WeierstrassCurveQ, rational_log_height


class HeightTests(unittest.TestCase):
    def test_rational_log_height(self) -> None:
        self.assertAlmostEqual(rational_log_height(Fraction(-12, 35)), 3.5553480614894135)

    def test_general_curve_group_law(self) -> None:
        curve = WeierstrassCurveQ.from_coefficients([0, 0, 1, -1, 0])
        point = (Fraction(0), Fraction(0))
        expected = [
            (Fraction(0), Fraction(0)),
            (Fraction(1), Fraction(0)),
            (Fraction(-1), Fraction(-1)),
            (Fraction(2), Fraction(-3)),
        ]
        self.assertEqual([curve.scalar_mul(n, point) for n in range(1, 5)], expected)
        self.assertTrue(all(curve.contains(item) for item in expected))

    def test_lmfdb_canonical_heights(self) -> None:
        # LMFDB 37.a1 and 389.a1 generator values, in its non-normalized convention.
        cases = [
            ([0, 0, 1, -1, 0], (0, 0), 0.0511114082399688),
            ([0, 1, 1, -2, 0], (0, 0), 0.32700077365160495),
            ([0, 1, 1, -2, 0], (1, 0), 0.47671165934373954),
        ]
        for coefficients, coordinates, expected in cases:
            curve = WeierstrassCurveQ.from_coefficients(coefficients)
            point = tuple(Fraction(value) for value in coordinates)
            estimate = curve.canonical_height_estimate(point, iterations=9)
            self.assertAlmostEqual(estimate.value, expected, delta=2e-6)

    def test_height_quadratic_scaling(self) -> None:
        curve = WeierstrassCurveQ.from_coefficients([0, 0, 1, -1, 0])
        point = (Fraction(0), Fraction(0))
        twice = curve.scalar_mul(2, point)
        base_height = curve.canonical_height_estimate(point, iterations=8).value
        twice_height = curve.canonical_height_estimate(twice, iterations=8).value
        self.assertAlmostEqual(twice_height / base_height, 4.0, delta=5e-4)


if __name__ == "__main__":
    unittest.main()
