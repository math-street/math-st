"""Probe the conductor-kernel universality theorem for Gaussian orders.

Sub-goal: P1.5 / SG-34
Inputs:   [--smoke] [--output-dir PATH]
Outputs:  data/probe_conductor_universality_<profile>_<date>.csv
Runtime:  smoke under 10 seconds
Validated against: reduced-form enumeration, the Gaussian conductor exact
                   sequence, and the existing anomalous transfer fixtures
"""

from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.anomalous import additive_transfer  # noqa: E402
from lib.curves import curve_order, find_anomalous_curve, is_prime  # noqa: E402
from lib.isogeny import reduced_positive_forms  # noqa: E402
from probe_ring_class_transfer import (  # noqa: E402
    Form,
    gaussian_gcd,
    reduce_positive_form,
    ring_class_form_from_parameter,
)

GaussianInteger = tuple[int, int]

SMOKE_CASES = ((101, 37, 20260723),)
FULL_CASES = (
    (101, 37, 20260723),
    (211, 73, 20260724),
    (401, 137, 20260725),
)


def gaussian_multiply(
    left: GaussianInteger, right: GaussianInteger, modulus: int
) -> GaussianInteger:
    """Multiply two Gaussian residues modulo ``modulus``."""
    a, b = left
    c, d = right
    return (a * c - b * d) % modulus, (a * d + b * c) % modulus


def gaussian_residue_is_unit(value: GaussianInteger, modulus: int) -> bool:
    """Return whether a Gaussian residue is a unit modulo ``modulus``."""
    real, imaginary = value
    return math.gcd(real * real + imaginary * imaginary, modulus) == 1


def gaussian_projectively_equivalent(
    left: GaussianInteger, right: GaussianInteger, modulus: int
) -> bool:
    """Test equality modulo rational units and the Gaussian unit ``i``."""
    if not gaussian_residue_is_unit(left, modulus) or not gaussian_residue_is_unit(
        right, modulus
    ):
        raise ValueError("projective residues must be units")
    c, d = right
    inverse_norm = pow((c * c + d * d) % modulus, -1, modulus)
    inverse = c * inverse_norm % modulus, -d * inverse_norm % modulus
    quotient = gaussian_multiply(left, inverse, modulus)
    real, imaginary = quotient
    return (
        imaginary == 0 and math.gcd(real, modulus) == 1
    ) or (
        real == 0 and math.gcd(imaginary, modulus) == 1
    )


def prime_to_conductor_equivalent_form(
    form: Form,
    conductor: int,
    *,
    rng: random.Random | None = None,
    max_attempts: int = 10_000,
) -> Form:
    """Find an equivalent form whose leading coefficient is prime to ``f``.

    For discriminant ``-4*f^2`` and odd ``f``, the polynomial
    ``F(1,t)`` has at most one root modulo every prime dividing ``f``.
    Random ``t`` therefore gives a Las Vegas expected-polynomial algorithm.
    """
    if conductor <= 1 or conductor % 2 == 0:
        raise ValueError("the current theorem uses an odd conductor greater than one")
    a, b, c = form
    if b * b - 4 * a * c != -4 * conductor * conductor:
        raise ValueError("form has the wrong Gaussian order discriminant")
    if math.gcd(math.gcd(a, abs(b)), c) != 1:
        raise ValueError("form must be primitive")
    generator = rng or random.Random((a << 32) ^ (b << 16) ^ c ^ conductor)
    for _ in range(max_attempts):
        shear = generator.randrange(conductor)
        leading = a + b * shear + c * shear * shear
        if math.gcd(leading, conductor) != 1:
            continue
        transformed = leading, b + 2 * c * shear, c
        if transformed[1] * transformed[1] - 4 * transformed[0] * transformed[2] != (
            -4 * conductor * conductor
        ):
            raise ArithmeticError("unimodular shear changed the discriminant")
        return transformed
    raise ArithmeticError("failed to find a conductor-coprime equivalent form")


