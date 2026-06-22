"""Ordinary binary elliptic curves for small, auditable experiments."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Iterable, TypeAlias

from lib.curves import BinaryField

BinaryPoint: TypeAlias = tuple[int, int] | None


@dataclass(frozen=True, slots=True)
class BinaryEllipticCurve:
    """The nonsupersingular curve y^2 + xy = x^3 + ax^2 + b in characteristic two."""

    field: BinaryField
    a: int
    b: int

    def __post_init__(self) -> None:
        self.field._check_element(self.a)
        self.field._check_element(self.b)
        if self.b == 0:
            raise ValueError("b must be nonzero for a nonsingular binary curve")

    def contains(self, point: BinaryPoint) -> bool:
        if point is None:
            return True
        x, y = point
        try:
            left = self.field.add(self.field.square(y), self.field.mul(x, y))
            x_squared = self.field.square(x)
            right = self.field.add(
                self.field.add(self.field.mul(x_squared, x), self.field.mul(self.a, x_squared)),
                self.b,
            )
        except ValueError:
            return False
        return left == right

    def neg(self, point: BinaryPoint) -> BinaryPoint:
        if point is None:
            return None
        x, y = point
        if not self.contains(point):
            raise ValueError("point is not on the curve")
        return x, self.field.add(x, y)

    def add(self, left: BinaryPoint, right: BinaryPoint) -> BinaryPoint:
        """Add two points using the affine group law, with None as infinity."""
        if left is None:
            if not self.contains(right):
                raise ValueError("right point is not on the curve")
            return right
        if right is None:
            if not self.contains(left):
                raise ValueError("left point is not on the curve")
            return left
        if not self.contains(left) or not self.contains(right):
            raise ValueError("both points must be on the curve")

        x1, y1 = left
        x2, y2 = right
        if x1 == x2:
            if y1 != y2 or x1 == 0:
                return None
            slope = self.field.add(x1, self.field.div(y1, x1))
            x3 = self.field.add(
                self.field.add(self.field.square(slope), slope),
                self.a,
            )
            y3 = self.field.add(
                self.field.square(x1),
                self.field.mul(self.field.add(slope, 1), x3),
            )
        else:
            slope = self.field.div(
                self.field.add(y1, y2),
                self.field.add(x1, x2),
            )
            x3 = self.field.add(
                self.field.add(
                    self.field.add(self.field.square(slope), slope),
                    self.field.add(x1, x2),
                ),
                self.a,
            )
            y3 = self.field.add(
                self.field.add(self.field.mul(slope, self.field.add(x1, x3)), x3),
                y1,
            )

        result = x3, y3
        if not self.contains(result):
            raise ArithmeticError("binary-curve addition produced an off-curve point")
        return result

    def scalar_mul(self, scalar: int, point: BinaryPoint) -> BinaryPoint:
        if scalar < 0:
            return self.scalar_mul(-scalar, self.neg(point))
        if not self.contains(point):
            raise ValueError("point is not on the curve")
        result: BinaryPoint = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def frobenius_point(self, point: BinaryPoint, power: int = 1) -> BinaryPoint:
        """Apply the absolute 2-power Frobenius coordinatewise."""
        if point is None:
            return None
        if not self.contains(point):
            raise ValueError("point is not on the curve")
        image = (
            self.field.frobenius(point[0], power),
            self.field.frobenius(point[1], power),
        )
        return image

    def points(self, coordinate_values: Iterable[int] | None = None) -> list[BinaryPoint]:
        """Enumerate points over the supplied coordinate set (the whole field by default)."""
        values = tuple(range(self.field.order) if coordinate_values is None else coordinate_values)
        points: list[BinaryPoint] = [None]
        for x in values:
            for y in values:
                point = x, y
                if self.contains(point):
                    points.append(point)
        return points

    def point_order(self, point: BinaryPoint, maximum: int | None = None) -> int:
        """Return a point order by repeated addition, for toy-size validation only."""
        if point is None:
            return 1
        if not self.contains(point):
            raise ValueError("point is not on the curve")
        bound = (
            self.field.order + 1 + 2 * isqrt(self.field.order)
            if maximum is None
            else maximum
        )
        current: BinaryPoint = None
        for order in range(1, bound + 1):
            current = self.add(current, point)
            if current is None:
                return order
        raise ArithmeticError("point order exceeds the configured bound")
