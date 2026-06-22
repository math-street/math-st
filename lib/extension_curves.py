"""Short-Weierstrass curves over the tiny extension fields in finite_fields.py."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from random import Random
from typing import Iterator, TypeAlias

from .curves import is_prime
from .finite_fields import ExtensionElement, ExtensionField

ExtensionPoint: TypeAlias = tuple[ExtensionElement, ExtensionElement] | None


@dataclass(frozen=True, slots=True)
class ExtensionCurve:
    field: ExtensionField
    a: ExtensionElement
    b: ExtensionElement

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", self.field.element(self.a))
        object.__setattr__(self, "b", self.field.element(self.b))
        if not 4 * self.a**3 + 27 * self.b**2:
            raise ValueError("singular curve")

    def contains(self, point: ExtensionPoint) -> bool:
        if point is None:
            return True
        x, y = point
        return y * y == x**3 + self.a * x + self.b

    def neg(self, point: ExtensionPoint) -> ExtensionPoint:
        if point is None:
            return None
        return point[0], -point[1]

    def add(self, left: ExtensionPoint, right: ExtensionPoint) -> ExtensionPoint:
        if left is None:
            return right
        if right is None:
            return left
        x1, y1 = left
        x2, y2 = right
        if x1 == x2:
            if y1 + y2 == self.field.zero:
                return None
            slope = (3 * x1 * x1 + self.a) / (2 * y1)
        else:
            slope = (y2 - y1) / (x2 - x1)
        x3 = slope * slope - x1 - x2
        y3 = slope * (x1 - x3) - y1
        return x3, y3

    def scalar_mul(self, scalar: int, point: ExtensionPoint) -> ExtensionPoint:
        if scalar < 0:
            return self.scalar_mul(-scalar, self.neg(point))
        result: ExtensionPoint = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def square_roots(self) -> dict[ExtensionElement, list[ExtensionElement]]:
        roots: dict[ExtensionElement, list[ExtensionElement]] = defaultdict(list)
        for value in self.field.elements():
            roots[value * value].append(value)
        return dict(roots)

    def affine_points(
        self,
        roots: dict[ExtensionElement, list[ExtensionElement]] | None = None,
    ) -> Iterator[tuple[ExtensionElement, ExtensionElement]]:
        roots = roots or self.square_roots()
        for x in self.field.elements():
            rhs = x**3 + self.a * x + self.b
            for y in roots.get(rhs, ()):
                yield x, y

    def points(
        self,
        roots: dict[ExtensionElement, list[ExtensionElement]] | None = None,
    ) -> list[ExtensionPoint]:
        return [None, *self.affine_points(roots)]


def find_prime_order_extension_curve(
    field: ExtensionField,
    rng: Random,
    max_attempts: int = 10_000,
) -> tuple[ExtensionCurve, list[ExtensionPoint], int]:
    """Sample curves and enumerate points until the group order is prime."""
    elements = list(field.elements())
    square_roots: dict[ExtensionElement, list[ExtensionElement]] = defaultdict(list)
    for value in elements:
        square_roots[value * value].append(value)
    for attempt in range(1, max_attempts + 1):
        try:
            curve = ExtensionCurve(field, rng.choice(elements), rng.choice(elements))
        except ValueError:
            continue
        points = curve.points(dict(square_roots))
        if is_prime(len(points)):
            return curve, points, attempt
    raise RuntimeError(f"no prime-order extension curve found in {max_attempts} attempts")


def subfield_x_factor_base(
    curve: ExtensionCurve,
    roots: dict[ExtensionElement, list[ExtensionElement]] | None = None,
) -> list[ExtensionPoint]:
    roots = roots or curve.square_roots()
    factor_base: list[ExtensionPoint] = []
    for x in curve.field.base_elements():
        rhs = x**3 + curve.a * x + curve.b
        factor_base.extend((x, y) for y in roots.get(rhs, ()))
    return factor_base
