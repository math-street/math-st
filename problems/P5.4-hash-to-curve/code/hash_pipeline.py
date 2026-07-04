"""RFC-shaped toy hash-to-curve pipeline with compile-time map selection."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from lib.curves import (
    AffinePoint,
    Curve,
    MontgomeryCurve,
    MontgomeryPoint,
    TwistedEdwardsCurve,
    TwistedEdwardsPoint,
    curve_order,
    map_to_curve_elligator2,
    map_to_curve_elligator2_edwards,
    map_to_curve_simple_swu,
    map_to_curve_svdw,
    montgomery_to_weierstrass,
    montgomery_weierstrass_curve,
    twisted_edwards_from_montgomery,
    weierstrass_to_montgomery,
)
from lib.isogeny import velu_map_affine_nonkernel, velu_quotient


def expand_message_xmd_sha256(msg: bytes, dst: bytes, length: int) -> bytes:
    """Implement RFC 9380 Section 5.3.1 with SHA-256."""
    if length < 0 or length > 65535:
        raise ValueError("length must be in [0, 65535]")
    if len(dst) > 255:
        dst = sha256(b"H2C-OVERSIZE-DST-" + dst).digest()
    digest_size = sha256().digest_size
    block_size = sha256().block_size
    ell = (length + digest_size - 1) // digest_size
    if ell > 255:
        raise ValueError("requested output needs more than 255 digest blocks")
    dst_prime = dst + len(dst).to_bytes(1, "big")
    msg_prime = (
        bytes(block_size)
        + msg
        + length.to_bytes(2, "big")
        + b"\x00"
        + dst_prime
    )
    b0 = sha256(msg_prime).digest()
    if ell == 0:
        return b""
    blocks = [sha256(b0 + b"\x01" + dst_prime).digest()]
    for index in range(2, ell + 1):
        xor_block = bytes(left ^ right for left, right in zip(b0, blocks[-1]))
        blocks.append(sha256(xor_block + bytes([index]) + dst_prime).digest())
    return b"".join(blocks)[:length]


def hash_to_field_sha256(
    msg: bytes,
    count: int,
    p: int,
    dst: bytes,
    *,
    security_bits: int = 128,
) -> tuple[int, ...]:
    """Implement RFC 9380 hash_to_field for a prime field (m = 1)."""
    if count <= 0:
        raise ValueError("count must be positive")
    if p <= 1 or security_bits <= 0:
        raise ValueError("p and security_bits must be positive")
    field_bits = (p - 1).bit_length()
    element_length = (field_bits + security_bits + 7) // 8
    uniform = expand_message_xmd_sha256(msg, dst, count * element_length)
    return tuple(
        int.from_bytes(
            uniform[index * element_length : (index + 1) * element_length],
            "big",
        )
        % p
        for index in range(count)
    )


@dataclass(frozen=True, slots=True)
class ToyHashToCurveSuite:
    """Public compile-time parameters for one toy short-Weierstrass suite."""

    suite_id: str
    dst: bytes
    curve: Curve
    method: str
    z: int
    subgroup_order: int
    cofactor: int
    source_curve: Curve | None = None
    isogeny_degree: int | None = None
    kernel_generator: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        if len(self.dst) < 16:
            raise ValueError("toy suites require a DST of at least 16 bytes")
        if curve_order(self.curve) != self.subgroup_order * self.cofactor:
            raise ValueError("subgroup order times cofactor must equal curve order")
        if self.method not in {"sswu", "svdw", "sswu_isogeny"}:
            raise ValueError("unknown map method")
        if self.method == "sswu_isogeny":
            if (
                self.source_curve is None
                or self.isogeny_degree is None
                or self.kernel_generator is None
            ):
                raise ValueError("isogeny suites require source, degree, and kernel")
            quotient = velu_quotient(
                self.source_curve,
                self.kernel_generator,
                self.isogeny_degree,
            )
            if quotient != self.curve:
                raise ValueError("isogeny parameters do not target the suite curve")

    def map_field_element(
        self,
        u: int,
        *,
        trace: list[str] | None = None,
    ) -> tuple[int, int]:
        """Dispatch using only the public, compile-time suite method."""
        if self.method == "sswu":
            return map_to_curve_simple_swu(self.curve, u, self.z, trace=trace)
        if self.method == "svdw":
            return map_to_curve_svdw(self.curve, u, self.z, trace=trace)
        assert self.source_curve is not None
        assert self.isogeny_degree is not None
        assert self.kernel_generator is not None
        source_point = map_to_curve_simple_swu(
            self.source_curve,
            u,
            self.z,
            trace=trace,
        )
        return velu_map_affine_nonkernel(
            self.source_curve,
            source_point,
            self.kernel_generator,
            self.isogeny_degree,
            trace=trace,
        )

    def hash_field_pair(self, u0: int, u1: int) -> AffinePoint:
        """Map two field elements, add, and clear the public cofactor."""
        q0 = self.map_field_element(u0)
        q1 = self.map_field_element(u1)
        return self.curve.scalar_mul(self.cofactor, self.curve.add(q0, q1))

    def hash_to_curve(self, msg: bytes) -> AffinePoint:
        """Apply RFC 9380's two-element random-oracle composition."""
        u0, u1 = hash_to_field_sha256(msg, 2, self.curve.p, self.dst)
        return self.hash_field_pair(u0, u1)


