"""Exact Frobenius-span invariants for the classical binary GHS descent."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import BinaryField


def gf2_basis(values: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    """Return a deterministic echelon basis for integer bit vectors over F_2."""
    pivots: dict[int, int] = {}
    for original in values:
        value = original
        while value:
            pivot = value.bit_length() - 1
            if pivot in pivots:
                value ^= pivots[pivot]
                continue
            pivots[pivot] = value
            break
    return tuple(pivots[pivot] for pivot in sorted(pivots, reverse=True))


def gf2_in_span(target: int, basis: tuple[int, ...]) -> bool:
    """Return whether target is in the span of an echelon basis."""
    value = target
    by_pivot = {row.bit_length() - 1: row for row in basis}
    while value:
        pivot = value.bit_length() - 1
        if pivot not in by_pivot:
            return False
        value ^= by_pivot[pivot]
    return True


def frobenius_orbit(
    field: BinaryField, value: int, base_degree: int
) -> tuple[int, ...]:
    """Return one full orbit under x -> x^(2^base_degree)."""
    if base_degree <= 0:
        raise ValueError("base degree must be positive")
    if field.degree % base_degree != 0:
        raise ValueError("base degree must divide the absolute field degree")
    orbit = []
    conjugate = value
    for _ in range(field.degree // base_degree):
        orbit.append(conjugate)
        conjugate = field.frobenius(conjugate, base_degree)
    if conjugate != value:
        raise ArithmeticError("Frobenius did not close after the extension degree")
    return tuple(orbit)


def distinct_orbit_size(orbit: tuple[int, ...]) -> int:
    """Return the least positive period of a closed Frobenius orbit."""
    first = orbit[0]
    for index in range(1, len(orbit)):
        if orbit[index] == first:
            return index
    return len(orbit)


def apply_frobenius_polynomial(
    field: BinaryField, value: int, polynomial: int, base_degree: int
) -> int:
    """Evaluate a binary polynomial at Frobenius and apply it to value."""
    result = 0
    conjugate = value
    coefficients = polynomial
    while coefficients:
        if coefficients & 1:
            result ^= conjugate
        coefficients >>= 1
        conjugate = field.frobenius(conjugate, base_degree)
    return result


def frobenius_annihilator(
    field: BinaryField, value: int, base_degree: int
) -> int:
    """Return the least-degree monic binary polynomial annihilating value."""
    if base_degree <= 0 or field.degree % base_degree != 0:
        raise ValueError("base degree must be a positive divisor of the field degree")
    extension_degree = field.degree // base_degree
    for degree in range(extension_degree + 1):
        leading = 1 << degree
        for lower_coefficients in range(1 << degree):
            candidate = leading | lower_coefficients
            if apply_frobenius_polynomial(field, value, candidate, base_degree) == 0:
                return candidate
    raise ArithmeticError("no Frobenius annihilator found")


def format_binary_polynomial(polynomial: int, variable: str = "t") -> str:
    """Format an integer-encoded binary polynomial deterministically."""
    if polynomial == 0:
        return "0"
    terms = []
    for degree in range(polynomial.bit_length() - 1, -1, -1):
        if not polynomial >> degree & 1:
            continue
        if degree == 0:
            terms.append("1")
        elif degree == 1:
            terms.append(variable)
        else:
            terms.append(f"{variable}^{degree}")
    return "+".join(terms)


@dataclass(frozen=True, slots=True)
class GHSProfile:
    """The exact span data determining the basic binary GHS genus."""

    absolute_degree: int
    base_degree: int
    extension_degree: int
    b: int
    sqrt_b: int
    annihilator_polynomial: int
    conjugate_rank: int
    one_in_conjugate_span: bool
    pair_rank: int
    magic_number: int
    genus: int
    orbit_size: int
    regularity_satisfied: bool


def ghs_profile(
    field: BinaryField, b: int, *, a: int = 0, base_degree: int = 1
) -> GHSProfile:
    """Compute the exact classical GHS genus invariant for a binary curve."""
    if b == 0:
        raise ValueError("the ordinary binary model requires nonzero b")
    if base_degree <= 0 or field.degree % base_degree != 0:
        raise ValueError("base degree must be a positive divisor of the field degree")
    if not 0 <= a < field.order:
        raise ValueError("a must be a field element")
    extension_degree = field.degree // base_degree
    sqrt_b = field.sqrt(b)
    orbit = frobenius_orbit(field, sqrt_b, base_degree)
    conjugate_basis = gf2_basis(orbit)
    conjugate_rank = len(conjugate_basis)
    annihilator = frobenius_annihilator(field, sqrt_b, base_degree)
    if annihilator.bit_length() - 1 != conjugate_rank:
        raise ArithmeticError("annihilator degree disagrees with conjugate rank")
    one_in_span = gf2_in_span(1, conjugate_basis)

    pair_vectors = tuple((1 << field.degree) | conjugate for conjugate in orbit)
    pair_rank = len(gf2_basis(pair_vectors))
    magic_number = conjugate_rank if one_in_span else conjugate_rank + 1
    if pair_rank != magic_number:
        raise ArithmeticError("pair rank disagrees with the span-containment formula")

    genus = (1 << (magic_number - 1)) - (1 << (magic_number - conjugate_rank)) + 1
    regularity_satisfied = (
        extension_degree % 2 == 1
        or magic_number == extension_degree
        or field.absolute_trace(a) == 0
    )
    return GHSProfile(
        absolute_degree=field.degree,
        base_degree=base_degree,
        extension_degree=extension_degree,
        b=b,
        sqrt_b=sqrt_b,
        annihilator_polynomial=annihilator,
        conjugate_rank=conjugate_rank,
        one_in_conjugate_span=one_in_span,
        pair_rank=pair_rank,
        magic_number=magic_number,
        genus=genus,
        orbit_size=distinct_orbit_size(orbit),
        regularity_satisfied=regularity_satisfied,
    )
