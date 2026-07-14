"""analyze_lift_relations - exact bounded-relation audit of measured lifts.

Sub-goal: P1.6 / SG-08
Inputs:   --groups-csv <path> --points-csv <path> --bound <int> --bits <list>
Outputs:  data/analyze_lift_relations_<params>_20260714_{rows,summary}.csv
Runtime:  ~76 s for 144 rows at bound eight; exact arithmetic is time-capped per row.
Validated against: known relations among multiples on 37.a1 and an independent
                   generator pair on 389.a1.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from fractions import Fraction
from itertools import groupby, product
from pathlib import Path
import sys
from time import perf_counter
from typing import Callable, Hashable, Sequence, TypeVar

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve  # noqa: E402
from lib.heights import RationalPoint, WeierstrassCurveQ  # noqa: E402
from measure_height_growth import fraction_mod, write_csv  # noqa: E402

DATE_STAMP = "20260714"
PointT = TypeVar("PointT", bound=Hashable)


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def linear_combination(
    coefficients: Sequence[int],
    multiples: Sequence[dict[int, PointT]],
    add: Callable[[PointT, PointT], PointT],
    identity: PointT,
) -> PointT:
    result = identity
    for coefficient, point_multiples in zip(coefficients, multiples, strict=True):
        result = add(result, point_multiples[coefficient])
    return result


def bounded_relation(
    points: Sequence[PointT],
    *,
    add: Callable[[PointT, PointT], PointT],
    neg: Callable[[PointT], PointT],
    scalar_mul: Callable[[int, PointT], PointT],
    identity: PointT,
    bound: int,
    deadline: float | None = None,
) -> tuple[int, tuple[int, ...]] | None:
    """Return a minimum-L-infinity nonzero relation, or None through bound.

    A meet-in-the-middle search is exact. If several witnesses have the same
    minimum bound, the lexicographically earliest encountered one is returned.
    """
    if not points:
        raise ValueError("at least one point is required")
    if bound < 1:
        raise ValueError("bound must be positive")
    max_multiples: list[dict[int, PointT]] = []
    for point in points:
        max_multiples.append(
            {coefficient: scalar_mul(coefficient, point) for coefficient in range(-bound, bound + 1)}
        )

    split = len(points) // 2
    if split == 0:
        split = 1
    for current_bound in range(1, bound + 1):
        if deadline is not None and perf_counter() > deadline:
            raise TimeoutError("bounded relation search exceeded its deadline")
        values = range(-current_bound, current_bound + 1)
        left_multiples = max_multiples[:split]
        right_multiples = max_multiples[split:]
        left_sums: dict[PointT, tuple[int, ...]] = {}
        for left_coefficients in product(values, repeat=split):
            point_sum = linear_combination(left_coefficients, left_multiples, add, identity)
            previous = left_sums.get(point_sum)
            if previous is None or (not any(previous) and any(left_coefficients)):
                left_sums[point_sum] = left_coefficients
        right_products = product(values, repeat=len(points) - split)
        for right_coefficients in right_products:
            right_sum = linear_combination(right_coefficients, right_multiples, add, identity)
            left_coefficients = left_sums.get(neg(right_sum))
            if left_coefficients is None:
                continue
            witness = left_coefficients + right_coefficients
            if not any(witness):
                continue
            if max(abs(value) for value in witness) != current_bound:
                continue
            if linear_combination(witness, max_multiples, add, identity) != identity:
                raise AssertionError("relation witness failed exact re-evaluation")
            return current_bound, witness
    return None


def rational_neg(curve: WeierstrassCurveQ, point: RationalPoint) -> RationalPoint:
    if point is None:
        return None
    x, y = point
    return x, -y - curve.a1 * x - curve.a3


def relation_text(result: tuple[int, tuple[int, ...]] | None) -> str:
    return "" if result is None else ";".join(str(value) for value in result[1])


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def analyze(
    groups: Sequence[dict[str, str]],
    points: Sequence[dict[str, str]],
    *,
    bits_values: set[int],
    bound: int,
    row_timeout_seconds: float,
) -> list[dict[str, object]]:
    points_by_curve: dict[str, list[dict[str, str]]] = defaultdict(list)
    for point in points:
        points_by_curve[point["curve_id"]].append(point)
    for curve_points in points_by_curve.values():
        curve_points.sort(key=lambda row: int(row["point_index"]))

    output: list[dict[str, object]] = []
    selected_groups = [
        row
        for row in groups
        if row["family"] == "random_general" and int(row["bits"]) in bits_values
    ]
    for index, group in enumerate(selected_groups, start=1):
        p = int(group["p"])
        coefficient_values = [
            parse_fraction(text)
            for text in points_by_curve[group["curve_id"]][0]["coefficients_a1_a2_a3_a4_a6"].split(";")
        ]
        rational_curve = WeierstrassCurveQ.from_coefficients(coefficient_values)
        rational_points = [
            (parse_fraction(row["x"]), parse_fraction(row["y"]))
            for row in points_by_curve[group["curve_id"]]
        ]
        finite_a = fraction_mod(rational_curve.a4, p)
        finite_b = fraction_mod(rational_curve.a6, p)
        finite_curve = Curve(p, finite_a, finite_b)
        finite_points: list[AffinePoint] = [
            (fraction_mod(point[0], p), fraction_mod(point[1], p))
            for point in rational_points
        ]

        finite_start = perf_counter()
        finite_result = bounded_relation(
            finite_points,
            add=finite_curve.add,
            neg=finite_curve.neg,
            scalar_mul=finite_curve.scalar_mul,
            identity=None,
            bound=bound,
        )
        finite_runtime = perf_counter() - finite_start

        rational_result: tuple[int, tuple[int, ...]] | None = None
        rational_status = "skipped-no-finite-relation"
        rational_runtime = 0.0
        if finite_result is not None:
            rational_start = perf_counter()
            try:
                rational_result = bounded_relation(
                    rational_points,
                    add=rational_curve.add,
                    neg=lambda point: rational_neg(rational_curve, point),
                    scalar_mul=rational_curve.scalar_mul,
                    identity=None,
                    bound=bound,
                    deadline=rational_start + row_timeout_seconds,
                )
                rational_status = "relation" if rational_result is not None else "no-relation-through-bound"
            except TimeoutError:
                rational_status = "censored-timeout"
            rational_runtime = perf_counter() - rational_start

        output.append(
            {
                "curve_id": group["curve_id"],
                "p": p,
                "bits": int(group["bits"]),
                "trial": int(group["trial"]),
                "k": int(group["k"]),
                "variant": int(group["variant"]),
                "variant_kind": "least-norm" if int(group["variant"]) == 0 else "nullspace-offset",
                "bound": bound,
                "finite_relation_found": int(finite_result is not None),
                "finite_min_linf": "" if finite_result is None else finite_result[0],
                "finite_relation": relation_text(finite_result),
                "finite_runtime_ms": 1000 * finite_runtime,
                "rational_status": rational_status,
                "rational_relation_found": int(rational_result is not None),
                "rational_min_linf": "" if rational_result is None else rational_result[0],
                "rational_relation": relation_text(rational_result),
                "rational_runtime_ms": 1000 * rational_runtime,
                "max_canonical_height": group["max_canonical_height"],
                "curve_coefficient_log_height": group["curve_coefficient_log_height"],
                "discriminant_log_height": group["discriminant_log_height"],
            }
        )
        if index % 25 == 0:
            print(f"analyzed {index}/{len(selected_groups)} curves", flush=True)
    return output


def _mean_or_blank(values: Sequence[float]) -> float | str:
    return "" if not values else sum(values) / len(values)


def summarize(rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    expanded = list(rows)
    for row in rows:
        all_copy = dict(row)
        all_copy["variant_kind"] = "all"
        expanded.append(all_copy)
    ordered = sorted(
        expanded,
        key=lambda row: (str(row["variant_kind"]), int(row["k"]), int(row["bits"])),
    )
    output: list[dict[str, object]] = []
    for (variant_kind, k, bits), items_iter in groupby(
        ordered,
        key=lambda row: (str(row["variant_kind"]), int(row["k"]), int(row["bits"])),
    ):
        items = list(items_iter)
        finite_count = sum(int(row["finite_relation_found"]) for row in items)
        rational_count = sum(int(row["rational_relation_found"]) for row in items)
        censored = sum(row["rational_status"] == "censored-timeout" for row in items)
        rational_related = [
            float(row["max_canonical_height"])
            for row in items
            if int(row["rational_relation_found"])
        ]
        rational_unrelated = [
            float(row["max_canonical_height"])
            for row in items
            if row["rational_status"] in {"no-relation-through-bound", "skipped-no-finite-relation"}
        ]
        finite_related_heights = [
            float(row["max_canonical_height"])
            for row in items
            if int(row["finite_relation_found"])
        ]
        finite_unrelated_heights = [
            float(row["max_canonical_height"])
            for row in items
            if not int(row["finite_relation_found"])
        ]
        finite_related_discriminants = [
            float(row["discriminant_log_height"])
            for row in items
            if int(row["finite_relation_found"])
        ]
        finite_unrelated_discriminants = [
            float(row["discriminant_log_height"])
            for row in items
            if not int(row["finite_relation_found"])
        ]
        rational_related_discriminants = [
            float(row["discriminant_log_height"])
            for row in items
            if int(row["rational_relation_found"])
        ]
        output.append(
            {
                "variant_kind": variant_kind,
                "k": k,
                "bits": bits,
                "p": items[0]["p"],
                "n": len(items),
                "finite_relation_count": finite_count,
                "finite_relation_rate": finite_count / len(items),
                "rational_relation_count": rational_count,
                "rational_relation_rate": rational_count / len(items),
                "rational_censored_count": censored,
                "mean_height_rational_relation": _mean_or_blank(rational_related),
                "mean_height_no_rational_relation": _mean_or_blank(rational_unrelated),
                "mean_discriminant_rational_relation": _mean_or_blank(
                    rational_related_discriminants
                ),
                "mean_height_finite_relation": _mean_or_blank(finite_related_heights),
                "mean_height_no_finite_relation": _mean_or_blank(finite_unrelated_heights),
                "mean_discriminant_finite_relation": _mean_or_blank(
                    finite_related_discriminants
                ),
                "mean_discriminant_no_finite_relation": _mean_or_blank(
                    finite_unrelated_discriminants
                ),
                "mean_discriminant_log_height": sum(
                    float(row["discriminant_log_height"]) for row in items
                )
                / len(items),
            }
        )
    return output


def parse_args() -> argparse.Namespace:
    data_dir = Path(__file__).resolve().parents[1] / "data"
    tag = "b5-7-9-11-13-15_t3_v3_i5_s16062026_20260703"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--groups-csv",
        type=Path,
        default=data_dir / f"measure_height_growth_{tag}_groups.csv",
    )
    parser.add_argument(
        "--points-csv",
        type=Path,
        default=data_dir / f"measure_height_growth_{tag}_points.csv",
    )
    parser.add_argument("--bits", default="5,7,9,11")
    parser.add_argument("--bound", type=int, default=8)
    parser.add_argument("--row-timeout", type=float, default=60.0)
    parser.add_argument("--output-dir", type=Path, default=data_dir)
    parser.add_argument("--summary-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bits_values = {int(value) for value in args.bits.split(",")}
    bits_tag = "-".join(str(value) for value in sorted(bits_values))
    tag = f"b{bits_tag}_B{args.bound}_allv_{DATE_STAMP}"
    rows_path = args.output_dir / f"analyze_lift_relations_{tag}_rows.csv"
    summary_path = args.output_dir / f"analyze_lift_relations_{tag}_summary.csv"
    if args.summary_only:
        rows = load_csv(rows_path)
    else:
        rows = analyze(
            load_csv(args.groups_csv),
            load_csv(args.points_csv),
            bits_values=bits_values,
            bound=args.bound,
            row_timeout_seconds=args.row_timeout,
        )
        write_csv(rows_path, rows)
        print(f"wrote {len(rows)} rows to {rows_path}")
    summary_rows = summarize(rows)
    write_csv(summary_path, summary_rows)
    print(f"wrote {len(summary_rows)} rows to {summary_path}")


if __name__ == "__main__":
    main()
