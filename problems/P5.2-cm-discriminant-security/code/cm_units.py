"""Explicit unit endomorphisms for the toy D=-3 and D=-4 CM families."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Callable

from lib.curves import (
    INFINITY,
    Curve,
    Point,
    ShortWeierstrassCurve,
    curve_order,
    curve_order_bsgs,
    find_point_of_order,
    is_prime,
    sqrt_mod,
    square_root_multiplicities,
)
from lib.dlog import bsgs


@dataclass(frozen=True, slots=True)
class CMCase:
    """A verified-input candidate for one explicit unit action."""

    discriminant: int
    curve: ShortWeierstrassCurve
    group_order: int
    subgroup_order: int
    generator: Point
    field_unit: int
    automorphism_scalar: int
    automorphism_order: int

    @property
    def cofactor(self) -> int:
        return self.group_order // self.subgroup_order


def prime_below_in_residue_class(bits: int, modulus: int, residue: int) -> int:
    """Return the largest prime below 2**bits in one residue class."""

    if bits < 6:
        raise ValueError("bits must be at least six")
    if not 0 <= residue < modulus:
        raise ValueError("residue must be reduced modulo a positive modulus")
    candidate = (1 << bits) - 1
    candidate -= (candidate - residue) % modulus
    while candidate > 3 and not is_prime(candidate):
        candidate -= modulus
    if candidate <= 3:
        raise RuntimeError("no suitable prime found")
    return candidate


def prime_divisors(integer: int) -> tuple[int, ...]:
    """Return the distinct prime divisors by deterministic trial division."""

    if integer < 1:
        raise ValueError("integer must be positive")
    divisors: list[int] = []
    remainder = integer
    candidate = 2
    while candidate * candidate <= remainder:
        if remainder % candidate == 0:
            divisors.append(candidate)
            while remainder % candidate == 0:
                remainder //= candidate
        candidate += 1 if candidate == 2 else 2
    if remainder > 1:
        divisors.append(remainder)
    return tuple(divisors)


def _primitive_cube_root(p: int) -> int:
    for base in range(2, p):
        root = pow(base, (p - 1) // 3, p)
        if root != 1:
            if pow(root, 3, p) != 1:
                raise ArithmeticError("cube-root construction failed")
            return root
    raise RuntimeError("no primitive cube root found")


def unit_automorphism(case: CMCase, point: Point) -> Point:
    """Apply the order-six or order-four unit generator for ``case``."""

    if point.is_infinity:
        return INFINITY
    assert point.x is not None and point.y is not None
    if case.discriminant == -3:
        return case.curve.point(
            case.field_unit * point.x,
            -point.y,
        )
    if case.discriminant == -4:
        return case.curve.point(
            -point.x,
            case.field_unit * point.y,
        )
    raise ValueError("only discriminants -3 and -4 are implemented")


def automorphism_callback(case: CMCase) -> Callable[[Point], Point]:
    """Bind a CM case as a point-map callback."""

    return lambda point: unit_automorphism(case, point)


def _construct_at_prime(
    p: int,
    discriminant: int,
    minimum_subgroup_bits: int,
    roots: bytearray,
) -> CMCase | None:
    if discriminant == -3:
        coefficients = ((0, parameter) for parameter in range(1, min(p, 49)))
        field_unit = _primitive_cube_root(p)
        automorphism_order = 6
    elif discriminant == -4:
        coefficients = ((parameter, 0) for parameter in range(1, min(p, 49)))
        field_unit = sqrt_mod(-1, p)
        if field_unit is None:
            raise ArithmeticError("-1 has no square root at the selected prime")
        automorphism_order = 4
    else:
        raise ValueError("only discriminants -3 and -4 are implemented")

    for a_coeff, b_coeff in coefficients:
        affine_curve = Curve(p, a_coeff, b_coeff)
        group_order = curve_order(affine_curve, roots)
        eligible = [
            prime
            for prime in prime_divisors(group_order)
            if prime.bit_length() >= minimum_subgroup_bits
            and (prime - 1) % automorphism_order == 0
        ]
        if not eligible:
            continue
        subgroup_order = max(eligible)
        affine_generator = find_point_of_order(
            affine_curve,
            group_order,
            subgroup_order,
        )
        curve = ShortWeierstrassCurve(p, a_coeff, b_coeff)
        generator = curve.point(*affine_generator)

        provisional = CMCase(
            discriminant=discriminant,
            curve=curve,
            group_order=group_order,
            subgroup_order=subgroup_order,
            generator=generator,
            field_unit=field_unit,
            automorphism_scalar=1,
            automorphism_order=automorphism_order,
        )
        image = unit_automorphism(provisional, generator)
        scalar = bsgs(
            curve,
            generator,
            image,
            subgroup_order,
            charge=False,
        )
        return CMCase(
            discriminant=discriminant,
            curve=curve,
            group_order=group_order,
            subgroup_order=subgroup_order,
            generator=generator,
            field_unit=field_unit,
            automorphism_scalar=scalar,
            automorphism_order=automorphism_order,
        )
    return None


def construct_cm_pair(bits: int, minimum_subgroup_bits: int | None = None) -> tuple[CMCase, CMCase]:
    """Find D=-3 and D=-4 cases over the same prime field."""

    threshold = minimum_subgroup_bits or max(5, bits - 6)
    p = prime_below_in_residue_class(bits, 12, 1)
    lower_bound = 1 << (bits - 1)
    while p >= lower_bound:
        roots = square_root_multiplicities(p)
        minus_three = _construct_at_prime(p, -3, threshold, roots)
        minus_four = _construct_at_prime(p, -4, threshold, roots)
        if minus_three is not None and minus_four is not None:
            return minus_three, minus_four
        p -= 12
        while p >= lower_bound and not is_prime(p):
            p -= 12
    raise RuntimeError(f"no paired CM cases found at {bits} bits")


def _sample_affine_point(curve: ShortWeierstrassCurve, rng: Random) -> Point:
    affine_curve = Curve(curve.p, curve.a, curve.b)
    while True:
        points = affine_curve.points_for_x(rng.randrange(curve.p))
        if points:
            x_coord, y_coord = points[rng.randrange(len(points))]  # type: ignore[misc]
            return curve.point(x_coord, y_coord)


def validate_cm_case(case: CMCase, *, samples: int = 32, seed: int = 20260722) -> dict[str, int]:
    """Run independent order, subgroup, and endomorphism checks."""

    if samples < 1:
        raise ValueError("samples must be positive")
    affine_curve = Curve(case.curve.p, case.curve.a, case.curve.b)
    exhaustive_order = curve_order(affine_curve)
    bsgs_order = curve_order_bsgs(affine_curve, Random(seed))
    if exhaustive_order != case.group_order or bsgs_order != case.group_order:
        raise ArithmeticError("independent point counts disagree")
    if case.curve.scalar_mul(case.subgroup_order, case.generator, charge=False) != INFINITY:
        raise ArithmeticError("subgroup order does not annihilate its generator")
    if case.generator == INFINITY:
        raise ArithmeticError("subgroup generator is the identity")
    if unit_automorphism(case, case.generator) != case.curve.scalar_mul(
        case.automorphism_scalar,
        case.generator,
        charge=False,
    ):
        raise ArithmeticError("endomorphism eigenvalue is wrong")

    scalar = case.automorphism_scalar % case.subgroup_order
    if case.discriminant == -3:
        characteristic_value = (scalar * scalar - scalar + 1) % case.subgroup_order
    else:
        characteristic_value = (scalar * scalar + 1) % case.subgroup_order
    if characteristic_value:
        raise ArithmeticError("endomorphism scalar violates its characteristic equation")

    rng = Random(seed)
    for _ in range(samples):
        point = _sample_affine_point(case.curve, rng)
        image = unit_automorphism(case, point)
        second_image = unit_automorphism(case, image)
        if case.discriminant == -3:
            characteristic_point = case.curve.add(
                case.curve.add(second_image, case.curve.neg(image), charge=False),
                point,
                charge=False,
            )
        else:
            characteristic_point = case.curve.add(second_image, point, charge=False)
        if characteristic_point != INFINITY:
            raise ArithmeticError("endomorphism characteristic equation failed")

        orbit_point = point
        for _ in range(case.automorphism_order):
            orbit_point = unit_automorphism(case, orbit_point)
        if orbit_point != point:
            raise ArithmeticError("unit action has the wrong exponent")

    return {
        "exhaustive_order": exhaustive_order,
        "bsgs_order": bsgs_order,
        "samples": samples,
        "subgroup_order": case.subgroup_order,
        "automorphism_scalar": case.automorphism_scalar,
    }
