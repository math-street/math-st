"""A genus-one specialization of the GHS Weil-descent class-group map."""

from __future__ import annotations

from dataclasses import dataclass

from lib.binary_curves import BinaryEllipticCurve, BinaryPoint
from lib.curves import BinaryField


def relative_trace(field: BinaryField, value: int, base_degree: int) -> int:
    """Return Tr_(F_(2^m)/F_(2^d))(value), where d divides m."""
    if base_degree <= 0 or field.degree % base_degree:
        raise ValueError("base_degree must be a positive divisor of the field degree")
    field._check_element(value)
    result = 0
    conjugate = value
    for _ in range(field.degree // base_degree):
        result = field.add(result, conjugate)
        conjugate = field.frobenius(conjugate, base_degree)
    return result


def is_in_subfield(field: BinaryField, value: int, base_degree: int) -> bool:
    """Return whether value is fixed by the F_(2^base_degree) Frobenius."""
    if base_degree <= 0 or field.degree % base_degree:
        raise ValueError("base_degree must be a positive divisor of the field degree")
    field._check_element(value)
    return field.frobenius(value, base_degree) == value


def fixed_subfield_elements(field: BinaryField, base_degree: int) -> tuple[int, ...]:
    """Enumerate the embedded F_(2^base_degree) elements in a toy ambient field."""
    values = tuple(
        value for value in range(field.order) if is_in_subfield(field, value, base_degree)
    )
    if len(values) != 1 << base_degree:
        raise ArithmeticError("fixed-field enumeration has the wrong cardinality")
    return values


@dataclass(frozen=True, slots=True)
class GenusOneGHSTransfer:
    """The m=1 odd-degree GHS conorm/norm map, represented on elliptic curves.

    The source is y^2+xy=x^3+a*x^2+b over K, with b in the base field k.
    For odd [K:k], its descended genus-one curve has A=Tr(a) and the same b.
    A root s of s^2+s=a+A gives a K-isomorphism to that curve.  The transfer
    is the sum of the k-Frobenius conjugates of the isomorphic image.
    """

    source: BinaryEllipticCurve
    target: BinaryEllipticCurve
    base_degree: int
    extension_degree: int
    twist: int

    @classmethod
    def from_source(
        cls,
        source: BinaryEllipticCurve,
        base_degree: int,
        *,
        twist: int | None = None,
    ) -> "GenusOneGHSTransfer":
        field = source.field
        if base_degree <= 0 or field.degree % base_degree:
            raise ValueError("base_degree must be a positive divisor of the field degree")
        extension_degree = field.degree // base_degree
        if extension_degree % 2 == 0:
            raise ValueError("this genus-one specialization requires odd extension degree")
        if not is_in_subfield(field, source.b, base_degree):
            raise ValueError("the genus-one specialization requires b in the base field")

        target_a = relative_trace(field, source.a, base_degree)
        target_b = relative_trace(field, source.b, base_degree)
        if target_b != source.b:
            raise ArithmeticError("odd relative trace should fix a base-field b")
        if not is_in_subfield(field, target_a, base_degree):
            raise ArithmeticError("relative trace did not land in the base field")

        difference = field.add(source.a, target_a)
        if twist is None:
            twist = next(
                (
                    candidate
                    for candidate in range(field.order)
                    if field.add(field.square(candidate), candidate) == difference
                ),
                None,
            )
            if twist is None:
                raise ArithmeticError("Artin--Schreier twist equation has no root")
        else:
            field._check_element(twist)
            if field.add(field.square(twist), twist) != difference:
                raise ValueError("twist must satisfy s^2+s=a+Tr(a)")

        return cls(
            source=source,
            target=BinaryEllipticCurve(field, target_a, target_b),
            base_degree=base_degree,
            extension_degree=extension_degree,
            twist=twist,
        )

    @property
    def field(self) -> BinaryField:
        return self.source.field

    def isomorphism(self, point: BinaryPoint) -> BinaryPoint:
        """Map the source to its base-defined isomorphic target over K."""
        if point is None:
            return None
        if not self.source.contains(point):
            raise ValueError("point is not on the source curve")
        x, y = point
        image = x, self.field.add(y, self.field.mul(self.twist, x))
        if not self.target.contains(image):
            raise ArithmeticError("Artin--Schreier isomorphism produced an off-curve point")
        return image

    def inverse_isomorphism(self, point: BinaryPoint) -> BinaryPoint:
        """Invert the characteristic-two shear; the same formula is involutive."""
        if point is None:
            return None
        if not self.target.contains(point):
            raise ValueError("point is not on the target curve")
        x, y = point
        image = x, self.field.add(y, self.field.mul(self.twist, x))
        if not self.source.contains(image):
            raise ArithmeticError("inverse isomorphism produced an off-curve point")
        return image

    def transfer(self, point: BinaryPoint) -> BinaryPoint:
        """Apply conorm followed by norm as a sum of k-Frobenius conjugates."""
        image = self.isomorphism(point)
        result: BinaryPoint = None
        conjugate = image
        for _ in range(self.extension_degree):
            result = self.target.add(result, conjugate)
            conjugate = self.target.frobenius_point(conjugate, self.base_degree)
        if result is not None and (
            not is_in_subfield(self.field, result[0], self.base_degree)
            or not is_in_subfield(self.field, result[1], self.base_degree)
        ):
            raise ArithmeticError("norm image is not rational over the base field")
        return result
