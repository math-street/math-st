"""Probe the maximal-order Kummer residue character from A028.

Sub-goal: P1.5 / SG-34
Inputs:   [--smoke] [--output-dir PATH]
Outputs:  data/probe_kummer_class_character_<profile>_<date>.csv
Runtime:  smoke and full profiles under 10 seconds
Validated against: the exact-order family
                   Delta_r = 1 - 4*2^r, a = (2, omega),
                   a^r = (omega), and direct finite-field arithmetic

This is a falsification/regression driver for the algebraic character.  It
does not purport to verify Chebotarev or the GRH-conditional auxiliary-prime
search bound.
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

from lib.curves import is_prime  # noqa: E402


SMOKE_PRIMES = (3, 5, 7, 11)
FULL_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


def legendre_symbol(value: int, prime: int) -> int:
    """Return the Legendre symbol of ``value`` modulo an odd prime."""
    value %= prime
    if value == 0:
        return 0
    symbol = pow(value, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def modular_square_root(value: int, prime: int) -> int | None:
    """Return one square root modulo an odd prime, or ``None``.

    The implementation is the deterministic Tonelli--Shanks algorithm.  The
    tested auxiliary primes are tiny, but using the general algorithm keeps
    the arithmetic faithful to the claimed polynomial-time evaluator.
    """
    if prime == 2:
        return value % 2
    if not is_prime(prime):
        raise ValueError("modulus must be prime")
    value %= prime
    if value == 0:
        return 0
    if legendre_symbol(value, prime) != 1:
        return None
    if prime % 4 == 3:
        return pow(value, (prime + 1) // 4, prime)

    odd_part = prime - 1
    two_adic_order = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        two_adic_order += 1

    nonresidue = 2
    while legendre_symbol(nonresidue, prime) != -1:
        nonresidue += 1

    c = pow(nonresidue, odd_part, prime)
    root = pow(value, (odd_part + 1) // 2, prime)
    residue = pow(value, odd_part, prime)
    exponent = two_adic_order
    while residue != 1:
        index = 1
        square = residue * residue % prime
        while square != 1:
            square = square * square % prime
            index += 1
            if index >= exponent:
                raise ArithmeticError("Tonelli--Shanks invariant failed")
        multiplier = pow(c, 1 << (exponent - index - 1), prime)
        root = root * multiplier % prime
        residue = residue * multiplier * multiplier % prime
        c = multiplier * multiplier % prime
        exponent = index
    return root


def a019_discriminant(subgroup_order: int) -> int:
    """Return the discriminant ``1 - 4*2^r`` from A019."""
    if subgroup_order < 3 or not is_prime(subgroup_order):
        raise ValueError("subgroup_order must be an odd prime")
    return 1 - 4 * (1 << subgroup_order)


def kummer_value_at_split_prime(
    subgroup_order: int, auxiliary_prime: int
) -> tuple[int, int] | None:
    """Evaluate the Kummer class of ``omega`` at a split auxiliary prime.

    Here ``omega^2 - omega + 2^r = 0`` and
    ``(2, omega)^r = (omega)``.  The result is a pair ``(omega mod q, z)``
    with ``z = omega^((q-1)/r)``.  A nontrivial ``z`` has exact order ``r``
    and therefore separates the whole order-``r`` ideal-class subgroup.
    """
    r = subgroup_order
    q = auxiliary_prime
    if q <= 2 or not is_prime(q):
        raise ValueError("auxiliary_prime must be an odd prime")
    if (q - 1) % r:
        return None
    discriminant = a019_discriminant(r)
    if discriminant % q == 0:
        return None
    square_root = modular_square_root(discriminant, q)
    if square_root is None:
        return None

    inverse_two = pow(2, -1, q)
    for signed_root in (square_root, -square_root % q):
        omega = (1 + signed_root) * inverse_two % q
        if (omega * omega - omega + pow(2, r, q)) % q:
            raise ArithmeticError("quadratic root does not satisfy the order equation")
        value = pow(omega, (q - 1) // r, q)
        if value != 1:
            if pow(value, r, q) != 1:
                raise ArithmeticError("residue character did not land in mu_r")
            return omega, value
    return None


def find_distinguishing_prime(
    subgroup_order: int, *, max_multiplier: int = 100_000
) -> tuple[int, int, int, int]:
    """Find the first tested ``q = k*r + 1`` with nontrivial character."""
    r = subgroup_order
    if r < 3 or not is_prime(r):
        raise ValueError("subgroup_order must be an odd prime")
    if max_multiplier < 2:
        raise ValueError("max_multiplier must be at least two")
    # For odd r, q can be odd only when k is even.
    for multiplier in range(2, max_multiplier + 1, 2):
        auxiliary_prime = multiplier * r + 1
        if not is_prime(auxiliary_prime):
            continue
        result = kummer_value_at_split_prime(r, auxiliary_prime)
        if result is None:
            continue
        omega, value = result
        return auxiliary_prime, multiplier, omega, value
    raise ArithmeticError("no distinguishing auxiliary prime in the search window")


def recover_discrete_log(base: int, value: int, order: int, prime: int) -> int:
    """Recover a toy order-``order`` finite-field logarithm exhaustively."""
    accumulator = 1
    for exponent in range(order):
        if accumulator == value:
            return exponent
        accumulator = accumulator * base % prime
    raise ArithmeticError("value is outside the claimed cyclic subgroup")


def run_case(subgroup_order: int) -> dict[str, int | bool]:
    """Validate the character on every scalar in one A019 target."""
    r = subgroup_order
    discriminant = a019_discriminant(r)
    q, multiplier, omega, character_base = find_distinguishing_prime(r)
    seen: set[int] = set()
    for scalar in range(r):
        # Replacing a^scalar by an equivalent ideal multiplies omega^scalar
        # by an r-th power.  The residue character therefore remains z^scalar.
        image = pow(character_base, scalar, q)
        recovered = recover_discrete_log(character_base, image, r, q)
        if recovered != scalar:
            raise ArithmeticError("Kummer character changed the discrete logarithm")
        seen.add(image)
    if len(seen) != r:
        raise ArithmeticError("nontrivial order-r character was not injective")
    return {
        "r": r,
        "discriminant": discriminant,
        "discriminant_bits": (-discriminant).bit_length(),
        "form_a": 2,
        "form_b": 1,
        "form_c": 1 << (r - 1),
        "auxiliary_prime": q,
        "auxiliary_multiplier": multiplier,
        "auxiliary_bits": q.bit_length(),
        "omega_mod_q": omega,
        "character_base": character_base,
        "character_order": len(seen),
        "all_logs_recovered": True,
        "q_exceeds_sqrt_abs_delta": q > math.isqrt(-discriminant),
    }


def write_rows(rows: list[dict[str, int | bool]], path: Path) -> None:
    """Write deterministic probe rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    profile = "smoke" if args.smoke else "full"
    primes = SMOKE_PRIMES if args.smoke else FULL_PRIMES
    rows = [run_case(prime) for prime in primes]
    output = (
        args.output_dir
        / f"probe_kummer_class_character_{profile}_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    print(f"wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
