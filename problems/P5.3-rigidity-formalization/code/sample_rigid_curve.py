"""
sample_rigid_curve.py — forced first-passing toy curve generator
Sub-goal: P5.3 / SG-08
Inputs:   --bits <int> --samples <int> --beacon <text> --max-counter <int>
Outputs:  data/sample_rigid_curve_b<bits>_n<samples>_<date>.csv
Runtime:  <10 s in --smoke mode; intended only for bits <= 16
Validated against: #E(F_5)=9 for y^2=x^3+x+1 and independent enumeration
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.curves import (  # noqa: E402
    Curve,
    curve_order,
    find_point_of_order,
    prime_below_power_of_two,
    square_root_multiplicities,
)


@dataclass(frozen=True, slots=True)
class SafetyProfile:
    min_subgroup_bits: int
    max_cofactor: int
    min_twist_subgroup_bits: int
    max_twist_cofactor: int
    min_embedding_degree: int
    min_frobenius_discriminant: int


@dataclass(frozen=True, slots=True)
class GeneratedCurve:
    sample: int
    beacon: str
    counter: int
    p: int
    a: int
    b: int
    order: int
    subgroup_order: int
    cofactor: int
    twist_order: int
    twist_subgroup_order: int
    twist_cofactor: int
    trace: int
    frobenius_discriminant: int
    base_x: int
    base_y: int


def _encode_xof_input(
    beacon: str, sample: int, counter: int, component: str, retry: int
) -> bytes:
    fields = (
        b"P5.3/toy-rigid-curve/v1",
        beacon.encode("utf-8"),
        str(sample).encode("ascii"),
        str(counter).encode("ascii"),
        component.encode("ascii"),
        str(retry).encode("ascii"),
    )
    return b"".join(len(field).to_bytes(4, "big") + field for field in fields)


def sample_field_element(
    p: int, beacon: str, sample: int, counter: int, component: str
) -> int:
    """Map an ideal-XOF stream exactly uniformly into F_p by rejection."""
    width = (p.bit_length() + 7) // 8
    modulus = 1 << (8 * width)
    limit = modulus - modulus % p
    retry = 0
    while True:
        encoded = _encode_xof_input(beacon, sample, counter, component, retry)
        value = int.from_bytes(hashlib.shake_256(encoded).digest(width), "big")
        if value < limit:
            return value % p
        retry += 1


def largest_prime_factor(value: int) -> int:
    """Return the largest prime factor of a positive toy-size integer."""
    if value < 2:
        return 1
    largest = 1
    factor = 2
    while factor * factor <= value:
        while value % factor == 0:
            largest = factor
            value //= factor
        factor = 3 if factor == 2 else factor + 2
    return max(largest, value)


def has_embedding_degree_below(p: int, subgroup_order: int, minimum: int) -> bool:
    """Return whether the embedding degree is strictly below minimum."""
    if subgroup_order <= 2 or p % subgroup_order == 0:
        return True
    residue = 1
    for _degree in range(1, minimum):
        residue = residue * p % subgroup_order
        if residue == 1:
            return True
    return False


def evaluate_safety(
    curve: Curve, roots: bytearray, profile: SafetyProfile
) -> tuple[int, int, int, int, int, int, int, int] | None:
    """Return public safety data, or None when the curve fails the profile."""
    order = curve_order(curve, roots)
    subgroup_order = largest_prime_factor(order)
    cofactor = order // subgroup_order
    twist_order = 2 * curve.p + 2 - order
    twist_subgroup_order = largest_prime_factor(twist_order)
    twist_cofactor = twist_order // twist_subgroup_order
    trace = curve.p + 1 - order
    discriminant = trace * trace - 4 * curve.p

    if trace in (0, 1):
        return None
    if subgroup_order.bit_length() < profile.min_subgroup_bits:
        return None
    if cofactor > profile.max_cofactor:
        return None
    if twist_subgroup_order.bit_length() < profile.min_twist_subgroup_bits:
        return None
    if twist_cofactor > profile.max_twist_cofactor:
        return None
    if has_embedding_degree_below(
        curve.p, subgroup_order, profile.min_embedding_degree
    ):
        return None
    if abs(discriminant) < profile.min_frobenius_discriminant:
        return None
    return (
        order,
        subgroup_order,
        cofactor,
        twist_order,
        twist_subgroup_order,
        twist_cofactor,
        trace,
        discriminant,
    )


def generate_curve(
    bits: int,
    beacon: str,
    sample: int,
    max_counter: int,
    profile: SafetyProfile,
) -> GeneratedCurve:
    """Return the first curve passing the fixed toy safety profile."""
    if not 5 <= bits <= 16:
        raise ValueError("bits must be in [5, 16] for exhaustive toy point counting")
    p = prime_below_power_of_two(bits, residue_mod_4=3)
    roots = square_root_multiplicities(p)
    for counter in range(max_counter):
        a = sample_field_element(p, beacon, sample, counter, "a")
        b = sample_field_element(p, beacon, sample, counter, "b")
        try:
            curve = Curve(p, a, b)
        except ValueError:
            continue
        safety = evaluate_safety(curve, roots, profile)
        if safety is None:
            continue
        (
            order,
            subgroup_order,
            cofactor,
            twist_order,
            twist_subgroup_order,
            twist_cofactor,
            trace,
            discriminant,
        ) = safety
        base_x, base_y = find_point_of_order(curve, order, subgroup_order)
        return GeneratedCurve(
            sample=sample,
            beacon=beacon,
            counter=counter,
            p=p,
            a=a,
            b=b,
            order=order,
            subgroup_order=subgroup_order,
            cofactor=cofactor,
            twist_order=twist_order,
            twist_subgroup_order=twist_subgroup_order,
            twist_cofactor=twist_cofactor,
            trace=trace,
            frobenius_discriminant=discriminant,
            base_x=base_x,
            base_y=base_y,
        )
    raise RuntimeError(f"no safe curve found within max_counter={max_counter}")


def default_profile(bits: int) -> SafetyProfile:
    """Return the version-one toy safety profile for the requested size."""
    return SafetyProfile(
        min_subgroup_bits=max(3, bits - 2),
        max_cofactor=8,
        min_twist_subgroup_bits=max(3, bits - 2),
        max_twist_cofactor=8,
        min_embedding_degree=4,
        min_frobenius_discriminant=16,
    )


def write_rows(rows: list[GeneratedCurve], output: Path) -> None:
    """Write deterministic CSV output."""
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys())
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=9)
    parser.add_argument("--samples", type=int, default=32)
    parser.add_argument("--beacon", default="public-beacon")
    parser.add_argument("--max-counter", type=int, default=10_000)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bits = 7 if args.smoke else args.bits
    samples = 8 if args.smoke else args.samples
    if samples <= 0:
        raise ValueError("samples must be positive")
    if args.max_counter <= 0:
        raise ValueError("max-counter must be positive")
    profile = default_profile(bits)
    rows = [
        generate_curve(bits, args.beacon, sample, args.max_counter, profile)
        for sample in range(samples)
    ]
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"sample_rigid_curve_b{bits}_n{samples}_{date.today():%Y%m%d}.csv"
        )
    write_rows(rows, output)
    max_seen = max(row.counter for row in rows)
    print(f"wrote={output}")
    print(f"samples={len(rows)} p={rows[0].p} max_counter_seen={max_seen}")


if __name__ == "__main__":
    main()
