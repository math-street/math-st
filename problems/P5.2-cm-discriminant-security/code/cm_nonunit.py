"""The explicit norm-two discriminant -7 GLV endomorphism at toy scale."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

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
)

from cm_units import prime_divisors


@dataclass(frozen=True, slots=True)
class CM7Case:
    """One prime-field realization of the GLV discriminant -7 example."""

    curve: ShortWeierstrassCurve
    group_order: int
    subgroup_order: int
    generator: Point
    omega: int
    kernel_x: int
    endomorphism_scalar: int
    scalar_order: int

    @property
    def cofactor(self) -> int:
        return self.group_order // self.subgroup_order


def cm7_short_coefficients(p: int) -> tuple[int, int]:
    """Return the short model after x_old = x_short + 1/4."""

    return (-35 * pow(16, -1, p)) % p, (-49 * pow(32, -1, p)) % p


def make_cm7_parameters(p: int) -> tuple[int, int]:
    """Return omega=(1+sqrt(-7))/2 and a=(omega-3)/4."""

    root = sqrt_mod(-7, p)
    if root is None or root == 0:
        raise ValueError("-7 must have a nonzero square root in the field")
    omega = (1 + root) * pow(2, -1, p) % p
    kernel_x = (omega - 3) * pow(4, -1, p) % p
    if (omega * omega - omega + 2) % p:
        raise ArithmeticError("omega does not satisfy its defining polynomial")
    return omega, kernel_x


def cm7_endomorphism(case: CM7Case, point: Point) -> Point:
    """Apply GLV Example 5 on the translated short-Weierstrass model."""

    if point.is_infinity:
        return INFINITY
    assert point.x is not None and point.y is not None
    p = case.curve.p
    old_x = (point.x + pow(4, -1, p)) % p
    denominator = (old_x - case.kernel_x) % p
    if denominator == 0:
        return INFINITY

    x_numerator = (old_x * old_x - case.omega) % p
    y_numerator = (
        old_x * old_x - 2 * case.kernel_x * old_x + case.omega
    ) % p
    image_old_x = (
        pow(case.omega, -2, p)
        * x_numerator
        * pow(denominator, -1, p)
    ) % p
    image_y = (
        pow(case.omega, -3, p)
        * point.y
        * y_numerator
        * pow(denominator * denominator % p, -1, p)
    ) % p
    image_x = (image_old_x - pow(4, -1, p)) % p
    return case.curve.point(image_x, image_y)


def multiplicative_order_mod_prime(value: int, prime: int) -> int:
    """Return the exact order of a nonzero residue modulo a prime."""

    value %= prime
    if value == 0:
        raise ValueError("zero has no multiplicative order")
    order = prime - 1
    for divisor in prime_divisors(order):
        while order % divisor == 0 and pow(value, order // divisor, prime) == 1:
            order //= divisor
    return order


def _construct_at_prime(p: int, minimum_subgroup_bits: int) -> CM7Case | None:
    try:
        omega, kernel_x = make_cm7_parameters(p)
    except ValueError:
        return None
    a_coeff, b_coeff = cm7_short_coefficients(p)
    affine_curve = Curve(p, a_coeff, b_coeff)
    group_order = curve_order(affine_curve)

    for subgroup_order in sorted(prime_divisors(group_order), reverse=True):
        if subgroup_order <= 2 or subgroup_order.bit_length() < minimum_subgroup_bits:
            continue
        discriminant_root = sqrt_mod(-7, subgroup_order)
        if discriminant_root is None:
            continue
        affine_generator = find_point_of_order(
            affine_curve,
            group_order,
            subgroup_order,
        )
        curve = ShortWeierstrassCurve(p, a_coeff, b_coeff)
        generator = curve.point(*affine_generator)
        provisional = CM7Case(
            curve=curve,
            group_order=group_order,
            subgroup_order=subgroup_order,
            generator=generator,
            omega=omega,
            kernel_x=kernel_x,
            endomorphism_scalar=1,
            scalar_order=1,
        )
        image = cm7_endomorphism(provisional, generator)
        inverse_two = pow(2, -1, subgroup_order)
        candidates = (
            (1 + discriminant_root) * inverse_two % subgroup_order,
            (1 - discriminant_root) * inverse_two % subgroup_order,
        )
        matching = [
            scalar
            for scalar in candidates
            if curve.scalar_mul(scalar, generator, charge=False) == image
        ]
        if len(matching) != 1:
            continue
        scalar = matching[0]
        return CM7Case(
            curve=curve,
            group_order=group_order,
            subgroup_order=subgroup_order,
            generator=generator,
            omega=omega,
            kernel_x=kernel_x,
            endomorphism_scalar=scalar,
            scalar_order=multiplicative_order_mod_prime(scalar, subgroup_order),
        )
    return None


def construct_cm7_case(bits: int, minimum_subgroup_bits: int | None = None) -> CM7Case:
    """Search downward for a split prime with a large invariant subgroup."""

    if bits < 7:
        raise ValueError("bits must be at least seven")
    threshold = minimum_subgroup_bits or max(5, bits - 2)
    candidate = (1 << bits) - 1
    if candidate % 2 == 0:
        candidate -= 1
    lower_bound = 1 << (bits - 1)
    while candidate >= lower_bound:
        if is_prime(candidate):
            case = _construct_at_prime(candidate, threshold)
            if case is not None:
                return case
        candidate -= 2
    raise RuntimeError(f"no discriminant -7 case found at {bits} bits")


def _sample_affine_point(curve: ShortWeierstrassCurve, rng: Random) -> Point:
    affine_curve = Curve(curve.p, curve.a, curve.b)
    while True:
        points = affine_curve.points_for_x(rng.randrange(curve.p))
        if points:
            x_coord, y_coord = points[rng.randrange(len(points))]  # type: ignore[misc]
            return curve.point(x_coord, y_coord)


def canonicalize_cm7_orbit(case: CM7Case, point: Point) -> tuple[Point, int, int]:
    """Enumerate the full scalar orbit and return its least point and exponent."""

    if point.is_infinity:
        return INFINITY, 0, 0

    def key(active: Point) -> tuple[int, int]:
        assert active.x is not None and active.y is not None
        return active.x, active.y

    best = point
    best_exponent = 0
    current = point
    for exponent in range(1, case.scalar_order):
        current = cm7_endomorphism(case, current)
        if key(current) < key(best):
            best = current
            best_exponent = exponent
    closure = cm7_endomorphism(case, current)
    if closure != point:
        raise ArithmeticError("endomorphism orbit did not close at the scalar order")
    return best, best_exponent, case.scalar_order - 1


def validate_cm7_case(
    case: CM7Case,
    *,
    samples: int = 32,
    seed: int = 20260722,
) -> dict[str, int]:
    """Validate independent counts, the CM relation, and subgroup action."""

    if samples < 1:
        raise ValueError("samples must be positive")
    affine_curve = Curve(case.curve.p, case.curve.a, case.curve.b)
    exhaustive_order = curve_order(affine_curve)
    bsgs_order = curve_order_bsgs(affine_curve, Random(seed))
    if exhaustive_order != case.group_order or bsgs_order != case.group_order:
        raise ArithmeticError("independent point counts disagree")
    if case.curve.scalar_mul(case.subgroup_order, case.generator, charge=False) != INFINITY:
        raise ArithmeticError("subgroup order does not annihilate its generator")
    image = cm7_endomorphism(case, case.generator)
    if image != case.curve.scalar_mul(
        case.endomorphism_scalar,
        case.generator,
        charge=False,
    ):
        raise ArithmeticError("endomorphism scalar is wrong")
    scalar = case.endomorphism_scalar
    if (scalar * scalar - scalar + 2) % case.subgroup_order:
        raise ArithmeticError("endomorphism scalar violates x^2-x+2")
    if multiplicative_order_mod_prime(scalar, case.subgroup_order) != case.scalar_order:
        raise ArithmeticError("stored scalar order is not exact")

    rng = Random(seed)
    for _ in range(samples):
        point = _sample_affine_point(case.curve, rng)
        first_image = cm7_endomorphism(case, point)
        second_image = cm7_endomorphism(case, first_image)
        characteristic_point = case.curve.add(
            case.curve.add(second_image, case.curve.neg(first_image), charge=False),
            case.curve.scalar_mul(2, point, charge=False),
            charge=False,
        )
        if characteristic_point != INFINITY:
            raise ArithmeticError("endomorphism characteristic equation failed")

        left_scalar = rng.randrange(case.subgroup_order)
        right_scalar = rng.randrange(case.subgroup_order)
        left = case.curve.scalar_mul(left_scalar, case.generator, charge=False)
        right = case.curve.scalar_mul(right_scalar, case.generator, charge=False)
        if cm7_endomorphism(case, case.curve.add(left, right, charge=False)) != case.curve.add(
            cm7_endomorphism(case, left),
            cm7_endomorphism(case, right),
            charge=False,
        ):
            raise ArithmeticError("endomorphism additivity check failed")

    return {
        "exhaustive_order": exhaustive_order,
        "bsgs_order": bsgs_order,
        "samples": samples,
        "endomorphism_scalar": case.endomorphism_scalar,
        "scalar_order": case.scalar_order,
    }
