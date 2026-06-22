"""Exact rational elliptic-curve arithmetic and canonical-height estimates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log
from typing import TypeAlias

RationalPoint: TypeAlias = tuple[Fraction, Fraction] | None


def _as_fraction(value: int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _log_abs_integer(value: int) -> float:
    """Compute log(abs(value)) without converting a huge integer to float."""
    value = abs(value)
    if value == 0:
        raise ValueError("logarithmic height is undefined for zero numerator and denominator")
    bits = value.bit_length()
    if bits <= 53:
        return log(value)
    shift = bits - 53
    return log(value >> shift) + shift * log(2.0)


def rational_log_height(value: Fraction) -> float:
    """Return log(max(abs(numerator), denominator)) for a reduced rational."""
    if value.numerator == 0:
        return 0.0
    return max(_log_abs_integer(value.numerator), _log_abs_integer(value.denominator))


@dataclass(frozen=True, slots=True)
class HeightEstimate:
    """A finite-iteration canonical-height estimate and convergence diagnostic."""

    value: float
    previous: float | None
    delta: float | None
    iterations: int


@dataclass(frozen=True, slots=True)
class WeierstrassCurveQ:
    """A generalized Weierstrass curve over Q.

    The equation is
    y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6.
    """

    a1: Fraction
    a2: Fraction
    a3: Fraction
    a4: Fraction
    a6: Fraction

    @classmethod
    def from_coefficients(
        cls, coefficients: tuple[int | Fraction, ...] | list[int | Fraction]
    ) -> "WeierstrassCurveQ":
        if len(coefficients) != 5:
            raise ValueError("expected the five coefficients a1,a2,a3,a4,a6")
        return cls(*(_as_fraction(value) for value in coefficients))

    @property
    def b2(self) -> Fraction:
        return self.a1 * self.a1 + 4 * self.a2

    @property
    def b4(self) -> Fraction:
        return 2 * self.a4 + self.a1 * self.a3

    @property
    def b6(self) -> Fraction:
        return self.a3 * self.a3 + 4 * self.a6

    @property
    def b8(self) -> Fraction:
        return (
            self.a1 * self.a1 * self.a6
            + 4 * self.a2 * self.a6
            - self.a1 * self.a3 * self.a4
            + self.a2 * self.a3 * self.a3
            - self.a4 * self.a4
        )

    @property
    def discriminant(self) -> Fraction:
        return (
            -(self.b2 * self.b2) * self.b8
            - 8 * self.b4**3
            - 27 * self.b6**2
            + 9 * self.b2 * self.b4 * self.b6
        )

    def contains(self, point: RationalPoint) -> bool:
        if point is None:
            return True
        x, y = point
        return (
            y * y + self.a1 * x * y + self.a3 * y
            == x**3 + self.a2 * x * x + self.a4 * x + self.a6
        )

    def short_model(self) -> tuple[Fraction, Fraction]:
        """Return A,B for the isomorphic curve Y^2 = X^3 + A*X + B."""
        c4 = self.b2 * self.b2 - 24 * self.b4
        c6 = -self.b2**3 + 36 * self.b2 * self.b4 - 216 * self.b6
        return -27 * c4, -54 * c6

    def to_short(self, point: RationalPoint) -> RationalPoint:
        if point is None:
            return None
        x, y = point
        return (
            36 * x + 3 * self.b2,
            108 * (2 * y + self.a1 * x + self.a3),
        )

    def from_short(self, point: RationalPoint) -> RationalPoint:
        if point is None:
            return None
        x_short, y_short = point
        x = (x_short - 3 * self.b2) / 36
        y = (y_short / 108 - self.a1 * x - self.a3) / 2
        return x, y

    def add(self, left: RationalPoint, right: RationalPoint) -> RationalPoint:
        short_a, _ = self.short_model()
        result = short_add(self.to_short(left), self.to_short(right), short_a)
        return self.from_short(result)

    def scalar_mul(self, scalar: int, point: RationalPoint) -> RationalPoint:
        if scalar < 0:
            if point is None:
                return None
            x, y = point
            return self.scalar_mul(-scalar, (x, -y - self.a1 * x - self.a3))
        result: RationalPoint = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def canonical_height_estimate(
        self, point: RationalPoint, iterations: int = 7
    ) -> HeightEstimate:
        """Estimate lim 4^-n h_x([2^n]P) using exact rational doubling.

        This is the non-normalized convention used by Sage and LMFDB over Q.
        The returned delta is diagnostic, not a rigorous error bound.
        """
        if iterations < 1:
            raise ValueError("iterations must be positive")
        if point is None:
            return HeightEstimate(0.0, 0.0, 0.0, iterations)
        if not self.contains(point):
            raise ValueError("point is not on the curve")

        short_a, _ = self.short_model()
        short_point = self.to_short(point)
        estimates: list[float] = []
        for step in range(1, iterations + 1):
            short_point = short_add(short_point, short_point, short_a)
            if short_point is None:
                return HeightEstimate(0.0, 0.0, 0.0, iterations)
            original_point = self.from_short(short_point)
            assert original_point is not None
            estimate = rational_log_height(original_point[0]) / (4**step)
            estimates.append(estimate)
        previous = estimates[-2] if len(estimates) >= 2 else None
        delta = abs(estimates[-1] - previous) if previous is not None else None
        return HeightEstimate(estimates[-1], previous, delta, iterations)


def short_add(
    left: RationalPoint, right: RationalPoint, coefficient_a: int | Fraction
) -> RationalPoint:
    """Add points on Y^2 = X^3 + coefficient_a*X + B over Q."""
    if left is None:
        return right
    if right is None:
        return left
    a = _as_fraction(coefficient_a)
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and y1 == -y2:
        return None
    if left == right:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1 + a) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = slope * slope - x1 - x2
    y3 = slope * (x1 - x3) - y1
    return x3, y3
