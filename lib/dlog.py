"""Auditable toy implementations of generic discrete-logarithm algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt
from random import Random
from typing import Any, Callable

from .curves import INFINITY, Point, ShortWeierstrassCurve


@dataclass(frozen=True, slots=True)
class PollardRhoResult:
    """A recovered logarithm and auditable online-walk counters."""

    logarithm: int
    iterations: int
    transitions: int
    collisions: int
    restarts: int
    orbit_applications: int
    cycle_escapes: int


def _factor_prime_powers(integer: int) -> list[tuple[int, int]]:
    factors: list[tuple[int, int]] = []
    divisor = 2
    remainder = integer
    while divisor * divisor <= remainder:
        exponent = 0
        while remainder % divisor == 0:
            remainder //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 1 if divisor == 2 else 2
    if remainder > 1:
        factors.append((remainder, 1))
    return factors


def bsgs(
    curve: ShortWeierstrassCurve,
    generator: Point,
    target: Point,
    order: int,
    *,
    charge: bool = True,
) -> int:
    """Solve ``target = [k]generator`` by baby-step giant-step."""

    width = isqrt(order - 1) + 1
    baby_steps: dict[Point, int] = {}
    current = INFINITY
    for index in range(width):
        curve.trace["equality_test"] += 1
        baby_steps.setdefault(current, index)
        current = curve.add(current, generator, charge=charge)

    giant_step = curve.scalar_mul(-width, generator, charge=charge)
    current = target
    for giant_index in range(width + 1):
        curve.trace["equality_test"] += 1
        baby_index = baby_steps.get(current)
        if baby_index is not None:
            answer = (giant_index * width + baby_index) % order
            if curve.scalar_mul(answer, generator, charge=charge) == target:
                return answer
        current = curve.add(current, giant_step, charge=charge)
    raise ValueError("target is not in the stated subgroup")


def pollard_rho(
    curve: ShortWeierstrassCurve,
    generator: Point,
    target: Point,
    order: int,
    *,
    seed: int = 0,
    max_steps: int | None = None,
) -> int:
    """Solve a prime-order ECDLP with a three-way Pollard-rho walk."""

    if order < 2 or any(order % divisor == 0 for divisor in range(2, isqrt(order) + 1)):
        raise ValueError("this Pollard-rho variant requires prime order")
    rng = Random(seed)
    limit = max_steps or 8 * order

    def step(state: tuple[Point, int, int]) -> tuple[Point, int, int]:
        point, a_coeff, b_coeff = state
        bucket = 0 if point.is_infinity else point.x % 3  # type: ignore[operator]
        if bucket == 0:
            return curve.add(point, generator), (a_coeff + 1) % order, b_coeff
        if bucket == 1:
            return curve.add(point, point), (2 * a_coeff) % order, (2 * b_coeff) % order
        return curve.add(point, target), a_coeff, (b_coeff + 1) % order

    for _ in range(16):
        a0 = rng.randrange(order)
        b0 = rng.randrange(order)
        start = curve.add(curve.scalar_mul(a0, generator), curve.scalar_mul(b0, target))
        tortoise = step((start, a0, b0))
        hare = step(step((start, a0, b0)))
        for _ in range(limit):
            curve.trace["equality_test"] += 1
            if tortoise[0] == hare[0]:
                denominator = (tortoise[2] - hare[2]) % order
                if denominator:
                    numerator = (hare[1] - tortoise[1]) % order
                    answer = numerator * pow(denominator, -1, order) % order
                    if curve.scalar_mul(answer, generator) == target:
                        return answer
                break
            tortoise = step(tortoise)
            hare = step(step(hare))
    raise RuntimeError("Pollard-rho failed after 16 deterministic restarts")


def pollard_rho_orbits(
    curve: ShortWeierstrassCurve,
    generator: Point,
    target: Point,
    order: int,
    *,
    automorphism: Callable[[Point], Point] | None = None,
    automorphism_scalar: int = 1,
    automorphism_order: int = 1,
    seed: int = 0,
    partitions: int = 16,
    max_steps: int | None = None,
    max_restarts: int = 32,
    cycle_escape: bool = False,
    collision_table: bool = False,
) -> PollardRhoResult:
    """Solve a prime-order DLP with an r-adding walk on finite point orbits.

    ``automorphism`` must generate an action of exact ``automorphism_order`` on the
    subgroup and act on ``generator`` as multiplication by
    ``automorphism_scalar``.  Passing no automorphism gives the matching
    unquotiented baseline walk.  The online counters exclude table setup and
    final answer verification.  ``collision_table`` stores visited points to
    expose the quotient-space collision factor; ``cycle_escape`` is an
    experimental local-doubling rule retained for negative-result reproduction.
    """

    if order < 2 or any(order % divisor == 0 for divisor in range(2, isqrt(order) + 1)):
        raise ValueError("this Pollard-rho variant requires prime order")
    if partitions < 3:
        raise ValueError("partitions must be at least three")
    if max_restarts < 1:
        raise ValueError("max_restarts must be positive")
    if automorphism is None:
        if automorphism_order != 1 or automorphism_scalar % order != 1:
            raise ValueError("the baseline walk has a trivial orbit action")
    elif automorphism_order < 2:
        raise ValueError("a supplied automorphism must have order at least two")

    scalar = automorphism_scalar % order
    if pow(scalar, automorphism_order, order) != 1:
        raise ValueError("automorphism scalar does not have the stated order")
    if any(pow(scalar, exponent, order) == 1 for exponent in range(1, automorphism_order)):
        raise ValueError("automorphism scalar has smaller than the stated order")
    if automorphism is not None:
        if automorphism(INFINITY) != INFINITY:
            raise ValueError("automorphism must fix the identity")
        if automorphism(generator) != curve.scalar_mul(scalar, generator, charge=False):
            raise ValueError("automorphism scalar is wrong on the generator")
        if automorphism(target) != curve.scalar_mul(scalar, target, charge=False):
            raise ValueError("automorphism scalar is wrong on the target")

    rng = Random(seed)
    limit = max_steps or 20 * (isqrt(order) + 1)
    total_iterations = 0
    total_transitions = 0
    total_collisions = 0
    total_orbit_applications = 0
    total_cycle_escapes = 0
    zero_denominator_collisions = 0
    wrong_answer_collisions = 0

    def point_key(point: Point) -> tuple[int, int, int]:
        if point.is_infinity:
            return (0, 0, 0)
        assert point.x is not None and point.y is not None
        return (1, point.x, point.y)

    def canonicalize(point: Point, a_coeff: int, b_coeff: int) -> tuple[Point, int, int]:
        nonlocal total_orbit_applications
        if automorphism is None or point.is_infinity:
            return point, a_coeff, b_coeff

        best_point = point
        best_factor = 1
        current = point
        factor = 1
        for _ in range(1, automorphism_order):
            current = automorphism(current)
            total_orbit_applications += 1
            factor = factor * scalar % order
            if point_key(current) < point_key(best_point):
                best_point = current
                best_factor = factor
        return (
            best_point,
            a_coeff * best_factor % order,
            b_coeff * best_factor % order,
        )

    def make_table() -> list[tuple[Point, int, int]]:
        table: list[tuple[Point, int, int]] = []
        for _ in range(partitions):
            u_coeff = rng.randrange(order)
            v_coeff = rng.randrange(order)
            step_point = curve.add(
                curve.scalar_mul(u_coeff, generator, charge=False),
                curve.scalar_mul(v_coeff, target, charge=False),
                charge=False,
            )
            table.append((step_point, u_coeff, v_coeff))
        return table

    def make_step(table: list[tuple[Point, int, int]]) -> Callable[
        [tuple[Point, int, int]], tuple[Point, int, int]
    ]:
        def step(state: tuple[Point, int, int]) -> tuple[Point, int, int]:
            nonlocal total_transitions
            point, a_coeff, b_coeff = state
            if point.is_infinity:
                bucket = 0
            else:
                assert point.x is not None and point.y is not None
                bucket = (point.x + 3 * point.y) % partitions
            step_point, u_coeff, v_coeff = table[bucket]
            next_state = (
                curve.add(point, step_point),
                (a_coeff + u_coeff) % order,
                (b_coeff + v_coeff) % order,
            )
            total_transitions += 1
            return canonicalize(*next_state)

        return step

    if collision_table:
        table = make_table()
        step = make_step(table)
        seen: dict[Point, tuple[int, int]] = {}
        for restart in range(1, max_restarts + 1):
            a0 = rng.randrange(order)
            b0 = rng.randrange(order)
            start_point = curve.add(
                curve.scalar_mul(a0, generator, charge=False),
                curve.scalar_mul(b0, target, charge=False),
                charge=False,
            )
            state = canonicalize(start_point, a0, b0)
            for _ in range(limit):
                total_iterations += 1
                curve.trace["equality_test"] += 1
                previous = seen.get(state[0])
                if previous is not None:
                    total_collisions += 1
                    denominator = (previous[1] - state[2]) % order
                    if denominator:
                        numerator = (state[1] - previous[0]) % order
                        answer = numerator * pow(denominator, -1, order) % order
                        if curve.scalar_mul(answer, generator, charge=False) == target:
                            return PollardRhoResult(
                                logarithm=answer,
                                iterations=total_iterations,
                                transitions=total_transitions,
                                collisions=total_collisions,
                                restarts=restart,
                                orbit_applications=total_orbit_applications,
                                cycle_escapes=0,
                            )
                        wrong_answer_collisions += 1
                        raise ArithmeticError("nondegenerate collision gave a wrong logarithm")
                    else:
                        zero_denominator_collisions += 1
                    break
                seen[state[0]] = (state[1], state[2])
                state = step(state)
        raise RuntimeError(
            f"collision-table orbit rho failed after {max_restarts} starts "
            f"(iterations={total_iterations}, transitions={total_transitions}, "
            f"collisions={total_collisions}, zero_denominators={zero_denominator_collisions}, "
            f"wrong_answers={wrong_answer_collisions})"
        )

    for restart in range(1, max_restarts + 1):
        table = make_table()
        step = make_step(table)

        a0 = rng.randrange(order)
        b0 = rng.randrange(order)
        start_point = curve.add(
            curve.scalar_mul(a0, generator, charge=False),
            curve.scalar_mul(b0, target, charge=False),
            charge=False,
        )
        start = canonicalize(start_point, a0, b0)
        tortoise = step(start)
        hare = step(step(start))

        for _ in range(limit):
            total_iterations += 1
            curve.trace["equality_test"] += 1
            if tortoise[0] == hare[0]:
                total_collisions += 1
                denominator = (tortoise[2] - hare[2]) % order
                if denominator:
                    numerator = (hare[1] - tortoise[1]) % order
                    answer = numerator * pow(denominator, -1, order) % order
                    if curve.scalar_mul(answer, generator, charge=False) == target:
                        return PollardRhoResult(
                            logarithm=answer,
                            iterations=total_iterations,
                            transitions=total_transitions,
                            collisions=total_collisions,
                            restarts=restart,
                            orbit_applications=total_orbit_applications,
                            cycle_escapes=total_cycle_escapes,
                        )
                    wrong_answer_collisions += 1
                    raise ArithmeticError("nondegenerate collision gave a wrong logarithm")
                else:
                    zero_denominator_collisions += 1
                    if cycle_escape:
                        doubled_point = curve.add(tortoise[0], tortoise[0])
                        total_transitions += 1
                        total_cycle_escapes += 1
                        escaped = canonicalize(
                            doubled_point,
                            2 * tortoise[1] % order,
                            2 * tortoise[2] % order,
                        )
                        tortoise = step(escaped)
                        hare = step(step(escaped))
                        continue
                break
            tortoise = step(tortoise)
            hare = step(step(hare))

    raise RuntimeError(
        f"orbit Pollard-rho failed after {max_restarts} deterministic restarts "
        f"(iterations={total_iterations}, transitions={total_transitions}, "
        f"collisions={total_collisions}, zero_denominators={zero_denominator_collisions}, "
        f"wrong_answers={wrong_answer_collisions}, cycle_escapes={total_cycle_escapes})"
    )


def _crt(congruences: list[tuple[int, int]]) -> int:
    modulus = 1
    result = 0
    for residue, next_modulus in congruences:
        if gcd(modulus, next_modulus) != 1:
            raise ValueError("CRT moduli must be pairwise coprime")
        correction = (residue - result) * pow(modulus, -1, next_modulus)
        result += modulus * (correction % next_modulus)
        modulus *= next_modulus
    return result % modulus


def pohlig_hellman(
    curve: ShortWeierstrassCurve,
    generator: Point,
    target: Point,
    order: int,
) -> int:
    """Solve an ECDLP by prime-power digit lifting and BSGS subproblems."""

    congruences: list[tuple[int, int]] = []
    for prime, exponent in _factor_prime_powers(order):
        residue = 0
        digit_generator = curve.scalar_mul(order // prime, generator)
        for digit_index in range(exponent):
            correction = curve.add(target, curve.neg(curve.scalar_mul(residue, generator)))
            digit_target = curve.scalar_mul(order // prime ** (digit_index + 1), correction)
            digit = bsgs(curve, digit_generator, digit_target, prime)
            residue += digit * prime**digit_index
        congruences.append((residue, prime**exponent))
    answer = _crt(congruences)
    if curve.scalar_mul(answer, generator) != target:
        raise ArithmeticError("Pohlig-Hellman reconstruction failed")
    return answer


def multiplicative_bsgs(base: Any, target: Any, order: int) -> int:
    """Solve target = base**k in a multiplicative group of known order."""
    if order < 2:
        raise ValueError("order must be at least two")
    identity = base**0
    width = isqrt(order - 1) + 1
    baby_steps: dict[Any, int] = {}
    current = identity
    for index in range(width):
        baby_steps.setdefault(current, index)
        current = current * base
    giant_step = (base.inverse()) ** width
    current = target
    for giant_index in range(width + 1):
        baby_index = baby_steps.get(current)
        if baby_index is not None:
            answer = (giant_index * width + baby_index) % order
            if base**answer == target:
                return answer
        current = current * giant_step
    raise ValueError("target is not in the stated multiplicative subgroup")