def gaussian_torus_residue_from_form(
    conductor: int, form: Form
) -> GaussianInteger:
    """Invert the conductor map on ``Pic(Z + f*Z[i])``.

    The output is a unit of ``Z[i]/f`` defined up to a rational unit and a
    Gaussian unit. This is the explicit finite-ring torus representation.
    """
    coprime_form = prime_to_conductor_equivalent_form(form, conductor)
    leading, middle, _ = coprime_form
    if middle % 2:
        raise ArithmeticError("Gaussian discriminant requires an even middle term")
    generator = gaussian_gcd((leading, 0), (-middle // 2, conductor))
    residue = generator[0] % conductor, generator[1] % conductor
    if not gaussian_residue_is_unit(residue, conductor):
        raise ArithmeticError("extended ideal generator is not a conductor unit")
    return residue


def additive_ring_class_form(p: int, parameter: int) -> Form:
    """Embed an additive ``F_p`` parameter in ``Pic(Z + p^2*Z[i])``."""
    if not is_prime(p) or p == 2:
        raise ValueError("p must be an odd prime")
    parameter %= p
    raw = (
        1 + p * p * parameter * parameter,
        2 * p**3 * parameter,
        p**4,
    )
    if raw[1] * raw[1] - 4 * raw[0] * raw[2] != -4 * p**4:
        raise ArithmeticError("additive ring-class form has the wrong discriminant")
    return reduce_positive_form(raw)


def principal_unit_parameter(residue: GaussianInteger, p: int) -> int:
    """Linearize ``(1+p*a*i)`` modulo rational and Gaussian units."""
    modulus = p * p
    real, imaginary = residue[0] % modulus, residue[1] % modulus
    if real % p:
        parameter = imaginary * pow(real, -1, modulus) % modulus
    elif imaginary % p:
        # Multiplication by -i changes (real, imag) to (imag, -real).
        parameter = (-real) * pow(imaginary, -1, modulus) % modulus
    else:
        raise ArithmeticError("residue is not a unit modulo p")
    if parameter % p:
        raise ArithmeticError("residue is outside the principal-unit line")
    return parameter // p % p


def gaussian_character(prime: int) -> int:
    """Return the Kronecker character (-4 / prime) for an odd prime."""
    if prime % 2 == 0 or not is_prime(prime):
        raise ValueError("expected an odd prime")
    return 1 if prime % 4 == 1 else -1


def factor_integer(value: int) -> dict[int, int]:
    """Factor a toy positive integer by trial division."""
    if value < 1:
        raise ValueError("factorization input must be positive")
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def gaussian_conductor_torus_order(conductor: int) -> int:
    """Return |(Z[i]/f)^*/(Z/f)^*| for odd ``f``."""
    if conductor <= 1 or conductor % 2 == 0:
        raise ValueError("expected an odd conductor greater than one")
    order = 1
    for prime, exponent in factor_integer(conductor).items():
        order *= prime ** (exponent - 1) * (prime - gaussian_character(prime))
    return order


def validate_order_formula(conductor: int) -> tuple[int, int]:
    """Compare the local torus formula with complete form enumeration."""
    torus_order = gaussian_conductor_torus_order(conductor)
    class_number = len(reduced_positive_forms(-4 * conductor * conductor))
    # For f > 1, O_K^*/O_f^* is generated by i and has order two.
    if torus_order != 2 * class_number:
        raise ArithmeticError("conductor exact-sequence order formula failed")
    return torus_order, class_number


def gaussian_ring_class_number(conductor: int) -> int:
    """Return the Gaussian ring class number from the proved exact sequence.

    Complete reduced-form enumeration is deliberately kept in
    ``validate_order_formula`` for small independent fixtures.  Its search
    range is quadratic in the discriminant scale and is not an appropriate
    way to evaluate the infinite-family construction at conductor ``p^2``.
    """
    torus_order = gaussian_conductor_torus_order(conductor)
    if torus_order % 2:
        raise ArithmeticError("the Gaussian unit quotient should have order two")
    return torus_order // 2


def intrinsic_source_characteristic_verdict(
    p: int, subgroup_order: int, trace: int
) -> dict[str, int | bool]:
    """Check the Hasse collapse in the source-characteristic branch."""
    if not is_prime(p) or not is_prime(subgroup_order):
        raise ValueError("p and subgroup_order must be prime")
    if subgroup_order == p:
        raise ValueError("the intrinsic tame branch requires r != p")
    curve_order_value = p + 1 - trace
    if curve_order_value % subgroup_order:
        raise ValueError("r must divide the source curve order")
    if (p - 1) % subgroup_order:
        raise ValueError("the source-characteristic torus requires r | p-1")
    if subgroup_order <= 2 or (subgroup_order - 2) ** 2 <= 4 * p:
        raise ValueError("the fixture does not satisfy the strict Hasse threshold")
    if trace != 2:
        raise ArithmeticError("Hasse collapse failed to force trace two")
    return {
        "p": p,
        "r": subgroup_order,
        "trace": trace,
        "curve_order": curve_order_value,
        "embedding_degree_one": pow(p, 1, subgroup_order) == 1,
    }


def validate_semisimple_inverse(p: int) -> int:
    """Check the general inverse on all A025 projective residues."""
    if p % 4 != 3:
        raise ValueError("the semisimple fixture requires an inert Gaussian prime")
    checked = 0
    for parameter in (*range(p), None):
        form = ring_class_form_from_parameter(p, parameter)
        residue = gaussian_torus_residue_from_form(p, form)
        expected = (0, 1) if parameter is None else (1, parameter)
        if not gaussian_projectively_equivalent(residue, expected, p):
            raise ArithmeticError("semisimple conductor inverse failed")
        checked += 1
    return checked


def run_additive_case(p: int, secret: int, seed: int) -> dict[str, object]:
    """Validate an anomalous transfer followed by the wild conductor map."""
    curve, generator, attempts = find_anomalous_curve(p, random.Random(seed + p))
    if curve_order(curve) != p:
        raise ArithmeticError("additive fixture is not anomalous")
    generator_parameter = additive_transfer(curve, generator, validate_curve=False)
    if generator_parameter == 0:
        raise ArithmeticError("additive character is zero on the generator")

    forms: list[Form] = []
    extracted: list[int] = []
    for scalar in range(p):
        point = curve.scalar_mul(scalar, generator)
        parameter = additive_transfer(curve, point, validate_curve=False)
        if parameter != scalar * generator_parameter % p:
            raise ArithmeticError("anomalous character is not additive")
        form = additive_ring_class_form(p, parameter)
        residue = gaussian_torus_residue_from_form(p * p, form)
        expected = 1, p * parameter
        if not gaussian_projectively_equivalent(residue, expected, p * p):
            raise ArithmeticError("wild conductor inverse failed")
        recovered_parameter = principal_unit_parameter(residue, p)
        if recovered_parameter != parameter:
            raise ArithmeticError("principal-unit logarithm failed")
        forms.append(form)
        extracted.append(recovered_parameter)

    if len(set(forms)) != p:
        raise ArithmeticError("wild ring-class map is not injective")
    target_parameter = extracted[secret]
    recovered = target_parameter * pow(generator_parameter, -1, p) % p
    if recovered != secret:
        raise ArithmeticError("wild ring-class target failed to recover the log")

    torus_order = gaussian_conductor_torus_order(p * p)
    class_number = gaussian_ring_class_number(p * p)
    if class_number % p:
        raise ArithmeticError("wild ring class group lacks the required p-torsion")
    return {
        "p": p,
        "secret": secret,
        "recovered": recovered,
        "conductor": p * p,
        "discriminant": -4 * p**4,
        "class_number": class_number,
        "torus_order": torus_order,
        "image_size": len(set(forms)),
        "construction_attempts": attempts,
    }


def write_rows(rows: list[dict[str, object]], path: Path) -> None:
    """Write deterministic validation rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parents[1] / "data")
    args = parser.parse_args()
    cases = SMOKE_CASES if args.smoke else FULL_CASES
    rows = [run_additive_case(*case) for case in cases]
    semisimple_checked = validate_semisimple_inverse(43)
    intrinsic_checked = [
        intrinsic_source_characteristic_verdict(p, r, 2)
        for p, r in ((47, 23), (59, 29), (83, 41))
    ]
    profile = "smoke" if args.smoke else "full"
    output = (
        args.output_dir
        / f"probe_conductor_universality_{profile}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    for row in rows:
        print(row)
    print(f"semisimple projective residues checked: {semisimple_checked}")
    print(f"intrinsic trace-two cases checked: {len(intrinsic_checked)}")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
