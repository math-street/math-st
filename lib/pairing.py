"""Stage-separated reduced Tate pairings for auditable toy experiments.

The implementation is deliberately affine and generic over ``ExtensionField``.
It retains vertical-line denominators so that the raw Miller value can be
studied independently of the final exponentiation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .curves import Curve
from .extension_curves import ExtensionCurve, ExtensionPoint
from .finite_fields import ExtensionElement, ExtensionField


@dataclass(frozen=True, slots=True)
class MillerStep:
    """One double or add transition in a left-to-right Miller loop."""

    operation: str
    source: ExtensionPoint
    addend: ExtensionPoint
    result: ExtensionPoint
    line_value: ExtensionElement
    accumulator: ExtensionElement


@dataclass(frozen=True, slots=True)
class SatohMillerInverseResult:
    """Result and audit counters for Satoh's degree-two MI algorithm."""

    point: ExtensionPoint
    candidates_tested: int
    x_candidates: tuple[int, ...]
    undefined_candidates: int = 0


def lift_base_point(
    field: ExtensionField,
    point: tuple[int, int] | None,
) -> ExtensionPoint:
    """Coerce a prime-field affine point into an extension-field curve."""
    if point is None:
        return None
    return field.element(point[0]), field.element(point[1])


def line_quotient(
    curve: ExtensionCurve,
    left: ExtensionPoint,
    right: ExtensionPoint,
    evaluation_point: ExtensionPoint,
    *,
    omit_vertical_denominator: bool = False,
) -> ExtensionElement:
    """Evaluate g_(left,right) = line_(left,right) / vertical_(left+right).

    An identity input represents the constant Miller factor
    ``g_(O,T) = g_(T,O) = 1``.  Otherwise the evaluation point must lie
    outside the zero/pole support of the function.
    """
    if evaluation_point is None:
        raise ValueError("line evaluation requires a finite evaluation point")
    if left is None or right is None:
        return curve.field.one

    x1, y1 = left
    x2, y2 = right
    xq, yq = evaluation_point

    if x1 == x2 and y1 + y2 == curve.field.zero:
        # The line through inverse points is vertical; left + right is O, so
        # the denominator associated with the result is the constant one.
        numerator = xq - x1
        denominator = curve.field.one
    else:
        if left == right:
            if not 2 * y1:
                # The tangent is vertical and the doubled point is O.
                numerator = xq - x1
                denominator = curve.field.one
                if not numerator:
                    raise ZeroDivisionError("evaluation point is a line zero")
                return numerator
            slope = (3 * x1 * x1 + curve.a) / (2 * y1)
        else:
            slope = (y2 - y1) / (x2 - x1)
        numerator = yq - y1 - slope * (xq - x1)
        result = curve.add(left, right)
        denominator = curve.field.one if result is None else xq - result[0]

    if not numerator:
        raise ZeroDivisionError("evaluation point is a line zero")
    if omit_vertical_denominator:
        return numerator
    if not denominator:
        raise ZeroDivisionError("evaluation point is a vertical-line pole")
    return numerator / denominator


def miller_loop_with_trace(
    curve: ExtensionCurve,
    order: int,
    point: ExtensionPoint,
    evaluation_point: ExtensionPoint,
    *,
    omit_vertical_denominators: bool = False,
) -> tuple[ExtensionElement, tuple[MillerStep, ...]]:
    """Evaluate the normalized Miller function f_(order,point)."""
    if order <= 0:
        raise ValueError("order must be positive")
    if point is None or evaluation_point is None:
        raise ValueError("Miller inputs must be finite points")
    if not curve.contains(point) or not curve.contains(evaluation_point):
        raise ValueError("Miller input is not on the curve")
    if order == 1:
        return curve.field.one, ()

    bits = bin(order)[3:]
    accumulator = curve.field.one
    running = point
    trace: list[MillerStep] = []
    for bit in bits:
        doubled = curve.add(running, running)
        factor = line_quotient(
            curve,
            running,
            running,
            evaluation_point,
            omit_vertical_denominator=omit_vertical_denominators,
        )
        accumulator = accumulator * accumulator * factor
        trace.append(
            MillerStep("double", running, running, doubled, factor, accumulator)
        )
        running = doubled

        if bit == "1":
            added = curve.add(running, point)
            factor = line_quotient(
                curve,
                running,
                point,
                evaluation_point,
                omit_vertical_denominator=omit_vertical_denominators,
            )
            accumulator = accumulator * factor
            trace.append(MillerStep("add", running, point, added, factor, accumulator))
            running = added

    expected = curve.scalar_mul(order, point)
    if running != expected:
        raise ArithmeticError("Miller point accumulator disagrees with scalar multiplication")
    return accumulator, tuple(trace)


def miller_loop(
    curve: ExtensionCurve,
    order: int,
    point: ExtensionPoint,
    evaluation_point: ExtensionPoint,
    *,
    omit_vertical_denominators: bool = False,
) -> ExtensionElement:
    """Return only the raw Miller-function evaluation."""
    return miller_loop_with_trace(
        curve,
        order,
        point,
        evaluation_point,
        omit_vertical_denominators=omit_vertical_denominators,
    )[0]


