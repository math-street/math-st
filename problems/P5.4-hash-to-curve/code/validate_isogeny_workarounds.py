"""
validate_isogeny_workarounds.py - Validate fixed SSWU-to-exceptional isogenies.
Sub-goals: P5.4 / SG-03a, SG-04a, and SG-05a
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_isogeny_workarounds_<params>_<date>.csv
Runtime:  under 1 second on Python 3.13
Checks:   exhaustive map inputs, fixed schedules, all group-law pairs
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import AffinePoint, Curve, map_to_curve_simple_swu
from lib.isogeny import (
    kernel_points,
    velu_map,
    velu_map_affine_nonkernel,
    velu_quotient,
)


@dataclass(frozen=True, slots=True)
class IsogenyFixture:
    family: str
    source: Curve
    z: int
    degree: int
    kernel_generator: tuple[int, int]
    target: Curve


FIXTURES = (
    IsogenyFixture("j0", Curve(29, 4, 11), 10, 3, (15, 16), Curve(29, 0, 9)),
    IsogenyFixture(
        "j1728", Curve(59, 2, 13), 18, 3, (41, 35), Curve(59, 56, 0)
    ),
)


def map_via_isogeny(
    fixture: IsogenyFixture,
    u: int,
    *,
    trace: list[str] | None = None,
) -> tuple[int, int]:
    """Apply SSWU on E' and the fixed affine nonkernel Velu map to E."""
    source_point = map_to_curve_simple_swu(
        fixture.source,
        u,
        fixture.z,
        trace=trace,
    )
    return velu_map_affine_nonkernel(
        fixture.source,
        source_point,
        fixture.kernel_generator,
        fixture.degree,
        trace=trace,
    )


def _validate_fixture(
    fixture: IsogenyFixture,
    seed: int,
) -> dict[str, int | str]:
    quotient = velu_quotient(
        fixture.source,
        fixture.kernel_generator,
        fixture.degree,
    )
    if quotient != fixture.target:
        raise AssertionError(f"unexpected quotient {quotient} != {fixture.target}")

    source_points: tuple[AffinePoint, ...] = (None, *fixture.source.affine_points())
    target_points: tuple[AffinePoint, ...] = (None, *fixture.target.affine_points())
    public_kernel = set(
        kernel_points(
            fixture.source,
            fixture.kernel_generator,
            fixture.degree,
        )
    )
    images: dict[AffinePoint, AffinePoint] = {}
    for point in source_points:
        image = velu_map(
            fixture.source,
            point,
            fixture.kernel_generator,
            fixture.degree,
        )
        if not fixture.target.contains(image):
            raise AssertionError(f"off-target Velu image {point} -> {image}")
        images[point] = image
    actual_kernel = {point for point, image in images.items() if image is None}
    if actual_kernel != {None, *public_kernel}:
        raise AssertionError("Velu map kernel differs from the declared kernel")
    for left in source_points:
        for right in source_points:
            lhs = images[fixture.source.add(left, right)]
            rhs = fixture.target.add(images[left], images[right])
            if lhs != rhs:
                raise AssertionError(f"homomorphism failure at {left}, {right}")

    schedules: set[tuple[str, ...]] = set()
    mapped_points: set[tuple[int, int]] = set()
    for u in range(fixture.source.p):
        source_point = map_to_curve_simple_swu(
            fixture.source,
            u,
            fixture.z,
        )
        if source_point in public_kernel:
            raise AssertionError(f"SSWU hit the isogeny kernel at u={u}")
        trace: list[str] = []
        target_point = map_via_isogeny(fixture, u, trace=trace)
        expected = images[source_point]
        if target_point != expected or not fixture.target.contains(target_point):
            raise AssertionError(f"isogeny workaround failed at u={u}")
        schedules.add(tuple(trace))
        mapped_points.add(target_point)

    if len(target_points) != len(source_points):
        raise AssertionError("isogenous toy curves have different point counts")
    return {
        "family": fixture.family,
        "seed": seed,
        "p": fixture.source.p,
        "source_curve": f"a={fixture.source.a};b={fixture.source.b}",
        "z": fixture.z,
        "degree": fixture.degree,
        "kernel": f"x={fixture.kernel_generator[0]};y={fixture.kernel_generator[1]}",
        "target_curve": f"a={fixture.target.a};b={fixture.target.b}",
        "source_order": len(source_points),
        "target_order": len(target_points),
        "map_inputs": fixture.source.p,
        "nonidentity_outputs": fixture.source.p,
        "distinct_outputs": len(mapped_points),
        "homomorphism_pairs": len(source_points) ** 2,
        "schedule_variants": len(schedules),
        "schedule_operations": len(next(iter(schedules))),
    }


def validate(seed: int, smoke: bool = False) -> list[dict[str, int | str]]:
    """Validate one or both fixed exceptional-invariant workarounds."""
    fixtures = FIXTURES[:1] if smoke else FIXTURES
    return [_validate_fixture(fixture, seed) for fixture in fixtures]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5405)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = perf_counter()
    rows = validate(args.seed, smoke=args.smoke)
    elapsed = perf_counter() - started

    label = "smoke" if args.smoke else "full"
    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"validate_isogeny_workarounds_{label}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {output}")
    print(f"validated {sum(int(row['map_inputs']) for row in rows)} map inputs")
    print(f"elapsed_seconds={elapsed:.6f}")


if __name__ == "__main__":
    main()
