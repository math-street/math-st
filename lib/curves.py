"""Small prime-field short-Weierstrass curve utilities for toy experiments."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import gcd, isqrt, lcm, log
from random import Random
from typing import Iterator, TypeAlias

AffinePoint: TypeAlias = tuple[int, int] | None


@dataclass(frozen=True, slots=True)
class Point:
    """Compatibility point type used by the shared generic-DLP helpers."""

    x: int | None
    y: int | None

    @property
    def is_infinity(self) -> bool:
        return self.x is None


INFINITY = Point(None, None)


def binary_polynomial_degree(value: int) -> int:
    """Return the degree of a polynomial over F_2 encoded as an integer."""
    return value.bit_length() - 1


def binary_polynomial_divmod(dividend: int, divisor: int) -> tuple[int, int]:
    """Return polynomial quotient and remainder over F_2."""
    if divisor <= 0:
        raise ValueError("divisor must be a nonzero binary polynomial")
    divisor_degree = binary_polynomial_degree(divisor)
    quotient = 0
    while binary_polynomial_degree(dividend) >= divisor_degree:
        shift = binary_polynomial_degree(dividend) - divisor_degree
        quotient |= 1 << shift
        dividend ^= divisor << shift
    return quotient, dividend


def binary_polynomial_mod(dividend: int, divisor: int) -> int:
    """Return the polynomial remainder over F_2."""
    return binary_polynomial_divmod(dividend, divisor)[1]


def binary_polynomial_gcd(left: int, right: int) -> int:
    """Return the monic polynomial gcd over F_2."""
    while right:
        left, right = right, binary_polynomial_mod(left, right)
    return left


def _binary_polynomial_square_mod(value: int, modulus: int) -> int:
    squared = 0
    bit = 0
    while value:
        if value & 1:
            squared |= 1 << (2 * bit)
        bit += 1
        value >>= 1
    return binary_polynomial_mod(squared, modulus)


def is_irreducible_binary_polynomial(modulus: int) -> bool:
    """Test irreducibility over F_2 with Rabin's criterion."""
    degree = binary_polynomial_degree(modulus)
    if degree <= 0 or modulus & 1 == 0:
        return False
    x = 0b10
    power = x
    for index in range(1, degree + 1):
        power = _binary_polynomial_square_mod(power, modulus)
        if index <= degree // 2 and binary_polynomial_gcd(power ^ x, modulus) != 1:
            return False
    return power == x


def find_irreducible_binary_polynomial(degree: int) -> int:
    """Find a deterministic monic irreducible polynomial of the given degree."""
    if degree < 2:
        raise ValueError("degree must be at least 2")
    leading_and_constant = (1 << degree) | 1
    for middle in range(1, 1 << (degree - 1)):
        candidate = leading_and_constant | (middle << 1)
        if is_irreducible_binary_polynomial(candidate):
            return candidate
    raise RuntimeError(f"no irreducible polynomial found at degree {degree}")


