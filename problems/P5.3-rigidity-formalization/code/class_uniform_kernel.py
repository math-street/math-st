"""
class_uniform_kernel.py — exact toy isomorphism-class audit and unranking
Sub-goal: P5.3 / SG-10
Inputs:   --bits <int> --beacon <text> --sample <int> --output-prefix <path>
          --smoke (fixed bits=5 quick profile)
Outputs:  <prefix>.json and <prefix>.csv
Runtime:  <4 s for bits=7, <1 s for --smoke; restricted to bits <= 8
Validated against: exhaustive scaling orbits and the existing safety evaluator
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from datetime import date
from fractions import Fraction
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from sample_rigid_curve import (
    Curve,
    SafetyProfile,
    default_profile,
    evaluate_safety,
    find_point_of_order,
    prime_below_power_of_two,
    square_root_multiplicities,
)


@dataclass(frozen=True, slots=True)
class SafeCurveClass:
    rank: int
    p: int
    a: int
    b: int
    orbit_size: int
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


def scaling_orbit(p: int, a: int, b: int) -> frozenset[tuple[int, int]]:
    """Return the short-Weierstrass F_p scaling orbit of (a,b)."""
    return frozenset(
        (a * pow(u, 4, p) % p, b * pow(u, 6, p) % p)
        for u in range(1, p)
    )


def isomorphism_class_key(p: int, a: int, b: int) -> tuple[int, int]:
    """Return the lexicographically least pair in the scaling orbit."""
    return min(scaling_orbit(p, a, b))


@lru_cache(maxsize=None)
def coefficient_class_sizes(p: int) -> tuple[tuple[tuple[int, int], int], ...]:
    """Exhaustively return canonical nonsingular class keys and orbit sizes."""
    if not 5 <= p <= 251:
        raise ValueError("class enumeration is restricted to toy primes in [5, 251]")
    counts: dict[tuple[int, int], int] = {}
    for a in range(p):
        for b in range(p):
            try:
                Curve(p, a, b)
            except ValueError:
                continue
            key = isomorphism_class_key(p, a, b)
            counts[key] = counts.get(key, 0) + 1
    return tuple(sorted(counts.items()))


@lru_cache(maxsize=None)
def enumerate_safe_classes(
    bits: int, profile: SafetyProfile | None = None
) -> tuple[SafeCurveClass, ...]:
    """Enumerate canonical safe curve classes for an exhaustive toy profile."""
    if not 5 <= bits <= 8:
        raise ValueError("class-uniform enumeration is restricted to bits in [5, 8]")
    p = prime_below_power_of_two(bits, residue_mod_4=3)
    roots = square_root_multiplicities(p)
    if profile is None:
        profile = default_profile(bits)
    pending: list[tuple[tuple[int, int], int, tuple[int, ...]]] = []
    for key, orbit_size in coefficient_class_sizes(p):
        safety = evaluate_safety(Curve(p, *key), roots, profile)
        if safety is not None:
            pending.append((key, orbit_size, safety))

    rows: list[SafeCurveClass] = []
    for rank, (key, orbit_size, safety) in enumerate(pending):
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
        curve = Curve(p, *key)
        base_x, base_y = find_point_of_order(curve, order, subgroup_order)
        rows.append(
            SafeCurveClass(
                rank=rank,
                p=p,
                a=key[0],
                b=key[1],
                orbit_size=orbit_size,
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
        )
    if not rows:
        raise RuntimeError("the fixed toy profile has no safe classes")
    return tuple(rows)


def _rank_xof_input(
    beacon: str, sample: int, component: str, retry: int
) -> bytes:
    fields = (
        b"P5.3/toy-class-uniform/v1",
        beacon.encode("utf-8"),
        str(sample).encode("ascii"),
        component.encode("ascii"),
        str(retry).encode("ascii"),
    )
    return b"".join(len(field).to_bytes(4, "big") + field for field in fields)


def sample_uniform_rank(
    bound: int, beacon: str, sample: int, component: str = "safe-class-rank"
) -> int:
    """Map an ideal-XOF stream exactly uniformly into range(bound)."""
    if bound <= 0:
        raise ValueError("bound must be positive")
    width = max(1, (bound.bit_length() + 7) // 8)
    modulus = 1 << (8 * width)
    limit = modulus - modulus % bound
    retry = 0
    while True:
        encoded = _rank_xof_input(beacon, sample, component, retry)
        value = int.from_bytes(hashlib.shake_256(encoded).digest(width), "big")
        if value < limit:
            return value % bound
        retry += 1


def unrank_safe_class(
    classes: tuple[SafeCurveClass, ...], rank: int
) -> SafeCurveClass:
    """Return the canonical class at a checked public rank."""
    if not 0 <= rank < len(classes):
        raise IndexError("safe-class rank out of range")
    return classes[rank]


def choose_safe_class(
    bits: int, beacon: str, sample: int = 0
) -> SafeCurveClass:
    """Choose one canonical safe class by exact XOF rejection."""
    classes = enumerate_safe_classes(bits)
    rank = sample_uniform_rank(len(classes), beacon, sample)
    return unrank_safe_class(classes, rank)


def _histogram(values: list[int]) -> dict[str, int]:
    return {
        str(value): values.count(value)
        for value in sorted(set(values))
    }


def audit_summary(bits: int) -> dict[str, object]:
    """Return exact counts and induced class-mass diagnostics."""
    p = prime_below_power_of_two(bits, residue_mod_4=3)
    all_sizes = [size for _key, size in coefficient_class_sizes(p)]
    classes = enumerate_safe_classes(bits)
    safe_sizes = [row.orbit_size for row in classes]
    safe_encodings = sum(safe_sizes)
    class_uniform_mass = Fraction(1, len(classes))
    coefficient_masses = [
        Fraction(size, safe_encodings) for size in safe_sizes
    ]
    total_variation = sum(
        abs(mass - class_uniform_mass) for mass in coefficient_masses
    ) / 2
    return {
        "bits": bits,
        "p": p,
        "nonsingular_encodings": sum(all_sizes),
        "all_classes": len(all_sizes),
        "all_orbit_histogram": _histogram(all_sizes),
        "safe_encodings": safe_encodings,
        "safe_classes": len(classes),
        "safe_orbit_histogram": _histogram(safe_sizes),
        "coefficient_kernel_min_class_mass": str(min(coefficient_masses)),
        "coefficient_kernel_max_class_mass": str(max(coefficient_masses)),
        "class_uniform_mass": str(class_uniform_mass),
        "total_variation_from_class_uniform": str(total_variation),
    }


def write_audit(
    classes: tuple[SafeCurveClass, ...],
    summary: dict[str, object],
    prefix: Path,
) -> None:
    """Write deterministic JSON summary and canonical-class CSV."""
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    csv_path = prefix.with_suffix(".csv")
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(asdict(classes[0]).keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in classes:
            writer.writerow(asdict(row))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=7)
    parser.add_argument("--beacon", default="public-beacon")
    parser.add_argument("--sample", type=int, default=0)
    parser.add_argument("--output-prefix", type=Path)
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="override --bits with the fixed bits=5 quick profile",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    bits = 5 if args.smoke else args.bits
    classes = enumerate_safe_classes(bits)
    summary = audit_summary(bits)
    prefix = args.output_prefix
    if prefix is None:
        prefix = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"class_kernel_b{bits}_{date.today():%Y%m%d}"
        )
    write_audit(classes, summary, prefix)
    chosen = choose_safe_class(bits, args.beacon, args.sample)
    print(f"summary={prefix.with_suffix('.json')}")
    print(f"classes={prefix.with_suffix('.csv')}")
    print(
        f"safe_classes={len(classes)} safe_encodings={summary['safe_encodings']} "
        f"chosen_rank={chosen.rank} chosen=({chosen.a},{chosen.b})"
    )


if __name__ == "__main__":
    main()
