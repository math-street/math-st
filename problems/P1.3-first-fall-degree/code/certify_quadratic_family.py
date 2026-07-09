"""Produce an exact symbolic certificate for the quadratic Semaev core.

Sub-goal: P1.3 / SG-09
Inputs: none
Outputs: data/certify_quadratic_family_<date>.json unless overridden
Runtime: under five seconds with SymPy 1.14.0
Validated against: exact fraction-field Groebner and polynomial identities
"""

from __future__ import annotations

import argparse
import itertools
import json
from datetime import date
from pathlib import Path

import sympy


def _localized_denominator_power(
    expression: sympy.Expr,
    delta: sympy.Expr,
    parameters: tuple[sympy.Symbol, ...],
) -> int:
    """Return k when expression lies in ZZ[parameters, delta^-1] with denominator delta^k."""
    cancelled = sympy.cancel(expression)
    _, denominator = sympy.fraction(cancelled)
    for power in range(8):
        ratio = sympy.cancel(denominator / delta**power)
        if ratio.free_symbols:
            continue
        cleared = sympy.cancel(cancelled * delta**power)
        cleared_numerator, cleared_denominator = sympy.fraction(cleared)
        if cleared_denominator.free_symbols or cleared_denominator == 0:
            continue
        polynomial = sympy.Poly(
            cleared_numerator / cleared_denominator,
            *parameters,
            domain=sympy.QQ,
        )
        if all(coefficient.q == 1 for coefficient in polynomial.coeffs()):
            return power
    raise AssertionError(f"coefficient is not in the expected localization: {expression}")


