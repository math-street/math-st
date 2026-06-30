"""
verify_toy_action.py — exhaustively verify a toy CSIDH isogeny action.
Sub-goal: P3.2 / SG-01
Inputs:   --p <prime> --degrees <comma-separated primes> --smoke
Outputs:  data/verify_toy_action_p<P>_<YYYYMMDD>.json
Runtime:  under 2 seconds at p=419 on the recorded Python 3.13 environment
Validated against: h(-4)=1, h(-20)=2, h(-23)=3 and Vélu map invariants
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.curves import Curve, curve_order, is_prime
from lib.isogeny import (
    class_number_from_reduced_forms,
    compose_permutations,
    enumerate_rational_isogeny_orbit,
    generated_permutation_group,
    reduced_positive_forms,
    transition_permutations,
)


def pairwise_commute(permutations: tuple[tuple[int, ...], ...]) -> bool:
    """Return whether all supplied permutations commute."""
    return all(
        compose_permutations(left, right) == compose_permutations(right, left)
        for left in permutations
        for right in permutations
    )


def build_report(p: int, degrees: tuple[int, ...]) -> dict[str, object]:
    """Build a complete exhaustive verification report."""
    if not is_prime(p) or p % 4 != 3:
        raise ValueError("p must be prime and congruent to 3 modulo 4")
    if any((p + 1) % degree for degree in degrees):
        raise ValueError("every degree must divide p + 1")

    start = Curve(p, 1, 0)
    expected_order = p + 1
    actual_order = curve_order(start)
    if actual_order != expected_order:
        raise ArithmeticError("the starting curve does not have trace zero")

    discriminant = -4 * p
    forms = reduced_positive_forms(discriminant)
    class_number = class_number_from_reduced_forms(discriminant)
    states, transitions = enumerate_rational_isogeny_orbit(
        start,
        degrees,
        expected_order,
        verify_orders=True,
    )
    permutations = transition_permutations(transitions)
    action_group = generated_permutation_group(permutations)
    images_of_base = {element[0] for element in action_group}
    base_stabilizer = [element for element in action_group if element[0] == 0]
    transitive = len(images_of_base) == len(states)
    free = len(base_stabilizer) == 1

    return {
        "schema_version": 1,
        "p": p,
        "field_bits": p.bit_length(),
        "discriminant": discriminant,
        "degrees": list(degrees),
        "curve_order": actual_order,
        "class_number": class_number,
        "reduced_forms": [list(form) for form in forms],
        "orbit_size": len(states),
        "action_group_order": len(action_group),
        "generators_commute": pairwise_commute(permutations),
        "transitive": transitive,
        "free": free,
        "regular": transitive and free,
        "matches_class_number": len(states) == class_number,
        "states": [[curve.a, curve.b] for curve in states],
        "transitions": [list(row) for row in transitions],
        "generator_permutations": [list(permutation) for permutation in permutations],
    }


def parse_degrees(value: str) -> tuple[int, ...]:
    """Parse a nonempty comma-separated tuple of odd primes."""
    degrees = tuple(int(part) for part in value.split(",") if part)
    if not degrees or any(degree < 3 or not is_prime(degree) for degree in degrees):
        raise argparse.ArgumentTypeError("degrees must be a comma-separated list of odd primes")
    return degrees


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=419)
    parser.add_argument("--degrees", type=parse_degrees, default=(3, 5, 7))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    p = 59 if args.smoke else args.p
    degrees = (3, 5) if args.smoke else args.degrees
    report = build_report(p, degrees)
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"verify_toy_action_p{p}_{date.today():%Y%m%d}.json"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in (
        "p",
        "class_number",
        "orbit_size",
        "action_group_order",
        "generators_commute",
        "transitive",
        "free",
        "regular",
        "matches_class_number",
    )}, sort_keys=True))
    print(output)


if __name__ == "__main__":
    main()
