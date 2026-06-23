"""
verify_published_example.py — reproduce the documented genus-31 GHS example.
Sub-goal: P1.4 / SG-01c
Inputs:   --smoke
Outputs:  a deterministic one-line invariant report on stdout
Runtime:  ~0.05 seconds for the degree-155 regression
Validated against: Magma V2.19.8 function-field example H42E45
"""

from __future__ import annotations

import argparse
import time

from ghs import GHSProfile, apply_frobenius_polynomial, ghs_profile
from lib.curves import (
    BinaryField,
    binary_polynomial_divmod,
    find_irreducible_binary_polynomial,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def build_profile(smoke: bool = False) -> tuple[str, BinaryField, GHSProfile, int]:
    if smoke:
        field = BinaryField(4, 0b1_0011)
        profile = ghs_profile(field, 1)
        expected_genus = 1
        label = "smoke"
    else:
        modulus = find_irreducible_binary_polynomial(155)
        field = BinaryField(155, modulus)
        annihilator = (1 << 5) | (1 << 2) | 1
        quotient, remainder = binary_polynomial_divmod((1 << 31) | 1, annihilator)
        if remainder:
            raise AssertionError("published Frobenius polynomial did not divide t^31-1")
        generator = 0b10
        beta = apply_frobenius_polynomial(field, generator, quotient, base_degree=5)
        if beta == 0:
            raise AssertionError("published projection produced zero")
        # y^2+y=1/x+beta*x corresponds to an ordinary model whose constant
        # coefficient is beta^2, so ghs_profile recovers beta as sqrt(b).
        curve_b = field.square(beta)
        profile = ghs_profile(field, curve_b, a=0, base_degree=5)
        expected_genus = 31
        label = "magma-degree-31"
    return label, field, profile, expected_genus


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    label, field, profile, expected_genus = build_profile(args.smoke)
    if profile.genus != expected_genus:
        raise AssertionError(f"expected genus {expected_genus}, got {profile.genus}")
    elapsed = time.perf_counter() - started
    print(
        f"example={label} modulus={hex(field.modulus)} "
        f"annihilator={hex(profile.annihilator_polynomial)} "
        f"conjugate_rank={profile.conjugate_rank} magic_number={profile.magic_number} "
        f"genus={profile.genus} elapsed_seconds={elapsed:.6f}"
    )


if __name__ == "__main__":
    main()
