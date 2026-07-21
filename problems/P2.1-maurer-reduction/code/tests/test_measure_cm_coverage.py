from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from lib.curves import Curve, curve_order
from measure_cm_coverage import (
    class_number,
    cm_trace_conductors,
    explicit_order_families,
    fundamental_discriminant_and_conductor,
    fundamental_discriminants,
)
from summarize_cm_residues import summarize_residues


class CmCoverageTests(unittest.TestCase):
    def test_residue_summary_counts_successes(self) -> None:
        rows = [
            {
                "bits": "60",
                "smoothness_exponent": "3",
                "discriminant_bound": "3600",
                "prime_mod_12": "1",
                "explicit_success": "1",
                "bounded_cm_success": "1",
            },
            {
                "bits": "60",
                "smoothness_exponent": "3",
                "discriminant_bound": "3600",
                "prime_mod_12": "1",
                "explicit_success": "0",
                "bounded_cm_success": "1",
            },
            {
                "bits": "60",
                "smoothness_exponent": "3",
                "discriminant_bound": "3600",
                "prime_mod_12": "11",
                "explicit_success": "0",
                "bounded_cm_success": "0",
            },
        ]
        summary = summarize_residues(rows)
        self.assertEqual(
            [
                (
                    row["prime_mod_12"],
                    row["primes"],
                    row["explicit_successes"],
                    row["bounded_cm_successes"],
                )
                for row in summary
            ],
            [(1, 2, 1, 2), (11, 1, 0, 0)],
        )

    def test_known_class_numbers(self) -> None:
        self.assertEqual(class_number(-3), 1)
        self.assertEqual(class_number(-4), 1)
        self.assertEqual(class_number(-20), 2)
        self.assertEqual(class_number(-23), 3)

    def test_known_extra_unit_cm_traces(self) -> None:
        self.assertEqual(
            {trace for trace, _ in cm_trace_conductors(5, -4)},
            {2, 4},
        )
        self.assertEqual(
            {trace for trace, _ in cm_trace_conductors(7, -3)},
            {1, 4, 5},
        )

    def test_explicit_order_formulas_match_all_twists(self) -> None:
        for prime in (7, 13, 17, 19, 31, 37):
            predicted = explicit_order_families(prime)
            actual_j0 = {
                curve_order(Curve(prime, 0, coefficient))
                for coefficient in range(1, prime)
            }
            actual_j1728 = {
                curve_order(Curve(prime, -coefficient, 0))
                for coefficient in range(1, prime)
            }
            self.assertEqual(
                {order for order, families in predicted.items() if "j0" in families},
                actual_j0,
            )
            self.assertEqual(
                {
                    order
                    for order, families in predicted.items()
                    if "j1728" in families
                },
                actual_j1728,
            )

    def test_bounded_cm_enumeration_matches_brute_traces(self) -> None:
        for prime in (101, 211):
            radius = math.isqrt(4 * prime)
            brute: set[tuple[int, int]] = set()
            for trace in range(0, radius + 1):
                discriminant, _ = fundamental_discriminant_and_conductor(
                    prime, trace
                )
                if abs(discriminant) <= 200:
                    brute.add((discriminant, trace))
            enumerated = {
                (discriminant, trace)
                for discriminant in fundamental_discriminants(200)
                for trace, _ in cm_trace_conductors(prime, discriminant)
            }
            self.assertEqual(enumerated, brute)


if __name__ == "__main__":
    unittest.main()
