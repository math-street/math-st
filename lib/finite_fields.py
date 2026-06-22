"""Small, fixed-degree prime-extension fields and short-Weierstrass maps.

This module is deliberately limited to the toy fields permitted by the P5.4
scaffold.  Elements use a public, fixed polynomial basis and are represented by
tuples of coefficients in ascending degree order.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field
from itertools import product
from typing import Callable, Iterator


FieldElement = tuple[int, ...]
TraceHook = Callable[[str], None] | None
ExtensionMaskedPoint = tuple[FieldElement, FieldElement, int]


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


@dataclass(frozen=True)
class PrimePolynomialField:
    """A quadratic or cubic extension of an odd prime field.

    ``modulus`` is monic and stored in ascending coefficient order.  Degree
    two and three are enough for this project and admit the simple, complete
    irreducibility test used here: a polynomial is irreducible iff it has no
    root in the base field.
    """

    characteristic: int
    modulus: tuple[int, ...]

    def __post_init__(self) -> None:
        p = self.characteristic
        if not _is_prime(p) or p == 2:
            raise ValueError("the characteristic must be an odd prime")
        if len(self.modulus) not in (3, 4):
            raise ValueError("only degree-two and degree-three fields are supported")
        reduced = tuple(coefficient % p for coefficient in self.modulus)
        if reduced[-1] != 1:
            raise ValueError("the modulus must be monic")
        object.__setattr__(self, "modulus", reduced)
        for value in range(p):
            evaluation = 0
            for coefficient in reversed(reduced):
                evaluation = (evaluation * value + coefficient) % p
            if evaluation == 0:
                raise ValueError("the modulus is reducible over the base field")

    @property
    def degree(self) -> int:
        return len(self.modulus) - 1

    @property
    def order(self) -> int:
        return self.characteristic**self.degree

    @property
    def zero(self) -> FieldElement:
        return (0,) * self.degree

    @property
    def one(self) -> FieldElement:
        return (1,) + (0,) * (self.degree - 1)

    def constant(self, value: int) -> FieldElement:
        return (value % self.characteristic,) + (0,) * (self.degree - 1)

    def normalize(self, value: FieldElement) -> FieldElement:
        if len(value) != self.degree:
            raise ValueError("wrong polynomial-basis element length")
        return tuple(coefficient % self.characteristic for coefficient in value)

    def elements(self) -> Iterator[FieldElement]:
        yield from product(range(self.characteristic), repeat=self.degree)

    def add(self, left: FieldElement, right: FieldElement) -> FieldElement:
        p = self.characteristic
        return tuple((left[index] + right[index]) % p for index in range(self.degree))

    def sub(self, left: FieldElement, right: FieldElement) -> FieldElement:
        p = self.characteristic
        return tuple((left[index] - right[index]) % p for index in range(self.degree))

    def neg(self, value: FieldElement) -> FieldElement:
        p = self.characteristic
        return tuple((-value[index]) % p for index in range(self.degree))

    def mul(self, left: FieldElement, right: FieldElement) -> FieldElement:
        p = self.characteristic
        degree = self.degree
        coefficients = [0] * (2 * degree - 1)
        for left_index in range(degree):
            for right_index in range(degree):
                target = left_index + right_index
                coefficients[target] = (
                    coefficients[target] + left[left_index] * right[right_index]
                ) % p
        for source in range(2 * degree - 2, degree - 1, -1):
            leading = coefficients[source]
            for modulus_index in range(degree):
                target = source - degree + modulus_index
                coefficients[target] = (
                    coefficients[target] - leading * self.modulus[modulus_index]
                ) % p
        return tuple(coefficients[:degree])

    def square(self, value: FieldElement) -> FieldElement:
        return self.mul(value, value)

    def pow(self, value: FieldElement, exponent: int) -> FieldElement:
        if exponent < 0:
            raise ValueError("negative exponents are unsupported")
        result = self.one
        base = value
        for bit in bin(exponent)[2:]:
            result = self.square(result)
            if bit == "1":  # the exponent is a public field parameter
                result = self.mul(result, base)
        return result

    def inv0(self, value: FieldElement) -> FieldElement:
        """Return value**(-1), with the total convention inv0(0) = 0."""

        return self.pow(value, self.order - 2)

    def is_square(self, value: FieldElement) -> int:
        euler = self.pow(value, (self.order - 1) // 2)
        return int((value == self.zero) | (euler == self.one))

    def sqrt(self, value: FieldElement) -> FieldElement:
        if self.order % 4 != 3:
            raise ValueError("this fixed-exponent square root requires q = 3 mod 4")
        return self.pow(value, (self.order + 1) // 4)

    def sgn0(self, value: FieldElement) -> int:
        """RFC-style sign: the low bit of the first nonzero coefficient."""

        sign = 0
        prefix_is_zero = 1
        for coefficient in value:
            sign |= prefix_is_zero & (coefficient & 1)
            prefix_is_zero &= int(coefficient == 0)
        return sign

    def cmov(
        self,
        false_value: FieldElement,
        true_value: FieldElement,
        selector: int,
    ) -> FieldElement:
        selector = int(bool(selector))
        p = self.characteristic
        return tuple(
            (false_value[index] + selector * (true_value[index] - false_value[index])) % p
            for index in range(self.degree)
        )


# Compatibility API used by the pairing, extension-curve, and P1.2 modules.
# PrimePolynomialField is the tuple-oriented API; ExtensionField wraps the same
# arithmetic in operator-overloaded immutable elements.


@dataclass(frozen=True, slots=True)
class ExtensionField:
    p: int
    modulus: tuple[int, ...]
    _backend: PrimePolynomialField = dataclass_field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        backend = PrimePolynomialField(self.p, self.modulus)
        object.__setattr__(self, "modulus", backend.modulus)
        object.__setattr__(self, "_backend", backend)

    @property
    def degree(self) -> int:
        return self._backend.degree

    @property
    def order(self) -> int:
        return self._backend.order

    @property
    def zero(self) -> "ExtensionElement":
        return ExtensionElement(self, self._backend.zero)

    @property
    def one(self) -> "ExtensionElement":
        return ExtensionElement(self, self._backend.one)

    def element(
        self,
        value: int | tuple[int, ...] | list[int] | "ExtensionElement",
    ) -> "ExtensionElement":
        if isinstance(value, ExtensionElement):
            if value.field != self:
                raise ValueError("cannot coerce an element from a different field")
            return value
        if isinstance(value, int):
            coefficients = self._backend.constant(value)
        else:
            coefficients = self._backend.normalize(tuple(value))
        return ExtensionElement(self, coefficients)

    def elements(self) -> Iterator["ExtensionElement"]:
        for coefficients in self._backend.elements():
            yield ExtensionElement(self, coefficients)

    def base_elements(self) -> Iterator["ExtensionElement"]:
        for value in range(self.p):
            yield self.element(value)


@dataclass(frozen=True, slots=True)
class ExtensionElement:
    field: ExtensionField
    coefficients: tuple[int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "coefficients",
            self.field._backend.normalize(tuple(self.coefficients)),
        )

    def _coerce(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self.field.element(other)

    def __bool__(self) -> bool:
        return self.coefficients != self.field._backend.zero

    def __add__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        right = self._coerce(other)
        return ExtensionElement(
            self.field,
            self.field._backend.add(self.coefficients, right.coefficients),
        )

    def __radd__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self + other

    def __neg__(self) -> "ExtensionElement":
        return ExtensionElement(self.field, self.field._backend.neg(self.coefficients))

    def __sub__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self + (-self._coerce(other))

    def __rsub__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self._coerce(other) - self

    def __mul__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        right = self._coerce(other)
        return ExtensionElement(
            self.field,
            self.field._backend.mul(self.coefficients, right.coefficients),
        )

    def __rmul__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self * other

    def __pow__(self, exponent: int) -> "ExtensionElement":
        if exponent < 0:
            return self.inverse() ** (-exponent)
        return ExtensionElement(
            self.field,
            self.field._backend.pow(self.coefficients, exponent),
        )

    def inverse(self) -> "ExtensionElement":
        if not self:
            raise ZeroDivisionError("zero has no multiplicative inverse")
        return self ** (self.field.order - 2)

    def __truediv__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self._coerce(other) / self


def find_irreducible_cubic(p: int) -> tuple[int, int, int, int]:
    """Return the first monic cubic with no root over F_p."""

    if not _is_prime(p) or p == 2:
        raise ValueError("p must be an odd prime")
    for constant in range(1, p):
        for linear in range(p):
            for quadratic in range(p):
                modulus = (constant, linear, quadratic, 1)
                if all(
                    (constant + linear * value + quadratic * value * value + value**3) % p
                    for value in range(p)
                ):
                    return modulus
    raise ArithmeticError("no irreducible cubic found")


def cubic_field(p: int) -> ExtensionField:
    return ExtensionField(p, find_irreducible_cubic(p))


@dataclass(frozen=True, slots=True)
class ExtensionElement:
    """Operator-friendly compatibility wrapper used by the shared toy code."""

    field: "ExtensionField"
    coefficients: tuple[int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "coefficients",
            self.field.backend.normalize(self.coefficients),
        )

    def _coerce(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self.field.element(other)

    def __add__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        right = self._coerce(other)
        return ExtensionElement(
            self.field,
            self.field.backend.add(self.coefficients, right.coefficients),
        )

    __radd__ = __add__

    def __sub__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        right = self._coerce(other)
        return ExtensionElement(
            self.field,
            self.field.backend.sub(self.coefficients, right.coefficients),
        )

    def __rsub__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self._coerce(other) - self

    def __neg__(self) -> "ExtensionElement":
        return ExtensionElement(self.field, self.field.backend.neg(self.coefficients))

    def __mul__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        right = self._coerce(other)
        return ExtensionElement(
            self.field,
            self.field.backend.mul(self.coefficients, right.coefficients),
        )

    __rmul__ = __mul__

    def inverse(self) -> "ExtensionElement":
        if not self:
            raise ZeroDivisionError("zero has no multiplicative inverse")
        return ExtensionElement(self.field, self.field.backend.inv0(self.coefficients))

    def __truediv__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other: int | "ExtensionElement") -> "ExtensionElement":
        return self._coerce(other) * self.inverse()

    def __pow__(self, exponent: int) -> "ExtensionElement":
        if exponent < 0:
            return self.inverse() ** (-exponent)
        return ExtensionElement(
            self.field,
            self.field.backend.pow(self.coefficients, exponent),
        )

    def __bool__(self) -> bool:
        return self.coefficients != self.field.backend.zero

    def __int__(self) -> int:
        if any(self.coefficients[1:]):
            raise ValueError("a non-base-field element has no integer representative")
        return self.coefficients[0]

    def __str__(self) -> str:
        """Preserve the repository's compact polynomial-basis serialization."""

        return "[" + ",".join(str(value) for value in self.coefficients) + "]"