def final_exponentiation(
    value: ExtensionElement,
    subgroup_order: int,
) -> ExtensionElement:
    """Map a nonzero field element to the reduced-Tate target subgroup."""
    if subgroup_order <= 0 or (value.field.order - 1) % subgroup_order:
        raise ValueError("subgroup order must divide the multiplicative field order")
    if not value:
        raise ValueError("final exponentiation is defined on nonzero elements")
    return value ** ((value.field.order - 1) // subgroup_order)


def reduced_tate_pairing(
    curve: ExtensionCurve,
    subgroup_order: int,
    point: ExtensionPoint,
    evaluation_point: ExtensionPoint,
) -> ExtensionElement:
    """Compose the exposed Miller and final-exponentiation stages."""
    return final_exponentiation(
        miller_loop(curve, subgroup_order, point, evaluation_point),
        subgroup_order,
    )


def j1728_distortion_map(
    field: ExtensionField,
    point: tuple[int | ExtensionElement, int | ExtensionElement] | None,
    square_root_of_minus_one: ExtensionElement,
) -> ExtensionPoint:
    """Return (x,y) -> (-x, i*y) for y^2 = x^3 + a*x."""
    if square_root_of_minus_one * square_root_of_minus_one != field.element(-1):
        raise ValueError("the supplied element does not square to -1")
    if point is None:
        return None
    x, y = point
    return field.element(-x), square_root_of_minus_one * y


def satoh_even_miller_inverse_k2(
    curve: ExtensionCurve,
    point_order: int,
    miller_scalar: int,
    fixed_point: ExtensionPoint,
    raw_target: ExtensionElement,
) -> SatohMillerInverseResult:
    """Invert ``f_(miller_scalar,fixed_point)`` on E(F_q) for degree two.

    This is the ``k = 2`` specialization of Satoh's even-embedding-degree
    Miller-inversion algorithm.  It expects ``point_order | miller_scalar``
    and ``miller_scalar | q + 1``.  The fixed point is in the nontrivial
    Frobenius eigenspace, while the returned point is in ``E(F_q)``.
    """
    field = curve.field
    if field.degree != 2:
        raise ValueError("this implementation is specialized to extension degree two")
    if point_order <= 0 or miller_scalar <= 0:
        raise ValueError("point order and Miller scalar must be positive")
    if miller_scalar % point_order or (field.q + 1) % miller_scalar:
        raise ValueError("require point_order | miller_scalar | q + 1")
    if fixed_point is None or not curve.contains(fixed_point):
        raise ValueError("fixed point must be a finite point on the curve")
    if curve.scalar_mul(point_order, fixed_point) is not None:
        raise ValueError("fixed point is not killed by point_order")
    raw_target = field.element(raw_target)
    if not raw_target:
        raise ValueError("raw Miller target must be nonzero")
    if not field.is_base_element(curve.a) or not field.is_base_element(curve.b):
        raise ValueError("curve coefficients must lie in the prime subfield")
    if not field.is_base_element(fixed_point[0]):
        raise ValueError("fixed-point x-coordinate must lie in the prime subfield")

    q = field.q
    u = (raw_target ** ((q + 1) // miller_scalar)) ** ((q + 1) // 2)
    if not field.is_base_element(u):
        return SatohMillerInverseResult(None, 0, ())

    x0 = int(fixed_point[0])
    u0 = int(u)
    x_candidates = tuple(dict.fromkeys(((x0 + u0) % q, (x0 - u0) % q)))
    base_curve = Curve(q, int(curve.a), int(curve.b))
    candidates_tested = 0
    undefined_candidates = 0
    for x_coordinate in x_candidates:
        for base_point in base_curve.points_for_x(x_coordinate):
            candidates_tested += 1
            candidate = lift_base_point(field, base_point)
            if curve.scalar_mul(point_order, candidate) is not None:
                continue
            try:
                observed = miller_loop(curve, miller_scalar, fixed_point, candidate)
            except ZeroDivisionError:
                undefined_candidates += 1
                continue
            if observed == raw_target:
                return SatohMillerInverseResult(
                    candidate,
                    candidates_tested,
                    x_candidates,
                    undefined_candidates,
                )
    return SatohMillerInverseResult(
        None,
        candidates_tested,
        x_candidates,
        undefined_candidates,
    )


def j1728_fapi1_miller_inverse_k2(
    curve: ExtensionCurve,
    subgroup_order: int,
    fixed_base_point: tuple[int, int],
    raw_target: ExtensionElement,
    square_root_of_minus_one: ExtensionElement,
) -> SatohMillerInverseResult:
    """Invert the raw fixed-base Miller map on the distorted subgroup.

    For ``psi(x,y)=(-x,i*y)``, normalized Miller functions satisfy
    ``f_(r,P)(psi(R)) = i**(-r) f_(r,psi**(-1)(P))(R)``.  The function
    transfers the target, invokes Satoh's degree-two algorithm on ``R``, and
    maps the result back with ``psi``.
    """
    field = curve.field
    square_root_of_minus_one = field.element(square_root_of_minus_one)
    fixed_point = lift_base_point(field, fixed_base_point)
    if fixed_point is None or not curve.contains(fixed_point):
        raise ValueError("fixed base point must lie on the curve")
    inverse_distorted_fixed = j1728_distortion_map(
        field,
        fixed_base_point,
        -square_root_of_minus_one,
    )
    transferred_target = square_root_of_minus_one**subgroup_order * raw_target
    base_result = satoh_even_miller_inverse_k2(
        curve,
        subgroup_order,
        subgroup_order,
        inverse_distorted_fixed,
        transferred_target,
    )
    if base_result.point is None:
        return base_result
    distorted = j1728_distortion_map(
        field,
        base_result.point,
        square_root_of_minus_one,
    )
    return SatohMillerInverseResult(
        distorted,
        base_result.candidates_tested,
        base_result.x_candidates,
        base_result.undefined_candidates,
    )
