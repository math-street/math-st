"""Toy straight-line encodings for characteristics two and three.

The formulas are from Brier--Coron--Icart--Madore--Randriam--Tibouchi,
"Efficient Indifferentiable Hashing into Ordinary Elliptic Curves" (2010),
Sections 8.1 and E.  They are intentionally restricted to the small fields
permitted by this repository's scaffold.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .curves import (
    BinaryField,
    cmov_mod,
    inv0_mod,
    is_square_mod,
    sgn0_prime,
    sqrt_mod_ct,
)

MaskedPoint: TypeAlias = tuple[int, int, int]


@dataclass(frozen=True, slots=True)
class CharacteristicThreeCurve:
    """The ordinary characteristic-three model y^2 = x^3 + a*x^2 + b."""

    a: int
    b: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", self.a % 3)
        object.__setattr__(self, "b", self.b % 3)
        if self.a == 0 or self.b == 0:
            raise ValueError("the characteristic-three model requires a*b != 0")

    def rhs(self, x: int) -> int:
        x %= 3
        return (x * x * x + self.a * x * x + self.b) % 3

    def contains(self, point: tuple[int, int]) -> bool:
        x, y = point
        return y * y % 3 == self.rhs(x)


def map_characteristic_three_square_discriminant(
    curve: CharacteristicThreeCurve,
    t: int,
    *,
    eta: int = 2,
    c: int = 1,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Section 8.1 encoding for the square-discriminant family over F_3."""

    t %= 3
    eta %= 3
    c %= 3
    if is_square_mod(eta, 3) or c * c % 3 != -curve.b * inv0_mod(curve.a, 3) % 3:
        raise ValueError("eta and c do not satisfy the Section 8.1 predicates")

    if trace is not None:
        trace.append("char3.square_input")
    u = eta * t * t % 3
    inverse = inv0_mod(u, 3)
    if trace is not None:
        trace.append("char3.inv0")
    x1 = c * (1 - inverse) % 3
    x2 = u * x1 % 3
    gx1 = curve.rhs(x1)
    gx2 = curve.rhs(x2)
    use_x1 = is_square_mod(gx1, 3)
    if trace is not None:
        trace.append("char3.two_candidates")
    x = cmov_mod(x2, x1, use_x1, 3)
    gx = cmov_mod(gx2, gx1, use_x1, 3)
    y = sqrt_mod_ct(gx, 3)
    signs_match = sgn0_prime(y, 3) == sgn0_prime(t, 3)
    y = cmov_mod(-y, y, signs_match, 3)
    if trace is not None:
        trace.append("char3.select_sqrt")
    return x, y


def add_complete_characteristic_three(
    curve: CharacteristicThreeCurve,
    left: MaskedPoint,
    right: MaskedPoint,
    *,
    trace: list[str] | None = None,
) -> MaskedPoint:
    """Masked complete affine addition on valid points of the stated model."""

    x1, y1, infinity1 = left
    x2, y2, infinity2 = right
    dx = (x2 - x1) % 3
    dy = (y2 - y1) % 3
    generic_slope = dy * inv0_mod(dx, 3) % 3
    generic_x = (generic_slope * generic_slope - curve.a - x1 - x2) % 3
    generic_y = (generic_slope * (x1 - generic_x) - y1) % 3
    generic = (generic_x, generic_y, 0)

    double_numerator = 2 * curve.a * x1 % 3
    double_denominator = 2 * y1 % 3
    double_slope = double_numerator * inv0_mod(double_denominator, 3) % 3
    double_x = (double_slope * double_slope - curve.a - 2 * x1) % 3
    double_y = (double_slope * (x1 - double_x) - y1) % 3
    doubled = (double_x, double_y, 0)

    same_x = int(x1 == x2)
    same_y = int(y1 == y2)
    y_nonzero = int(y1 != 0)
    use_double = same_x & same_y & y_nonzero
    use_infinity = same_x & (use_double ^ 1)

    result = tuple(
        cmov_mod(generic[index], doubled[index], use_double, 3)
        for index in range(3)
    )
    result = tuple(
        cmov_mod(result[index], (0, 0, 1)[index], use_infinity, 3)
        for index in range(3)
    )
    result = tuple(
        cmov_mod(result[index], right[index], infinity1, 3)
        for index in range(3)
    )
    result = tuple(
        cmov_mod(result[index], left[index], infinity2, 3)
        for index in range(3)
    )
    if trace is not None:
        trace.append("char3.complete_add")
    return result  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class BinaryWeierstrassCurve:
    """Ordinary binary model y^2 + x*y = x^3 + a*x^2 + b."""

    field: BinaryField
    a: int
    b: int

    def __post_init__(self) -> None:
        self.field._check_element(self.a)
        self.field._check_element(self.b)
        if self.b == 0:
            raise ValueError("the ordinary binary model requires b != 0")

    def contains(self, point: tuple[int, int]) -> bool:
        x, y = point
        field = self.field
        left = field.add(field.square_fixed(y), field.mul_fixed(x, y))
        x2 = field.square_fixed(x)
        right = field.add(
            field.add(field.mul_fixed(x2, x), field.mul_fixed(self.a, x2)),
            self.b,
        )
        return left == right


