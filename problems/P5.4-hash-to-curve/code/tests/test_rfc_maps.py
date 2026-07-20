from __future__ import annotations

import ast
import inspect
import sys
import unittest
from pathlib import Path
from random import Random

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from lib.curves import (
    Curve,
    MontgomeryCurve,
    cmov_mod,
    map_to_curve_elligator2,
    map_to_curve_simple_swu,
    simple_swu_parameters_are_valid,
    sqrt_mod_ct,
    sqrt_ratio_mod,
)
from validate_rfc_maps import (
    ELLIGATOR2_CASES,
    SSWU_CASES,
    elligator2_oracle,
    simple_swu_oracle,
    validate_primes,
)
from measure_map_timing import (
    bootstrap_mean_ratio,
    bootstrap_paired_mean_ratio,
    percentile,
)


class FixedScheduleMapTests(unittest.TestCase):
    def test_timing_summary_helpers_known_values(self) -> None:
        self.assertEqual(percentile([1.0, 2.0, 3.0], 0.5), 2.0)
        ratio, low, high = bootstrap_mean_ratio(
            [2.0, 2.0, 2.0],
            [2.0, 2.0, 2.0],
            resamples=20,
            rng=Random(5402),
        )
        self.assertEqual((ratio, low, high), (1.0, 1.0, 1.0))
        paired_ratio, paired_low, paired_high = bootstrap_paired_mean_ratio(
            [2.0, 2.0, 2.0],
            [2.0, 2.0, 2.0],
            resamples=20,
            rng=Random(5402),
        )
        self.assertEqual(
            (paired_ratio, paired_low, paired_high),
            (1.0, 1.0, 1.0),
        )

    def test_source_has_no_secret_dependent_branches_or_indexing(self) -> None:
        audited = (
            (map_to_curve_simple_swu, {"u"}),
            (map_to_curve_elligator2, {"u"}),
            (sqrt_ratio_mod, {"numerator", "denominator"}),
            (sqrt_mod_ct, {"value"}),
            (cmov_mod, {"condition"}),
        )
        for function, secret_names in audited:
            tree = ast.parse(inspect.getsource(function))
            function_node = tree.body[0]
            self.assertIsInstance(function_node, ast.FunctionDef)
            body_nodes = (
                node
                for statement in function_node.body
                for node in ast.walk(statement)
            )
            for node in body_nodes:
                if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                    referenced = {
                        child.id
                        for child in ast.walk(node.test)
                        if isinstance(child, ast.Name)
                    }
                    self.assertTrue(
                        referenced.isdisjoint(secret_names),
                        f"{function.__name__} branches on {referenced & secret_names}",
                    )
                self.assertNotIsInstance(
                    node,
                    ast.Subscript,
                    f"{function.__name__} contains indexed memory access",
                )

    def test_fixed_known_outputs(self) -> None:
        self.assertEqual(
            map_to_curve_simple_swu(Curve(11, 1, 1), 0, 6),
            (2, 0),
        )
        self.assertEqual(
            map_to_curve_elligator2(MontgomeryCurve(11, 1, 1), 4, 2),
            (0, 0),
        )

    def test_generic_sqrt_ratio_treats_zero_as_square(self) -> None:
        is_qr, root = sqrt_ratio_mod(0, 1, 11, 2)
        self.assertTrue(is_qr)
        self.assertEqual(root, 0)

    def test_rfc_generic_sqrt_ratio_zero_counterexample(self) -> None:
        curve = Curve(11, 1, 1)
        self.assertTrue(simple_swu_parameters_are_valid(curve, 6))
        numerator = 0
        denominator = 7
        tv2 = pow(denominator, 1, 11)
        tv3 = tv2 * tv2 * denominator % 11
        tv5 = numerator * tv3 % 11
        tv5 = pow(tv5, 2, 11) * tv2 % 11
        tv2 = tv5 * denominator % 11
        tv3 = tv5 * numerator % 11
        tv4 = tv3 * tv2 % 11
        published_tv5 = pow(tv4, 1, 11)
        published_is_qr = published_tv5 == 1
        self.assertEqual(published_tv5, 0)
        self.assertFalse(published_is_qr)
        self.assertFalse(curve.contains((0, 0)))
        corrected_is_qr, corrected_root = sqrt_ratio_mod(
            numerator,
            denominator,
            11,
            6,
        )
        self.assertTrue(corrected_is_qr)
        self.assertEqual(corrected_root, 0)
        self.assertEqual(map_to_curve_simple_swu(curve, 0, 6), (2, 0))

    def test_fixed_loop_square_root_exhaustively(self) -> None:
        for p in (7, 11, 13, 17, 19, 29, 37):
            for value in range(p):
                square = value * value % p
                root = sqrt_mod_ct(square, p)
                self.assertEqual(root * root % p, square)

    def test_sswu_exhaustive_oracle_and_schedule(self) -> None:
        for p, (a, b, z) in SSWU_CASES.items():
            curve = Curve(p, a, b)
            self.assertTrue(simple_swu_parameters_are_valid(curve, z))
            schedules = set()
            for u in range(p):
                trace: list[str] = []
                actual = map_to_curve_simple_swu(curve, u, z, trace=trace)
                self.assertEqual(actual, simple_swu_oracle(curve, u, z))
                self.assertTrue(curve.contains(actual))
                schedules.add(tuple(trace))
            self.assertEqual(len(schedules), 1)

    def test_elligator2_exhaustive_oracle_and_schedule(self) -> None:
        for p, (j, k, z) in ELLIGATOR2_CASES.items():
            curve = MontgomeryCurve(p, j, k)
            self.assertTrue(curve.supports_elligator2())
            schedules = set()
            for u in range(p):
                trace: list[str] = []
                actual = map_to_curve_elligator2(curve, u, z, trace=trace)
                self.assertEqual(actual, elligator2_oracle(curve, u, z))
                self.assertTrue(curve.contains(actual))
                schedules.add(tuple(trace))
            self.assertEqual(len(schedules), 1)

    def test_invalid_applicability_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "nonzero a and b"):
            map_to_curve_simple_swu(Curve(11, 0, 1), 3, 2)
        unsupported = MontgomeryCurve(11, 3, 1)
        self.assertFalse(unsupported.supports_elligator2())
        with self.assertRaisesRegex(ValueError, "Elligator 2 predicates"):
            map_to_curve_elligator2(unsupported, 3, 2)

    def test_smoke_summary_has_no_failures(self) -> None:
        rows = validate_primes([11, 13], seed=5401)
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(row["inputs_tested"], row["on_curve"])
            self.assertEqual(row["inputs_tested"], row["oracle_matches"])
            self.assertEqual(row["schedule_variants"], 1)


if __name__ == "__main__":
    unittest.main()
