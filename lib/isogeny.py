"""Toy prime-field isogenies and imaginary-quadratic reduced forms.

The routines are deliberately exhaustive.  They are intended for auditable
experiments below roughly 2**16, not cryptographic-size computation.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import gcd, isqrt

from .curves import AffinePoint, Curve, curve_order, is_prime
from .finite_fields import FieldElement, PrimePolynomialField


def least_quadratic_nonresidue(prime: int) -> int:
    """Return the least positive quadratic nonresidue modulo an odd prime."""

    if prime <= 3 or not is_prime(prime):
        raise ValueError("prime must be greater than three")
    for candidate in range(2, prime):
        if pow(candidate, (prime - 1) // 2, prime) == prime - 1:
            return candidate
    raise ArithmeticError("no quadratic nonresidue was found")


def quadratic_field(prime: int) -> PrimePolynomialField:
    """Return F_(p^2) in the canonical basis u^2 = least nonresidue."""

    nonresidue = least_quadratic_nonresidue(prime)
    return PrimePolynomialField(prime, (-nonresidue, 0, 1))


def extension_element_key(value: FieldElement) -> tuple[int, ...]:
    """Return the polynomial-basis coefficient key of an extension element."""

    return value


def _field_mul_int(
    field: PrimePolynomialField, value: FieldElement, scalar: int
) -> FieldElement:
    return field.mul(field.constant(scalar), value)


@dataclass(frozen=True, slots=True)
class QuadraticExtensionCurve:
    """Short-Weierstrass curve over a canonical quadratic extension field."""

    field: PrimePolynomialField
    a: FieldElement
    b: FieldElement

    def __post_init__(self) -> None:
        if self.field.degree != 2:
            raise ValueError("curve field must be a quadratic extension")
        field = self.field
        a = field.normalize(self.a)
        b = field.normalize(self.b)
        discriminant = field.add(
            _field_mul_int(field, field.mul(field.square(a), a), 4),
            _field_mul_int(field, field.square(b), 27),
        )
        if discriminant == field.zero:
            raise ValueError("singular short-Weierstrass curve")
        object.__setattr__(self, "a", a)
        object.__setattr__(self, "b", b)

    def scale(self, scalar: FieldElement) -> QuadraticExtensionCurve:
        """Return the isomorphic equation with coefficients c^4*a,c^6*b."""

        scalar = self.field.normalize(scalar)
        if scalar == self.field.zero:
            raise ValueError("scaling factor must be nonzero")
        return QuadraticExtensionCurve(
            self.field,
            self.field.mul(self.field.pow(scalar, 4), self.a),
            self.field.mul(self.field.pow(scalar, 6), self.b),
        )

    def frobenius_twist(self) -> QuadraticExtensionCurve:
        """Apply the p-power Frobenius to the curve coefficients."""

        prime = self.field.characteristic
        return QuadraticExtensionCurve(
            self.field,
            self.field.pow(self.a, prime),
            self.field.pow(self.b, prime),
        )

    def contains(
        self, point: tuple[FieldElement, FieldElement] | None
    ) -> bool:
        """Return whether a projective identity or affine point lies on the curve."""

        if point is None:
            return True
        x, y = point
        field = self.field
        right = field.add(
            field.add(field.mul(field.square(x), x), field.mul(self.a, x)),
            self.b,
        )
        return field.square(y) == right

    def add(
        self,
        left: tuple[FieldElement, FieldElement] | None,
        right: tuple[FieldElement, FieldElement] | None,
    ) -> tuple[FieldElement, FieldElement] | None:
        """Add two points by affine short-Weierstrass formulas."""

        if left is None:
            return right
        if right is None:
            return left
        field = self.field
        x1, y1 = left
        x2, y2 = right
        if x1 == x2 and y1 == field.neg(y2):
            return None
        if left == right:
            if y1 == field.zero:
                return None
            numerator = field.add(_field_mul_int(field, field.square(x1), 3), self.a)
            denominator = _field_mul_int(field, y1, 2)
            slope = field.mul(numerator, field.inv0(denominator))
        else:
            slope = field.mul(
                field.sub(y2, y1),
                field.inv0(field.sub(x2, x1)),
            )
        x3 = field.sub(field.sub(field.square(slope), x1), x2)
        y3 = field.sub(field.mul(slope, field.sub(x1, x3)), y1)
        result = (x3, y3)
        if not self.contains(result):
            raise ArithmeticError("extension-curve addition left the curve")
        return result

    def scalar_mul(
        self,
        scalar: int,
        point: tuple[FieldElement, FieldElement] | None,
    ) -> tuple[FieldElement, FieldElement] | None:
        """Multiply a point by a nonnegative integer."""

        if scalar < 0:
            if point is None:
                return None
            return self.scalar_mul(-scalar, (point[0], self.field.neg(point[1])))
        result = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def affine_points(self) -> Iterable[tuple[FieldElement, FieldElement]]:
        """Enumerate affine points exhaustively for toy-size fields."""

        elements = tuple(self.field.elements())
        square_roots: dict[FieldElement, list[FieldElement]] = {}
        for y in elements:
            square_roots.setdefault(self.field.square(y), []).append(y)
        for x in elements:
            right = self.field.add(
                self.field.add(
                    self.field.mul(self.field.square(x), x),
                    self.field.mul(self.a, x),
                ),
                self.b,
            )
            for y in square_roots.get(right, ()):
                yield x, y


def quadratic_curve_key(curve: QuadraticExtensionCurve) -> tuple[int, ...]:
    """Canonical exhaustive key for the F_(p^2)-isomorphism class."""

    return min(
        extension_element_key(scaled.a) + extension_element_key(scaled.b)
        for scalar in curve.field.elements()
        if scalar != curve.field.zero
        for scaled in (curve.scale(scalar),)
    )


def deuring_curve_key(curve: QuadraticExtensionCurve) -> tuple[int, ...]:
    """Canonical key modulo coefficient Frobenius."""

    return min(quadratic_curve_key(curve), quadratic_curve_key(curve.frobenius_twist()))


def quadratic_curve_order(curve: QuadraticExtensionCurve) -> int:
    """Count points exhaustively, including the identity."""

    return 1 + sum(1 for _ in curve.affine_points())


def find_extension_torsion_generator(
    curve: QuadraticExtensionCurve,
    degree: int,
    group_order: int,
) -> tuple[FieldElement, FieldElement]:
    """Find a point of requested odd prime order by exhaustive projection."""

    if degree < 3 or not is_prime(degree):
        raise ValueError("degree must be an odd prime")
    if group_order % degree:
        raise ValueError("degree must divide the supplied group order")
    for candidate in curve.affine_points():
        if curve.scalar_mul(degree, candidate) is None:
            return candidate
    raise RuntimeError("no extension-field torsion generator was found")


def extension_kernel_points(
    curve: QuadraticExtensionCurve,
    generator: tuple[FieldElement, FieldElement],
    degree: int,
) -> tuple[tuple[FieldElement, FieldElement], ...]:
    """Return nonidentity points in the cyclic extension-field kernel."""

    if curve.scalar_mul(degree, generator) is not None:
        raise ValueError("generator is not annihilated by degree")
    points = tuple(curve.scalar_mul(index, generator) for index in range(1, degree))
    if any(point is None for point in points) or len(set(points)) != degree - 1:
        raise ValueError("generator does not have the requested order")
    return tuple(point for point in points if point is not None)


def extension_velu_quotient(
    curve: QuadraticExtensionCurve,
    generator: tuple[FieldElement, FieldElement],
    degree: int,
) -> QuadraticExtensionCurve:
    """Return the normalized Velu quotient over F_(p^2)."""

    points = extension_kernel_points(curve, generator, degree)
    field = curve.field
    t = field.zero
    w = field.zero
    for x, _ in points:
        t = field.add(t, field.add(_field_mul_int(field, field.square(x), 3), curve.a))
        w = field.add(
            w,
            field.add(
                field.add(
                    _field_mul_int(field, field.mul(field.square(x), x), 5),
                    _field_mul_int(field, field.mul(curve.a, x), 3),
                ),
                _field_mul_int(field, curve.b, 2),
            ),
        )
    return QuadraticExtensionCurve(
        field,
        field.sub(curve.a, _field_mul_int(field, t, 5)),
        field.sub(curve.b, _field_mul_int(field, w, 7)),
    )


def extension_velu_map(
    curve: QuadraticExtensionCurve,
    point: tuple[FieldElement, FieldElement] | None,
    generator: tuple[FieldElement, FieldElement],
    degree: int,
) -> tuple[FieldElement, FieldElement] | None:
    """Evaluate the normalized Velu map on a toy extension-field point."""

    if point is None:
        return None
    points = extension_kernel_points(curve, generator, degree)
    if point in points:
        return None
    x_image, y_image = point
    for kernel_point in points:
        translated = curve.add(point, kernel_point)
        if translated is None:
            return None
        x_image = curve.field.add(
            x_image,
            curve.field.sub(translated[0], kernel_point[0]),
        )
        y_image = curve.field.add(
            y_image,
            curve.field.sub(translated[1], kernel_point[1]),
        )
    return x_image, y_image


def reduced_positive_forms(discriminant: int) -> tuple[tuple[int, int, int], ...]:
    """Enumerate primitive reduced positive-definite forms of negative D.

    A returned triple represents ``a*x**2 + b*x*y + c*y**2``.  Boundary
    representatives use nonnegative ``b``, making the output unique.
    """
    if discriminant >= 0 or discriminant % 4 not in (0, 1):
        raise ValueError("discriminant must be negative and congruent to 0 or 1 mod 4")

    forms: list[tuple[int, int, int]] = []
    maximum_a = isqrt(abs(discriminant) // 3) + 1
    for a in range(1, maximum_a + 1):
        for b in range(-a, a + 1):
            numerator = b * b - discriminant
            denominator = 4 * a
            if numerator % denominator:
                continue
            c = numerator // denominator
            if a > c:
                continue
            if b < 0 and (abs(b) == a or a == c):
                continue
            if gcd(gcd(a, abs(b)), c) != 1:
                continue
            forms.append((a, b, c))
    return tuple(forms)


def class_number_from_reduced_forms(discriminant: int) -> int:
    """Return the class number by counting reduced primitive forms."""
    return len(reduced_positive_forms(discriminant))


def canonical_curve(curve: Curve) -> Curve:
    """Return a canonical representative of the F_p-isomorphism class.

    Prime-field twists are retained: only changes ``x = u**2*x'`` and
    ``y = u**3*y'`` with nonzero ``u`` in F_p are considered.
    """
    best = min(
        (
            curve.a * pow(u, 4, curve.p) % curve.p,
            curve.b * pow(u, 6, curve.p) % curve.p,
        )
        for u in range(1, curve.p)
    )
    return Curve(curve.p, *best)


def curve_class_key(curve: Curve) -> tuple[int, int]:
    """Return the canonical coefficient pair for an F_p-isomorphism class."""
    representative = canonical_curve(curve)
    return representative.a, representative.b


def kernel_points(curve: Curve, generator: AffinePoint, degree: int) -> tuple[tuple[int, int], ...]:
    """Return all nonidentity points in the cyclic kernel generated by P."""
    if degree < 3 or not is_prime(degree):
        raise ValueError("degree must be an odd prime")
    if generator is None or not curve.contains(generator):
        raise ValueError("generator must be an affine point on the curve")
    if curve.scalar_mul(degree, generator) is not None:
        raise ValueError("generator is not annihilated by degree")

    points = tuple(curve.scalar_mul(k, generator) for k in range(1, degree))
    if any(point is None for point in points) or len(set(points)) != degree - 1:
        raise ValueError("generator does not have the requested prime order")
    return tuple(point for point in points if point is not None)


def velu_quotient(curve: Curve, generator: AffinePoint, degree: int) -> Curve:
    """Return the short-Weierstrass Vélu quotient by ``<generator>``."""
    points = kernel_points(curve, generator, degree)
    p = curve.p
    t = sum(3 * x * x + curve.a for x, _ in points) % p
    w = sum(5 * x**3 + 3 * curve.a * x + 2 * curve.b for x, _ in points) % p
    return Curve(p, (curve.a - 5 * t) % p, (curve.b - 7 * w) % p)


def velu_map(
    curve: Curve,
    point: AffinePoint,
    generator: AffinePoint,
    degree: int,
) -> AffinePoint:
    """Evaluate Vélu's normalized quotient map by its defining sums."""
    if point is None:
        return None
    points = kernel_points(curve, generator, degree)
    if point in points:
        return None

    x_image, y_image = point
    for kernel_point in points:
        translated = curve.add(point, kernel_point)
        if translated is None:
            return None
        x_image += translated[0] - kernel_point[0]
        y_image += translated[1] - kernel_point[1]
    return x_image % curve.p, y_image % curve.p


