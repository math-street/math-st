"""Toy-scale arithmetic for ideals in a maximal order of ``B_{p,infinity}``.

The implementation is deliberately narrow: it supports primes ``p == 3 mod 4``
and the order with basis ``1, i, (1+j)/2, (i+ij)/2`` in ``(-1, -p)``.
All algebraic checks use exact integer or rational arithmetic.  It is intended
for the P3.3 experiments, not as a production KLPT implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt, lcm
from random import Random
from typing import Iterable, Sequence

from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form


def _fraction(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def _modular_sqrt(value: int, prime: int) -> int | None:
    """Return a square root modulo an odd prime, or ``None`` if absent."""

    value %= prime
    if value == 0:
        return 0
    if pow(value, (prime - 1) // 2, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(value, (prime + 1) // 4, prime)
    exponent = prime - 1
    power_of_two = 0
    while exponent % 2 == 0:
        power_of_two += 1
        exponent //= 2
    nonresidue = 2
    while pow(nonresidue, (prime - 1) // 2, prime) != prime - 1:
        nonresidue += 1
    root = pow(value, (exponent + 1) // 2, prime)
    residue_power = pow(value, exponent, prime)
    correction = pow(nonresidue, exponent, prime)
    order_power = power_of_two
    while residue_power != 1:
        index = 1
        squared = residue_power * residue_power % prime
        while squared != 1:
            squared = squared * squared % prime
            index += 1
            if index == order_power:
                raise ArithmeticError("Tonelli--Shanks failed to converge")
        factor = pow(correction, 1 << (order_power - index - 1), prime)
        root = root * factor % prime
        correction = factor * factor % prime
        residue_power = residue_power * correction % prime
        order_power = index
    if root * root % prime != value:
        raise ArithmeticError("invalid modular square root")
    return root


def _nearest_integer(value: Fraction) -> int:
    """Return a nearest integer, resolving half ties toward positive infinity."""

    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def _row_hnf(generators: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Return a canonical row basis for the lattice spanned by ``generators``."""

    matrix = Matrix(generators)
    if matrix.cols != 4 or matrix.rank() != 4:
        raise ValueError("ideal generators must span a rank-4 lattice")
    column_hnf = hermite_normal_form(matrix.T)
    if column_hnf.shape != (4, 4):
        raise ValueError("unexpected Hermite normal form shape")
    return tuple(
        tuple(int(column_hnf[col, row]) for col in range(4))
        for row in range(4)
    )


def _matrix_det(rows: Sequence[Sequence[int]]) -> int:
    return int(Matrix(rows).det())


def _linear_combination(
    coefficients: Sequence[int], rows: Sequence[Sequence[int]]
) -> tuple[int, ...]:
    return tuple(
        sum(coefficients[row] * rows[row][col] for row in range(4))
        for col in range(4)
    )


def _ldl_decomposition(
    gram: Sequence[Sequence[int]],
) -> tuple[list[list[Fraction]], list[Fraction]]:
    dimension = len(gram)
    lower = [
        [Fraction(int(row == col)) for col in range(dimension)]
        for row in range(dimension)
    ]
    diagonal: list[Fraction] = []
    for row in range(dimension):
        value = Fraction(gram[row][row])
        for prior in range(row):
            value -= lower[row][prior] * lower[row][prior] * diagonal[prior]
        if value <= 0:
            raise ValueError("Gram matrix is not positive definite")
        diagonal.append(value)
        for later in range(row + 1, dimension):
            numerator = Fraction(gram[later][row])
            for prior in range(row):
                numerator -= (
                    lower[later][prior]
                    * lower[row][prior]
                    * diagonal[prior]
                )
            lower[later][row] = numerator / value
    return lower, diagonal