@dataclass(frozen=True, slots=True)
class ExtensionField:
    """Compatibility facade for the repository's original extension API."""

    q: int
    modulus: tuple[int, ...]
    backend: PrimePolynomialField = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        backend = PrimePolynomialField(self.q, tuple(self.modulus))
        object.__setattr__(self, "modulus", backend.modulus)
        object.__setattr__(self, "backend", backend)

    @property
    def degree(self) -> int:
        return self.backend.degree

    @property
    def order(self) -> int:
        return self.backend.order

    @property
    def zero(self) -> ExtensionElement:
        return ExtensionElement(self, self.backend.zero)

    @property
    def one(self) -> ExtensionElement:
        return ExtensionElement(self, self.backend.one)

    def element(
        self,
        value: int | tuple[int, ...] | list[int] | ExtensionElement,
    ) -> ExtensionElement:
        if isinstance(value, ExtensionElement):
            if value.field != self:
                raise ValueError("cannot mix elements from different fields")
            return value
        if isinstance(value, int):
            coefficients = self.backend.constant(value)
        else:
            coefficients = tuple(value)
        return ExtensionElement(self, coefficients)

    def elements(self) -> Iterator[ExtensionElement]:
        for coefficients in self.backend.elements():
            yield ExtensionElement(self, coefficients)

    def base_elements(self) -> Iterator[ExtensionElement]:
        for value in range(self.q):
            yield self.element(value)

    def is_base_element(self, value: int | ExtensionElement) -> bool:
        element = self.element(value)
        return not any(element.coefficients[1:])


