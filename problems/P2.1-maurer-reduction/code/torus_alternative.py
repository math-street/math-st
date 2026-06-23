"""
torus_alternative - Toy validation of the quadratic norm-one torus formulas.
Sub-goal: P2.1 / SG-09 and A004
Inputs:   an odd toy prime p, a nonsquare d modulo p, and explicit elements
Outputs:  explicit points on x^2 - d*y^2 = 1 over F_p
Runtime:  exhaustive enumeration is O(p^2) and restricted to tests below 60 bits.
Validated against: exhaustive point sets in code/tests/test_torus_alternative.py.
"""

from __future__ import annotations

TorusPoint = tuple[int, int]


def torus_on_curve(prime: int, nonsquare: int, point: TorusPoint) -> bool:
    """Return whether point satisfies x^2 - d*y^2 = 1 modulo prime."""
    x, y = point
    return (x * x - nonsquare * y * y - 1) % prime == 0


def torus_mul(
    prime: int,
    nonsquare: int,
    left: TorusPoint,
    right: TorusPoint,
) -> TorusPoint:
    """Multiply x+y*sqrt(d) coordinates in the norm-one torus."""
    x, y = left
    u, v = right
    return (
        (x * u + nonsquare * y * v) % prime,
        (x * v + y * u) % prime,
    )


def torus_embed(prime: int, nonsquare: int, value: int) -> TorusPoint:
    """Parametrize the torus minus (-1,0) by one base-field value."""
    value %= prime
    denominator = (1 - nonsquare * value * value) % prime
    if denominator == 0:
        raise ValueError("parameter denominator is zero; d must be a nonsquare")
    inverse = pow(denominator, -1, prime)
    return (
        ((1 + nonsquare * value * value) * inverse) % prime,
        (2 * value * inverse) % prime,
    )


def torus_extract(prime: int, point: TorusPoint) -> int:
    """Invert torus_embed on every point other than (-1,0)."""
    x, y = point
    denominator = (x + 1) % prime
    if denominator == 0:
        raise ValueError("the exceptional point (-1,0) has no finite parameter")
    return y * pow(denominator, -1, prime) % prime


def enumerate_norm_one_torus(prime: int, nonsquare: int) -> set[TorusPoint]:
    """Exhaustively enumerate the toy norm-one torus."""
    return {
        (x, y)
        for x in range(prime)
        for y in range(prime)
        if torus_on_curve(prime, nonsquare, (x, y))
    }