def _binary_candidate(
    curve: BinaryWeierstrassCurve,
    x: int,
    square_root_b: int,
) -> tuple[int, int]:
    field = curve.field
    x2 = field.square_fixed(x)
    numerator = field.add(
        field.add(field.mul_fixed(x2, x), field.mul_fixed(curve.a, x2)),
        curve.b,
    )
    h = field.mul_fixed(numerator, field.inv0_fixed(x2))
    trace_zero = field.absolute_trace_fixed(h) ^ 1
    x_is_zero = int(x == 0)
    generic_y = field.mul_fixed(field.half_trace_fixed(h), x)
    y = field.cmov(generic_y, square_root_b, x_is_zero)
    valid = trace_zero | x_is_zero
    return y, valid


def map_binary_shallue_van_de_woestijne(
    curve: BinaryWeierstrassCurve,
    t: int,
    *,
    w: int = 0,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Appendix-E binary SvdW map with three candidates and masked selection."""

    field = curve.field
    field._check_element(t)
    field._check_element(w)
    if field.degree % 2 == 0:
        raise ValueError("the Appendix-E formula requires odd extension degree")
    c = field.add(curve.a, field.add(w, field.square_fixed(w)))
    if c == 0:
        raise ValueError("choose public w with w^2 + w != a")

    t2 = field.square_fixed(t)
    denominator = field.add(1, field.add(t, t2))
    x1 = field.mul_fixed(
        field.mul_fixed(t, c),
        field.inv0_fixed(denominator),
    )
    x2 = field.add(field.mul_fixed(t, x1), c)
    x3 = field.mul_fixed(
        field.mul_fixed(x1, x2),
        field.inv0_fixed(field.add(x1, x2)),
    )
    if trace is not None:
        trace.append("char2.three_x_candidates")

    square_root_b = field.pow_fixed(curve.b, 1 << (field.degree - 1))
    y1, valid1 = _binary_candidate(curve, x1, square_root_b)
    y2, valid2 = _binary_candidate(curve, x2, square_root_b)
    y3, _valid3 = _binary_candidate(curve, x3, square_root_b)
    if trace is not None:
        trace.append("char2.three_y_candidates")

    select1 = valid1
    select2 = valid2 & (valid1 ^ 1)
    x = field.cmov(x3, x1, select1)
    x = field.cmov(x, x2, select2)
    y = field.cmov(y3, y1, select1)
    y = field.cmov(y, y2, select2)
    if trace is not None:
        trace.append("char2.masked_selection")
    return x, y


def _binary_point_cmov(
    field: BinaryField,
    false_value: MaskedPoint,
    true_value: MaskedPoint,
    selector: int,
) -> MaskedPoint:
    return (
        field.cmov(false_value[0], true_value[0], selector),
        field.cmov(false_value[1], true_value[1], selector),
        false_value[2] ^ ((0 - selector) & (false_value[2] ^ true_value[2])),
    )


def add_complete_binary(
    curve: BinaryWeierstrassCurve,
    left: MaskedPoint,
    right: MaskedPoint,
    *,
    trace: list[str] | None = None,
) -> MaskedPoint:
    """Masked complete affine addition on valid ordinary binary points."""

    field = curve.field
    x1, y1, infinity1 = left
    x2, y2, infinity2 = right
    dx = field.add(x1, x2)
    dy = field.add(y1, y2)
    generic_slope = field.mul_fixed(dy, field.inv0_fixed(dx))
    generic_x = field.add(
        field.add(field.square_fixed(generic_slope), generic_slope),
        field.add(field.add(x1, x2), curve.a),
    )
    generic_y = field.add(
        field.add(
            field.mul_fixed(generic_slope, field.add(x1, generic_x)),
            generic_x,
        ),
        y1,
    )
    generic = (generic_x, generic_y, 0)

    double_slope = field.add(
        x1,
        field.mul_fixed(y1, field.inv0_fixed(x1)),
    )
    double_x = field.add(
        field.add(field.square_fixed(double_slope), double_slope),
        curve.a,
    )
    double_y = field.add(
        field.square_fixed(x1),
        field.mul_fixed(field.add(double_slope, 1), double_x),
    )
    doubled = (double_x, double_y, 0)

    same_x = int(x1 == x2)
    same_y = int(y1 == y2)
    x_nonzero = int(x1 != 0)
    use_double = same_x & same_y & x_nonzero
    use_infinity = same_x & (use_double ^ 1)
    result = _binary_point_cmov(field, generic, doubled, use_double)
    result = _binary_point_cmov(field, result, (0, 0, 1), use_infinity)
    result = _binary_point_cmov(field, result, right, infinity1)
    result = _binary_point_cmov(field, result, left, infinity2)
    if trace is not None:
        trace.append("char2.complete_add")
    return result
