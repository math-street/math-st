"""Certify a genuine quadratic Semaev field-equation counterexample.

Sub-goal: P1.3 / SG-11
Inputs: none
Outputs: data/certify_quadratic_field_equations_<date>.json unless overridden
Runtime: under two seconds with SymPy 1.14.0
Validated against: symbolic family identities, exact normal forms, and closed spaces
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import sympy

from measure_toy_degrees import closed_macaulay_space, in_rowspace, polynomial_degree
from measure_weil_degrees import (
    degree_of_regularity_exact,
    field_equations,
    first_fall_degree_exact,
    solving_degree_exact,
    sympy_groebner,
)
from sparse_weil import (
    FiniteField,
    PrimePolynomial,
    build_weil_coordinate_system,
    curve_is_nonsingular,
    evaluate_prime_polynomial,
    find_irreducible_modulus,
)


def _expression(
    polynomial: PrimePolynomial, variables: tuple[sympy.Symbol, sympy.Symbol]
) -> sympy.Expr:
    return sympy.expand(
        sum(
            coefficient
            * variables[0] ** monomial[0]
            * variables[1] ** monomial[1]
            for monomial, coefficient in polynomial.items()
        )
    )


def _assert_rational_identity(expression: sympy.Expr) -> None:
    numerator, _ = sympy.fraction(sympy.cancel(expression))
    assert sympy.expand(numerator) == 0


def symbolic_infinite_family_certificate() -> dict[str, object]:
    """Check the identities for the counterexample family over q = 3 mod 4."""
    h, u, x, y = sympy.symbols("h u x y")
    rho = (h + 1 / h) / 2
    sigma = (1 / h - h) / 2
    curve_a = -4 * sigma**2
    target_x = 2 * u
    target_y = 2 * rho * (1 - u)

    # Work in ZZ[1/2,h,h^-1,u]/(u^2+1).  Clearing the Laurent
    # denominators before the remainder check makes the coefficient ring explicit.
    curve_identity = sympy.cancel(
        target_y**2 - (target_x**3 + curve_a * target_x)
    )
    numerator, denominator = sympy.fraction(curve_identity)
    assert not denominator.has(u)
    remainder = sympy.rem(
        sympy.Poly(numerator, u, domain=sympy.QQ.frac_field(h)),
        sympy.Poly(u**2 + 1, u, domain=sympy.QQ.frac_field(h)),
    )
    assert remainder.is_zero
    _assert_rational_identity(rho**2 - sigma**2 - 1)

    core_zero = (x * y - curve_a) ** 2 - 4 * (x - y) ** 2
    core_one = (x + y) * (x * y + curve_a)
    anti_diagonal_values = [
        2 * (1 + rho),
        -2 * (1 + rho),
        2 * (1 - rho),
        -2 * (1 - rho),
    ]
    points = [(value, -value) for value in anti_diagonal_values]
    second_left = 2 * sigma * (rho + sigma)
    second_right = 2 * sigma * (rho - sigma)
    points.extend(
        [
            (second_left, second_right),
            (second_right, second_left),
            (-second_left, -second_right),
            (-second_right, -second_left),
        ]
    )
    for point_x, point_y in points:
        _assert_rational_identity(core_zero.subs({x: point_x, y: point_y}))
        _assert_rational_identity(core_one.subs({x: point_x, y: point_y}))

    # These factorizations are the exact noncollision conditions used in the proof.
    factorizations = {
        "rho": sympy.factor(rho),
        "sigma": sympy.factor(sigma),
        "one_plus_rho": sympy.factor(1 + rho),
        "one_minus_rho": sympy.factor(1 - rho),
        "second_branch_discriminant": sympy.factor(
            (4 * sigma * rho) ** 2 - 4 * (4 * sigma**2)
        ),
    }
    expected_factorizations = {
        "rho": (h**2 + 1) / (2 * h),
        "sigma": -(h - 1) * (h + 1) / (2 * h),
        "one_plus_rho": (h + 1) ** 2 / (2 * h),
        "one_minus_rho": -(h - 1) ** 2 / (2 * h),
        "second_branch_discriminant": (h - 1) ** 4 * (h + 1) ** 4 / h**4,
    }
    for key, value in factorizations.items():
        _assert_rational_identity(value - expected_factorizations[key])
    return {
        "coefficient_ring": "ZZ[1/2,h,h^-1,u]/(u^2+1)",
        "base_field_conditions": "q == 3 mod 4, q >= 7, h != 0,+1,-1",
        "curve_a": str(sympy.factor(curve_a)),
        "curve_b": "0",
        "target_point": [str(target_x), str(sympy.factor(target_y))],
        "eight_symbolic_core_points_checked": len(points),
        "noncollision_factorizations": {
            key: str(value) for key, value in factorizations.items()
        },
    }


def _multiplication_matrix(
    groebner_basis: sympy.GroebnerBasis,
    multiplier: sympy.Symbol,
    standard_monomials: list[sympy.Expr],
    variables: tuple[sympy.Symbol, sympy.Symbol],
    modulus: int,
) -> sympy.Matrix:
    columns: list[list[int]] = []
    for monomial in standard_monomials:
        remainder = sympy.Poly(
            groebner_basis.reduce(multiplier * monomial)[1],
            *variables,
            modulus=modulus,
        )
        columns.append(
            [int(remainder.coeff_monomial(item)) % modulus for item in standard_monomials]
        )
    return sympy.Matrix(columns).T.applyfunc(lambda value: int(value) % modulus)


def concrete_q7_certificate() -> dict[str, object]:
    """Verify every hypothesis, ideal statement, and degree for the q=7 example."""
    q = 7
    curve_a = (3, 0)
    curve_b = (0, 0)
    target_x = (0, 2)
    target_y = (6, 1)
    field = FiniteField(q, find_irreducible_modulus(q, 2))
    assert field.modulus == (1, 0, 1)
    assert curve_is_nonsingular(field, curve_a, curve_b)
    target_rhs = field.add(
        field.add(
            field.mul(field.mul(target_x, target_x), target_x),
            field.mul(curve_a, target_x),
        ),
        curve_b,
    )
    assert field.mul(target_y, target_y) == target_rhs

    _, coordinates, _ = build_weil_coordinate_system(
        q, 2, 2, target_x, curve_a, curve_b
    )
    core = [polynomial for polynomial in coordinates if polynomial]
    expected_core = [
        {(2, 2): 1, (2, 0): 3, (1, 1): 2, (0, 2): 3, (0, 0): 2},
        {(2, 1): 3, (1, 2): 3, (1, 0): 2, (0, 1): 2},
    ]
    assert core == expected_core

    x, y = sympy.symbols("x y")
    variables = (x, y)
    basis = sympy.groebner(
        [_expression(polynomial, variables) for polynomial in core],
        *variables,
        modulus=q,
        order="grevlex",
    )
    leading_monomials = [str(item.LM(order="grevlex")) for item in basis.polys]
    assert leading_monomials == [
        "x**1*y**3",
        "x**0*y**4",
        "x**3*y**0",
        "x**2*y**1",
    ]
    remainders = [sympy.expand(basis.reduce(variable**q - variable)[1]) for variable in variables]
    assert remainders == [0, 0]

    zeros = [
        (value_x, value_y)
        for value_x in range(q)
        for value_y in range(q)
        if all(
            evaluate_prime_polynomial(polynomial, (value_x, value_y), q) == 0
            for polynomial in core
        )
    ]
    assert zeros == [
        (1, 4),
        (1, 6),
        (3, 4),
        (3, 6),
        (4, 1),
        (4, 3),
        (6, 1),
        (6, 3),
    ]

    standard_monomials = [1, y, y**2, y**3, x, x * y, x * y**2, x**2]
    multiplication_x = _multiplication_matrix(
        basis, x, standard_monomials, variables, q
    )
    multiplication_y = _multiplication_matrix(
        basis, y, standard_monomials, variables, q
    )
    assert (multiplication_x**q - multiplication_x).applyfunc(
        lambda value: int(value) % q
    ).is_zero_matrix
    assert (multiplication_y**q - multiplication_y).applyfunc(
        lambda value: int(value) % q
    ).is_zero_matrix

    full = [*core, *field_equations(2, q)]
    target_basis, target_basis_text = sympy_groebner(full, 2, q)
    first_fall, _ = first_fall_degree_exact(core, 2, q, 5, 10_000)
    regularity, _ = degree_of_regularity_exact(
        full, 2, q, q, 100_000, 100_000
    )
    solving_degree, _, _, _ = solving_degree_exact(
        full, target_basis, 2, q, q, 100_000, 100_000
    )
    assert (first_fall, regularity, solving_degree) == (5, 7, 5)

    degree_four_space = closed_macaulay_space(core, 2, 4, q)
    degree_five_space = closed_macaulay_space(core, 2, 5, q)
    degree_four_membership = [
        polynomial_degree(item) <= 4
        and in_rowspace(
            item, degree_four_space.rows, degree_four_space.columns, q
        )
        for item in target_basis
    ]
    assert degree_four_membership == [True, False, False, True]
    assert all(
        in_rowspace(item, degree_five_space.rows, degree_five_space.columns, q)
        for item in target_basis
    )

    return {
        "q": q,
        "quadratic_modulus": list(field.modulus),
        "curve": "Y^2 = X^3 + 3*X",
        "curve_nonsingular": True,
        "target_point_coordinates": [list(target_x), list(target_y)],
        "target_is_on_curve": True,
        "target_x_is_nonbase": True,
        "core_generators": [str(_expression(item, variables)) for item in core],
        "core_groebner_basis": target_basis_text,
        "leading_monomials": leading_monomials,
        "quotient_dimension": len(standard_monomials),
        "base_field_core_zeros": [list(point) for point in zeros],
        "field_equation_normal_forms": [str(item) for item in remainders],
        "q_frobenius_is_identity": True,
        "first_fall_degree": first_fall,
        "degree_of_regularity": regularity,
        "solving_degree_grevlex": solving_degree,
        "degree_four_closed_space_rank": degree_four_space.rank,
        "degree_four_groebner_membership": degree_four_membership,
        "degree_five_closed_space_contains_basis": True,
    }


def certificate() -> dict[str, object]:
    return {
        "status": "exact symbolic and finite-field counterexample certificate passed",
        "engine": "SymPy exact identities + exact F_7 closed Macaulay spaces",
        "engine_version": sympy.__version__,
        "infinite_family": symbolic_infinite_family_certificate(),
        "concrete_counterexample": concrete_q7_certificate(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"certify_quadratic_field_equations_{date.today():%Y%m%d}.json"
    )
    result = certificate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"wrote certificate to {output}")


if __name__ == "__main__":
    main()