def velu_map_affine_nonkernel(
    curve: Curve,
    point: tuple[int, int],
    generator: AffinePoint,
    degree: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Evaluate a fixed-degree Velu map on an affine nonkernel point.

    The caller must guarantee that ``point`` is not in the public kernel.
    Under that precondition every denominator below is nonzero. The loop bound
    and kernel accesses depend only on public suite parameters; the routine is
    a straight-line toy model, not a production constant-time backend.
    """
    points = kernel_points(curve, generator, degree)
    p = curve.p
    x, y = point
    x_image = x
    y_image = y
    for kernel_x, kernel_y in points:
        if trace is not None:
            trace.append("velu.sub")
        delta_x = (x - kernel_x) % p
        if trace is not None:
            trace.append("velu.sub")
        delta_y = (y - kernel_y) % p
        if trace is not None:
            trace.append("velu.inv0")
        inverse = pow(delta_x, p - 2, p)
        if trace is not None:
            trace.append("velu.mul")
        slope = delta_y * inverse % p
        if trace is not None:
            trace.append("velu.square")
        translated_x = (slope * slope - x - kernel_x) % p
        if trace is not None:
            trace.append("velu.sub")
        translated_y = (slope * (x - translated_x) - y) % p
        if trace is not None:
            trace.append("velu.add")
        x_image = (x_image + translated_x - kernel_x) % p
        if trace is not None:
            trace.append("velu.add")
        y_image = (y_image + translated_y - kernel_y) % p
    return x_image, y_image


def find_rational_torsion_generator(
    curve: Curve,
    degree: int,
    group_order: int,
) -> tuple[int, int]:
    """Find a rational point of the requested prime order exhaustively."""
    if degree < 3 or not is_prime(degree):
        raise ValueError("degree must be an odd prime")
    if group_order % degree:
        raise ValueError("degree must divide the supplied group order")
    if curve.scalar_mul(group_order, curve.first_affine_point()) is not None:
        raise ValueError("supplied group order does not annihilate the curve")

    cofactor = group_order // degree
    for candidate in curve.affine_points():
        point = curve.scalar_mul(cofactor, candidate)
        if point is not None and curve.scalar_mul(degree, point) is None:
            return point
    raise RuntimeError(f"no rational point of order {degree} was found")


def rational_isogeny_step(
    curve: Curve,
    degree: int,
    group_order: int | None = None,
    *,
    verify_order: bool = False,
) -> Curve:
    """Apply the rational Frobenius-eigenline isogeny and canonicalize."""
    order = curve_order(curve) if group_order is None else group_order
    generator = find_rational_torsion_generator(curve, degree, order)
    quotient = canonical_curve(velu_quotient(curve, generator, degree))
    if verify_order and curve_order(quotient) != order:
        raise ArithmeticError("Vélu quotient changed the rational point count")
    return quotient


def enumerate_rational_isogeny_orbit(
    start: Curve,
    degrees: Iterable[int],
    group_order: int,
    *,
    verify_orders: bool = False,
) -> tuple[tuple[Curve, ...], tuple[tuple[int, ...], ...]]:
    """Enumerate the positive-generator orbit and its transition table."""
    degree_tuple = tuple(degrees)
    if not degree_tuple:
        raise ValueError("at least one degree is required")

    first = canonical_curve(start)
    states = [first]
    indices = {curve_class_key(first): 0}
    cursor = 0
    while cursor < len(states):
        curve = states[cursor]
        for degree in degree_tuple:
            target = rational_isogeny_step(
                curve,
                degree,
                group_order,
                verify_order=verify_orders,
            )
            key = curve_class_key(target)
            if key not in indices:
                indices[key] = len(states)
                states.append(target)
        cursor += 1

    transitions: list[tuple[int, ...]] = []
    for curve in states:
        row = []
        for degree in degree_tuple:
            target = rational_isogeny_step(
                curve,
                degree,
                group_order,
                verify_order=verify_orders,
            )
            row.append(indices[curve_class_key(target)])
        transitions.append(tuple(row))
    return tuple(states), tuple(transitions)


def transition_permutations(
    transitions: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    """Transpose a state-by-generator table into generator permutations."""
    if not transitions:
        return ()
    width = len(transitions[0])
    if any(len(row) != width for row in transitions):
        raise ValueError("transition table rows have inconsistent widths")
    permutations = tuple(
        tuple(row[column] for row in transitions) for column in range(width)
    )
    expected = tuple(range(len(transitions)))
    if any(tuple(sorted(permutation)) != expected for permutation in permutations):
        raise ValueError("a generator transition is not a permutation")
    return permutations


def compose_permutations(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    """Return ``left`` after ``right``."""
    if len(left) != len(right):
        raise ValueError("permutations must have equal sizes")
    return tuple(left[right[index]] for index in range(len(left)))


def generated_permutation_group(
    generators: Iterable[tuple[int, ...]],
) -> tuple[tuple[int, ...], ...]:
    """Enumerate a small permutation group generated by the supplied maps."""
    generator_tuple = tuple(generators)
    if not generator_tuple:
        return ((),)
    size = len(generator_tuple[0])
    if any(len(generator) != size for generator in generator_tuple):
        raise ValueError("generator permutations must have equal sizes")
    identity = tuple(range(size))
    elements = [identity]
    seen = {identity}
    cursor = 0
    while cursor < len(elements):
        element = elements[cursor]
        for generator in generator_tuple:
            product = compose_permutations(generator, element)
            if product not in seen:
                seen.add(product)
                elements.append(product)
        cursor += 1
    return tuple(elements)
