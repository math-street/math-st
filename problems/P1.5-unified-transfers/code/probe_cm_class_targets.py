"""Probe natural CM ideal, isogeny, and ray-class transfer candidates.

Sub-goal: P1.5 / A001
Inputs:   [--smoke] [--output-dir PATH]
Outputs:  data/probe_cm_class_targets_<profile>_<date>.csv
Runtime:  under 10 seconds at the default toy sizes

The experiment is deliberately exhaustive.  For each ordinary j=1728 curve,
it checks every nonzero multiple of a prime-order generator rather than sampling
candidate collisions.
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

from lib.curves import Curve, curve_order, find_point_of_order, is_prime  # noqa: E402
from lib.isogeny import (  # noqa: E402
    canonical_curve,
    class_number_from_reduced_forms,
    kernel_points,
    velu_quotient,
)


def largest_prime_factor(integer: int) -> int:
    """Return the largest prime factor of a positive integer."""
    if integer < 2:
        raise ValueError("integer must be at least 2")
    remaining = integer
    largest = 1
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            largest = divisor
            remaining //= divisor
        divisor += 1
    return max(largest, remaining)


def sqrt_minus_one(p: int) -> int:
    """Return the least square root of -1 in F_p."""
    for candidate in range(2, p):
        if candidate * candidate % p == p - 1:
            return candidate
    raise ValueError(f"-1 is not a square modulo {p}")


def j1728_automorphism(curve: Curve, point: tuple[int, int], root: int) -> tuple[int, int]:
    """Evaluate the CM automorphism [i](x,y)=(-x, i*y)."""
    image = ((-point[0]) % curve.p, root * point[1] % curve.p)
    if not curve.contains(image):
        raise ArithmeticError("the j=1728 automorphism left the curve")
    return image


def subgroup_log(curve: Curve, generator: tuple[int, int], target: tuple[int, int], r: int) -> int:
    """Solve a toy subgroup log exhaustively for invariant validation."""
    for scalar in range(r):
        if curve.scalar_mul(scalar, generator) == target:
            return scalar
    raise ArithmeticError("target is not in the stated subgroup")


def ray_class_order_qi(r: int, exponent: int = 1) -> int:
    """Return |Cl_{r**exponent O}(Q(i))| for odd unramified prime r."""
    if r == 2 or not is_prime(r) or exponent < 1:
        raise ValueError("r must be an odd prime and exponent must be positive")
    if r % 4 == 1:
        euler_factor = r ** (2 * (exponent - 1)) * (r - 1) ** 2
    else:
        euler_factor = r ** (2 * (exponent - 1)) * (r * r - 1)
    return euler_factor // 4


def r_adic_valuation(integer: int, r: int) -> int:
    """Return v_r(integer)."""
    valuation = 0
    while integer % r == 0:
        integer //= r
        valuation += 1
    return valuation


def gaussian_multiply(
    left: tuple[int, int], right: tuple[int, int], modulus: int
) -> tuple[int, int]:
    """Multiply Gaussian residue pairs modulo ``modulus``."""
    a, b = left
    c, d = right
    return (a * c - b * d) % modulus, (a * d + b * c) % modulus


def gaussian_power(base: tuple[int, int], exponent: int, modulus: int) -> tuple[int, int]:
    """Exponentiate a Gaussian residue pair."""
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = gaussian_multiply(result, base, modulus)
        base = gaussian_multiply(base, base, modulus)
        exponent >>= 1
    return result


def principal_unit_log(unit: tuple[int, int], r: int) -> tuple[int, int]:
    """Linearize 1+r*O modulo r**2 into the additive group O/r*O."""
    a, b = unit
    modulus = r * r
    a %= modulus
    b %= modulus
    if a % r != 1 or b % r != 0:
        raise ValueError("unit is not congruent to 1 modulo r")
    return ((a - 1) // r) % r, (b // r) % r


def level_lift_orbits(r: int) -> tuple[int, int, int]:
    """Count source reductions of principal and full unit orbits mod r**2.

    In the cyclic module Z/r**2, multiplication by r maps a level-r**2 lift
    to its order-r point.  Principal units preserve one fibre of this map;
    all units act transitively on the nonzero order-r generators.
    """
    if r == 2 or not is_prime(r):
        raise ValueError("r must be an odd prime")
    modulus = r * r
    principal_lifts = {(1 + r * scalar) % modulus for scalar in range(r)}
    principal_reductions = {r * lift % modulus for lift in principal_lifts}
    full_reductions = {
        r * unit % modulus
        for unit in range(1, modulus)
        if math.gcd(unit, modulus) == 1
    }
    return len(principal_lifts), len(principal_reductions), len(full_reductions)


def ring_class_number_upper_bound(q: int) -> float:
    """Explicit bound for an elliptic endomorphism order over F_q."""
    return (6 / math.pi) * math.sqrt(q) * (math.log(4 * q) + 2) ** 2


def size_obstruction_threshold_bits() -> int:
    """First k such that the bound is below q/2 for every q >= 2**k."""
    # sqrt(q)/(log(4q)+2)^2 is increasing for q >= 2, so checking powers of
    # two identifies a valid threshold for the whole final interval onward.
    for bits in range(1, 10_000):
        q = 2**bits
        if ring_class_number_upper_bound(q) < q / 2:
            return bits
    raise ArithmeticError("failed to locate the class-number threshold")


def probe_case(p: int) -> dict[str, object]:
    """Exhaust all natural labels on one ordinary j=1728 prime subgroup."""
    if p % 4 != 1 or not is_prime(p):
        raise ValueError("p must be prime and congruent to 1 modulo 4")
    curve = Curve(p, 1, 0)
    group_order = curve_order(curve)
    r = largest_prime_factor(group_order)
    if r <= 2 or group_order % (r * r) == 0:
        raise ValueError("the largest prime factor must occur exactly once")
    generator = find_point_of_order(curve, group_order, r)
    root = sqrt_minus_one(p)
    eigenvalue = subgroup_log(
        curve, generator, j1728_automorphism(curve, generator, root), r
    )

    annihilator_labels: set[tuple[tuple[int, int], ...]] = set()
    kernel_labels: set[tuple[tuple[int, int], ...]] = set()
    quotient_labels: set[tuple[int, int]] = set()
    eigenvalues: set[int] = set()
    for scalar in range(1, r):
        point = curve.scalar_mul(scalar, generator)
        if point is None:
            raise ArithmeticError("a nonzero scalar produced the identity")
        point_eigenvalue = subgroup_log(
            curve, point, j1728_automorphism(curve, point, root), r
        )
        eigenvalues.add(point_eigenvalue)
        annihilator_labels.add(
            tuple(sorted(((-b * point_eigenvalue) % r, b) for b in range(r)))
        )
        kernel_labels.add(tuple(sorted(kernel_points(curve, point, r))))
        quotient = canonical_curve(velu_quotient(curve, point, r))
        quotient_labels.add((quotient.a, quotient.b))

    if eigenvalues != {eigenvalue}:
        raise ArithmeticError("the CM eigenvalue changed on a nonzero multiple")
    if len(annihilator_labels) != 1 or len(kernel_labels) != 1 or len(quotient_labels) != 1:
        raise ArithmeticError("a supposedly unoriented label varied with the generator")

    trace = p + 1 - group_order
    frobenius_discriminant = trace * trace - 4 * p
    conductor_squared, remainder = divmod(abs(frobenius_discriminant), 4)
    conductor = math.isqrt(conductor_squared)
    if remainder or conductor * conductor != conductor_squared:
        raise ArithmeticError("the j=1728 Frobenius discriminant is not -4 f^2")
    quotient_a, quotient_b = next(iter(quotient_labels))
    ray_r = ray_class_order_qi(r)
    ray_r2 = ray_class_order_qi(r, 2)
    principal_generator = (1 + r, 0)
    principal_logs = {
        principal_unit_log(gaussian_power(principal_generator, scalar, r * r), r)
        for scalar in range(r)
    }
    if principal_logs != {(scalar, 0) for scalar in range(r)}:
        raise ArithmeticError("principal-unit linearization failed")
    level_lifts, principal_reductions, full_reductions = level_lift_orbits(r)
    if (level_lifts, principal_reductions, full_reductions) != (r, 1, r - 1):
        raise ArithmeticError("the level-lift orbit counts are inconsistent")
    return {
        "p": p,
        "group_order": group_order,
        "subgroup_order": r,
        "trace": trace,
        "frobenius_discriminant": frobenius_discriminant,
        "frobenius_conductor_in_Zi": conductor,
        "frobenius_order_class_number": class_number_from_reduced_forms(
            frobenius_discriminant
        ),
        "endomorphism_order_discriminant": -4,
        "endomorphism_order_class_number": class_number_from_reduced_forms(-4),
        "sqrt_minus_one_mod_p": root,
        "cm_eigenvalue_mod_r": eigenvalue,
        "nonzero_points_checked": r - 1,
        "distinct_cm_eigenvalues": len(eigenvalues),
        "distinct_annihilator_labels": len(annihilator_labels),
        "distinct_kernel_labels": len(kernel_labels),
        "distinct_velu_quotients": len(quotient_labels),
        "velu_quotient_a": quotient_a,
        "velu_quotient_b": quotient_b,
        "ray_mod_r_order": ray_r,
        "ray_mod_r_divisible_by_r": ray_r % r == 0,
        "ray_mod_r2_order": ray_r2,
        "ray_mod_r2_r_valuation": r_adic_valuation(ray_r2, r),
        "principal_unit_logs_checked": len(principal_logs),
        "level_r2_lifts_in_principal_orbit": level_lifts,
        "source_points_in_principal_orbit": principal_reductions,
        "nonzero_source_points_in_full_unit_orbit": full_reductions,
        "ring_class_bound": round(ring_class_number_upper_bound(p), 6),
        "bound_excludes_r_when_r_ge_q_over_2": ring_class_number_upper_bound(p) < p / 2,
    }


def run_experiment(smoke: bool) -> list[dict[str, object]]:
    primes = (13, 53) if smoke else (13, 53, 61, 109, 149, 269, 373, 421)
    return [probe_case(p) for p in primes]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    arguments = parser.parse_args()
    rows = run_experiment(arguments.smoke)
    output_dir = arguments.output_dir or Path(__file__).resolve().parents[1] / "data"
    profile = "smoke" if arguments.smoke else "full"
    path = output_dir / f"probe_cm_class_targets_{profile}_{date.today():%Y%m%d}.csv"
    write_csv(path, rows)
    print(f"class-number obstruction begins at q >= 2^{size_obstruction_threshold_bits()}")
    for row in rows:
        print(
            f"p={row['p']:>3} r={row['subgroup_order']:>3} "
            f"ann={row['distinct_annihilator_labels']} "
            f"kernels={row['distinct_kernel_labels']} "
            f"quotients={row['distinct_velu_quotients']} "
            f"r|Cl_r={row['ray_mod_r_divisible_by_r']} "
            f"v_r(Cl_r2)={row['ray_mod_r2_r_valuation']}"
        )


if __name__ == "__main__":
    main()