def find_irreducible_cubic(prime: int) -> tuple[int, int, int, int]:
    """Return the first monic cubic without a base-field root."""

    if not _is_prime(prime):
        raise ValueError("prime must be prime")
    for constant in range(1, prime):
        for linear in range(prime):
            for quadratic in range(prime):
                candidate = (constant, linear, quadratic, 1)
                if all(
                    sum(
                        coefficient * value**degree
                        for degree, coefficient in enumerate(candidate)
                    )
                    % prime
                    for value in range(prime)
                ):
                    return candidate
    raise ArithmeticError("no irreducible cubic found")


def cubic_field(prime: int) -> ExtensionField:
    return ExtensionField(prime, find_irreducible_cubic(prime))


@dataclass(frozen=True)
class ExtensionWeierstrassCurve:
    field: PrimePolynomialField
    a: FieldElement
    b: FieldElement

    def __post_init__(self) -> None:
        field = self.field
        a = field.normalize(self.a)
        b = field.normalize(self.b)
        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)
        four = field.constant(4)
        twenty_seven = field.constant(27)
        discriminant_term = field.add(
            field.mul(four, field.mul(field.square(a), a)),
            field.mul(twenty_seven, field.square(b)),
        )
        if discriminant_term == field.zero:
            raise ValueError("singular short-Weierstrass curve")

    def rhs(self, x: FieldElement) -> FieldElement:
        field = self.field
        return field.add(
            field.add(field.mul(field.square(x), x), field.mul(self.a, x)),
            self.b,
        )

    def contains(self, point: tuple[FieldElement, FieldElement]) -> bool:
        x, y = point
        return self.field.square(y) == self.rhs(x)