@dataclass(frozen=True, slots=True)
class BinaryField:
    """Polynomial-basis arithmetic in F_(2^degree), with elements as integers."""

    degree: int
    modulus: int

    def __post_init__(self) -> None:
        if self.degree < 2:
            raise ValueError("degree must be at least 2")
        if binary_polynomial_degree(self.modulus) != self.degree:
            raise ValueError("modulus must be monic of the requested degree")
        if not is_irreducible_binary_polynomial(self.modulus):
            raise ValueError("modulus must be irreducible over F_2")

    @property
    def order(self) -> int:
        return 1 << self.degree

    @property
    def element_mask(self) -> int:
        return self.order - 1

    def _check_element(self, value: int) -> None:
        if not 0 <= value < self.order:
            raise ValueError(f"element must be in [0, {self.order})")

    def add(self, left: int, right: int) -> int:
        self._check_element(left)
        self._check_element(right)
        return left ^ right

    def mul(self, left: int, right: int) -> int:
        self._check_element(left)
        self._check_element(right)
        product = 0
        while right:
            if right & 1:
                product ^= left
            right >>= 1
            left <<= 1
            if left & self.order:
                left ^= self.modulus
        return product

    def cmov(self, false_value: int, true_value: int, selector: int) -> int:
        """Select an encoded element with an arithmetic mask."""
        self._check_element(false_value)
        self._check_element(true_value)
        selector = int(bool(selector))
        mask = -selector & self.element_mask
        return false_value ^ (mask & (false_value ^ true_value))

    def mul_fixed(self, left: int, right: int) -> int:
        """Multiply with exactly ``degree`` shift-and-reduce iterations."""
        self._check_element(left)
        self._check_element(right)
        product = 0
        reduction = self.modulus & self.element_mask
        for _ in range(self.degree):
            bit_mask = -(right & 1) & self.element_mask
            product ^= left & bit_mask
            right >>= 1
            overflow = (left >> (self.degree - 1)) & 1
            left = (left << 1) & self.element_mask
            left ^= reduction & (-overflow & self.element_mask)
        return product

    def square_fixed(self, value: int) -> int:
        return self.mul_fixed(value, value)

    def pow_fixed(self, value: int, exponent: int) -> int:
        """Exponentiate on a public exponent with a fixed per-field schedule."""
        self._check_element(value)
        if exponent < 0:
            raise ValueError("negative exponents are unsupported by pow_fixed")
        result = 1
        for bit in bin(exponent)[2:]:
            result = self.square_fixed(result)
            if bit == "1":  # the exponent is public
                result = self.mul_fixed(result, value)
        return result

    def inv0_fixed(self, value: int) -> int:
        """Return the inverse with the total convention inv0(0) = 0."""
        return self.pow_fixed(value, self.order - 2)

    def absolute_trace_fixed(self, value: int) -> int:
        self._check_element(value)
        result = 0
        conjugate = value
        for _ in range(self.degree):
            result ^= conjugate
            conjugate = self.square_fixed(conjugate)
        return result

    def half_trace_fixed(self, value: int) -> int:
        """Solve z^2 + z = value when degree is odd and trace(value) = 0."""
        self._check_element(value)
        if self.degree % 2 == 0:
            raise ValueError("half trace requires odd extension degree")
        result = 0
        conjugate = value
        for _ in range((self.degree + 1) // 2):
            result ^= conjugate
            conjugate = self.square_fixed(self.square_fixed(conjugate))
        return result

    def square(self, value: int) -> int:
        return self.mul(value, value)

    def pow(self, value: int, exponent: int) -> int:
        self._check_element(value)
        if exponent < 0:
            return self.pow(self.inverse(value), -exponent)
        result = 1
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.square(base)
            exponent >>= 1
        return result

    def inverse(self, value: int) -> int:
        self._check_element(value)
        if value == 0:
            raise ZeroDivisionError("zero has no multiplicative inverse")
        return self.pow(value, self.order - 2)

    def div(self, numerator: int, denominator: int) -> int:
        return self.mul(numerator, self.inverse(denominator))

    def frobenius(self, value: int, power: int = 1) -> int:
        """Apply x -> x^(2^power), reducing power modulo the field degree."""
        self._check_element(value)
        if power < 0:
            raise ValueError("Frobenius power must be nonnegative")
        for _ in range(power % self.degree):
            value = self.square(value)
        return value

    def sqrt(self, value: int) -> int:
        """Return the unique square root in this characteristic-two field."""
        self._check_element(value)
        return self.frobenius(value, self.degree - 1)

    def absolute_trace(self, value: int) -> int:
        """Return Tr_(F_(2^degree)/F_2)(value) as 0 or 1."""
        self._check_element(value)
        result = 0
        conjugate = value
        for _ in range(self.degree):
            result ^= conjugate
            conjugate = self.square(conjugate)
        if result not in (0, 1):
            raise ArithmeticError("absolute trace did not land in F_2")
        return result


def is_prime(n: int) -> bool:
    """Return primality for n < 2**64 using deterministic Miller--Rabin."""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if n % prime == 0:
            return n == prime

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % n == 0:
            continue
        x = pow(base, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_below_power_of_two(bits: int, residue_mod_4: int = 3) -> int:
    """Find the largest prime below 2**bits with the requested residue mod 4."""
    if bits < 4:
        raise ValueError("bits must be at least 4")
    candidate = (1 << bits) - 1
    candidate -= (candidate - residue_mod_4) % 4
    while not is_prime(candidate):
        candidate -= 4
    return candidate


def sqrt_mod(n: int, p: int) -> int | None:
    """Return one square root of n modulo an odd prime p, or None."""
    n %= p
    if n == 0:
        return 0
    if pow(n, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    while t != 1:
        i = 1
        t2i = t * t % p
        while t2i != 1:
            t2i = t2i * t2i % p
            i += 1
            if i == m:
                raise ArithmeticError("Tonelli--Shanks invariant failed")
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def inv0_mod(value: int, p: int) -> int:
    """Return value**(-1) in F_p, extended by inv0(0) = 0."""
    return pow(value % p, p - 2, p)


def is_square_mod(value: int, p: int) -> bool:
    """Return whether value is zero or a quadratic residue in F_p."""
    return pow(value % p, (p - 1) // 2, p) != p - 1


def sgn0_prime(value: int, p: int) -> int:
    """Return the RFC 9380 sgn0 value for an element of a prime field."""
    return (value % p) & 1


def cmov_mod(left: int, right: int, condition: bool, p: int) -> int:
    """Select right when condition is true using arithmetic selection.

    This models a field-level conditional move. Python integers and the
    conversion of a bool to int are not a production constant-time backend.
    """
    selector = int(condition)
    return ((1 - selector) * (left % p) + selector * (right % p)) % p


def _record_schedule(trace: list[str] | None, operation: str) -> None:
    """Append an operation label when schedule instrumentation is enabled."""
    if trace is not None:
        trace.append(operation)


def _two_adicity(value: int) -> int:
    """Return the largest c such that 2**c divides a positive integer."""
    if value <= 0:
        raise ValueError("value must be positive")
    result = 0
    while value & 1 == 0:
        result += 1
        value >>= 1
    return result


@lru_cache(maxsize=None)
def first_nonsquare(p: int) -> int:
    """Return the least positive quadratic non-residue in F_p."""
    if p <= 2 or not is_prime(p):
        raise ValueError("p must be an odd prime")
    for candidate in range(2, p):
        if not is_square_mod(candidate, p):
            return candidate
    raise ArithmeticError("odd prime field has no quadratic non-residue")


def sqrt_mod_ct(
    value: int,
    p: int,
    *,
    trace: list[str] | None = None,
) -> int:
    """Return a square root using the fixed-loop RFC 9380 Tonelli--Shanks map.

    The loop bounds depend only on the public field modulus. Callers must
    ensure that value is square. The trace records the high-level schedule;
    it is not a claim that Python big-integer arithmetic is constant-time.
    """
    value %= p
    c1 = _two_adicity(p - 1)
    c2 = (p - 1) >> c1
    c3 = (c2 - 1) // 2
    c4 = first_nonsquare(p)
    c5 = pow(c4, c2, p)

    _record_schedule(trace, "sqrt.pow")
    z = pow(value, c3, p)
    _record_schedule(trace, "sqrt.mul")
    t = z * z % p
    _record_schedule(trace, "sqrt.mul")
    t = t * value % p
    _record_schedule(trace, "sqrt.mul")
    z = z * value % p
    b = t
    c = c5
    for index in range(c1, 1, -1):
        for _ in range(1, index - 1):
            _record_schedule(trace, "sqrt.square")
            b = b * b % p
        _record_schedule(trace, "sqrt.equal")
        use_current = b == 1
        _record_schedule(trace, "sqrt.mul")
        z_times_c = z * c % p
        _record_schedule(trace, "sqrt.cmov")
        z = cmov_mod(z_times_c, z, use_current, p)
        _record_schedule(trace, "sqrt.square")
        c = c * c % p
        _record_schedule(trace, "sqrt.mul")
        t_times_c = t * c % p
        _record_schedule(trace, "sqrt.cmov")
        t = cmov_mod(t_times_c, t, use_current, p)
        b = t
    return z


def sqrt_ratio_mod(
    numerator: int,
    denominator: int,
    p: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> tuple[bool, int]:
    """Implement RFC 9380 F.2.1.1 sqrt_ratio for an odd prime field.

    The RFC interface requires a nonzero denominator; this straight-line path
    deliberately does not branch to recheck that per-input precondition.
    """
    numerator %= p
    denominator %= p
    z %= p
    if is_square_mod(z, p):
        raise ValueError("z must be a quadratic non-residue")

    c1 = _two_adicity(p - 1)
    c2 = (p - 1) >> c1
    c3 = (c2 - 1) // 2
    c4 = (1 << c1) - 1
    c5 = 1 << (c1 - 1)
    c6 = pow(z, c2, p)
    c7 = pow(z, (c2 + 1) // 2, p)

    tv1 = c6
    _record_schedule(trace, "sqrt_ratio.pow")
    tv2 = pow(denominator, c4, p)
    _record_schedule(trace, "sqrt_ratio.square")
    tv3 = tv2 * tv2 % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv3 = tv3 * denominator % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv5 = numerator * tv3 % p
    _record_schedule(trace, "sqrt_ratio.pow")
    tv5 = pow(tv5, c3, p)
    _record_schedule(trace, "sqrt_ratio.mul")
    tv5 = tv5 * tv2 % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv2 = tv5 * denominator % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv3 = tv5 * numerator % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv4 = tv3 * tv2 % p
    _record_schedule(trace, "sqrt_ratio.pow")
    tv5 = pow(tv4, c5, p)
    _record_schedule(trace, "sqrt_ratio.equal")
    is_qr = (tv5 == 1) | (numerator == 0)
    _record_schedule(trace, "sqrt_ratio.mul")
    tv2 = tv3 * c7 % p
    _record_schedule(trace, "sqrt_ratio.mul")
    tv5 = tv4 * tv1 % p
    _record_schedule(trace, "sqrt_ratio.cmov")
    tv3 = cmov_mod(tv2, tv3, is_qr, p)
    _record_schedule(trace, "sqrt_ratio.cmov")
    tv4 = cmov_mod(tv5, tv4, is_qr, p)
    for index in range(c1, 1, -1):
        _record_schedule(trace, "sqrt_ratio.pow")
        tv5 = pow(tv4, 1 << (index - 2), p)
        _record_schedule(trace, "sqrt_ratio.equal")
        use_current = tv5 == 1
        _record_schedule(trace, "sqrt_ratio.mul")
        tv2 = tv3 * tv1 % p
        _record_schedule(trace, "sqrt_ratio.square")
        tv1 = tv1 * tv1 % p
        _record_schedule(trace, "sqrt_ratio.mul")
        tv5 = tv4 * tv1 % p
        _record_schedule(trace, "sqrt_ratio.cmov")
        tv3 = cmov_mod(tv2, tv3, use_current, p)
        _record_schedule(trace, "sqrt_ratio.cmov")
        tv4 = cmov_mod(tv5, tv4, use_current, p)
    return is_qr, tv3


def simple_swu_parameters_are_valid(curve: "Curve", z: int) -> bool:
    """Check the RFC 9380 SSWU parameter predicates by toy-field enumeration.

    The irreducibility test enumerates the base field and is intended only for
    setup and toy validation, never for the per-input mapping path.
    """
    p = curve.p
    z %= p
    if curve.a % p == 0 or curve.b % p == 0:
        return False
    if is_square_mod(z, p) or z == p - 1:
        return False
    if any(
        (x * x * x + curve.a * x + curve.b - z) % p == 0
        for x in range(p)
    ):
        return False
    exceptional_x = curve.b * inv0_mod(z * curve.a, p) % p
    gx = (
        exceptional_x * exceptional_x * exceptional_x
        + curve.a * exceptional_x
        + curve.b
    ) % p
    return is_square_mod(gx, p)


def map_to_curve_simple_swu(
    curve: "Curve",
    u: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Map u to a short-Weierstrass point using RFC 9380 Appendix F.2."""
    p = curve.p
    a = curve.a % p
    b = curve.b % p
    u %= p
    z %= p
    if a == 0 or b == 0:
        raise ValueError("direct simplified SWU requires nonzero a and b")
    if is_square_mod(z, p):
        raise ValueError("simplified SWU requires a nonsquare z")

    _record_schedule(trace, "sswu.square")
    tv1 = u * u % p
    _record_schedule(trace, "sswu.mul")
    tv1 = z * tv1 % p
    _record_schedule(trace, "sswu.square")
    tv2 = tv1 * tv1 % p
    _record_schedule(trace, "sswu.add")
    tv2 = (tv2 + tv1) % p
    _record_schedule(trace, "sswu.add")
    tv3 = (tv2 + 1) % p
    _record_schedule(trace, "sswu.mul")
    tv3 = b * tv3 % p
    _record_schedule(trace, "sswu.equal")
    nonzero = tv2 != 0
    _record_schedule(trace, "sswu.cmov")
    tv4 = cmov_mod(z, -tv2, nonzero, p)
    _record_schedule(trace, "sswu.mul")
    tv4 = a * tv4 % p
    _record_schedule(trace, "sswu.square")
    tv2 = tv3 * tv3 % p
    _record_schedule(trace, "sswu.square")
    tv6 = tv4 * tv4 % p
    _record_schedule(trace, "sswu.mul")
    tv5 = a * tv6 % p
    _record_schedule(trace, "sswu.add")
    tv2 = (tv2 + tv5) % p
    _record_schedule(trace, "sswu.mul")
    tv2 = tv2 * tv3 % p
    _record_schedule(trace, "sswu.mul")
    tv6 = tv6 * tv4 % p
    _record_schedule(trace, "sswu.mul")
    tv5 = b * tv6 % p
    _record_schedule(trace, "sswu.add")
    tv2 = (tv2 + tv5) % p
    _record_schedule(trace, "sswu.mul")
    x = tv1 * tv3 % p
    is_gx1_square, y1 = sqrt_ratio_mod(tv2, tv6, p, z, trace=trace)
    _record_schedule(trace, "sswu.mul")
    y = tv1 * u % p
    _record_schedule(trace, "sswu.mul")
    y = y * y1 % p
    _record_schedule(trace, "sswu.cmov")
    x = cmov_mod(x, tv3, is_gx1_square, p)
    _record_schedule(trace, "sswu.cmov")
    y = cmov_mod(y, y1, is_gx1_square, p)
    _record_schedule(trace, "sswu.equal")
    signs_match = sgn0_prime(u, p) == sgn0_prime(y, p)
    _record_schedule(trace, "sswu.cmov")
    y = cmov_mod(-y, y, signs_match, p)
    _record_schedule(trace, "sswu.inv0")
    x = x * inv0_mod(tv4, p) % p
    return x, y


def svdw_parameters_are_valid(curve: "Curve", z: int) -> bool:
    """Check the RFC 9380 Shallue--van de Woestijne Z predicates.

    This is a public-parameter setup check for short-Weierstrass curves over
    prime fields of characteristic greater than three. It is not part of the
    per-input straight-line mapping path.
    """
    p = curve.p
    z %= p
    gz = (z * z * z + curve.a * z + curve.b) % p
    numerator = (3 * z * z + 4 * curve.a) % p
    if z == 0 or gz == 0 or numerator == 0:
        return False
    h = -numerator * inv0_mod(4 * gz, p) % p
    if h == 0 or not is_square_mod(h, p):
        return False
    minus_half_z = -z * inv0_mod(2, p) % p
    g_minus_half_z = (
        minus_half_z * minus_half_z * minus_half_z
        + curve.a * minus_half_z
        + curve.b
    ) % p
    return is_square_mod(gz, p) or is_square_mod(g_minus_half_z, p)


def find_svdw_z(curve: "Curve") -> int:
    """Return the first valid SvdW Z in the RFC's 1, -1, 2, -2 order."""
    seen: set[int] = set()
    for magnitude in range(1, curve.p):
        for candidate in (magnitude, -magnitude):
            z = candidate % curve.p
            if z not in seen:
                seen.add(z)
                if svdw_parameters_are_valid(curve, z):
                    return z
    raise ValueError("curve has no SvdW Z over the base field")


def map_to_curve_svdw(
    curve: "Curve",
    u: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Map u with the straight-line RFC 9380 Appendix F.1 SvdW map."""
    p = curve.p
    a = curve.a % p
    b = curve.b % p
    u %= p
    z %= p
    if not svdw_parameters_are_valid(curve, z):
        raise ValueError("z does not satisfy the SvdW parameter predicates")

    c1 = (z * z * z + a * z + b) % p
    c2 = -z * inv0_mod(2, p) % p
    numerator = (3 * z * z + 4 * a) % p
    c3 = sqrt_mod_ct(-c1 * numerator, p, trace=trace)
    _record_schedule(trace, "svdw.equal")
    c3_is_negative = sgn0_prime(c3, p) == 1
    _record_schedule(trace, "svdw.cmov")
    c3 = cmov_mod(c3, -c3, c3_is_negative, p)
    c4 = -4 * c1 * inv0_mod(numerator, p) % p

    _record_schedule(trace, "svdw.square")
    tv1 = u * u % p
    _record_schedule(trace, "svdw.mul")
    tv1 = tv1 * c1 % p
    _record_schedule(trace, "svdw.add")
    tv2 = (1 + tv1) % p
    _record_schedule(trace, "svdw.sub")
    tv1 = (1 - tv1) % p
    _record_schedule(trace, "svdw.mul")
    tv3 = tv1 * tv2 % p
    _record_schedule(trace, "svdw.inv0")
    tv3 = inv0_mod(tv3, p)
    _record_schedule(trace, "svdw.mul")
    tv4 = u * tv1 % p
    _record_schedule(trace, "svdw.mul")
    tv4 = tv4 * tv3 % p
    _record_schedule(trace, "svdw.mul")
    tv4 = tv4 * c3 % p
    _record_schedule(trace, "svdw.sub")
    x1 = (c2 - tv4) % p
    _record_schedule(trace, "svdw.square")
    gx1 = x1 * x1 % p
    _record_schedule(trace, "svdw.add")
    gx1 = (gx1 + a) % p
    _record_schedule(trace, "svdw.mul")
    gx1 = gx1 * x1 % p
    _record_schedule(trace, "svdw.add")
    gx1 = (gx1 + b) % p
    _record_schedule(trace, "svdw.is_square")
    e1 = is_square_mod(gx1, p)
    _record_schedule(trace, "svdw.add")
    x2 = (c2 + tv4) % p
    _record_schedule(trace, "svdw.square")
    gx2 = x2 * x2 % p
    _record_schedule(trace, "svdw.add")
    gx2 = (gx2 + a) % p
    _record_schedule(trace, "svdw.mul")
    gx2 = gx2 * x2 % p
    _record_schedule(trace, "svdw.add")
    gx2 = (gx2 + b) % p
    _record_schedule(trace, "svdw.is_square")
    e2 = is_square_mod(gx2, p) & (not e1)
    _record_schedule(trace, "svdw.square")
    x3 = tv2 * tv2 % p
    _record_schedule(trace, "svdw.mul")
    x3 = x3 * tv3 % p
    _record_schedule(trace, "svdw.square")
    x3 = x3 * x3 % p
    _record_schedule(trace, "svdw.mul")
    x3 = x3 * c4 % p
    _record_schedule(trace, "svdw.add")
    x3 = (x3 + z) % p
    _record_schedule(trace, "svdw.cmov")
    x = cmov_mod(x3, x1, e1, p)
    _record_schedule(trace, "svdw.cmov")
    x = cmov_mod(x, x2, e2, p)
    _record_schedule(trace, "svdw.square")
    gx = x * x % p
    _record_schedule(trace, "svdw.add")
    gx = (gx + a) % p
    _record_schedule(trace, "svdw.mul")
    gx = gx * x % p
    _record_schedule(trace, "svdw.add")
    gx = (gx + b) % p
    y = sqrt_mod_ct(gx, p, trace=trace)
    _record_schedule(trace, "svdw.equal")
    signs_match = sgn0_prime(u, p) == sgn0_prime(y, p)
    _record_schedule(trace, "svdw.cmov")
    y = cmov_mod(-y, y, signs_match, p)
    return x, y


MontgomeryPoint: TypeAlias = tuple[int, int] | None


@dataclass(frozen=True, slots=True)
class MontgomeryCurve:
    """The curve K*t^2 = s^3 + J*s^2 + s over an odd prime field."""

    p: int
    j: int
    k: int

    def __post_init__(self) -> None:
        if self.p <= 3 or not is_prime(self.p):
            raise ValueError("p must be an odd prime greater than 3")
        if self.j % self.p == 0 or self.k % self.p == 0:
            raise ValueError("Montgomery parameters j and k must be nonzero")
        if (self.j * self.j - 4) % self.p == 0:
            raise ValueError("singular Montgomery curve")

    def contains(self, point: MontgomeryPoint) -> bool:
        if point is None:
            return True
        s, t = point
        return (
            self.k * t * t - (s * s * s + self.j * s * s + s)
        ) % self.p == 0

    def supports_elligator2(self) -> bool:
        discriminant = (
            (self.j * self.j - 4) * inv0_mod(self.k * self.k, self.p)
        ) % self.p
        return discriminant != 0 and not is_square_mod(discriminant, self.p)


def map_to_curve_elligator2(
    curve: MontgomeryCurve,
    u: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Map u to a Montgomery point using RFC 9380 Appendix F.3."""
    p = curve.p
    u %= p
    z %= p
    if not curve.supports_elligator2():
        raise ValueError("curve does not satisfy the Elligator 2 predicates")
    if is_square_mod(z, p):
        raise ValueError("Elligator 2 requires a nonsquare z")

    c1 = curve.j * inv0_mod(curve.k, p) % p
    c2 = inv0_mod(curve.k * curve.k, p)
    _record_schedule(trace, "ell2.square")
    tv1 = u * u % p
    _record_schedule(trace, "ell2.mul")
    tv1 = z * tv1 % p
    _record_schedule(trace, "ell2.equal")
    exceptional = tv1 == p - 1
    _record_schedule(trace, "ell2.cmov")
    tv1 = cmov_mod(tv1, 0, exceptional, p)
    _record_schedule(trace, "ell2.add")
    x1 = (tv1 + 1) % p
    _record_schedule(trace, "ell2.inv0")
    x1 = inv0_mod(x1, p)
    _record_schedule(trace, "ell2.mul")
    x1 = -c1 * x1 % p
    _record_schedule(trace, "ell2.add")
    gx1 = (x1 + c1) % p
    _record_schedule(trace, "ell2.mul")
    gx1 = gx1 * x1 % p
    _record_schedule(trace, "ell2.add")
    gx1 = (gx1 + c2) % p
    _record_schedule(trace, "ell2.mul")
    gx1 = gx1 * x1 % p
    _record_schedule(trace, "ell2.add")
    x2 = (-x1 - c1) % p
    _record_schedule(trace, "ell2.mul")
    gx2 = tv1 * gx1 % p
    _record_schedule(trace, "ell2.is_square")
    gx1_is_square = is_square_mod(gx1, p)
    _record_schedule(trace, "ell2.cmov")
    x = cmov_mod(x2, x1, gx1_is_square, p)
    _record_schedule(trace, "ell2.cmov")
    y2 = cmov_mod(gx2, gx1, gx1_is_square, p)
    y = sqrt_mod_ct(y2, p, trace=trace)
    _record_schedule(trace, "ell2.equal")
    y_is_negative = sgn0_prime(y, p) == 1
    _record_schedule(trace, "ell2.cmov")
    y = cmov_mod(y, -y, gx1_is_square ^ y_is_negative, p)
    _record_schedule(trace, "ell2.mul")
    s = x * curve.k % p
    _record_schedule(trace, "ell2.mul")
    t = y * curve.k % p
    return s, t


TwistedEdwardsPoint: TypeAlias = tuple[int, int]


@dataclass(frozen=True, slots=True)
class TwistedEdwardsCurve:
    """The affine curve a*v^2 + w^2 = 1 + d*v^2*w^2 over F_p."""

    p: int
    a: int
    d: int

    def __post_init__(self) -> None:
        if self.p <= 3 or not is_prime(self.p):
            raise ValueError("p must be an odd prime greater than 3")
        if self.a % self.p == 0 or self.d % self.p == 0:
            raise ValueError("twisted Edwards parameters must be nonzero")
        if (self.a - self.d) % self.p == 0:
            raise ValueError("singular twisted Edwards curve")

    @property
    def identity(self) -> TwistedEdwardsPoint:
        return 0, 1

    def contains(self, point: TwistedEdwardsPoint) -> bool:
        v, w = point
        return (
            self.a * v * v
            + w * w
            - 1
            - self.d * v * v * w * w
        ) % self.p == 0

    def neg(self, point: TwistedEdwardsPoint) -> TwistedEdwardsPoint:
        return (-point[0]) % self.p, point[1] % self.p

    def add(
        self,
        left: TwistedEdwardsPoint,
        right: TwistedEdwardsPoint,
    ) -> TwistedEdwardsPoint:
        """Apply the affine twisted-Edwards addition law using inv0."""
        v1, w1 = left
        v2, w2 = right
        p = self.p
        product = self.d * v1 * v2 * w1 * w2 % p
        v3 = (v1 * w2 + w1 * v2) * inv0_mod(1 + product, p) % p
        w3 = (w1 * w2 - self.a * v1 * v2) * inv0_mod(1 - product, p) % p
        return v3, w3

    def scalar_mul(
        self,
        scalar: int,
        point: TwistedEdwardsPoint,
    ) -> TwistedEdwardsPoint:
        if scalar < 0:
            return self.scalar_mul(-scalar, self.neg(point))
        result = self.identity
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def points(self) -> Iterator[TwistedEdwardsPoint]:
        for v in range(self.p):
            for w in range(self.p):
                if self.contains((v, w)):
                    yield v, w


def twisted_edwards_from_montgomery(curve: MontgomeryCurve) -> TwistedEdwardsCurve:
    """Return the RFC 9380 Appendix D.1 twisted-Edwards equivalent."""
    inverse_k = inv0_mod(curve.k, curve.p)
    a = (curve.j + 2) * inverse_k % curve.p
    d = (curve.j - 2) * inverse_k % curve.p
    return TwistedEdwardsCurve(curve.p, a, d)


def montgomery_to_twisted_edwards(
    curve: MontgomeryCurve,
    point: tuple[int, int],
    *,
    trace: list[str] | None = None,
) -> TwistedEdwardsPoint:
    """Apply the straight-line exceptional-safe RFC Appendix D.1 map."""
    p = curve.p
    s, t = point
    _record_schedule(trace, "monty_edw.add")
    tv1 = (s + 1) % p
    _record_schedule(trace, "monty_edw.mul")
    tv2 = tv1 * t % p
    _record_schedule(trace, "monty_edw.inv0")
    tv2 = inv0_mod(tv2, p)
    _record_schedule(trace, "monty_edw.mul")
    v = tv2 * tv1 % p
    _record_schedule(trace, "monty_edw.mul")
    v = v * s % p
    _record_schedule(trace, "monty_edw.mul")
    w = tv2 * t % p
    _record_schedule(trace, "monty_edw.sub")
    tv1 = (s - 1) % p
    _record_schedule(trace, "monty_edw.mul")
    w = w * tv1 % p
    _record_schedule(trace, "monty_edw.equal")
    exceptional = tv2 == 0
    _record_schedule(trace, "monty_edw.cmov")
    w = cmov_mod(w, 1, exceptional, p)
    return v, w


def montgomery_weierstrass_curve(curve: MontgomeryCurve) -> "Curve":
    """Return the RFC 9380 Appendix D.2 short-Weierstrass equivalent."""
    p = curve.p
    inverse_3k2 = inv0_mod(3 * curve.k * curve.k, p)
    inverse_27k3 = inv0_mod(27 * pow(curve.k, 3, p), p)
    a = (3 - curve.j * curve.j) * inverse_3k2 % p
    b = (2 * pow(curve.j, 3, p) - 9 * curve.j) * inverse_27k3 % p
    return Curve(p, a, b)


def weierstrass_to_montgomery(
    curve: MontgomeryCurve,
    point: tuple[int, int],
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Apply the inverse affine coordinate map in RFC Appendix D.2."""
    x, y = point
    p = curve.p
    _record_schedule(trace, "weier_monty.mul")
    s = 3 * curve.k * x % p
    _record_schedule(trace, "weier_monty.sub")
    s = (s - curve.j) % p
    _record_schedule(trace, "weier_monty.mul")
    s = s * inv0_mod(3, p) % p
    _record_schedule(trace, "weier_monty.mul")
    t = y * curve.k % p
    return s, t


def montgomery_to_weierstrass(
    curve: MontgomeryCurve,
    point: tuple[int, int],
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Apply the affine coordinate map in RFC 9380 Appendix D.2."""
    s, t = point
    p = curve.p
    _record_schedule(trace, "monty_weier.mul")
    x = 3 * s % p
    _record_schedule(trace, "monty_weier.add")
    x = (x + curve.j) % p
    _record_schedule(trace, "monty_weier.mul")
    x = x * inv0_mod(3 * curve.k, p) % p
    _record_schedule(trace, "monty_weier.mul")
    y = t * inv0_mod(curve.k, p) % p
    return x, y


def map_to_curve_svdw_montgomery(
    curve: MontgomeryCurve,
    u: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Map through the equivalent Weierstrass model and RFC Appendix D.2."""
    weierstrass = montgomery_weierstrass_curve(curve)
    point = map_to_curve_svdw(weierstrass, u, z, trace=trace)
    return weierstrass_to_montgomery(curve, point, trace=trace)


def map_to_curve_elligator2_edwards(
    curve: MontgomeryCurve,
    u: int,
    z: int,
    *,
    trace: list[str] | None = None,
) -> TwistedEdwardsPoint:
    """Map with Elligator 2 and the RFC Appendix D.1 rational map."""
    point = map_to_curve_elligator2(curve, u, z, trace=trace)
    return montgomery_to_twisted_edwards(curve, point, trace=trace)


@dataclass(frozen=True, slots=True)
class Curve:
    """The curve y^2 = x^3 + a*x + b over F_p; None is the identity."""

    p: int
    a: int
    b: int

    def __post_init__(self) -> None:
        if self.p <= 3 or not is_prime(self.p):
            raise ValueError("p must be an odd prime greater than 3")
        if (4 * self.a**3 + 27 * self.b**2) % self.p == 0:
            raise ValueError("singular curve")

    def contains(self, point: AffinePoint) -> bool:
        if point is None:
            return True
        x, y = point
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def neg(self, point: AffinePoint) -> AffinePoint:
        if point is None:
            return None
        return point[0], (-point[1]) % self.p

    def add(self, left: AffinePoint, right: AffinePoint) -> AffinePoint:
        if left is None:
            return right
        if right is None:
            return left
        x1, y1 = left
        x2, y2 = right
        if x1 == x2:
            if (y1 + y2) % self.p == 0:
                return None
            slope = (3 * x1 * x1 + self.a) * pow(2 * y1, self.p - 2, self.p)
        else:
            slope = (y2 - y1) * pow((x2 - x1) % self.p, self.p - 2, self.p)
        slope %= self.p
        x3 = (slope * slope - x1 - x2) % self.p
        y3 = (slope * (x1 - x3) - y1) % self.p
        return x3, y3

    def scalar_mul(self, scalar: int, point: AffinePoint) -> AffinePoint:
        if scalar < 0:
            return self.scalar_mul(-scalar, self.neg(point))
        result: AffinePoint = None
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            scalar >>= 1
        return result

    def points_for_x(self, x: int) -> tuple[AffinePoint, ...]:
        x %= self.p
        rhs = (x * x * x + self.a * x + self.b) % self.p
        y = sqrt_mod(rhs, self.p)
        if y is None:
            return ()
        if y == 0:
            return ((x, 0),)
        return ((x, y), (x, (-y) % self.p))

    def affine_points(self, x_stop: int | None = None) -> Iterator[tuple[int, int]]:
        stop = self.p if x_stop is None else min(self.p, x_stop)
        for x in range(stop):
            yield from self.points_for_x(x)  # type: ignore[misc]

    def first_affine_point(self) -> tuple[int, int]:
        return next(self.affine_points())


def square_root_multiplicities(p: int) -> bytearray:
    """Return a table whose entry z is the number of y with y^2 = z mod p."""
    roots = bytearray(p)
    for y in range(p):
        roots[y * y % p] += 1
    return roots


def curve_order(curve: Curve, root_counts: bytearray | None = None) -> int:
    """Count E(F_p) exactly by enumerating x-coordinates."""
    roots = root_counts if root_counts is not None else square_root_multiplicities(curve.p)
    total = 1
    for x in range(curve.p):
        rhs = (x * x * x + curve.a * x + curve.b) % curve.p
        total += roots[rhs]
    return total


def _bounded_dlog(
    curve: Curve,
    generator: AffinePoint,
    target: AffinePoint,
    maximum: int,
) -> int:
    """Find k in [0, maximum] with target = [k]generator using BSGS."""
    if generator is None:
        raise ValueError("generator must be affine")
    if maximum < 0:
        raise ValueError("maximum must be nonnegative")

    width = isqrt(maximum) + 1
    baby_steps: dict[AffinePoint, int] = {}
    current: AffinePoint = None
    for index in range(width):
        baby_steps.setdefault(current, index)
        current = curve.add(current, generator)

    giant_step = curve.scalar_mul(-width, generator)
    current = target
    giant_count = maximum // width + 2
    for giant_index in range(giant_count):
        baby_index = baby_steps.get(current)
        if baby_index is not None:
            answer = giant_index * width + baby_index
            if answer <= maximum and curve.scalar_mul(answer, generator) == target:
                return answer
        current = curve.add(current, giant_step)
    raise ArithmeticError("bounded discrete logarithm not found")


def _point_order_from_multiple(
    curve: Curve,
    point: AffinePoint,
    multiple: int,
) -> int:
    """Recover the exact point order from a known positive multiple."""
    if point is None:
        return 1
    if multiple <= 0 or curve.scalar_mul(multiple, point) is not None:
        raise ValueError("multiple does not annihilate the point")

    from sympy import factorint

    order = multiple
    for prime_value in factorint(multiple):
        prime = int(prime_value)
        while order % prime == 0 and curve.scalar_mul(order // prime, point) is None:
            order //= prime
    return order


def _random_affine_point(curve: Curve, rng: Random) -> tuple[int, int]:
    """Sample an affine point by rejection on uniformly sampled x-coordinates."""
    for _ in range(max(64, 4 * curve.p.bit_length())):
        x = rng.randrange(curve.p)
        points = curve.points_for_x(x)
        if points:
            point = points[rng.randrange(len(points))]
            assert point is not None
            return point
    raise RuntimeError("failed to sample an affine point")


def quadratic_twist(curve: Curve) -> Curve:
    """Return a quadratic twist of a short-Weierstrass curve."""
    nonsquare = 2
    while pow(nonsquare, (curve.p - 1) // 2, curve.p) != curve.p - 1:
        nonsquare += 1
    return Curve(
        curve.p,
        curve.a * nonsquare**2 % curve.p,
        curve.b * nonsquare**3 % curve.p,
    )


def _point_order_from_hasse_interval(curve: Curve, point: AffinePoint) -> int:
    """Compute a point order using the Hasse interval and bounded BSGS."""
    radius = isqrt(4 * curve.p)
    center_multiple = curve.scalar_mul(curve.p + 1, point)
    shifted_target = curve.add(center_multiple, curve.scalar_mul(radius, point))
    shifted_trace = _bounded_dlog(curve, point, shifted_target, 2 * radius)
    trace = shifted_trace - radius
    annihilating_multiple = curve.p + 1 - trace
    return _point_order_from_multiple(curve, point, annihilating_multiple)


def _crt_pair(
    left_residue: int,
    left_modulus: int,
    right_residue: int,
    right_modulus: int,
) -> tuple[int, int]:
    """Combine two compatible congruences, allowing non-coprime moduli."""
    common = gcd(left_modulus, right_modulus)
    difference = right_residue - left_residue
    if difference % common:
        raise ArithmeticError("incompatible point-order congruences")
    reduced_right = right_modulus // common
    if reduced_right == 1:
        multiplier = 0
    else:
        multiplier = (
            difference // common
            * pow(left_modulus // common, -1, reduced_right)
        ) % reduced_right
    combined_modulus = left_modulus * reduced_right
    combined_residue = (left_residue + left_modulus * multiplier) % combined_modulus
    return combined_residue, combined_modulus


def curve_order_bsgs(curve: Curve, rng: Random, max_points: int = 32) -> int:
    """Count E(F_p) exactly using Hasse, BSGS, and the quadratic twist.

    The routine gathers exact orders of sampled points on E and its twist. The
    true order must satisfy the resulting pair of congruences and the Hasse
    bound. It returns only when those conditions leave one integer.
    """
    if max_points < 2:
        raise ValueError("max_points must be at least 2")

    twist = quadratic_twist(curve)
    radius = isqrt(4 * curve.p)
    lower = curve.p + 1 - radius
    upper = curve.p + 1 + radius
    curve_exponent_multiple = 1
    twist_exponent_multiple = 1

    for sample_index in range(max_points):
        active_curve = curve if sample_index % 2 == 0 else twist
        point = _random_affine_point(active_curve, rng)
        point_order = _point_order_from_hasse_interval(active_curve, point)
        if active_curve is curve:
            curve_exponent_multiple = lcm(curve_exponent_multiple, point_order)
        else:
            twist_exponent_multiple = lcm(twist_exponent_multiple, point_order)

        residue, modulus = _crt_pair(
            0,
            curve_exponent_multiple,
            2 * curve.p + 2,
            twist_exponent_multiple,
        )
        first = residue
        if first < lower:
            first += ((lower - first + modulus - 1) // modulus) * modulus
        if first <= upper and first + modulus > upper:
            return first

    raise RuntimeError(
        "point orders did not isolate the curve order within max_points="
        f"{max_points}"
    )


def find_prime_order_curve(p: int, rng: Random, max_attempts: int = 10_000) -> tuple[Curve, int, int]:
    """Sample nonsingular curves until the exact group order is prime."""
    roots = square_root_multiplicities(p)
    for attempt in range(1, max_attempts + 1):
        a = rng.randrange(p)
        b = rng.randrange(p)
        try:
            curve = Curve(p, a, b)
        except ValueError:
            continue
        order = curve_order(curve, roots)
        if is_prime(order):
            return curve, order, attempt
    raise RuntimeError(f"no prime-order curve found in {max_attempts} attempts")


def embedding_degree(q: int, subgroup_order: int, max_degree: int = 10_000) -> int:
    """Return the least positive k with subgroup_order dividing q**k - 1."""
    if subgroup_order <= 1 or q % subgroup_order == 0:
        raise ValueError("the subgroup order must be nontrivial and coprime to q")
    residue = 1
    for degree in range(1, max_degree + 1):
        residue = residue * q % subgroup_order
        if residue == 1:
            return degree
    raise ValueError(f"embedding degree exceeds max_degree={max_degree}")


@dataclass(frozen=True)
class PairingFamilyParameters:
    """Exact integer parameters obtained from a pairing-family seed."""

    family: str
    seed: int
    p: int
    r: int
    trace: int
    embedding_degree: int
    cofactor: int

    @property
    def rho(self) -> float:
        """Return log(p) / log(r) without converting either integer to float."""
        return log(self.p) / log(self.r)


@dataclass(frozen=True)
class PairingFamilyValidation:
    """Results of the independent arithmetic checks for family parameters."""

    order_divisible: bool
    exact_embedding_degree: bool
    p_is_prime: bool | None
    r_is_prime: bool | None

    @property
    def valid(self) -> bool:
        """Return whether all requested checks passed."""
        prime_checks = (self.p_is_prime, self.r_is_prime)
        return (
            self.order_divisible
            and self.exact_embedding_degree
            and all(value is not False for value in prime_checks)
        )


PAIRING_FAMILIES = ("BN", "BLS12", "BLS24", "KSS16")


def _exact_quotient(numerator: int, denominator: int, label: str) -> int:
    quotient, remainder = divmod(numerator, denominator)
    if remainder:
        raise ValueError(f"seed does not make {label} integral")
    return quotient


def evaluate_pairing_family(family: str, seed: int) -> PairingFamilyParameters:
    """Evaluate the BN, BLS12, BLS24, or KSS16 family polynomials exactly."""
    normalized = family.upper()
    u = seed
    if normalized == "BN":
        p = 36 * u**4 + 36 * u**3 + 24 * u**2 + 6 * u + 1
        r = 36 * u**4 + 36 * u**3 + 18 * u**2 + 6 * u + 1
        trace = 6 * u**2 + 1
        degree = 12
    elif normalized == "BLS12":
        r = u**4 - u**2 + 1
        p = _exact_quotient((u - 1) ** 2 * r, 3, "BLS12 p") + u
        trace = u + 1
        degree = 12
    elif normalized == "BLS24":
        r = u**8 - u**4 + 1
        p = _exact_quotient((u - 1) ** 2 * r, 3, "BLS24 p") + u
        trace = u + 1
        degree = 24
    elif normalized == "KSS16":
        p = _exact_quotient(
            u**10
            + 2 * u**9
            + 5 * u**8
            + 48 * u**6
            + 152 * u**5
            + 240 * u**4
            + 625 * u**2
            + 2398 * u
            + 3125,
            980,
            "KSS16 p",
        )
        r = _exact_quotient(u**8 + 48 * u**4 + 625, 61_250, "KSS16 r")
        trace = _exact_quotient(2 * u**5 + 41 * u + 35, 35, "KSS16 trace")
        degree = 16
    else:
        choices = ", ".join(PAIRING_FAMILIES)
        raise ValueError(f"unknown pairing family {family!r}; expected one of {choices}")

    if p <= 1 or r <= 1:
        raise ValueError("seed produced non-positive field or subgroup parameters")
    cofactor = _exact_quotient(p + 1 - trace, r, "curve cofactor")
    return PairingFamilyParameters(normalized, u, p, r, trace, degree, cofactor)


def validate_pairing_family(
    parameters: PairingFamilyParameters,
    *,
    check_primality: bool = True,
    deterministic_prime_limit_bits: int = 64,
) -> PairingFamilyValidation:
    """Check the subgroup relation, exact embedding degree, and toy primality."""
    p_prime: bool | None = None
    r_prime: bool | None = None
    if check_primality:
        if max(parameters.p.bit_length(), parameters.r.bit_length()) > deterministic_prime_limit_bits:
            raise ValueError(
                "deterministic primality validation is restricted to the configured bit ceiling"
            )
        p_prime = is_prime(parameters.p)
        r_prime = is_prime(parameters.r)

    order_divisible = (parameters.p + 1 - parameters.trace) % parameters.r == 0
    try:
        actual_degree = embedding_degree(
            parameters.p,
            parameters.r,
            max_degree=parameters.embedding_degree,
        )
    except ValueError:
        actual_degree = None
    return PairingFamilyValidation(
        order_divisible=order_divisible,
        exact_embedding_degree=actual_degree == parameters.embedding_degree,
        p_is_prime=p_prime,
        r_is_prime=r_prime,
    )


def generate_pairing_family(family: str, seed: int) -> PairingFamilyParameters:
    """Return toy parameters only when all deterministic validity checks pass."""
    parameters = evaluate_pairing_family(family, seed)
    validation = validate_pairing_family(parameters)
    if not validation.valid:
        raise ValueError(f"seed {seed} does not generate a valid toy {parameters.family} curve")
    return parameters


def find_anomalous_curve(
    p: int, rng: Random, max_attempts: int = 100_000
) -> tuple[Curve, tuple[int, int], int]:
    """Find a toy curve with exactly p points by exhaustive point counting."""
    roots = square_root_multiplicities(p)
    for attempt in range(1, max_attempts + 1):
        a = rng.randrange(p)
        b = rng.randrange(p)
        try:
            curve = Curve(p, a, b)
        except ValueError:
            continue
        if curve_order(curve, roots) == p:
            return curve, curve.first_affine_point(), attempt
    raise RuntimeError(f"no anomalous curve found in {max_attempts} attempts")


def find_point_of_order(
    curve: Curve, group_order: int, subgroup_order: int
) -> tuple[int, int]:
    """Return the first affine point whose order is the stated prime divisor."""
    if group_order % subgroup_order:
        raise ValueError("subgroup_order must divide group_order")
    cofactor = group_order // subgroup_order
    for candidate in curve.affine_points():
        point = curve.scalar_mul(cofactor, candidate)
        if point is not None and curve.scalar_mul(subgroup_order, point) is None:
            return point
    raise RuntimeError("no point of the requested order was found")


def supersingular_k2_curve(
    p: int, subgroup_order: int
) -> tuple[Curve, tuple[int, int], int]:
    """Construct the j=1728 CM family y^2=x^3+x with embedding degree two."""
    if p % 4 != 3:
        raise ValueError("the j=1728 construction requires p congruent to 3 mod 4")
    curve = Curve(p, 1, 0)
    group_order = curve_order(curve)
    if group_order != p + 1:
        raise ArithmeticError("the supersingular curve did not have order p + 1")
    if group_order % subgroup_order or embedding_degree(p, subgroup_order) != 2:
        raise ValueError("the requested subgroup does not have embedding degree two")
    return curve, find_point_of_order(curve, group_order, subgroup_order), group_order


def points_from_scalars(
    curve: Curve, generator: AffinePoint, scalars: list[int]
) -> list[AffinePoint]:
    """Map explicitly sampled group scalars to distinct curve points."""
    return [curve.scalar_mul(scalar, generator) for scalar in scalars]


class ShortWeierstrassCurve:
    """Object-point compatibility layer with auditable operation counters."""

    def __init__(self, p: int, a: int, b: int) -> None:
        self._curve = Curve(p, a, b)
        self.p = p
        self.a = a % p
        self.b = b % p
        self.trace: dict[str, int] = {}
        self.reset_trace()

    def reset_trace(self) -> None:
        self.trace = {
            "group_operation": 0,
            "coordinate_arithmetic": 0,
            "equality_test": 0,
        }

    def point(self, x: int, y: int) -> Point:
        affine = (x % self.p, y % self.p)
        if not self._curve.contains(affine):
            raise ValueError("point is not on the curve")
        return Point(*affine)

    @staticmethod
    def _to_affine(point: Point) -> AffinePoint:
        if point.is_infinity:
            return None
        assert point.x is not None and point.y is not None
        return point.x, point.y

    @staticmethod
    def _from_affine(point: AffinePoint) -> Point:
        return INFINITY if point is None else Point(*point)

    def add(self, left: Point, right: Point, *, charge: bool = True) -> Point:
        if charge:
            self.trace["group_operation"] += 1
        self.trace["coordinate_arithmetic"] += 1
        result = self._curve.add(self._to_affine(left), self._to_affine(right))
        return self._from_affine(result)

    def neg(self, point: Point) -> Point:
        return self._from_affine(self._curve.neg(self._to_affine(point)))

    def scalar_mul(self, scalar: int, point: Point, *, charge: bool = True) -> Point:
        if scalar < 0:
            return self.scalar_mul(-scalar, self.neg(point), charge=charge)
        result = INFINITY
        addend = point
        while scalar:
            if scalar & 1:
                result = self.add(result, addend, charge=charge)
            addend = self.add(addend, addend, charge=charge)
            scalar >>= 1
        return result

    def cardinality(self) -> int:
        return curve_order(self._curve)
