"""Auditable toy implementation of Cheon's divisor-case recovery algorithm."""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Generic, Protocol, TypeVar

from lib.curves import is_prime


ElementT = TypeVar("ElementT")


class ScalarMultiplicationGroup(Protocol[ElementT]):
    """The group interface used by the attack; elements remain opaque."""

    def scalar_mul(self, scalar: int, point: ElementT) -> ElementT: ...


@dataclass(frozen=True, slots=True)
class OrbitSearchStats:
    orbit_order: int
    width: int
    baby_entries: int
    giant_probes: int
    scalar_multiplications: int


@dataclass(frozen=True, slots=True)
class CheonStats:
    stage_one: OrbitSearchStats | None
    stage_two: OrbitSearchStats | None
    verification_scalar_multiplications: int
    zero_secret: bool = False

    @property
    def scalar_multiplications(self) -> int:
        return (
            (self.stage_one.scalar_multiplications if self.stage_one else 0)
            + (self.stage_two.scalar_multiplications if self.stage_two else 0)
            + self.verification_scalar_multiplications
        )

    @property
    def table_probes(self) -> int:
        return (
            (self.stage_one.giant_probes if self.stage_one else 0)
            + (self.stage_two.giant_probes if self.stage_two else 0)
        )


def _prime_factors(integer: int) -> list[int]:
    """Return the distinct prime divisors of a positive integer."""

    if integer < 1:
        raise ValueError("integer must be positive")
    factors: list[int] = []
    divisor = 2
    remainder = integer
    while divisor * divisor <= remainder:
        if remainder % divisor == 0:
            factors.append(divisor)
            while remainder % divisor == 0:
                remainder //= divisor
        divisor += 1 if divisor == 2 else 2
    if remainder > 1:
        factors.append(remainder)
    return factors


def primitive_root_mod_prime(prime: int) -> int:
    """Return the least primitive root modulo an odd prime."""

    if prime <= 2 or not is_prime(prime):
        raise ValueError("modulus must be an odd prime")
    factors = _prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ArithmeticError("an odd prime must have a primitive root")


def multiplicative_orbit_bsgs(
    group: ScalarMultiplicationGroup[ElementT],
    generator: ElementT,
    target: ElementT,
    *,
    field_modulus: int,
    offset: int,
    multiplier: int,
    orbit_order: int,
) -> tuple[int, OrbitSearchStats]:
    """Find ``k`` with target exponent ``offset * multiplier**k`` modulo p."""

    if orbit_order < 1:
        raise ValueError("orbit order must be positive")
    offset %= field_modulus
    multiplier %= field_modulus
    if offset == 0 or multiplier == 0:
        raise ValueError("offset and multiplier must be nonzero field elements")
    if pow(multiplier, orbit_order, field_modulus) != 1:
        raise ValueError("multiplier does not have the stated orbit order")

    width = isqrt(orbit_order - 1) + 1
    scalar_multiplications = 1
    current = group.scalar_mul(offset, generator)
    babies: dict[ElementT, int] = {}
    for baby_index in range(width):
        babies.setdefault(current, baby_index)
        if baby_index + 1 < width:
            current = group.scalar_mul(multiplier, current)
            scalar_multiplications += 1

    inverse_giant_multiplier = pow(pow(multiplier, width, field_modulus), -1, field_modulus)
    current = target
    giant_probes = 0
    for giant_index in range(width + 1):
        giant_probes += 1
        baby_index = babies.get(current)
        if baby_index is not None:
            candidate = giant_index * width + baby_index
            if candidate < orbit_order:
                return candidate, OrbitSearchStats(
                    orbit_order=orbit_order,
                    width=width,
                    baby_entries=len(babies),
                    giant_probes=giant_probes,
                    scalar_multiplications=scalar_multiplications,
                )
        if giant_index < width:
            current = group.scalar_mul(inverse_giant_multiplier, current)
            scalar_multiplications += 1
    raise ValueError("target is not in the stated multiplicative orbit")


def cheon_recover(
    group: ScalarMultiplicationGroup[ElementT],
    generator: ElementT,
    identity: ElementT,
    gx: ElementT,
    gxd: ElementT,
    order: int,
    d: int,
    *,
    primitive_root: int | None = None,
) -> tuple[int, CheonStats]:
    """Recover x from g, g^x, and g^(x^d) when d divides order - 1."""

    if not is_prime(order):
        raise ValueError("group order must be prime")
    if d < 1 or (order - 1) % d:
        raise ValueError("d must be a positive divisor of order - 1")
    if gx == identity:
        return 0, CheonStats(None, None, 0, zero_secret=True)

    root = primitive_root if primitive_root is not None else primitive_root_mod_prime(order)
    if pow(root, order - 1, order) != 1 or any(
        pow(root, (order - 1) // factor, order) == 1
        for factor in _prime_factors(order - 1)
    ):
        raise ValueError("primitive_root does not generate the multiplicative field group")

    quotient = (order - 1) // d
    dth_power_generator = pow(root, d, order)
    power_index, stage_one = multiplicative_orbit_bsgs(
        group,
        generator,
        gxd,
        field_modulus=order,
        offset=1,
        multiplier=dth_power_generator,
        orbit_order=quotient,
    )

    canonical_root = pow(root, power_index, order)
    root_of_unity = pow(root, quotient, order)
    root_index, stage_two = multiplicative_orbit_bsgs(
        group,
        generator,
        gx,
        field_modulus=order,
        offset=canonical_root,
        multiplier=root_of_unity,
        orbit_order=d,
    )
    recovered = canonical_root * pow(root_of_unity, root_index, order) % order
    if group.scalar_mul(recovered, generator) != gx:
        raise ArithmeticError("recovered scalar does not reproduce g^x")
    return recovered, CheonStats(stage_one, stage_two, 1)


@dataclass(frozen=True, slots=True)
class OpaqueElement:
    """An opaque handle used by the toy generic-group simulator."""

    _encoding: int


class OpaquePrimeOrderGroup(Generic[ElementT]):
    """Additive prime-order group simulator with auditable scalar-mul costs."""

    def __init__(self, order: int) -> None:
        if not is_prime(order):
            raise ValueError("order must be prime")
        self.order = order
        self.identity = OpaqueElement(0)
        self.generator = OpaqueElement(1)
        self.trace: dict[str, int] = {}
        self.reset_trace()

    def reset_trace(self) -> None:
        self.trace = {
            "oracle_scalar_multiplication": 0,
            "group_operation": 0,
        }

    def scalar_mul(self, scalar: int, point: OpaqueElement) -> OpaqueElement:
        normalized = scalar % self.order
        self.trace["oracle_scalar_multiplication"] += 1
        if normalized:
            self.trace["group_operation"] += normalized.bit_length() + normalized.bit_count()
        return OpaqueElement(normalized * point._encoding % self.order)