def find_svdw_z_extension(curve: ExtensionWeierstrassCurve) -> FieldElement:
    """Find the first field element satisfying RFC 9380 SvdW constraints."""

    field = curve.field
    two = field.constant(2)
    three = field.constant(3)
    four = field.constant(4)
    inv_two = field.inv0(two)
    for z in field.elements():
        if z == field.zero:
            continue
        gz = curve.rhs(z)
        numerator = field.add(field.mul(three, field.square(z)), field.mul(four, curve.a))
        minus_z_over_two = field.neg(field.mul(z, inv_two))
        h = field.neg(
            field.mul(
                numerator,
                field.inv0(field.mul(four, gz)),
            )
        )
        if gz == field.zero or numerator == field.zero:
            continue
        if not field.is_square(h):
            continue
        if field.is_square(gz) or field.is_square(curve.rhs(minus_z_over_two)):
            return z
    raise ValueError("no SvdW Z parameter found")


def map_to_curve_svdw_extension(
    curve: ExtensionWeierstrassCurve,
    z: FieldElement,
    u: FieldElement,
    *,
    trace: TraceHook = None,
) -> tuple[FieldElement, FieldElement]:
    """RFC 9380 F.1 SvdW over a small odd-degree prime extension."""

    field = curve.field

    def record(label: str) -> None:
        if trace is not None:
            trace(label)

    one = field.one
    two = field.constant(2)
    three = field.constant(3)
    four = field.constant(4)
    record("constants")
    gz = curve.rhs(z)
    denominator = field.add(
        field.mul(three, field.square(z)),
        field.mul(four, curve.a),
    )
    c1 = gz
    c2 = field.neg(field.mul(z, field.inv0(two)))
    c3 = field.sqrt(field.neg(field.mul(gz, denominator)))
    c3 = field.cmov(c3, field.neg(c3), field.sgn0(c3))
    c4 = field.neg(field.mul(field.mul(four, gz), field.inv0(denominator)))
    record("derive_public_constants")

    tv1 = field.square(u)
    tv1 = field.mul(tv1, c1)
    tv2 = field.add(one, tv1)
    tv1 = field.sub(one, tv1)
    tv3 = field.mul(tv1, tv2)
    tv3 = field.inv0(tv3)
    tv4 = field.mul(field.mul(u, tv1), tv3)
    tv4 = field.mul(tv4, c3)
    x1 = field.sub(c2, tv4)
    gx1 = curve.rhs(x1)
    e1 = field.is_square(gx1)
    record("candidate_one")

    x2 = field.add(c2, tv4)
    gx2 = curve.rhs(x2)
    e2 = field.is_square(gx2) & (1 ^ e1)
    record("candidate_two")

    x3 = field.square(tv2)
    x3 = field.mul(x3, tv3)
    x3 = field.square(x3)
    x3 = field.mul(x3, c4)
    x3 = field.add(x3, z)
    gx3 = curve.rhs(x3)
    record("candidate_three")

    x = field.cmov(x3, x1, e1)
    x = field.cmov(x, x2, e2)
    gx = field.cmov(gx3, gx1, e1)
    gx = field.cmov(gx, gx2, e2)
    y = field.sqrt(gx)
    y = field.cmov(y, field.neg(y), field.sgn0(y) ^ field.sgn0(u))
    record("select_and_sqrt")
    return x, y