TOY_SUITES = (
    ToyHashToCurveSuite(
        "TOY-P13-SHA256-SSWU-RO",
        b"P5.4-TOY-P13-SSWU-RO-v1",
        Curve(13, 1, 1),
        "sswu",
        6,
        3,
        6,
    ),
    ToyHashToCurveSuite(
        "TOY-P13-SHA256-SVDW-RO",
        b"P5.4-TOY-P13-SVDW-RO-v1",
        Curve(13, 1, 1),
        "svdw",
        11,
        3,
        6,
    ),
    ToyHashToCurveSuite(
        "TOY-P29-SHA256-SVDW-J0-RO",
        b"P5.4-TOY-P29-SVDW-J0-RO-v1",
        Curve(29, 0, 9),
        "svdw",
        28,
        5,
        6,
    ),
    ToyHashToCurveSuite(
        "TOY-P29-SHA256-SSWU-ISO-J0-RO",
        b"P5.4-TOY-P29-ISO-J0-RO-v1",
        Curve(29, 0, 9),
        "sswu_isogeny",
        10,
        5,
        6,
        Curve(29, 4, 11),
        3,
        (15, 16),
    ),
    ToyHashToCurveSuite(
        "TOY-P59-SHA256-SVDW-J1728-RO",
        b"P5.4-TOY-P59-SVDW-J1728-RO-v1",
        Curve(59, 56, 0),
        "svdw",
        1,
        5,
        12,
    ),
    ToyHashToCurveSuite(
        "TOY-P59-SHA256-SSWU-ISO-J1728-RO",
        b"P5.4-TOY-P59-ISO-J1728-RO-v1",
        Curve(59, 56, 0),
        "sswu_isogeny",
        18,
        5,
        12,
        Curve(59, 2, 13),
        3,
        (41, 35),
    ),
)


@dataclass(frozen=True, slots=True)
class ToyMontgomeryHashToCurveSuite:
    """Toy Elligator-2 suite with correctness-only affine group transport."""

    suite_id: str
    dst: bytes
    curve: MontgomeryCurve
    z: int
    subgroup_order: int
    cofactor: int

    def map_field_element(
        self,
        u: int,
        *,
        trace: list[str] | None = None,
    ) -> tuple[int, int]:
        return map_to_curve_elligator2(self.curve, u, self.z, trace=trace)

    def _to_weierstrass(self, point: MontgomeryPoint) -> AffinePoint:
        if point is None:
            return None
        return montgomery_to_weierstrass(self.curve, point)

    def _from_weierstrass(self, point: AffinePoint) -> MontgomeryPoint:
        if point is None:
            return None
        return weierstrass_to_montgomery(self.curve, point)

    def add(self, left: MontgomeryPoint, right: MontgomeryPoint) -> MontgomeryPoint:
        model = montgomery_weierstrass_curve(self.curve)
        result = model.add(self._to_weierstrass(left), self._to_weierstrass(right))
        return self._from_weierstrass(result)

    def scalar_mul(self, scalar: int, point: MontgomeryPoint) -> MontgomeryPoint:
        model = montgomery_weierstrass_curve(self.curve)
        result = model.scalar_mul(scalar, self._to_weierstrass(point))
        return self._from_weierstrass(result)

    def hash_field_pair(self, u0: int, u1: int) -> MontgomeryPoint:
        total = self.add(self.map_field_element(u0), self.map_field_element(u1))
        return self.scalar_mul(self.cofactor, total)

    def hash_to_curve(self, msg: bytes) -> MontgomeryPoint:
        u0, u1 = hash_to_field_sha256(msg, 2, self.curve.p, self.dst)
        return self.hash_field_pair(u0, u1)


@dataclass(frozen=True, slots=True)
class ToyEdwardsHashToCurveSuite:
    """Toy Elligator-2-to-Edwards suite with affine group arithmetic."""

    suite_id: str
    dst: bytes
    montgomery_curve: MontgomeryCurve
    curve: TwistedEdwardsCurve
    z: int
    subgroup_order: int
    cofactor: int

    def map_field_element(
        self,
        u: int,
        *,
        trace: list[str] | None = None,
    ) -> TwistedEdwardsPoint:
        return map_to_curve_elligator2_edwards(
            self.montgomery_curve,
            u,
            self.z,
            trace=trace,
        )

    def hash_field_pair(self, u0: int, u1: int) -> TwistedEdwardsPoint:
        total = self.curve.add(
            self.map_field_element(u0),
            self.map_field_element(u1),
        )
        return self.curve.scalar_mul(self.cofactor, total)

    def hash_to_curve(self, msg: bytes) -> TwistedEdwardsPoint:
        u0, u1 = hash_to_field_sha256(msg, 2, self.curve.p, self.dst)
        return self.hash_field_pair(u0, u1)


_TRANSPORT_MONTGOMERY = MontgomeryCurve(7, 4, 3)
TOY_MONTGOMERY_SUITE = ToyMontgomeryHashToCurveSuite(
    "TOY-MONTGOMERY-P7-SHA256-ELL2-RO",
    b"P5.4-TOY-MONTY-P7-ELL2-RO-v1",
    _TRANSPORT_MONTGOMERY,
    3,
    3,
    4,
)
TOY_EDWARDS_SUITE = ToyEdwardsHashToCurveSuite(
    "TOY-EDWARDS-P7-SHA256-ELL2-RO",
    b"P5.4-TOY-EDWARDS-P7-ELL2-RO-v1",
    _TRANSPORT_MONTGOMERY,
    twisted_edwards_from_montgomery(_TRANSPORT_MONTGOMERY),
    3,
    3,
    4,
)
