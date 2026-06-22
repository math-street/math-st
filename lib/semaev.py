"""Semaev summation-polynomial evaluation for short-Weierstrass curves."""

from __future__ import annotations

from collections.abc import Sequence


def f3_coefficients(x1: int, x2: int, a: int, b: int, p: int) -> tuple[int, int, int]:
    """Return A,B,C for f3(x1,x2,z) = A*z^2 + B*z + C over F_p."""
    x1 %= p
    x2 %= p
    a %= p
    b %= p
    leading = (x1 - x2) ** 2
    linear = -2 * ((x1 + x2) * (x1 * x2 + a) + 2 * b)
    constant = (x1 * x2 - a) ** 2 - 4 * b * (x1 + x2)
    return leading % p, linear % p, constant % p


def f3_value(x1: int, x2: int, x3: int, a: int, b: int, p: int) -> int:
    """Evaluate the third summation polynomial modulo p."""
    leading, linear, constant = f3_coefficients(x1, x2, a, b, p)
    return (leading * x3 * x3 + linear * x3 + constant) % p


def quadratic_resultant(
    first: tuple[int, int, int], second: tuple[int, int, int], p: int
) -> int:
    """Return Res(Az^2+Bz+C, Dz^2+Ez+F) modulo p."""
    aa, bb, cc = first
    dd, ee, ff = second
    return ((aa * ff - cc * dd) ** 2 - (aa * ee - bb * dd) * (bb * ff - cc * ee)) % p


def f4_value(x1: int, x2: int, x3: int, x4: int, a: int, b: int, p: int) -> int:
    """Evaluate f4 as Res_z(f3(x1,x2,z), f3(x3,x4,z))."""
    first = f3_coefficients(x1, x2, a, b, p)
    second = f3_coefficients(x3, x4, a, b, p)
    return quadratic_resultant(first, second, p)


def _interpolate(values: Sequence[int], p: int) -> list[int]:
    """Interpolate values at 0,1,... into ascending coefficients modulo p."""
    result = [0] * len(values)
    for i, value in enumerate(values):
        basis = [1]
        denominator = 1
        for j in range(len(values)):
            if i == j:
                continue
            next_basis = [0] * (len(basis) + 1)
            for degree, coefficient in enumerate(basis):
                next_basis[degree] = (next_basis[degree] - j * coefficient) % p
                next_basis[degree + 1] = (next_basis[degree + 1] + coefficient) % p
            basis = next_basis
            denominator = denominator * (i - j) % p
        scale = value * pow(denominator, p - 2, p) % p
        for degree, coefficient in enumerate(basis):
            result[degree] = (result[degree] + scale * coefficient) % p
    return result


def _determinant_mod(matrix: list[list[int]], p: int) -> int:
    """Compute a square-matrix determinant by modular elimination."""
    work = [[entry % p for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % p
        inverse = pow(pivot_value, p - 2, p)
        for row in range(column + 1, len(work)):
            if work[row][column] == 0:
                continue
            factor = work[row][column] * inverse % p
            for index in range(column, len(work)):
                work[row][index] = (work[row][index] - factor * work[column][index]) % p
    return determinant % p


def polynomial_resultant(first: Sequence[int], second: Sequence[int], p: int) -> int:
    """Return the resultant using degrees declared by the coefficient lengths."""
    first = list(first)
    second = list(second)
    m = len(first) - 1
    n = len(second) - 1
    if m == 0:
        return pow(first[0], n, p)
    if n == 0:
        return pow(second[0], m, p)
    first_desc = list(reversed(first))
    second_desc = list(reversed(second))
    size = m + n
    matrix = [[0] * size for _ in range(size)]
    for row in range(n):
        matrix[row][row : row + m + 1] = first_desc
    for row in range(m):
        matrix[n + row][row : row + n + 1] = second_desc
    return _determinant_mod(matrix, p)


def f5_value(
    x1: int, x2: int, x3: int, x4: int, x5: int, a: int, b: int, p: int
) -> int:
    """Evaluate f5 using its recursive resultant definition."""
    if p <= 5:
        raise ValueError("f5 interpolation requires p > 5")
    f4_samples = [f4_value(x1, x2, x3, z, a, b, p) for z in range(5)]
    f4_coefficients = _interpolate(f4_samples, p)
    f3_descending = f3_coefficients(x4, x5, a, b, p)
    f3_ascending = list(reversed(f3_descending))
    return polynomial_resultant(f4_coefficients, f3_ascending, p)


def f6_value(
    x1: int,
    x2: int,
    x3: int,
    x4: int,
    x5: int,
    x6: int,
    a: int,
    b: int,
    p: int,
) -> int:
    """Evaluate f6 using Res_z(f5(x1,x2,x3,x4,z), f3(x5,x6,z))."""
    if p <= 8:
        raise ValueError("f6 interpolation requires p > 8")
    f5_samples = [f5_value(x1, x2, x3, x4, z, a, b, p) for z in range(9)]
    f5_coefficients = _interpolate(f5_samples, p)
    f3_descending = f3_coefficients(x5, x6, a, b, p)
    f3_ascending = list(reversed(f3_descending))
    return polynomial_resultant(f5_coefficients, f3_ascending, p)