def _extension_point_cmov(
    field: PrimePolynomialField,
    false_value: ExtensionMaskedPoint,
    true_value: ExtensionMaskedPoint,
    selector: int,
) -> ExtensionMaskedPoint:
    selector = int(bool(selector))
    return (
        field.cmov(false_value[0], true_value[0], selector),
        field.cmov(false_value[1], true_value[1], selector),
        false_value[2] + selector * (true_value[2] - false_value[2]),
    )


def add_complete_extension_weierstrass(
    curve: ExtensionWeierstrassCurve,
    left: ExtensionMaskedPoint,
    right: ExtensionMaskedPoint,
    *,
    trace: TraceHook = None,
) -> ExtensionMaskedPoint:
    """Masked complete affine addition on valid short-Weierstrass points."""

    field = curve.field
    x1, y1, infinity1 = left
    x2, y2, infinity2 = right
    dx = field.sub(x2, x1)
    dy = field.sub(y2, y1)
    generic_slope = field.mul(dy, field.inv0(dx))
    generic_x = field.sub(field.sub(field.square(generic_slope), x1), x2)
    generic_y = field.sub(field.mul(generic_slope, field.sub(x1, generic_x)), y1)
    generic = (generic_x, generic_y, 0)

    double_numerator = field.add(
        field.mul(field.constant(3), field.square(x1)),
        curve.a,
    )
    double_denominator = field.mul(field.constant(2), y1)
    double_slope = field.mul(double_numerator, field.inv0(double_denominator))
    double_x = field.sub(
        field.square(double_slope),
        field.mul(field.constant(2), x1),
    )
    double_y = field.sub(field.mul(double_slope, field.sub(x1, double_x)), y1)
    doubled = (double_x, double_y, 0)

    same_x = int(x1 == x2)
    same_y = int(y1 == y2)
    y_nonzero = int(y1 != field.zero)
    use_double = same_x & same_y & y_nonzero
    use_infinity = same_x & (use_double ^ 1)
    infinity = (field.zero, field.zero, 1)
    result = _extension_point_cmov(field, generic, doubled, use_double)
    result = _extension_point_cmov(field, result, infinity, use_infinity)
    result = _extension_point_cmov(field, result, right, infinity1)
    result = _extension_point_cmov(field, result, left, infinity2)
    if trace is not None:
        trace("extension.complete_add")
    return result
