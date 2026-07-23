"""Construct the uniform succinct ordinary ring-class target from A029.

Sub-goal: SG-30
Inputs:   [--smoke] [--prime R ...] [--output-dir PATH]
Outputs:  data/construct_sg30_ring_class_target_<profile>_<date>.csv
Runtime:  smoke and full profiles under 10 seconds
Validated against: the conductor exact sequence for
                   O_r = Z + r^2 Z[i], exact Gaussian residue arithmetic,
                   canonical positive-form reduction, and small complete
                   class-group enumerations

For every odd prime r, the residue 1 + r*i modulo r^2 has exact order r
after quotienting by rational and Gaussian units.  Its contracted ideal is
represented by the primitive form

    (1 + r^2, 2*r^3, r^4)

of discriminant -4*r^4.  Reduction gives the especially simple canonical
representative (r^2, 2*r, r^2 + 1).
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))
CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from lib.curves import is_prime  # noqa: E402
from probe_ring_class_transfer import reduce_positive_form  # noqa: E402

Form = tuple[int, int, int]
GaussianInteger = tuple[int, int]

SMOKE_PRIMES = (3, 5, 7, 11)
FULL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 43, 101, 211, 1009, 10007)


def gaussian_multiply_mod(
    left: GaussianInteger, right: GaussianInteger, modulus: int
) -> GaussianInteger:
    """Multiply Gaussian residues modulo ``modulus``."""
    a, b = left
    c, d = right
    return (a * c - b * d) % modulus, (a * d + b * c) % modulus


def gaussian_power_mod(
    value: GaussianInteger, exponent: int, modulus: int
) -> GaussianInteger:
    """Exponentiate a Gaussian residue by binary powering."""
    if exponent < 0 or modulus < 2:
        raise ValueError("expected a nonnegative exponent and positive modulus")
    result = (1, 0)
    base = value[0] % modulus, value[1] % modulus
    while exponent:
        if exponent & 1:
            result = gaussian_multiply_mod(result, base, modulus)
        base = gaussian_multiply_mod(base, base, modulus)
        exponent >>= 1
    return result


def projectively_trivial(value: GaussianInteger, modulus: int) -> bool:
    """Test membership in rational units times ``{+-1, +-i}``."""
    real, imaginary = value[0] % modulus, value[1] % modulus
    return (
        imaginary == 0 and math.gcd(real, modulus) == 1
    ) or (
        real == 0 and math.gcd(imaginary, modulus) == 1
    )


def gaussian_character(prime: int) -> int:
    """Return the Kronecker character ``(-4 / prime)``."""
    if prime == 2 or not is_prime(prime):
        raise ValueError("expected an odd prime")
    return 1 if prime % 4 == 1 else -1


def raw_parameter_form(prime: int, parameter: int) -> Form:
    """Return the contracted form for ``1 + prime*parameter*i``."""
    if prime == 2 or not is_prime(prime):
        raise ValueError("prime must be odd")
    parameter %= prime
    form = (
        1 + prime * prime * parameter * parameter,
        2 * prime**3 * parameter,
        prime**4,
    )
    discriminant = form[1] * form[1] - 4 * form[0] * form[2]
    if discriminant != -4 * prime**4:
        raise ArithmeticError("contracted form has the wrong discriminant")
    if math.gcd(math.gcd(form[0], abs(form[1])), form[2]) != 1:
        raise ArithmeticError("contracted form is not primitive")
    return form


def reduced_parameter_form(prime: int, parameter: int) -> Form:
    """Return the canonical reduced representative of a subgroup element."""
    return reduce_positive_form(raw_parameter_form(prime, parameter))


def wild_parameter(value: GaussianInteger, prime: int) -> int:
    """Recover ``a`` from the class of ``1 + prime*a*i`` modulo ``prime^2``."""
    modulus = prime * prime
    real, imaginary = value[0] % modulus, value[1] % modulus
    if real % prime:
        slope = imaginary * pow(real, -1, modulus) % modulus
    elif imaginary % prime:
        # Multiplication by -i sends (real, imaginary) to
        # (imaginary, -real), which fixes the projective class.
        slope = (-real) * pow(imaginary, -1, modulus) % modulus
    else:
        raise ArithmeticError("residue is not a unit modulo prime")
    if slope % prime:
        raise ArithmeticError("residue is outside the wild principal-unit line")
    return slope // prime % prime


def construct_target(prime: int) -> dict[str, int | bool]:
    """Construct and certify the SG-30 target for one odd prime."""
    if prime == 2 or not is_prime(prime):
        raise ValueError("prime must be odd")

    r = prime
    conductor = r * r
    discriminant = -4 * r**4
    raw = raw_parameter_form(r, 1)
    reduced = reduce_positive_form(raw)
    expected_reduced = (r * r, 2 * r, r * r + 1)
    if reduced != expected_reduced:
        raise ArithmeticError("unexpected canonical reduced representative")

    generator = (1, r)
    generator_power = gaussian_power_mod(generator, r, conductor)
    if not projectively_trivial(generator_power, conductor):
        raise ArithmeticError("generator r-th power is not trivial")
    if projectively_trivial(generator, conductor):
        raise ArithmeticError("generator is already trivial")
    if wild_parameter(generator, r) != 1:
        raise ArithmeticError("wild logarithm does not recover the generator")

    character = gaussian_character(r)
    class_number = r * (r - character) // 2
    if class_number % r:
        raise ArithmeticError("ring class number is not divisible by r")

    n = r.bit_length()
    discriminant_bits = (-discriminant).bit_length()
    return {
        "r": r,
        "input_bits": n,
        "conductor": conductor,
        "discriminant": discriminant,
        "discriminant_bits": discriminant_bits,
        "raw_a": raw[0],
        "raw_b": raw[1],
        "raw_c": raw[2],
        "reduced_a": reduced[0],
        "reduced_b": reduced[1],
        "reduced_c": reduced[2],
        "gaussian_character": character,
        "class_number": class_number,
        "class_number_multiple": class_number // r,
        "generator_power_real": generator_power[0],
        "generator_power_imaginary": generator_power[1],
        "exact_order_r_certified": True,
        "inside_sg25_lower_scale": discriminant_bits >= 2 * n - 2,
        "under_60_bit_ceiling": discriminant_bits <= 60,
    }


def write_rows(rows: list[dict[str, int | bool]], path: Path) -> None:
    """Write deterministic constructor records."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--prime",
        type=int,
        action="append",
        dest="primes",
        help="construct a target for this odd prime; may be repeated",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.primes:
        primes = tuple(args.primes)
        profile = "custom"
    elif args.smoke:
        primes = SMOKE_PRIMES
        profile = "smoke"
    else:
        primes = FULL_PRIMES
        profile = "full"
    rows = [construct_target(prime) for prime in primes]
    output = (
        args.output_dir
        / f"construct_sg30_ring_class_target_{profile}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    print(f"wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