def _ellipsoid_coefficients(
    gram: Sequence[Sequence[int]],
    quadratic_bound: int,
    max_candidates: int | None = None,
) -> Iterable[tuple[int, ...]]:
    """Yield every integer vector with ``c^T gram c <= quadratic_bound``."""

    lower, diagonal = _ldl_decomposition(gram)
    dimension = len(gram)
    coefficients = [0] * dimension
    emitted = 0

    def recurse(index: int, remaining: Fraction) -> Iterable[tuple[int, ...]]:
        nonlocal emitted
        if index < 0:
            emitted += 1
            if max_candidates is not None and emitted > max_candidates:
                raise RuntimeError(
                    f"ellipsoid contains more than {max_candidates} tuples"
                )
            yield tuple(coefficients)
            return
        offset = sum(
            lower[later][index] * coefficients[later]
            for later in range(index + 1, dimension)
        )
        squared_radius = remaining / diagonal[index]
        if squared_radius < 0:
            return
        radius = isqrt(squared_radius.numerator // squared_radius.denominator) + 2
        center = -offset
        center_floor = center.numerator // center.denominator
        for value in range(center_floor - radius, center_floor + radius + 1):
            shifted = Fraction(value) + offset
            cost = diagonal[index] * shifted * shifted
            if cost <= remaining:
                coefficients[index] = value
                yield from recurse(index - 1, remaining - cost)

    yield from recurse(dimension - 1, Fraction(quadratic_bound))


def _ellipsoid_coefficients_vectorized(
    gram: Sequence[Sequence[int]],
    bounds: Sequence[int],
    quadratic_bound: int,
    max_candidates: int | None = None,
) -> Iterable[tuple[int, ...]]:
    """Exact int64 enumeration of an inverse-Gram certified coefficient box."""

    import numpy as np

    max_coefficient = max(bounds)
    max_gram = max(abs(value) for row in gram for value in row)
    conservative_magnitude = 16 * max_gram * max_coefficient * max_coefficient
    if conservative_magnitude >= 1 << 62:
        yield from _ellipsoid_coefficients(gram, quadratic_bound, max_candidates)
        return
    values2, values3 = np.meshgrid(
        np.arange(-bounds[2], bounds[2] + 1, dtype=np.int64),
        np.arange(-bounds[3], bounds[3] + 1, dtype=np.int64),
        indexing="ij",
    )
    coefficient2 = values2.ravel()
    coefficient3 = values3.ravel()
    tail_quadratic = (
        gram[2][2] * coefficient2 * coefficient2
        + 2 * gram[2][3] * coefficient2 * coefficient3
        + gram[3][3] * coefficient3 * coefficient3
    )
    emitted = 0
    for coefficient0 in range(-bounds[0], bounds[0] + 1):
        for coefficient1 in range(-bounds[1], bounds[1] + 1):
            fixed = (
                gram[0][0] * coefficient0 * coefficient0
                + 2 * gram[0][1] * coefficient0 * coefficient1
                + gram[1][1] * coefficient1 * coefficient1
            )
            quadratic = (
                tail_quadratic
                + fixed
                + 2
                * coefficient2
                * (gram[0][2] * coefficient0 + gram[1][2] * coefficient1)
                + 2
                * coefficient3
                * (gram[0][3] * coefficient0 + gram[1][3] * coefficient1)
            )
            for index in np.flatnonzero(quadratic <= quadratic_bound):
                emitted += 1
                if max_candidates is not None and emitted > max_candidates:
                    raise RuntimeError(
                        f"ellipsoid contains more than {max_candidates} tuples"
                    )
                yield (
                    coefficient0,
                    coefficient1,
                    int(coefficient2[index]),
                    int(coefficient3[index]),
                )


def _normalized_spectrum_vectorized(
    ideal: IntegralIdeal,
    reduced_basis: Sequence[Sequence[int]],
    gram: Sequence[Sequence[int]],
    bounds: Sequence[int],
    quadratic_bound: int,
    max_candidates: int | None,
) -> tuple[dict[int, tuple[int, ...]], int] | None:
    """Return exact witnesses using int64 batches, or ``None`` if unsafe."""

    import numpy as np

    max_coefficient = max(bounds)
    max_gram = max(abs(value) for row in gram for value in row)
    conservative_magnitude = 16 * max_gram * max_coefficient * max_coefficient
    if conservative_magnitude >= 1 << 62:
        return None
    values2, values3 = np.meshgrid(
        np.arange(-bounds[2], bounds[2] + 1, dtype=np.int64),
        np.arange(-bounds[3], bounds[3] + 1, dtype=np.int64),
        indexing="ij",
    )
    coefficient2 = values2.ravel()
    coefficient3 = values3.ravel()
    tail_quadratic = (
        gram[2][2] * coefficient2 * coefficient2
        + 2 * gram[2][3] * coefficient2 * coefficient3
        + gram[3][3] * coefficient3 * coefficient3
    )
    divisor = 2 * ideal.norm
    witnesses: dict[int, tuple[int, ...]] = {}
    candidates_checked = 0
    for coefficient0 in range(-bounds[0], bounds[0] + 1):
        for coefficient1 in range(-bounds[1], bounds[1] + 1):
            fixed = (
                gram[0][0] * coefficient0 * coefficient0
                + 2 * gram[0][1] * coefficient0 * coefficient1
                + gram[1][1] * coefficient1 * coefficient1
            )
            quadratic = (
                tail_quadratic
                + fixed
                + 2
                * coefficient2
                * (gram[0][2] * coefficient0 + gram[1][2] * coefficient1)
                + 2
                * coefficient3
                * (gram[0][3] * coefficient0 + gram[1][3] * coefficient1)
            )
            valid_indices = np.flatnonzero(quadratic <= quadratic_bound)
            if coefficient0 == 0 and coefficient1 == 0:
                valid_indices = valid_indices[
                    (coefficient2[valid_indices] != 0)
                    | (coefficient3[valid_indices] != 0)
                ]
            candidates_checked += int(valid_indices.size)
            if max_candidates is not None and candidates_checked > max_candidates:
                raise RuntimeError(
                    f"ellipsoid contains more than {max_candidates} tuples"
                )
            if not valid_indices.size:
                continue
            valid_quadratic = quadratic[valid_indices]
            if np.any(valid_quadratic % divisor):
                raise ArithmeticError("ideal norm divisibility failed in batch")
            normalized = valid_quadratic // divisor
            unique_norms, first_positions = np.unique(normalized, return_index=True)
            for normalized_norm, position in zip(unique_norms, first_positions):
                index = int(valid_indices[int(position)])
                coefficients = (
                    coefficient0,
                    coefficient1,
                    int(coefficient2[index]),
                    int(coefficient3[index]),
                )
                vector = _linear_combination(coefficients, reduced_basis)
                norm = int(normalized_norm)
                if ideal.order.norm(vector) != norm * ideal.norm:
                    raise ArithmeticError("vectorized spectrum witness failed")
                previous = witnesses.get(norm)
                if previous is None or vector < previous:
                    witnesses[norm] = vector
    return witnesses, candidates_checked


@dataclass(frozen=True)
class Quaternion:
    """Element ``a + b*i + c*j + d*ij`` of ``(-1, -p)``."""

    p: int
    a: Fraction
    b: Fraction
    c: Fraction
    d: Fraction

    def __init__(
        self,
        p: int,
        a: int | Fraction = 0,
        b: int | Fraction = 0,
        c: int | Fraction = 0,
        d: int | Fraction = 0,
    ) -> None:
        object.__setattr__(self, "p", p)
        object.__setattr__(self, "a", _fraction(a))
        object.__setattr__(self, "b", _fraction(b))
        object.__setattr__(self, "c", _fraction(c))
        object.__setattr__(self, "d", _fraction(d))

    def __add__(self, other: Quaternion) -> Quaternion:
        self._check_same_algebra(other)
        return Quaternion(
            self.p,
            self.a + other.a,
            self.b + other.b,
            self.c + other.c,
            self.d + other.d,
        )

    def __sub__(self, other: Quaternion) -> Quaternion:
        return self + (-other)

    def __neg__(self) -> Quaternion:
        return Quaternion(self.p, -self.a, -self.b, -self.c, -self.d)

    def __mul__(self, other: Quaternion | int | Fraction) -> Quaternion:
        if not isinstance(other, Quaternion):
            scalar = _fraction(other)
            return Quaternion(
                self.p,
                scalar * self.a,
                scalar * self.b,
                scalar * self.c,
                scalar * self.d,
            )
        self._check_same_algebra(other)
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = other.a, other.b, other.c, other.d
        return Quaternion(
            self.p,
            a * e - b * f - self.p * c * g - self.p * d * h,
            a * f + b * e + self.p * (c * h - d * g),
            a * g + c * e - b * h + d * f,
            a * h + d * e + b * g - c * f,
        )

    def __rmul__(self, other: int | Fraction) -> Quaternion:
        return self * other

    def __truediv__(self, divisor: int | Fraction) -> Quaternion:
        return self * (Fraction(1) / _fraction(divisor))

    def conjugate(self) -> Quaternion:
        return Quaternion(self.p, self.a, -self.b, -self.c, -self.d)

    def reduced_trace(self) -> Fraction:
        return 2 * self.a

    def reduced_norm(self) -> Fraction:
        return (
            self.a * self.a
            + self.b * self.b
            + self.p * self.c * self.c
            + self.p * self.d * self.d
        )

    def _check_same_algebra(self, other: Quaternion) -> None:
        if self.p != other.p:
            raise ValueError("quaternions belong to different algebras")


class MaximalOrder:
    """The standard maximal order used by the toy P3.3 experiment."""

    def __init__(self, p: int) -> None:
        if not _is_prime(p) or p % 4 != 3:
            raise ValueError("p must be a prime congruent to 3 modulo 4")
        self.p = p
        self.basis = (
            Quaternion(p, 1),
            Quaternion(p, 0, 1),
            Quaternion(p, Fraction(1, 2), 0, Fraction(1, 2)),
            Quaternion(p, 0, Fraction(1, 2), 0, Fraction(1, 2)),
        )

    @property
    def doubled_norm_gram(self) -> tuple[tuple[int, ...], ...]:
        diagonal = (self.p + 1) // 2
        return (
            (2, 0, 1, 0),
            (0, 2, 0, 1),
            (1, 0, diagonal, 0),
            (0, 1, 0, diagonal),
        )

    def element(self, coordinates: Sequence[int | Fraction]) -> Quaternion:
        if len(coordinates) != 4:
            raise ValueError("order coordinates must have length four")
        result = Quaternion(self.p)
        for coefficient, basis_element in zip(coordinates, self.basis):
            result = result + coefficient * basis_element
        return result

    def rational_coordinates(self, element: Quaternion) -> tuple[Fraction, ...]:
        if element.p != self.p:
            raise ValueError("element belongs to a different algebra")
        return (
            element.a - element.c,
            element.b - element.d,
            2 * element.c,
            2 * element.d,
        )

    def coordinates(self, element: Quaternion) -> tuple[int, ...]:
        values = self.rational_coordinates(element)
        if any(value.denominator != 1 for value in values):
            raise ValueError("element is not in the order")
        return tuple(int(value) for value in values)

    def norm(self, coordinates: Sequence[int]) -> int:
        z0, z1, z2, z3 = coordinates
        value = (
            z0 * z0
            + z0 * z2
            + ((self.p + 1) // 4) * z2 * z2
            + z1 * z1
            + z1 * z3
            + ((self.p + 1) // 4) * z3 * z3
        )
        return value

    def trace_discriminant(self) -> int:
        trace_matrix = Matrix(
            [
                [int((left * right).reduced_trace()) for right in self.basis]
                for left in self.basis
            ]
        )
        return int(trace_matrix.det())

    def prime_ideal(self, ell: int, alpha: Sequence[int]) -> IntegralIdeal:
        if not _is_prime(ell) or ell == self.p:
            raise ValueError("ell must be prime and different from p")
        if len(alpha) != 4 or all(coordinate % ell == 0 for coordinate in alpha):
            raise ValueError("alpha must be nonzero modulo ell")
        if self.norm(alpha) % ell != 0:
            raise ValueError("alpha must have norm zero modulo ell")
        generators: list[tuple[int, ...]] = [
            tuple(ell if row == col else 0 for col in range(4))
            for row in range(4)
        ]
        alpha_element = self.element(alpha)
        for basis_element in self.basis:
            generators.append(self.coordinates(basis_element * alpha_element))
        ideal = IntegralIdeal(self, _row_hnf(generators))
        if ideal.index != ell * ell:
            raise ValueError("the residue did not define a prime-norm ideal")
        return ideal

    def random_prime_ideal(
        self, ell: int, rng: Random
    ) -> tuple[IntegralIdeal, tuple[int, ...]]:
        if not _is_prime(ell) or ell == self.p or ell == 2:
            raise ValueError("ell must be an odd prime different from p")
        if ell > 257:
            half_inverse = pow(2, -1, ell)
            norm_coefficient = (self.p + 1) // 4
            while True:
                z1, z2, z3 = (rng.randrange(ell) for _ in range(3))
                constant = (
                    norm_coefficient * z2 * z2
                    + z1 * z1
                    + z1 * z3
                    + norm_coefficient * z3 * z3
                ) % ell
                discriminant = (z2 * z2 - 4 * constant) % ell
                square_root = _modular_sqrt(discriminant, ell)
                if square_root is None:
                    continue
                z0 = (-z2 + square_root) * half_inverse % ell
                alpha = (z0, z1, z2, z3)
                if any(alpha):
                    return self.prime_ideal(ell, alpha), alpha
        while True:
            alpha = tuple(rng.randrange(ell) for _ in range(4))
            if any(alpha) and self.norm(alpha) % ell == 0:
                try:
                    return self.prime_ideal(ell, alpha), alpha
                except ValueError:
                    continue


@dataclass(frozen=True)
class IntegralIdeal:
    """A full-rank integral left ideal represented in order coordinates."""

    order: MaximalOrder
    basis: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if len(self.basis) != 4 or any(len(row) != 4 for row in self.basis):
            raise ValueError("ideal basis must be 4 by 4")
        if _matrix_det(self.basis) == 0:
            raise ValueError("ideal basis must have full rank")

    @property
    def index(self) -> int:
        return abs(_matrix_det(self.basis))

    @property
    def norm(self) -> int:
        root = isqrt(self.index)
        if root * root != self.index:
            raise ValueError("ideal index is not a square")
        return root

    @property
    def canonical_id(self) -> str:
        return ";".join(",".join(str(value) for value in row) for row in self.basis)

    def contains_coordinates(self, coordinates: Sequence[int]) -> bool:
        if len(coordinates) != 4:
            return False
        coefficients = Matrix(1, 4, coordinates) * Matrix(self.basis).inv()
        return all(value.q == 1 for value in coefficients)

    def contains(self, element: Quaternion) -> bool:
        try:
            coordinates = self.order.coordinates(element)
        except ValueError:
            return False
        return self.contains_coordinates(coordinates)

    def verifies_left_closure(self) -> bool:
        for order_element in self.order.basis:
            for ideal_row in self.basis:
                if not self.contains(order_element * self.order.element(ideal_row)):
                    return False
        return True

    def right_multiply_scaled(
        self, multiplier: Quaternion, divisor: int = 1
    ) -> IntegralIdeal:
        generators: list[tuple[int, ...]] = []
        for row in self.basis:
            product_element = (self.order.element(row) * multiplier) / divisor
            generators.append(self.order.coordinates(product_element))
        return IntegralIdeal(self.order, _row_hnf(generators))

    def equivalent_ideal_from_element(
        self, coordinates: Sequence[int]
    ) -> IntegralIdeal:
        if not self.contains_coordinates(coordinates):
            raise ValueError("the element is not in the ideal")
        element = self.order.element(coordinates)
        element_norm = self.order.norm(coordinates)
        if element_norm == 0 or element_norm % self.norm != 0:
            raise ValueError("element norm is incompatible with the ideal norm")
        result = self.right_multiply_scaled(element.conjugate(), self.norm)
        expected_norm = element_norm // self.norm
        if result.norm != expected_norm:
            raise ArithmeticError("equivalent-ideal norm identity failed")
        return result

    def right_order(self, *, max_residue_candidates: int = 2_000_000) -> EmbeddedOrder:
        """Compute the embedded right order by an exact toy congruence kernel.

        The routine is intended for small prime-norm ideals.  If ``N O`` is
        contained in ``I``, every right-order element lies in ``O/N``.  The
        closure constraints then form a rank-four congruence lattice, which is
        enumerated modulo its common denominator and canonicalized by row HNF.
        """

        scale = self.norm
        for coordinate in range(4):
            scaled_basis_vector = tuple(
                scale if index == coordinate else 0 for index in range(4)
            )
            if not self.contains_coordinates(scaled_basis_vector):
                raise ValueError("right-order routine requires norm(I) O inside I")

        ideal_matrix = Matrix(self.basis)
        constraints = []
        for ideal_row in self.basis:
            ideal_element = self.order.element(ideal_row)
            product_columns = [
                self.order.coordinates(ideal_element * basis_element)
                for basis_element in self.order.basis
            ]
            product_matrix = Matrix(4, 4, lambda row, col: product_columns[col][row])
            coefficient_matrix = ideal_matrix.T.inv() * product_matrix / scale
            constraints.extend(coefficient_matrix.tolist())

        denominator = 1
        for row in constraints:
            for value in row:
                denominator = lcm(denominator, int(value.q))
        residue_candidates = denominator**4
        if residue_candidates > max_residue_candidates:
            raise ValueError(
                f"right-order residue space has {residue_candidates} candidates"
            )
        integer_constraints = [
            [int(value * denominator) for value in row] for row in constraints
        ]
        generators: list[tuple[int, ...]] = [
            tuple(denominator if row == col else 0 for col in range(4))
            for row in range(4)
        ]
        for residue in product(range(denominator), repeat=4):
            if not any(residue):
                continue
            if all(
                sum(row[index] * residue[index] for index in range(4))
                % denominator
                == 0
                for row in integer_constraints
            ):
                generators.append(residue)
        numerator_basis = _row_hnf(generators)
        result = EmbeddedOrder(
            self.order,
            tuple(
                tuple(Fraction(value, scale) for value in row)
                for row in numerator_basis
            ),
        )
        if not result.verifies_multiplicative_closure():
            raise ArithmeticError("computed right order is not multiplicatively closed")
        if abs(result.trace_discriminant()) != self.order.p**2:
            raise ArithmeticError("computed right order has the wrong discriminant")
        return result

    def verifies_dual_product_identity(self) -> bool:
        """Check the invertible-ideal identity I * conjugate(I) = norm(I) O."""

        generators = []
        for left_row in self.basis:
            left = self.order.element(left_row)
            for right_row in self.basis:
                right_conjugate = self.order.element(right_row).conjugate()
                generators.append(self.order.coordinates(left * right_conjugate))
        product_basis = _row_hnf(generators)
        expected_basis = tuple(
            tuple(self.norm if row == col else 0 for col in range(4))
            for row in range(4)
        )
        return product_basis == expected_basis


@dataclass(frozen=True)
class EmbeddedOrder:
    """An exact order embedded in the parent toy quaternion algebra."""

    parent: MaximalOrder
    coordinate_basis: tuple[tuple[Fraction, ...], ...]

    def __post_init__(self) -> None:
        if len(self.coordinate_basis) != 4 or any(
            len(row) != 4 for row in self.coordinate_basis
        ):
            raise ValueError("embedded order basis must be 4 by 4")
        if Matrix(self.coordinate_basis).det() == 0:
            raise ValueError("embedded order basis must have full rank")

    @property
    def basis(self) -> tuple[Quaternion, ...]:
        return tuple(self.parent.element(row) for row in self.coordinate_basis)

    @property
    def canonical_id(self) -> str:
        def encode(value: Fraction) -> str:
            if value.denominator == 1:
                return str(value.numerator)
            return f"{value.numerator}/{value.denominator}"

        return ";".join(
            ",".join(encode(value) for value in row)
            for row in self.coordinate_basis
        )

    def contains(self, element: Quaternion) -> bool:
        coordinates = Matrix(1, 4, self.parent.rational_coordinates(element))
        coefficients = coordinates * Matrix(self.coordinate_basis).inv()
        return all(value.q == 1 for value in coefficients)

    def verifies_multiplicative_closure(self) -> bool:
        return all(self.contains(left * right) for left in self.basis for right in self.basis)

    def trace_discriminant(self) -> int:
        trace_matrix = Matrix(
            [
                [(left * right).reduced_trace() for right in self.basis]
                for left in self.basis
            ]
        )
        determinant = trace_matrix.det()
        if determinant.q != 1:
            raise ArithmeticError("embedded order discriminant is not integral")
        return int(determinant)


def _inner(
    left: Sequence[int], right: Sequence[int], gram: Sequence[Sequence[int]]
) -> int:
    return sum(
        left[row] * gram[row][col] * right[col]
        for row in range(4)
        for col in range(4)
    )


def _gram_schmidt(
    basis: Sequence[Sequence[int]], gram: Sequence[Sequence[int]]
) -> tuple[list[list[Fraction]], list[Fraction]]:
    dimension = len(basis)
    mu = [[Fraction(0) for _ in range(dimension)] for _ in range(dimension)]
    orthogonal_norms: list[Fraction] = []
    pairings = [
        [_inner(basis[row], basis[col], gram) for col in range(dimension)]
        for row in range(dimension)
    ]
    for row in range(dimension):
        norm = Fraction(pairings[row][row])
        for prior in range(row):
            numerator = Fraction(pairings[row][prior])
            for earlier in range(prior):
                numerator -= (
                    mu[row][earlier]
                    * mu[prior][earlier]
                    * orthogonal_norms[earlier]
                )
            mu[row][prior] = numerator / orthogonal_norms[prior]
            norm -= mu[row][prior] * mu[row][prior] * orthogonal_norms[prior]
        if norm <= 0:
            raise ValueError("basis Gram matrix is not positive definite")
        orthogonal_norms.append(norm)
    return mu, orthogonal_norms


def norm_lll_reduce(
    ideal: IntegralIdeal, delta: Fraction = Fraction(3, 4)
) -> tuple[tuple[int, ...], ...]:
    """LLL-reduce an ideal basis for the exact reduced-norm inner product."""

    if not (Fraction(1, 4) < delta < 1):
        raise ValueError("delta must lie strictly between 1/4 and 1")
    basis = [list(row) for row in ideal.basis]
    gram = ideal.order.doubled_norm_gram
    index = 1
    while index < len(basis):
        mu, orthogonal_norms = _gram_schmidt(basis, gram)
        for prior in range(index - 1, -1, -1):
            multiple = _nearest_integer(mu[index][prior])
            if multiple:
                basis[index] = [
                    basis[index][col] - multiple * basis[prior][col]
                    for col in range(4)
                ]
                mu, orthogonal_norms = _gram_schmidt(basis, gram)
        if orthogonal_norms[index] >= (
            delta - mu[index][index - 1] * mu[index][index - 1]
        ) * orthogonal_norms[index - 1]:
            index += 1
        else:
            basis[index], basis[index - 1] = basis[index - 1], basis[index]
            index = max(index - 1, 1)
    return tuple(tuple(row) for row in basis)


@dataclass(frozen=True)
class ShortVectorResult:
    order_coordinates: tuple[int, ...]
    norm: int
    reduced_basis: tuple[tuple[int, ...], ...]


def lll_short_vector(ideal: IntegralIdeal) -> ShortVectorResult:
    reduced_basis = norm_lll_reduce(ideal)
    vector = min(reduced_basis, key=ideal.order.norm)
    return ShortVectorResult(vector, ideal.order.norm(vector), reduced_basis)


@dataclass(frozen=True)
class ExactShortVectorResult:
    order_coordinates: tuple[int, ...]
    coefficients: tuple[int, ...]
    norm: int
    initial_norm_bound: int
    coefficient_bounds: tuple[int, ...]
    candidates_checked: int
    reduced_basis: tuple[tuple[int, ...], ...]


def exact_short_vector(
    ideal: IntegralIdeal, max_candidates: int | None = None
) -> ExactShortVectorResult:
    """Certify an SVP solution by exhaustive inverse-Gram bounded enumeration."""

    lll_result = lll_short_vector(ideal)
    reduced_basis = lll_result.reduced_basis
    coordinate_gram = Matrix(ideal.order.doubled_norm_gram)
    basis_matrix = Matrix(reduced_basis)
    coefficient_gram = basis_matrix * coordinate_gram * basis_matrix.T
    inverse_gram = coefficient_gram.inv()
    doubled_bound = 2 * lll_result.norm
    bounds = tuple(
        isqrt(
            (doubled_bound * int(inverse_gram[index, index].p))
            // int(inverse_gram[index, index].q)
        )
        for index in range(4)
    )
    search_size = 1
    for bound in bounds:
        search_size *= 2 * bound + 1
    if max_candidates is not None and search_size > max_candidates:
        raise RuntimeError(
            f"exact search requires {search_size} coefficient tuples, "
            f"above limit {max_candidates}"
        )

    best_vector = lll_result.order_coordinates
    best_coefficients = tuple(
        int(value)
        for value in (
            Matrix(1, 4, best_vector) * Matrix(reduced_basis).inv()
        )
    )
    best_norm = lll_result.norm
    candidates_checked = 0
    ranges: Iterable[range] = (range(-bound, bound + 1) for bound in bounds)
    for coefficients in product(*ranges):
        if not any(coefficients):
            continue
        candidates_checked += 1
        vector = _linear_combination(coefficients, reduced_basis)
        vector_norm = ideal.order.norm(vector)
        if vector_norm < best_norm or (
            vector_norm == best_norm and vector < best_vector
        ):
            best_vector = vector
            best_coefficients = tuple(coefficients)
            best_norm = vector_norm

    return ExactShortVectorResult(
        order_coordinates=best_vector,
        coefficients=best_coefficients,
        norm=best_norm,
        initial_norm_bound=lll_result.norm,
        coefficient_bounds=bounds,
        candidates_checked=candidates_checked,
        reduced_basis=reduced_basis,
    )


def theta_series_prefix(
    ideal: IntegralIdeal, max_normalized_norm: int
) -> tuple[int, ...]:
    """Count ideal vectors by ``nrd(x) / N(I)`` through a finite cutoff."""

    if max_normalized_norm < 0:
        raise ValueError("theta-series cutoff must be nonnegative")
    reduced_basis = norm_lll_reduce(ideal)
    coordinate_gram = Matrix(ideal.order.doubled_norm_gram)
    basis_matrix = Matrix(reduced_basis)
    coefficient_gram = basis_matrix * coordinate_gram * basis_matrix.T
    inverse_gram = coefficient_gram.inv()
    norm_bound = max_normalized_norm * ideal.norm
    doubled_bound = 2 * norm_bound
    bounds = tuple(
        isqrt(
            (doubled_bound * int(inverse_gram[index, index].p))
            // int(inverse_gram[index, index].q)
        )
        for index in range(4)
    )
    counts = [0] * (max_normalized_norm + 1)
    ranges: Iterable[range] = (range(-bound, bound + 1) for bound in bounds)
    for coefficients in product(*ranges):
        vector = _linear_combination(coefficients, reduced_basis)
        vector_norm = ideal.order.norm(vector)
        if vector_norm > norm_bound:
            continue
        if vector_norm % ideal.norm:
            raise ArithmeticError("ideal element norm is not divisible by ideal norm")
        counts[vector_norm // ideal.norm] += 1
    return tuple(counts)


@dataclass(frozen=True)
class NormalizedNormSpectrum:
    witnesses: dict[int, tuple[int, ...]]
    max_normalized_norm: int
    coefficient_bounds: tuple[int, ...]
    candidates_checked: int
    reduced_basis: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class TargetNormResult:
    normalized_norm: int | None
    order_coordinates: tuple[int, ...] | None
    targets_tested: tuple[int, ...]
    coefficient_bounds: tuple[int, ...]
    box_tuples_checked: int
    elimination_triples_checked: int
    coefficient_box_size: int
    search_method: str
    reduced_basis: tuple[tuple[int, ...], ...]


def _target_witness_by_coordinate_elimination(
    ideal: IntegralIdeal,
    reduced_basis: Sequence[Sequence[int]],
    gram: Sequence[Sequence[int]],
    bounds: Sequence[int],
    target_quadratic: int,
) -> tuple[tuple[int, ...] | None, int]:
    """Solve one quadratic coordinate exactly after enumerating the other three."""

    solved = max(range(4), key=lambda index: 2 * bounds[index] + 1)
    remaining = tuple(index for index in range(4) if index != solved)
    first, second, third = remaining
    diagonal = gram[solved][solved]
    checked = 0
    ranges = (
        range(-bounds[first], bounds[first] + 1),
        range(-bounds[second], bounds[second] + 1),
        range(-bounds[third], bounds[third] + 1),
    )
    for value_first, value_second, value_third in product(*ranges):
        checked += 1
        values = (value_first, value_second, value_third)
        linear = sum(
            gram[solved][index] * value
            for index, value in zip(remaining, values)
        )
        fixed = sum(
            gram[left][right] * values[left_position] * values[right_position]
            for left_position, left in enumerate(remaining)
            for right_position, right in enumerate(remaining)
        )
        discriminant = linear * linear + diagonal * (target_quadratic - fixed)
        if discriminant < 0:
            continue
        square_root = isqrt(discriminant)
        if square_root * square_root != discriminant:
            continue
        numerators = (-linear + square_root, -linear - square_root)
        for numerator in dict.fromkeys(numerators):
            if numerator % diagonal:
                continue
            solved_value = numerator // diagonal
            if abs(solved_value) > bounds[solved]:
                continue
            coefficients = [0, 0, 0, 0]
            coefficients[solved] = solved_value
            for index, value in zip(remaining, values):
                coefficients[index] = value
            vector = _linear_combination(coefficients, reduced_basis)
            if ideal.order.norm(vector) * 2 != target_quadratic:
                raise ArithmeticError("eliminated target witness failed exact validation")
            return vector, checked
    return None, checked


def normalized_norm_spectrum(
    ideal: IntegralIdeal,
    max_normalized_norm: int,
    max_candidates: int | None = None,
) -> NormalizedNormSpectrum:
    """Enumerate represented positive normalized norms through an exact bound."""

    if max_normalized_norm < 1:
        raise ValueError("spectrum cutoff must be positive")
    reduced_basis = norm_lll_reduce(ideal)
    coordinate_gram = Matrix(ideal.order.doubled_norm_gram)
    basis_matrix = Matrix(reduced_basis)
    coefficient_gram = basis_matrix * coordinate_gram * basis_matrix.T
    inverse_gram = coefficient_gram.inv()
    norm_bound = max_normalized_norm * ideal.norm
    doubled_bound = 2 * norm_bound
    bounds = tuple(
        isqrt(
            (doubled_bound * int(inverse_gram[index, index].p))
            // int(inverse_gram[index, index].q)
        )
        for index in range(4)
    )
    integer_gram = [
        [int(coefficient_gram[row, col]) for col in range(4)]
        for row in range(4)
    ]
    vectorized = _normalized_spectrum_vectorized(
        ideal,
        reduced_basis,
        integer_gram,
        bounds,
        doubled_bound,
        max_candidates,
    )
    if vectorized is not None:
        witnesses, candidates_checked = vectorized
    else:
        witnesses = {}
        candidates_checked = 0
        for coefficients in _ellipsoid_coefficients(
            integer_gram, doubled_bound, max_candidates
        ):
            if not any(coefficients):
                continue
            candidates_checked += 1
            vector = _linear_combination(coefficients, reduced_basis)
            vector_norm = ideal.order.norm(vector)
            if vector_norm > norm_bound:
                continue
            if vector_norm % ideal.norm:
                raise ArithmeticError("ideal element norm is not divisible by ideal norm")
            normalized_norm = vector_norm // ideal.norm
            previous = witnesses.get(normalized_norm)
            if previous is None or vector < previous:
                witnesses[normalized_norm] = vector
    return NormalizedNormSpectrum(
        witnesses=witnesses,
        max_normalized_norm=max_normalized_norm,
        coefficient_bounds=bounds,
        candidates_checked=candidates_checked,
        reduced_basis=reduced_basis,
    )


def first_represented_normalized_target(
    ideal: IntegralIdeal,
    targets: Sequence[int],
    max_box_candidates: int | None = None,
) -> TargetNormResult:
    """Return the first represented target after exact increasing-target scans.

    Boxes no larger than ``max_box_candidates`` use vectorized enumeration.  A
    larger certified box is still searched exactly by eliminating one quadratic
    coordinate and enumerating the remaining three; the argument is therefore
    a strategy threshold, not a censoring limit.
    """

    ordered_targets = tuple(sorted(set(targets)))
    if not ordered_targets or ordered_targets[0] < 1:
        raise ValueError("targets must contain positive integers")
    reduced_basis = norm_lll_reduce(ideal)
    coordinate_gram = Matrix(ideal.order.doubled_norm_gram)
    basis_matrix = Matrix(reduced_basis)
    coefficient_gram_matrix = basis_matrix * coordinate_gram * basis_matrix.T
    coefficient_gram = [
        [int(coefficient_gram_matrix[row, col]) for col in range(4)]
        for row in range(4)
    ]
    inverse_gram = coefficient_gram_matrix.inv()
    tested: list[int] = []
    total_box_tuples = 0
    total_elimination_triples = 0
    last_bounds = (0, 0, 0, 0)
    last_box_size = 0
    methods: set[str] = set()
    for target in ordered_targets:
        doubled_bound = 2 * target * ideal.norm
        bounds = tuple(
            isqrt(
                (doubled_bound * int(inverse_gram[index, index].p))
                // int(inverse_gram[index, index].q)
            )
            for index in range(4)
        )
        last_bounds = bounds
        box_size = 1
        for bound in bounds:
            box_size *= 2 * bound + 1
        last_box_size = box_size
        target_quadratic = 2 * target * ideal.norm
        tested.append(target)
        if max_box_candidates is not None and box_size > max_box_candidates:
            methods.add("coordinate-elimination")
            vector, checked = _target_witness_by_coordinate_elimination(
                ideal,
                reduced_basis,
                coefficient_gram,
                bounds,
                target_quadratic,
            )
            total_elimination_triples += checked
            if vector is not None:
                return TargetNormResult(
                    normalized_norm=target,
                    order_coordinates=vector,
                    targets_tested=tuple(tested),
                    coefficient_bounds=bounds,
                    box_tuples_checked=total_box_tuples,
                    elimination_triples_checked=total_elimination_triples,
                    coefficient_box_size=box_size,
                    search_method="+".join(sorted(methods)),
                    reduced_basis=reduced_basis,
                )
            continue
        max_coefficient = max(bounds)
        max_gram = max(abs(value) for row in coefficient_gram for value in row)
        if 16 * max_gram * max_coefficient * max_coefficient >= 1 << 62:
            raise RuntimeError("target scan exceeds the certified int64 range")

        import numpy as np

        methods.add("vectorized-box")

        values2, values3 = np.meshgrid(
            np.arange(-bounds[2], bounds[2] + 1, dtype=np.int64),
            np.arange(-bounds[3], bounds[3] + 1, dtype=np.int64),
            indexing="ij",
        )
        coefficient2 = values2.ravel()
        coefficient3 = values3.ravel()
        tail_quadratic = (
            coefficient_gram[2][2] * coefficient2 * coefficient2
            + 2 * coefficient_gram[2][3] * coefficient2 * coefficient3
            + coefficient_gram[3][3] * coefficient3 * coefficient3
        )
        for coefficient0 in range(-bounds[0], bounds[0] + 1):
            for coefficient1 in range(-bounds[1], bounds[1] + 1):
                total_box_tuples += coefficient2.size
                fixed = (
                    coefficient_gram[0][0] * coefficient0 * coefficient0
                    + 2
                    * coefficient_gram[0][1]
                    * coefficient0
                    * coefficient1
                    + coefficient_gram[1][1] * coefficient1 * coefficient1
                )
                quadratic = (
                    tail_quadratic
                    + fixed
                    + 2
                    * coefficient2
                    * (
                        coefficient_gram[0][2] * coefficient0
                        + coefficient_gram[1][2] * coefficient1
                    )
                    + 2
                    * coefficient3
                    * (
                        coefficient_gram[0][3] * coefficient0
                        + coefficient_gram[1][3] * coefficient1
                    )
                )
                matches = np.flatnonzero(quadratic == target_quadratic)
                if not matches.size:
                    continue
                index = int(matches[0])
                coefficients = (
                    coefficient0,
                    coefficient1,
                    int(coefficient2[index]),
                    int(coefficient3[index]),
                )
                vector = _linear_combination(coefficients, reduced_basis)
                if ideal.order.norm(vector) != target * ideal.norm:
                    raise ArithmeticError("target witness failed exact validation")
                return TargetNormResult(
                    normalized_norm=target,
                    order_coordinates=vector,
                    targets_tested=tuple(tested),
                    coefficient_bounds=bounds,
                    box_tuples_checked=total_box_tuples,
                    elimination_triples_checked=total_elimination_triples,
                    coefficient_box_size=box_size,
                    search_method="+".join(sorted(methods)),
                    reduced_basis=reduced_basis,
                )
    return TargetNormResult(
        normalized_norm=None,
        order_coordinates=None,
        targets_tested=tuple(tested),
        coefficient_bounds=last_bounds,
        box_tuples_checked=total_box_tuples,
        elimination_triples_checked=total_elimination_triples,
        coefficient_box_size=last_box_size,
        search_method="+".join(sorted(methods)),
        reduced_basis=reduced_basis,
    )


__all__ = [
    "ExactShortVectorResult",
    "IntegralIdeal",
    "MaximalOrder",
    "NormalizedNormSpectrum",
    "Quaternion",
    "ShortVectorResult",
    "TargetNormResult",
    "exact_short_vector",
    "first_represented_normalized_target",
    "lll_short_vector",
    "norm_lll_reduce",
    "normalized_norm_spectrum",
    "theta_series_prefix",
]
