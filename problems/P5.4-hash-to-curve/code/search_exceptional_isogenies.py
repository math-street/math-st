"""
search_exceptional_isogenies.py - Exhaust toy odd-degree exceptional targets.
Sub-goals: P5.4 / SG-03a and SG-04a
Inputs:   --bound <exclusive prime bound> --seed <int> [--smoke] [--output]
Outputs:  data/search_exceptional_isogenies_<params>_<date>.csv
Runtime:  a few seconds for --bound 100 on Python 3.13
Method:   every nonsingular AB != 0 curve, every rational 3/5-subgroup
"""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path
from time import perf_counter

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve, is_prime
from lib.isogeny import kernel_points, velu_quotient


def _rational_subgroups(
    curve: Curve,
    points: tuple[tuple[int, int], ...],
    degree: int,
) -> list[tuple[int, int]]:
    """Return one deterministic generator for each rational subgroup."""
    seen: set[tuple[tuple[int, int], ...]] = set()
    generators: list[tuple[int, int]] = []
    for point in points:
        if curve.scalar_mul(degree, point) is not None:
            continue
        kernel = tuple(sorted(kernel_points(curve, point, degree)))
        if kernel not in seen:
            seen.add(kernel)
            generators.append(point)
    return generators


def search(bound: int, seed: int) -> tuple[list[dict[str, int | str]], dict[str, int]]:
    """Exhaust all requested toy curves and return exceptional-target hits."""
    rows: list[dict[str, int | str]] = []
    counters = {"primes": 0, "curves": 0, "kernels": 0}
    for p in range(5, bound):
        if not is_prime(p):
            continue
        counters["primes"] += 1
        for a in range(1, p):
            for b in range(1, p):
                try:
                    curve = Curve(p, a, b)
                except ValueError:
                    continue
                counters["curves"] += 1
                points = tuple(curve.affine_points())
                group_order = len(points) + 1
                for degree in (3, 5):
                    if group_order % degree:
                        continue
                    for generator in _rational_subgroups(curve, points, degree):
                        counters["kernels"] += 1
                        quotient = velu_quotient(curve, generator, degree)
                        if quotient.a != 0 and quotient.b != 0:
                            continue
                        family = "j0" if quotient.a == 0 else "j1728"
                        rows.append(
                            {
                                "seed": seed,
                                "p": p,
                                "source_a": a,
                                "source_b": b,
                                "source_order": group_order,
                                "degree": degree,
                                "kernel_x": generator[0],
                                "kernel_y": generator[1],
                                "target_a": quotient.a,
                                "target_b": quotient.b,
                                "target_family": family,
                                "target_order": len(tuple(quotient.affine_points())) + 1,
                            }
                        )
    return rows, counters


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bound", type=int, default=100)
    parser.add_argument("--seed", type=int, default=5404)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bound = 20 if args.smoke else args.bound
    started = perf_counter()
    rows, counters = search(bound, args.seed)
    elapsed = perf_counter() - started
    if not rows:
        raise RuntimeError("search found no exceptional-invariant targets")

    output = args.output
    if output is None:
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / f"search_exceptional_isogenies_b{bound}_{date.today():%Y%m%d}.csv"
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    families = {str(row["target_family"]) for row in rows}
    print(f"wrote {len(rows)} rows to {output}")
    print(f"families={','.join(sorted(families))}")
    print(
        f"primes={counters['primes']} curves={counters['curves']} "
        f"kernels={counters['kernels']} elapsed_seconds={elapsed:.6f}"
    )


if __name__ == "__main__":
    main()
