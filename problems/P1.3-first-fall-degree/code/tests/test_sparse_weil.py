"""Tests for exact extension-field and sparse Weil-restriction utilities."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from sparse_weil import (  # noqa: E402
    FiniteField,
    SparsePolynomial,
    build_weil_coordinate_system,
    curve_is_nonsingular,
    evaluate_prime_polynomial,
    f3_polynomial,
    find_irreducible_modulus,
    generic_semaev_polynomial,
    known_decomposition,
    known_decomposition_candidates,
)
from measure_quadratic_variants import analyze_core, enumerate_cases  # noqa: E402
from certify_quadratic_family import symbolic_certificate  # noqa: E402
from certify_quadratic_field_equations import (  # noqa: E402
    concrete_q7_certificate,
    symbolic_infinite_family_certificate,
)
from search_quadratic_counterexamples import abstract_core  # noqa: E402
from measure_semaev_stats import measure_index  # noqa: E402
from measure_weil_degrees import (  # noqa: E402
    degree_of_regularity_exact,
    field_equations,
    first_fall_degree_exact,
    measure_case,
    solving_degree_exact,
    sympy_groebner,
)


class SparseWeilTests(unittest.TestCase):
    def test_extension_field_inverses(self) -> None:
        field = FiniteField(3, find_irreducible_modulus(3, 3))
        for value in field.elements():
            if value != field.zero:
                self.assertEqual(field.mul(value, field.inv(value)), field.one)

    def test_measured_curve_family_is_nonsingular(self) -> None:
        for q in (3, 5, 7, 11, 13, 17, 19, 23):
            for n in (2, 3):
                field = FiniteField(q, find_irreducible_modulus(q, n))
                a = (0, 1) + (0,) * (n - 2)
                self.assertTrue(curve_is_nonsingular(field, a, field.one))

    def test_f3_expansion_matches_published_formula_value(self) -> None:
        field = FiniteField(101, (0, 1))
        variables = [SparsePolynomial.variable(field, 5, index) for index in range(5)]
        expanded = f3_polynomial(*variables[:3], variables[3], variables[4])
        value = expanded.evaluate([field.element(item) for item in (1, 2, 3, 2, 3)])
        self.assertEqual(value, field.element(67))

    def test_generic_f3_and_f4_degrees(self) -> None:
        f3 = generic_semaev_polynomial(3)
        f4 = generic_semaev_polynomial(4)
        self.assertEqual([f3.variable_degree(index) for index in range(3)], [2, 2, 2])
        self.assertEqual([f4.variable_degree(index) for index in range(4)], [4, 4, 4, 4])

    def test_stats_wrapper_reports_complete_small_cases(self) -> None:
        result = measure_index(3, 10_000)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["x_variable_degrees"], "2;2;2")

    def test_known_decompositions_are_roots_after_weil_restriction(self) -> None:
        for n in (2, 3):
            for m in (2, 3, 4):
                field = FiniteField(3, find_irreducible_modulus(3, n))
                values, target = known_decomposition(field, m)
                _, coordinates, extension_polynomial = build_weil_coordinate_system(
                    3, n, m, target
                )
                self.assertEqual(
                    extension_polynomial.evaluate([field.element(value) for value in values]),
                    field.zero,
                )
                self.assertTrue(
                    all(evaluate_prime_polynomial(poly, values, 3) == 0 for poly in coordinates)
                )

    def test_quadratic_variant_enumeration_and_core_analysis(self) -> None:
        cases = enumerate_cases(5, 1, [1], 2, [0], 2)
        self.assertGreaterEqual(len(cases), 2)
        case = cases[0]
        analysis = analyze_core(
            5,
            case["curve_a"],  # type: ignore[arg-type]
            case["curve_b"],  # type: ignore[arg-type]
            case["target"],  # type: ignore[arg-type]
        )
        self.assertTrue(analysis["quadratic_top_shape_verified"])
        self.assertEqual(analysis["core_solving_degree"], 5)
        self.assertLessEqual(analysis["core_field_remainder_max_degree"], 3)
        self.assertLessEqual(analysis["mutant_degree_of_regularity"], 4)
        self.assertLessEqual(analysis["mutant_solving_degree"], 5)
        field = FiniteField(5, find_irreducible_modulus(5, 2))
        candidates = known_decomposition_candidates(
            field, 2, case["curve_a"], case["curve_b"], limit=2  # type: ignore[arg-type]
        )
        self.assertEqual(len({target for _, target in candidates}), len(candidates))

    def test_symbolic_quadratic_core_certificate(self) -> None:
        certificate = symbolic_certificate()
        self.assertEqual(certificate["basis_total_degrees"], [4, 4, 3, 3])
        self.assertEqual(
            certificate["semaev_delta_identity"],
            "-t1**2*(4*m0 - m1**2)/4",
        )
        self.assertEqual(
            certificate["coefficient_ring"],
            "ZZ[b,c,d,e,f,g,h,i][(c+g^2)^-1]",
        )
        self.assertTrue(certificate["explicit_localized_basis_identities"])
        self.assertEqual(certificate["buchberger_pairs_checked_symbolically"], 6)
        self.assertEqual(certificate["quartic_unit_minor_determinant"], -1)

    def test_actual_q7_semaev_system_has_redundant_field_equations(self) -> None:
        result = concrete_q7_certificate()
        self.assertTrue(result["curve_nonsingular"])
        self.assertTrue(result["target_is_on_curve"])
        self.assertTrue(result["target_x_is_nonbase"])
        self.assertEqual(result["field_equation_normal_forms"], ["0", "0"])
        self.assertEqual(result["quotient_dimension"], 8)
        self.assertEqual(len(result["base_field_core_zeros"]), 8)
        self.assertEqual(
            (
                result["first_fall_degree"],
                result["degree_of_regularity"],
                result["solving_degree_grevlex"],
            ),
            (5, 7, 5),
        )

    def test_symbolic_infinite_redundancy_family(self) -> None:
        result = symbolic_infinite_family_certificate()
        self.assertEqual(result["eight_symbolic_core_points_checked"], 8)
        self.assertIn("q == 3 mod 4", result["base_field_conditions"])

    def test_top_shape_alone_does_not_force_solving_degree_q(self) -> None:
        q = 5
        core = abstract_core(q, (3, 1, 4, 0, 1, 2, 0, 3))
        full = [*core, *field_equations(2, q)]
        basis, _ = sympy_groebner(full, 2, q)
        degree, _, _, _ = solving_degree_exact(
            full, basis, 2, q, q + 1, 100_000, 100_000
        )
        self.assertEqual(degree, q + 1)

    def test_quadratic_top_ideal_has_regularity_q(self) -> None:
        for q in (5, 7, 11):
            generators = [
                {(2, 2): 1},
                {(2, 1): 1, (1, 2): 1},
                *field_equations(2, q),
            ]
            regularity, _ = degree_of_regularity_exact(
                generators, 2, q, q, 100_000, 100_000
            )
            self.assertEqual(regularity, q)

    def test_general_first_fall_reproduces_toy_witness(self) -> None:
        generators = [
            {(1, 1, 0): 1, (0, 1, 0): 1},
            {(0, 2, 0): 1, (0, 0, 0): -1},
            {(0, 0, 4): 1, (0, 0, 0): -1},
            {(5, 0, 0): 1, (1, 0, 0): -1},
        ]
        degree, _ = first_fall_degree_exact(generators, 3, 5, 5, 10_000)
        self.assertEqual(degree, 3)

    def test_field_equations_have_expected_shape(self) -> None:
        equations = field_equations(2, 3)
        self.assertEqual(equations[0], {(3, 0): 1, (1, 0): -1})
        self.assertEqual(equations[1], {(0, 3): 1, (0, 1): -1})

    def test_small_case_completes_and_verifies_root(self) -> None:
        result = measure_case(3, 2, 2, "known", 10, 2_000, 5_000, 30.0)
        self.assertEqual(result["status"], "complete")
        self.assertTrue(result["known_solution_verified"])

    def test_q7_known_solution_is_a_strict_divergence(self) -> None:
        result = measure_case(7, 2, 2, "known", 10, 8_000, 30_000, 30.0)
        self.assertEqual(result["first_fall_degree"], 5)
        self.assertEqual(result["solving_degree"], 7)
        self.assertTrue(result["known_solution_verified"])


if __name__ == "__main__":
    unittest.main()
