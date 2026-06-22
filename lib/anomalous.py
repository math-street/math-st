"""Toy Smart-style anomalous-curve DLP over a lift modulo p squared.

This module is for primitive validation at small parameters. It is not a
constant-time or production elliptic-curve implementation.
"""

from __future__ import annotations

from collections import Counter
from typing import TypeAlias

from .curves import AffinePoint, Curve

JacobianPoint: TypeAlias = tuple[int, int, int] | None


def _lift_affine_point(curve: Curve, point: AffinePoint, trace: Counter[str]) -> JacobianPoint:
    if point is None:
        return None
    x, y = point
    p = curve.p
    modulus = p * p
    rhs = (x**3 + curve.a * x + curve.b) % modulus
    difference = (rhs - y * y) % modulus
    if difference % p:
        raise ArithmeticError("the input is not a point modulo p")
    correction = (difference // p) * pow(2 * y, -1, p) % p
    lifted_y = (y + correction * p) % modulus
    if (lifted_y * lifted_y - rhs) % modulus:
        raise ArithmeticError("Hensel lift failed")
    trace["p_adic_lift"] += 1
    trace["coordinate_arithmetic"] += 1
    return x % modulus, lifted_y, 1


def _double(
    point: JacobianPoint, curve_a: int, modulus: int, trace: Counter[str]
) -> JacobianPoint:
    if point is None:
        return None
    x_coord, y_coord, z_coord = point
    if y_coord % modulus == 0:
        return None
    square_y = y_coord * y_coord % modulus
    s_value = 4 * x_coord * square_y % modulus
    m_value = (3 * x_coord * x_coord + curve_a * pow(z_coord, 4, modulus)) % modulus
    x_result = (m_value * m_value - 2 * s_value) % modulus
    y_result = (m_value * (s_value - x_result) - 8 * square_y * square_y) % modulus
    z_result = 2 * y_coord * z_coord % modulus
    trace["lifted_group_operation"] += 1
    trace["coordinate_arithmetic"] += 1
    return x_result, y_result, z_result


def _add(
    left: JacobianPoint,
    right: JacobianPoint,
    curve_a: int,
    modulus: int,
    trace: Counter[str],
) -> JacobianPoint:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1, z1 = left
    x2, y2, z2 = right
    u1 = x1 * z2 * z2 % modulus
    u2 = x2 * z1 * z1 % modulus
    s1 = y1 * z2 * z2 * z2 % modulus
    s2 = y2 * z1 * z1 * z1 % modulus
    h_value = (u2 - u1) % modulus
    r_value = (s2 - s1) % modulus
    if h_value == 0:
        return _double(left, curve_a, modulus, trace) if r_value == 0 else None
    square_h = h_value * h_value % modulus
    cube_h = h_value * square_h % modulus
    v_value = u1 * square_h % modulus
    x_result = (r_value * r_value - cube_h - 2 * v_value) % modulus
    y_result = (r_value * (v_value - x_result) - s1 * cube_h) % modulus
    z_result = h_value * z1 * z2 % modulus
    trace["lifted_group_operation"] += 1
    trace["coordinate_arithmetic"] += 1
    return x_result, y_result, z_result


def _scalar_mul(
    scalar: int,
    point: JacobianPoint,
    curve_a: int,
    modulus: int,
    trace: Counter[str],
) -> JacobianPoint:
    result: JacobianPoint = None
    addend = point
    while scalar:
        if scalar & 1:
            result = _add(result, addend, curve_a, modulus, trace)
        addend = _double(addend, curve_a, modulus, trace)
        scalar >>= 1
    return result


def _formal_parameter_div_p(point: JacobianPoint, p: int) -> int:
    if point is None:
        raise ArithmeticError("the lifted p-multiple is the exact identity")
    x_coord, y_coord, z_coord = point
    if z_coord % p != 0 or y_coord % p == 0:
        raise ArithmeticError("the p-multiple is not in the expected formal-group chart")
    return (-x_coord * (z_coord // p) * pow(y_coord, -1, p)) % p


def additive_transfer(
    curve: Curve,
    point: AffinePoint,
    *,
    trace: Counter[str] | None = None,
    validate_curve: bool = True,
) -> int:
    """Evaluate the Smart formal-group character on one anomalous point."""
    if point is None:
        return 0
    if not curve.contains(point):
        raise ValueError("the input must lie on the curve")
    if validate_curve and sum(1 for _ in curve.affine_points()) + 1 != curve.p:
        raise ValueError("the additive transfer requires #E(F_p)=p")
    operation_trace = trace if trace is not None else Counter()
    p = curve.p
    lifted_point = _lift_affine_point(curve, point, operation_trace)
    p_point = _scalar_mul(p, lifted_point, curve.a, p * p, operation_trace)
    return _formal_parameter_div_p(p_point, p)


def smart_attack(
    curve: Curve,
    generator: AffinePoint,
    target: AffinePoint,
    *,
    trace: Counter[str] | None = None,
) -> int:
    """Recover ``k`` from ``target = [k]generator`` on an anomalous curve.

    The lift is performed modulo ``p^2`` and the formal parameter ``-x/y`` is
    read from the projective ``p``-multiples. Some exceptional lifts can make
    the denominator vanish; the validated fixtures avoid that degeneracy.
    """

    if generator is None or target is None:
        raise ValueError("generator and target must be affine")
    if not curve.contains(generator) or not curve.contains(target):
        raise ValueError("inputs must lie on the curve")
    if sum(1 for _ in curve.affine_points()) + 1 != curve.p:
        raise ValueError("Smart's attack requires an anomalous curve with #E(F_p)=p")
    operation_trace = trace if trace is not None else Counter()
    p = curve.p
    generator_log = additive_transfer(
        curve, generator, trace=operation_trace, validate_curve=False
    )
    target_log = additive_transfer(
        curve, target, trace=operation_trace, validate_curve=False
    )
    if generator_log == 0:
        raise ArithmeticError("exceptional lift produced a zero formal logarithm")
    recovered = target_log * pow(generator_log, -1, p) % p
    operation_trace["formal_group_ratio"] += 1
    return recovered
