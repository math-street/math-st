"""Exact sparse Semaev and Weil-restriction utilities for P1.3.

Sub-goals: P1.3 / SG-02 and SG-03
Inputs: finite prime q, extension degree n in {1,2,3}, factor-base size m
Outputs: sparse coordinate polynomials over F_q
Runtime: intended for toy systems only; operations enforce a term ceiling
Validated against: lib.semaev evaluators and constructed curve decompositions
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence


Element = tuple[int, ...]
Monomial = tuple[int, ...]
PrimePolynomial = dict[Monomial, int]


class ExpansionLimit(RuntimeError):
    """Raised when an expanded sparse polynomial exceeds its declared ceiling."""


@dataclass(frozen=True)
class FiniteField:
    """Polynomial-basis representation of F_{p^n} for prime p."""

    p: int
    modulus: tuple[int, ...]  # ascending, monic

    def __post_init__(self) -> None:
        if self.p < 2 or any(self.p % divisor == 0 for divisor in range(2, int(self.p**0.5) + 1)):
            raise ValueError("p must be prime")
        if len(self.modulus) < 2 or self.modulus[-1] % self.p != 1:
            raise ValueError("modulus must be monic and have positive degree")

    @property
    def n(self) -> int:
        return len(self.modulus) - 1

    @property
    def order(self) -> int:
        return self.p**self.n

    @property
    def zero(self) -> Element:
        return (0,) * self.n

    @property
    def one(self) -> Element:
        return (1, *([0] * (self.n - 1)))

    def element(self, value: int | Sequence[int] | Element) -> Element:
        if isinstance(value, int):
            return (value % self.p, *([0] * (self.n - 1)))
        values = tuple(int(item) % self.p for item in value)
        if len(values) != self.n:
            raise ValueError(f"expected {self.n} coordinates, got {len(values)}")
        return values

    def add(self, left: Element, right: Element) -> Element:
        return tuple((a + b) % self.p for a, b in zip(left, right, strict=True))

    def neg(self, value: Element) -> Element:
        return tuple((-item) % self.p for item in value)

    def sub(self, left: Element, right: Element) -> Element:
        return self.add(left, self.neg(right))

    def mul(self, left: Element, right: Element) -> Element:
        work = [0] * (2 * self.n - 1)
        for left_degree, left_coefficient in enumerate(left):
            for right_degree, right_coefficient in enumerate(right):
                work[left_degree + right_degree] = (
                    work[left_degree + right_degree] + left_coefficient * right_coefficient
                ) % self.p
        for degree in range(len(work) - 1, self.n - 1, -1):
            coefficient = work[degree] % self.p
            if coefficient == 0:
                continue
            shift = degree - self.n
            for modulus_degree in range(self.n):
                work[shift + modulus_degree] = (
                    work[shift + modulus_degree]
                    - coefficient * self.modulus[modulus_degree]
                ) % self.p
        return tuple(item % self.p for item in work[: self.n])

    def pow(self, value: Element, exponent: int) -> Element:
        if exponent < 0:
            return self.pow(self.inv(value), -exponent)
        result = self.one
        base = value
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            remaining >>= 1
        return result

    def inv(self, value: Element) -> Element:
        if value == self.zero:
            raise ZeroDivisionError("zero has no inverse")
        return self.pow(value, self.order - 2)

    def div(self, left: Element, right: Element) -> Element:
        return self.mul(left, self.inv(right))

    def elements(self) -> Iterable[Element]:
        return product(range(self.p), repeat=self.n)


def find_irreducible_modulus(p: int, n: int) -> tuple[int, ...]:
    """Return a deterministic irreducible monic polynomial for n <= 3."""
    if n == 1:
        return (0, 1)
    if n not in (2, 3):
        raise ValueError("the toy implementation supports extension degree at most 3")
    for coefficients in product(range(p), repeat=n):
        if coefficients[0] == 0:
            continue
        candidate = (*coefficients, 1)
        has_root = any(
            sum(coefficient * pow(value, degree, p) for degree, coefficient in enumerate(candidate))
            % p
            == 0
            for value in range(p)
        )
        if not has_root:  # root-free is equivalent to irreducible in degrees 2 and 3
            return candidate
    raise ValueError(f"no irreducible polynomial found for p={p}, n={n}")


@dataclass
class SparsePolynomial:
    field: FiniteField
    nvars: int
    terms: dict[Monomial, Element]
    reduce_vars: frozenset[int] = frozenset()
    term_limit: int = 250_000

    def __post_init__(self) -> None:
        normalized: dict[Monomial, Element] = {}
        for monomial, coefficient in self.terms.items():
            if len(monomial) != self.nvars:
                raise ValueError("monomial has the wrong number of variables")
            reduced = self._reduce_monomial(monomial)
            value = self.field.element(coefficient)
            if value == self.field.zero:
                continue
            normalized[reduced] = self.field.add(normalized.get(reduced, self.field.zero), value)
            if normalized[reduced] == self.field.zero:
                del normalized[reduced]
        self.terms = normalized
        self._check_limit()

    @classmethod
    def constant(
        cls,
        field: FiniteField,
        nvars: int,
        value: int | Sequence[int] | Element,
        reduce_vars: frozenset[int] = frozenset(),
        term_limit: int = 250_000,
    ) -> SparsePolynomial:
        coefficient = field.element(value)
        terms = {} if coefficient == field.zero else {(0,) * nvars: coefficient}
        return cls(field, nvars, terms, reduce_vars, term_limit)

    @classmethod
    def variable(
        cls,
        field: FiniteField,
        nvars: int,
        index: int,
        reduce_vars: frozenset[int] = frozenset(),
        term_limit: int = 250_000,
    ) -> SparsePolynomial:
        monomial = tuple(1 if position == index else 0 for position in range(nvars))
        return cls(field, nvars, {monomial: field.one}, reduce_vars, term_limit)

    @property
    def zero(self) -> SparsePolynomial:
        return SparsePolynomial.constant(
            self.field, self.nvars, 0, self.reduce_vars, self.term_limit
        )

    @property
    def one(self) -> SparsePolynomial:
        return SparsePolynomial.constant(
            self.field, self.nvars, 1, self.reduce_vars, self.term_limit
        )

    @property
    def degree(self) -> int:
        return max((sum(monomial) for monomial in self.terms), default=-1)

    @property
    def term_count(self) -> int:
        return len(self.terms)

    def variable_degree(self, index: int) -> int:
        return max((monomial[index] for monomial in self.terms), default=-1)

    def _check_limit(self) -> None:
        if len(self.terms) > self.term_limit:
            raise ExpansionLimit(
                f"term ceiling {self.term_limit} exceeded with {len(self.terms)} terms"
            )

    def _reduce_monomial(self, monomial: Monomial) -> Monomial:
        values = list(monomial)
        for index in self.reduce_vars:
            exponent = values[index]
            if exponent >= self.field.p:
                values[index] = 1 + (exponent - 1) % (self.field.p - 1)
        return tuple(values)

    def _compatible(self, other: SparsePolynomial) -> None:
        if (
            self.field != other.field
            or self.nvars != other.nvars
            or self.reduce_vars != other.reduce_vars
            or self.term_limit != other.term_limit
        ):
            raise ValueError("incompatible sparse polynomial rings")

    def __neg__(self) -> SparsePolynomial:
        return SparsePolynomial(
            self.field,
            self.nvars,
            {monomial: self.field.neg(coefficient) for monomial, coefficient in self.terms.items()},
            self.reduce_vars,
            self.term_limit,
        )

    def __add__(self, other: SparsePolynomial) -> SparsePolynomial:
        self._compatible(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = self.field.add(result.get(monomial, self.field.zero), coefficient)
            if result[monomial] == self.field.zero:
                del result[monomial]
        return SparsePolynomial(
            self.field, self.nvars, result, self.reduce_vars, self.term_limit
        )

    def __sub__(self, other: SparsePolynomial) -> SparsePolynomial:
        return self + (-other)

    def __mul__(self, other: SparsePolynomial) -> SparsePolynomial:
        self._compatible(other)
        result: dict[Monomial, Element] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = self._reduce_monomial(
                    tuple(
                        left + right
                        for left, right in zip(left_monomial, right_monomial, strict=True)
                    )
                )
                coefficient = self.field.mul(left_coefficient, right_coefficient)
                result[monomial] = self.field.add(result.get(monomial, self.field.zero), coefficient)
                if result[monomial] == self.field.zero:
                    del result[monomial]
            if len(result) > self.term_limit:
                raise ExpansionLimit(
                    f"term ceiling {self.term_limit} exceeded during multiplication"
                )
        return SparsePolynomial(
            self.field, self.nvars, result, self.reduce_vars, self.term_limit
        )

    def __pow__(self, exponent: int) -> SparsePolynomial:
        if exponent < 0:
            raise ValueError("polynomial exponent must be nonnegative")
        result = self.one
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * base
            base = base * base
            remaining >>= 1
        return result

    def evaluate(self, values: Sequence[Element]) -> Element:
        if len(values) != self.nvars:
            raise ValueError("wrong number of evaluation values")
        result = self.field.zero
        for monomial, coefficient in self.terms.items():
            value = coefficient
            for argument, exponent in zip(values, monomial, strict=True):
                value = self.field.mul(value, self.field.pow(argument, exponent))
            result = self.field.add(result, value)
        return result

    def coefficients_in(self, index: int) -> list[SparsePolynomial]:
        maximum = self.variable_degree(index)
        if maximum < 0:
            return [self.zero]
        coefficients = [self.zero for _ in range(maximum + 1)]
        buckets: list[dict[Monomial, Element]] = [{} for _ in range(maximum + 1)]
        for monomial, coefficient in self.terms.items():
            degree = monomial[index]
            reduced = list(monomial)
            reduced[index] = 0
            buckets[degree][tuple(reduced)] = coefficient
        return [
            SparsePolynomial(
                self.field, self.nvars, bucket, self.reduce_vars, self.term_limit
            )
            for bucket in buckets
        ]

    def drop_trailing_variables(self, keep: int) -> SparsePolynomial:
        if not 0 <= keep <= self.nvars:
            raise ValueError("invalid number of variables to keep")
        projected: dict[Monomial, Element] = {}
        for monomial, coefficient in self.terms.items():
            if any(monomial[keep:]):
                raise ValueError("cannot drop a variable that still occurs")
            projected[monomial[:keep]] = coefficient
        return SparsePolynomial(
            self.field,
            keep,
            projected,
            frozenset(index for index in self.reduce_vars if index < keep),
            self.term_limit,
        )


def f3_polynomial(
    x1: SparsePolynomial,
    x2: SparsePolynomial,
    x3: SparsePolynomial,
    a: SparsePolynomial,
    b: SparsePolynomial,
) -> SparsePolynomial:
    two = SparsePolynomial.constant(
        x1.field, x1.nvars, 2, x1.reduce_vars, x1.term_limit
    )
    four = SparsePolynomial.constant(
        x1.field, x1.nvars, 4, x1.reduce_vars, x1.term_limit
    )
    return (
        ((x1 - x2) ** 2) * (x3**2)
        - two * (((x1 + x2) * (x1 * x2 + a)) + two * b) * x3
        + ((x1 * x2 - a) ** 2)
        - four * b * (x1 + x2)
    )


def determinant(matrix: list[list[SparsePolynomial]]) -> SparsePolynomial:
    """Division-free subset DP determinant, suitable for sparse Sylvester matrices."""
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a square matrix")
    if size == 0:
        raise ValueError("empty determinant is not used here")
    template = matrix[0][0]
    states: dict[int, SparsePolynomial] = {0: template.one}
    for row_index, row in enumerate(matrix):
        next_states: dict[int, SparsePolynomial] = {}
        for mask, partial in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                inversions = sum(1 for selected in range(column + 1, size) if mask & (1 << selected))
                contribution = partial * entry
                if inversions % 2:
                    contribution = -contribution
                next_mask = mask | (1 << column)
                next_states[next_mask] = next_states.get(next_mask, template.zero) + contribution
        states = next_states
        if not states:
            return template.zero
        if row_index + 1 != max(mask.bit_count() for mask in states):
            raise AssertionError("invalid determinant state")
    return states.get((1 << size) - 1, template.zero)


def resultant_in(
    first: SparsePolynomial, second: SparsePolynomial, variable: int
) -> SparsePolynomial:
    first._compatible(second)
    first_coefficients = first.coefficients_in(variable)
    second_coefficients = second.coefficients_in(variable)
    while len(first_coefficients) > 1 and not first_coefficients[-1].terms:
        first_coefficients.pop()
    while len(second_coefficients) > 1 and not second_coefficients[-1].terms:
        second_coefficients.pop()
    first_degree = len(first_coefficients) - 1
    second_degree = len(second_coefficients) - 1
    if first_degree == 0:
        return first_coefficients[0] ** second_degree
    if second_degree == 0:
        return second_coefficients[0] ** first_degree
    first_descending = list(reversed(first_coefficients))
    second_descending = list(reversed(second_coefficients))
    size = first_degree + second_degree
    matrix = [[first.zero for _ in range(size)] for _ in range(size)]
    for row in range(second_degree):
        matrix[row][row : row + first_degree + 1] = first_descending
    for row in range(first_degree):
        matrix[second_degree + row][row : row + second_degree + 1] = second_descending
    return determinant(matrix)


def semaev_from_arguments(
    arguments: Sequence[SparsePolynomial],
    a: SparsePolynomial,
    b: SparsePolynomial,
    auxiliary_start: int,
    depth: int = 0,
) -> SparsePolynomial:
    if len(arguments) < 3:
        raise ValueError("Semaev index must be at least 3")
    if len(arguments) == 3:
        return f3_polynomial(arguments[0], arguments[1], arguments[2], a, b)
    template = arguments[0]
    auxiliary_index = auxiliary_start + depth
    auxiliary = SparsePolynomial.variable(
        template.field,
        template.nvars,
        auxiliary_index,
        template.reduce_vars,
        template.term_limit,
    )
    left = semaev_from_arguments(
        [*arguments[:-2], auxiliary], a, b, auxiliary_start, depth + 1
    )
    right = f3_polynomial(arguments[-2], arguments[-1], auxiliary, a, b)
    return resultant_in(left, right, auxiliary_index)


def generic_semaev_polynomial(index: int, term_limit: int = 250_000) -> SparsePolynomial:
    """Expand f_index with symbolic x variables and symbolic curve coefficients a,b."""
    if index < 3:
        raise ValueError("Semaev index must be at least 3")
    field = FiniteField(101, (0, 1))
    user_variables = index + 2  # x_1,...,x_index,a,b
    auxiliary_count = index - 3
    nvars = user_variables + auxiliary_count
    variables = [
        SparsePolynomial.variable(field, nvars, position, term_limit=term_limit)
        for position in range(index)
    ]
    a = SparsePolynomial.variable(field, nvars, index, term_limit=term_limit)
    b = SparsePolynomial.variable(field, nvars, index + 1, term_limit=term_limit)
    result = semaev_from_arguments(variables, a, b, user_variables)
    return result.drop_trailing_variables(user_variables)


def build_weil_coordinate_system(
    q: int,
    n: int,
    m: int,
    target_x: Element,
    a_value: Element | int = 1,
    b_value: Element | int = 1,
    term_limit: int = 250_000,
) -> tuple[FiniteField, list[PrimePolynomial], SparsePolynomial]:
    """Build the n coordinate equations of f_{m+1}(x_1,...,x_m,target_x)."""
    if m < 2:
        raise ValueError("the factor-base size must be at least 2")
    field = FiniteField(q, find_irreducible_modulus(q, n))
    target_x = field.element(target_x)
    auxiliary_count = m - 2
    nvars = m + auxiliary_count
    reduce_vars = frozenset(range(m))
    variables = [
        SparsePolynomial.variable(
            field, nvars, position, reduce_vars, term_limit
        )
        for position in range(m)
    ]
    a = SparsePolynomial.constant(field, nvars, a_value, reduce_vars, term_limit)
    b = SparsePolynomial.constant(field, nvars, b_value, reduce_vars, term_limit)
    target = SparsePolynomial.constant(field, nvars, target_x, reduce_vars, term_limit)
    extension_polynomial = semaev_from_arguments(
        [*variables, target], a, b, m
    ).drop_trailing_variables(m)
    coordinates: list[PrimePolynomial] = []
    for coordinate in range(n):
        polynomial = {
            monomial: coefficient[coordinate] % q
            for monomial, coefficient in extension_polynomial.terms.items()
            if coefficient[coordinate] % q
        }
        coordinates.append(polynomial)
    return field, coordinates, extension_polynomial


Point = tuple[Element, Element] | None


def curve_is_nonsingular(
    field: FiniteField, a: Element | int = 1, b: Element | int = 1
) -> bool:
    """Return whether y^2=x^3+a*x+b has nonzero discriminant in odd characteristic."""
    a_element = field.element(a)
    b_element = field.element(b)
    discriminant_factor = field.add(
        field.mul(field.element(4), field.mul(field.mul(a_element, a_element), a_element)),
        field.mul(field.element(27), field.mul(b_element, b_element)),
    )
    return discriminant_factor != field.zero


def curve_neg(field: FiniteField, point: Point) -> Point:
    if point is None:
        return None
    return point[0], field.neg(point[1])


def curve_add(field: FiniteField, a: Element, left: Point, right: Point) -> Point:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and field.add(y1, y2) == field.zero:
        return None
    if left == right:
        numerator = field.add(field.mul(field.element(3), field.mul(x1, x1)), a)
        denominator = field.mul(field.element(2), y1)
    else:
        numerator = field.sub(y2, y1)
        denominator = field.sub(x2, x1)
    slope = field.div(numerator, denominator)
    x3 = field.sub(field.sub(field.mul(slope, slope), x1), x2)
    y3 = field.sub(field.mul(slope, field.sub(x1, x3)), y1)
    return x3, y3


def factor_base_points(
    field: FiniteField, a: Element | int = 1, b: Element | int = 1
) -> list[Point]:
    if not curve_is_nonsingular(field, a, b):
        raise ValueError("singular short-Weierstrass curve")
    a_element = field.element(a)
    b_element = field.element(b)
    points: list[Point] = []
    elements = list(field.elements())
    for base_x in range(field.p):
        x = field.element(base_x)
        right_side = field.add(
            field.add(field.mul(field.mul(x, x), x), field.mul(a_element, x)),
            b_element,
        )
        for y in elements:
            if field.mul(y, y) == right_side:
                points.append((x, y))
    return points


def first_nonbase_target_x(
    field: FiniteField, a: Element | int = 1, b: Element | int = 1
) -> Element:
    """Return the first non-base-field x-coordinate occurring on the curve."""
    if not curve_is_nonsingular(field, a, b):
        raise ValueError("singular short-Weierstrass curve")
    a_element = field.element(a)
    b_element = field.element(b)
    elements = list(field.elements())
    for x in elements:
        if all(coordinate == 0 for coordinate in x[1:]):
            continue
        right_side = field.add(
            field.add(field.mul(field.mul(x, x), x), field.mul(a_element, x)),
            b_element,
        )
        if any(field.mul(y, y) == right_side for y in elements):
            return x
    raise ValueError("the curve has no point with a non-base-field x-coordinate")


def known_decomposition(
    field: FiniteField,
    m: int,
    a: Element | int = 1,
    b: Element | int = 1,
    require_nonbase_target: bool = False,
) -> tuple[list[int], Element]:
    """Return base-field x values and target x whose associated points sum to zero."""
    a_element = field.element(a)
    points = factor_base_points(field, a, b)
    if not points:
        raise ValueError("factor base is empty")
    best: tuple[list[int], Element] | None = None
    best_score = -1
    maximum_score = min(m, field.p)
    for indices in product(range(len(points)), repeat=m):
        total: Point = None
        for index in indices:
            total = curve_add(field, a_element, total, points[index])
        if total is None:
            continue
        target = curve_neg(field, total)
        assert target is not None
        if require_nonbase_target and not any(target[0][1:]):
            continue
        values = [int(points[index][0][0]) for index in indices]
        score = len(set(values))
        if score > best_score:
            best = values, target[0]
            best_score = score
        if score == maximum_score:
            return values, target[0]
    if best is not None:
        return best
    raise ValueError("failed to construct a nontrivial decomposition")


def known_decomposition_candidates(
    field: FiniteField,
    m: int,
    a: Element | int = 1,
    b: Element | int = 1,
    require_nonbase_target: bool = True,
    limit: int | None = None,
) -> list[tuple[list[int], Element]]:
    """Enumerate deterministic, target-distinct factor-base decompositions."""
    a_element = field.element(a)
    points = factor_base_points(field, a, b)
    best_by_target: dict[Element, tuple[int, list[int]]] = {}
    for indices in product(range(len(points)), repeat=m):
        total: Point = None
        for index in indices:
            total = curve_add(field, a_element, total, points[index])
        if total is None:
            continue
        target = curve_neg(field, total)
        assert target is not None
        target_x = target[0]
        if require_nonbase_target and not any(target_x[1:]):
            continue
        values = [int(points[index][0][0]) for index in indices]
        score = len(set(values))
        previous = best_by_target.get(target_x)
        if previous is None or (score, tuple(values)) > (previous[0], tuple(previous[1])):
            best_by_target[target_x] = score, values
    ordered = [
        (values, target)
        for target, (score, values) in sorted(
            best_by_target.items(),
            key=lambda item: (-item[1][0], item[0], tuple(item[1][1])),
        )
    ]
    return ordered if limit is None else ordered[:limit]


def evaluate_prime_polynomial(poly: PrimePolynomial, values: Sequence[int], q: int) -> int:
    result = 0
    for monomial, coefficient in poly.items():
        term = coefficient
        for value, exponent in zip(values, monomial, strict=True):
            term = term * pow(value, exponent, q) % q
        result = (result + term) % q
    return result