def symbolic_certificate() -> dict[str, object]:
    """Certify the universal core leading monomials and denominator condition."""
    x, y = sympy.symbols("x y")
    b, c, d, e, f, g, h, i = sympy.symbols("b c d e f g h i")
    symmetric_sum = x + y
    symmetric_product = x * y
    first = (
        symmetric_product**2
        + b * symmetric_product
        + c * symmetric_sum**2
        + d * symmetric_sum
        + e
    )
    second = (
        symmetric_product * symmetric_sum
        + f * symmetric_product
        + g * symmetric_sum**2
        + h * symmetric_sum
        + i
    )
    field = sympy.QQ.frac_field(b, c, d, e, f, g, h, i)
    basis = sympy.groebner(
        [first, second], x, y, order="grevlex", domain=field
    )
    basis_expressions = [item.as_expr() for item in basis.polys]
    delta_universal = c + g**2
    leading_monomials = [str(item.LM(order="grevlex")) for item in basis.polys]
    degrees = [item.total_degree() for item in basis.polys]
    denominator_factors: set[str] = set()
    for item in basis.polys:
        for coefficient in item.coeffs():
            _, denominator = sympy.fraction(coefficient.as_expr())
            if denominator != 1:
                denominator_factors.add(str(sympy.factor(denominator)))

    # These are explicit identities in ZZ[b,c,d,e,f,g,h,i][(c+g^2)^-1].
    # They prove that the fraction-field basis specializes over every field for
    # which delta_universal is nonzero, and they also record the precise
    # closed-Macaulay derivation used below.
    initial_degree_five_rows = [
        first,
        x * first,
        y * first,
        second,
        x * second,
        y * second,
        x**2 * second,
        x * y * second,
        y**2 * second,
    ]
    explicit_initial_representations = {
        0: -first - g * second + y * second,
        2: (
            f * first
            + x * first
            + y * first
            - (b + 3 * c + f * g + 3 * g**2 - h) * second
            + g * x * second
            + g * y * second
            - x * y * second
        )
        / delta_universal,
        3: second,
    }
    for index, representation in explicit_initial_representations.items():
        identity_numerator, _ = sympy.fraction(
            sympy.cancel(representation - basis_expressions[index])
        )
        assert sympy.Poly(
            identity_numerator, x, y, b, c, d, e, f, g, h, i, domain=sympy.QQ
        ).is_zero

    explicit_closed_representation_one = (
        (c + f * g + g**2) * first
        + g * x * first
        + g * y * first
        + (2 * c * g - d + f * g**2 + 2 * g**3 - g * h) * second
        - c * x * second
        + g**2 * y * second
        - g * x * y * second
    ) / delta_universal + y * basis_expressions[2]
    identity_numerator, _ = sympy.fraction(
        sympy.cancel(explicit_closed_representation_one - basis_expressions[1])
    )
    assert sympy.Poly(
        identity_numerator, x, y, b, c, d, e, f, g, h, i, domain=sympy.QQ
    ).is_zero

    localized_coefficients: list[sympy.Expr] = []
    for expression in [
        *basis_expressions,
        *explicit_initial_representations.values(),
        explicit_closed_representation_one,
    ]:
        localized_coefficients.extend(
            coefficient.as_expr()
            for coefficient in sympy.Poly(expression, x, y, domain=field).coeffs()
        )
    localized_denominator_powers = [
        _localized_denominator_power(
            coefficient, delta_universal, (b, c, d, e, f, g, h, i)
        )
        for coefficient in localized_coefficients
    ]

    # Buchberger's criterion is checked as polynomial identities in the same
    # localization, not by sampled specializations.
    buchberger_denominator_powers: list[int] = []
    for left_index, right_index in itertools.combinations(range(len(basis.polys)), 2):
        left = basis.polys[left_index]
        right = basis.polys[right_index]
        left_lm = left.LM(order="grevlex").exponents
        right_lm = right.LM(order="grevlex").exponents
        lcm = tuple(max(a, b_value) for a, b_value in zip(left_lm, right_lm))
        left_multiplier = x ** (lcm[0] - left_lm[0]) * y ** (lcm[1] - left_lm[1])
        right_multiplier = x ** (lcm[0] - right_lm[0]) * y ** (lcm[1] - right_lm[1])
        s_polynomial = sympy.expand(
            left_multiplier * left.as_expr() / left.LC(order="grevlex").as_expr()
            - right_multiplier * right.as_expr() / right.LC(order="grevlex").as_expr()
        )
        quotients, remainder = basis.reduce(s_polynomial)
        assert remainder == 0
        reduction_identity = sympy.cancel(
            s_polynomial
            - sum(
                quotient * item.as_expr()
                for quotient, item in zip(quotients, basis.polys, strict=True)
            )
        )
        identity_numerator, _ = sympy.fraction(reduction_identity)
        assert sympy.Poly(
            identity_numerator,
            x,
            y,
            b,
            c,
            d,
            e,
            f,
            g,
            h,
            i,
            domain=sympy.QQ,
        ).is_zero
        for quotient in quotients:
            for coefficient in sympy.Poly(quotient, x, y, domain=field).coeffs():
                buchberger_denominator_powers.append(
                    _localized_denominator_power(
                        coefficient.as_expr(),
                        delta_universal,
                        (b, c, d, e, f, g, h, i),
                    )
                )

    monomials = [
        x**x_degree * y**y_degree
        for total_degree in range(6)
        for x_degree in range(total_degree, -1, -1)
        for y_degree in [total_degree - x_degree]
    ]

    def coefficient_matrix(polynomials: list[sympy.Expr]):
        return sympy.polys.matrices.DomainMatrix.from_list_sympy(
            len(monomials),
            len(polynomials),
            [
                [
                    sympy.Poly(polynomial, x, y, domain=field).coeff_monomial(
                        monomial
                    )
                    for polynomial in polynomials
                ]
                for monomial in monomials
            ],
        ).to_field()

    initial_matrix = coefficient_matrix(initial_degree_five_rows)
    initially_contained_basis_indices = []
    for index, item in enumerate(basis.polys):
        target = coefficient_matrix([item.as_expr()])
        if initial_matrix.hstack(target).rank() == initial_matrix.rank():
            initially_contained_basis_indices.append(index)
    closure_rows = list(initial_degree_five_rows)
    for index in initially_contained_basis_indices:
        item = basis.polys[index]
        item_degree = item.total_degree()
        for multiplier_degree in range(5 - item_degree + 1):
            for x_degree in range(multiplier_degree, -1, -1):
                closure_rows.append(
                    x**x_degree
                    * y ** (multiplier_degree - x_degree)
                    * item.as_expr()
                )
    closure_matrix = coefficient_matrix(closure_rows)
    closed_degree_five_contains_basis = all(
        closure_matrix.hstack(coefficient_matrix([item.as_expr()])).rank()
        == closure_matrix.rank()
        for item in basis.polys
    )

    # The top parts of the four basis elements fill every quartic.  A unit
    # minor makes this valid after specialization in every characteristic,
    # including 3 and 5; it is stronger than merely listing leading monomials.
    quartic_monomials = [x**4, x**3 * y, x**2 * y**2, x * y**3, y**4]
    quartic_rows: list[list[sympy.Expr]] = []
    for item in basis.polys:
        item_degree = item.total_degree()
        top = sympy.Add(
            *[
                coefficient.as_expr() * x**monomial[0] * y**monomial[1]
                for monomial, coefficient in item.terms()
                if sum(monomial) == item_degree
            ]
        )
        for x_degree in range(4 - item_degree + 1):
            product = sympy.Poly(
                x**x_degree * y ** (4 - item_degree - x_degree) * top,
                x,
                y,
                domain=field,
            )
            quartic_rows.append(
                [product.coeff_monomial(monomial) for monomial in quartic_monomials]
            )
    quartic_matrix = sympy.Matrix(quartic_rows)
    unit_quartic_minor = next(
        (
            row_indices,
            int(determinant),
        )
        for row_indices in itertools.combinations(range(quartic_matrix.rows), 5)
        for determinant in [sympy.det(quartic_matrix[list(row_indices), :])]
        if determinant in (1, -1)
    )

    m0, m1, t0, t1 = sympy.symbols("m0 m1 t0 t1")
    curve_a0, curve_a1, curve_b0, curve_b1 = sympy.symbols(
        "curve_a0 curve_a1 curve_b0 curve_b1"
    )

    def extension_add(
        left: tuple[sympy.Expr, sympy.Expr],
        right: tuple[sympy.Expr, sympy.Expr],
    ) -> tuple[sympy.Expr, sympy.Expr]:
        return sympy.expand(left[0] + right[0]), sympy.expand(left[1] + right[1])

    def extension_scale(
        scalar: sympy.Expr, value: tuple[sympy.Expr, sympy.Expr]
    ) -> tuple[sympy.Expr, sympy.Expr]:
        return sympy.expand(scalar * value[0]), sympy.expand(scalar * value[1])

    def extension_multiply(
        left: tuple[sympy.Expr, sympy.Expr],
        right: tuple[sympy.Expr, sympy.Expr],
    ) -> tuple[sympy.Expr, sympy.Expr]:
        return (
            sympy.expand(left[0] * right[0] - m0 * left[1] * right[1]),
            sympy.expand(
                left[0] * right[1]
                + left[1] * right[0]
                - m1 * left[1] * right[1]
            ),
        )

    symmetric_sum_symbol, symmetric_product_symbol = sympy.symbols(
        "symmetric_sum symmetric_product"
    )
    target = (t0, t1)
    curve_a = (curve_a0, curve_a1)
    curve_b = (curve_b0, curve_b1)
    target_squared = extension_multiply(target, target)
    semaev_coordinates = extension_scale(
        symmetric_sum_symbol**2 - 4 * symmetric_product_symbol, target_squared
    )
    semaev_coordinates = extension_add(
        semaev_coordinates,
        extension_scale(
            -2,
            extension_multiply(
                extension_scale(
                    symmetric_sum_symbol,
                    extension_add(
                        (symmetric_product_symbol, sympy.Integer(0)), curve_a
                    ),
                ),
                target,
            ),
        ),
    )
    semaev_coordinates = extension_add(
        semaev_coordinates,
        extension_scale(-4, extension_multiply(curve_b, target)),
    )
    p_minus_a = (
        symmetric_product_symbol - curve_a0,
        -curve_a1,
    )
    semaev_coordinates = extension_add(
        semaev_coordinates, extension_multiply(p_minus_a, p_minus_a)
    )
    semaev_coordinates = extension_add(
        semaev_coordinates, extension_scale(-4 * symmetric_sum_symbol, curve_b)
    )

    normalized_second = sympy.expand(semaev_coordinates[1] / (-2 * t1))
    normalized_first = sympy.expand(
        semaev_coordinates[0] - (t0 / t1) * semaev_coordinates[1]
    )
    normalized_g = (m1 * t1 - 2 * t0) / 2
    normalized_c = -m0 * t1**2 - t0**2 + m1 * t0 * t1
    assert (
        sympy.Poly(
            normalized_second, symmetric_product_symbol, symmetric_sum_symbol
        ).coeff_monomial(symmetric_product_symbol * symmetric_sum_symbol)
        == 1
    )
    assert sympy.simplify(
        sympy.Poly(
            normalized_second, symmetric_product_symbol, symmetric_sum_symbol
        ).coeff_monomial(symmetric_sum_symbol**2)
        - normalized_g
    ) == 0
    assert (
        sympy.Poly(
            normalized_first, symmetric_product_symbol, symmetric_sum_symbol
        ).coeff_monomial(symmetric_product_symbol**2)
        == 1
    )
    assert sympy.simplify(
        sympy.Poly(
            normalized_first, symmetric_product_symbol, symmetric_sum_symbol
        ).coeff_monomial(symmetric_product_symbol * symmetric_sum_symbol)
    ) == 0
    assert sympy.simplify(
        sympy.Poly(
            normalized_first, symmetric_product_symbol, symmetric_sum_symbol
        ).coeff_monomial(symmetric_sum_symbol**2)
        - normalized_c
    ) == 0
    delta = sympy.factor(normalized_c + normalized_g**2)
    expected_delta = sympy.factor((m1**2 - 4 * m0) * t1**2 / 4)

    assert leading_monomials == [
        "x**1*y**3",
        "x**0*y**4",
        "x**3*y**0",
        "x**2*y**1",
    ]
    assert degrees == [4, 4, 3, 3]
    assert denominator_factors == {"c + g**2"}
    assert initially_contained_basis_indices == [0, 2, 3]
    assert closed_degree_five_contains_basis
    assert max(localized_denominator_powers, default=0) <= 1
    assert max(buchberger_denominator_powers, default=0) <= 3
    assert unit_quartic_minor[1] in (1, -1)
    assert sympy.expand(delta - expected_delta) == 0

    t, auxiliary = sympy.symbols("t auxiliary")
    representative_homogeneous_generators = [
        -t**4
        + 2 * t**3 * x
        + 2 * t**3 * y
        - t**2 * x**2
        + 2 * t**2 * x * y
        - t**2 * y**2
        + x**2 * y**2,
        -t**3
        + 2 * t**2 * x
        + 2 * t**2 * y
        - t * x**2
        - t * y**2
        - 2 * x**2 * y
        - 2 * x * y**2,
        x**5 - x * t**4,
        y**5 - y * t**4,
    ]
    representative_ideal = sympy.groebner(
        representative_homogeneous_generators,
        auxiliary,
        x,
        y,
        t,
        order="lex",
        modulus=5,
    )
    saturation_basis = sympy.groebner(
        [*representative_homogeneous_generators, 1 - auxiliary * t],
        auxiliary,
        x,
        y,
        t,
        order="lex",
        modulus=5,
    )
    saturation_new_elements = []
    for item in saturation_basis.polys:
        expression = item.as_expr()
        if expression.has(auxiliary):
            continue
        remainder = sympy.expand(representative_ideal.reduce(expression)[1])
        if remainder != 0:
            saturation_new_elements.append(str(expression))
    assert saturation_new_elements == ["-t + x + y", "-t*y + y**2"]
    return {
        "status": "exact symbolic certificate passed",
        "engine": "SymPy exact fraction-field Groebner basis",
        "engine_version": sympy.__version__,
        "coefficient_ring": "ZZ[b,c,d,e,f,g,h,i][(c+g^2)^-1]",
        "normalized_generators": [str(sympy.expand(first)), str(sympy.expand(second))],
        "basis_leading_monomials_grevlex_x_gt_y": leading_monomials,
        "basis_total_degrees": degrees,
        "nonconstant_denominator_factors": sorted(denominator_factors),
        "basis_indices_in_initial_degree_five_macaulay_span": (
            initially_contained_basis_indices
        ),
        "closed_degree_five_contains_entire_basis": (
            closed_degree_five_contains_basis
        ),
        "explicit_localized_basis_identities": True,
        "buchberger_pairs_checked_symbolically": 6,
        "maximum_buchberger_denominator_power": max(
            buchberger_denominator_powers, default=0
        ),
        "quartic_top_part_rank": quartic_matrix.rank(),
        "quartic_unit_minor_rows_zero_based": list(unit_quartic_minor[0]),
        "quartic_unit_minor_determinant": unit_quartic_minor[1],
        "semaev_delta_identity": str(delta),
        "representative_raw_homogenization_t_saturated": False,
        "representative_saturation_new_elements": saturation_new_elements,
        "interpretation": (
            "For an irreducible odd-characteristic quadratic modulus and "
            "a non-base target, the discriminant and t1 are nonzero, so the "
            "four-polynomial core basis specializes without a denominator pole."
        ),
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
        / f"certify_quadratic_family_{date.today():%Y%m%d}.json"
    )
    result = symbolic_certificate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"wrote certificate to {output}")


if __name__ == "__main__":
    main()
