"""measure_height_growth - construct simultaneous lifts and measure heights.

Sub-goal: P1.6 / SG-02--SG-06
Inputs:   --bits <comma-list> --trials <int> --variants <int> --seed <int>
Outputs:  data/measure_height_growth_<params>_20260703_{points,groups,summary,fits,residuals}.csv
Runtime:  ~40 s for the default matrix on Python 3.13; --smoke is under 2 s.
Validated against: LMFDB 37.a1 and 389.a1 canonical generator heights; see
                   lib/tests/test_heights.py.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from fractions import Fraction
from itertools import groupby
from math import exp, log, sqrt
from pathlib import Path
from random import Random
import sys
from typing import Iterable, Sequence

import numpy as np
from sympy import Matrix
from scipy.stats import t as student_t

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import Curve, prime_below_power_of_two  # noqa: E402
from lib.heights import (  # noqa: E402
    RationalPoint,
    WeierstrassCurveQ,
    rational_log_height,
)

DATE_STAMP = "20260703"


def balanced(value: int, p: int) -> int:
    """Return the representative in [-(p-1)/2, (p-1)/2]."""
    value %= p
    return value - p if value > p // 2 else value


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def fraction_mod(value: Fraction, p: int) -> int:
    denominator = value.denominator % p
    if denominator == 0:
        raise ValueError("rational number is not p-integral")
    return value.numerator * pow(denominator, -1, p) % p


def matrix_rank_mod_p(rows: Sequence[Sequence[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in rows]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(entry * inverse) % p for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % p
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def point_row(point: tuple[int, int]) -> list[int]:
    x, y = point
    return [x * y, -x * x, y, -x, -1]


def sample_curve_and_points(p: int, rng: Random, count: int = 4) -> tuple[Curve, list[tuple[int, int]]]:
    """Sample a nonsingular short curve and points with usable lift equations."""
    for _ in range(10_000):
        try:
            curve = Curve(p, rng.randrange(p), rng.randrange(p))
        except ValueError:
            continue
        points: list[tuple[int, int]] = []
        attempts = 0
        while len(points) < count and attempts < 20_000:
            attempts += 1
            x_mod = rng.randrange(p)
            candidates = curve.points_for_x(x_mod)
            if not candidates:
                continue
            chosen = candidates[rng.randrange(len(candidates))]
            assert chosen is not None
            point = balanced(chosen[0], p), balanced(chosen[1], p)
            if point in points:
                continue
            proposed = points + [point]
            if matrix_rank_mod_p([point_row(item) for item in proposed], p) != len(proposed):
                continue
            points.append(point)
        if len(points) == count:
            return curve, points
    raise RuntimeError("failed to sample a full-rank point set")


def _sympy_fraction(value: object) -> Fraction:
    numerator, denominator = value.as_numer_denom()  # type: ignore[attr-defined]
    return Fraction(int(numerator), int(denominator))


def lift_solution_space(
    p: int, a_mod: int, b_mod: int, points: Sequence[tuple[int, int]]
) -> tuple[list[Fraction], list[list[Fraction]]]:
    """Return the least-Euclidean-norm coefficient correction and a nullspace basis."""
    a0 = balanced(a_mod, p)
    b0 = balanced(b_mod, p)
    rows = [point_row(point) for point in points]
    right = [(x**3 + a0 * x + b0 - y * y) // p for x, y in points]
    matrix = Matrix(rows)
    rhs = Matrix(right)
    gram = matrix * matrix.T
    if gram.det() == 0:
        raise ValueError("lift constraint rows are not independent over Q")
    particular_matrix = matrix.T * gram.inv() * rhs
    particular = [_sympy_fraction(value) for value in particular_matrix]
    nullspace = [
        [_sympy_fraction(value) for value in vector]
        for vector in matrix.nullspace()
    ]
    if any(value.denominator % p == 0 for value in particular):
        raise ValueError("least-norm solution is not p-integral")
    if any(value.denominator % p == 0 for vector in nullspace for value in vector):
        raise ValueError("nullspace basis is not p-integral")
    return particular, nullspace


def corrected_curve(
    p: int,
    a_mod: int,
    b_mod: int,
    particular: Sequence[Fraction],
    nullspace: Sequence[Sequence[Fraction]],
    parameters: Sequence[int],
) -> WeierstrassCurveQ:
    if len(parameters) != len(nullspace):
        raise ValueError("one parameter is required per nullspace vector")
    correction = list(particular)
    for parameter, vector in zip(parameters, nullspace, strict=True):
        correction = [
            left + parameter * right
            for left, right in zip(correction, vector, strict=True)
        ]
    base = [Fraction(0), Fraction(0), Fraction(0), Fraction(balanced(a_mod, p)), Fraction(balanced(b_mod, p))]
    coefficients = [
        value + p * delta for value, delta in zip(base, correction, strict=True)
    ]
    return WeierstrassCurveQ.from_coefficients(coefficients)


def direct_short_lift(
    p: int, a_mod: int, point: tuple[int, int]
) -> WeierstrassCurveQ:
    x, y = point
    coefficient_a = balanced(a_mod, p)
    coefficient_b = y * y - x**3 - coefficient_a * x
    return WeierstrassCurveQ.from_coefficients([0, 0, 0, coefficient_a, coefficient_b])


def validate_reduction(
    curve: WeierstrassCurveQ,
    points: Sequence[RationalPoint],
    p: int,
    expected_a: int,
    expected_b: int,
    expected_coefficients: Sequence[int] | None = None,
) -> None:
    coefficients = [curve.a1, curve.a2, curve.a3, curve.a4, curve.a6]
    reduced_coefficients = [fraction_mod(value, p) for value in coefficients]
    expected = (
        [0, 0, 0, expected_a % p, expected_b % p]
        if expected_coefficients is None
        else [value % p for value in expected_coefficients]
    )
    if reduced_coefficients != expected:
        raise AssertionError("lifted curve has the wrong reduction")
    if curve.discriminant == 0 or fraction_mod(curve.discriminant, p) == 0:
        raise AssertionError("lifted curve does not have good reduction")
    a1, a2, a3, a4, a6 = expected
    for point in points:
        if point is None or not curve.contains(point):
            raise AssertionError("invalid rational lift point")
        x, y = point
        reduction = fraction_mod(x, p), fraction_mod(y, p)
        x_mod, y_mod = reduction
        if (
            y_mod * y_mod + a1 * x_mod * y_mod + a3 * y_mod
            - x_mod**3 - a2 * x_mod * x_mod - a4 * x_mod - a6
        ) % p != 0:
            raise AssertionError("point reduction is not on the target curve")


def curve_coefficient_log_height(curve: WeierstrassCurveQ) -> float:
    return max(
        rational_log_height(value)
        for value in (curve.a1, curve.a2, curve.a3, curve.a4, curve.a6)
    )


def measure_group(
    *,
    family: str,
    curve_id: str,
    curve: WeierstrassCurveQ,
    points: Sequence[RationalPoint],
    p: int,
    bits: int,
    trial: int,
    k: int,
    variant: int,
    seed: int,
    iterations: int,
    rank_status: str,
    known_rank: int | None,
    exact_heights: Sequence[float] | None = None,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    point_records: list[dict[str, object]] = []
    heights: list[float] = []
    deltas: list[float] = []
    coefficient_text = ";".join(
        fraction_text(value) for value in (curve.a1, curve.a2, curve.a3, curve.a4, curve.a6)
    )
    for index, point in enumerate(points, start=1):
        assert point is not None
        if exact_heights is None:
            estimate = curve.canonical_height_estimate(point, iterations=iterations)
            height = estimate.value
            previous = estimate.previous
            delta = estimate.delta
            method = f"doubling-limit-n{iterations}"
        else:
            height = exact_heights[index - 1]
            previous = height
            delta = 0.0
            method = "exact-torsion"
        heights.append(height)
        deltas.append(0.0 if delta is None else delta)
        point_records.append(
            {
                "family": family,
                "curve_id": curve_id,
                "p": p,
                "bits": bits,
                "trial": trial,
                "k": k,
                "variant": variant,
                "point_index": index,
                "seed": seed,
                "coefficients_a1_a2_a3_a4_a6": coefficient_text,
                "x": fraction_text(point[0]),
                "y": fraction_text(point[1]),
                "naive_x_height": rational_log_height(point[0]),
                "canonical_height": height,
                "previous_estimate": previous,
                "convergence_delta": delta,
                "height_method": method,
                "rank_status": rank_status,
                "known_rank": "" if known_rank is None else known_rank,
            }
        )
    group = {
        "family": family,
        "curve_id": curve_id,
        "p": p,
        "bits": bits,
        "trial": trial,
        "k": k,
        "variant": variant,
        "seed": seed,
        "max_canonical_height": max(heights),
        "mean_canonical_height": sum(heights) / len(heights),
        "max_naive_x_height": max(rational_log_height(point[0]) for point in points if point is not None),
        "max_convergence_delta": max(deltas),
        "curve_coefficient_log_height": curve_coefficient_log_height(curve),
        "discriminant_log_height": rational_log_height(curve.discriminant),
        "rank_status": rank_status,
        "known_rank": "" if known_rank is None else known_rank,
    }
    return point_records, group


def construct_random_groups(
    p: int,
    bits: int,
    trial: int,
    rng: Random,
    seed: int,
    variants: int,
    radius: int,
    iterations: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    for _ in range(1_000):
        finite_curve, sampled_points = sample_curve_and_points(p, rng)
        try:
            spaces = [
                lift_solution_space(p, finite_curve.a, finite_curve.b, sampled_points[:k])
                for k in range(1, 5)
            ]
        except ValueError:
            continue
        break
    else:
        raise RuntimeError("could not obtain p-integral simultaneous-lift spaces")

    point_records: list[dict[str, object]] = []
    group_records: list[dict[str, object]] = []
    rational_points = [
        (Fraction(x), Fraction(y)) for x, y in sampled_points
    ]

    direct = direct_short_lift(p, finite_curve.a, sampled_points[0])
    validate_reduction(direct, rational_points[:1], p, finite_curve.a, finite_curve.b)
    rows, group = measure_group(
        family="random_short_single",
        curve_id=f"p{p}-t{trial}-direct",
        curve=direct,
        points=rational_points[:1],
        p=p,
        bits=bits,
        trial=trial,
        k=1,
        variant=0,
        seed=seed,
        iterations=iterations,
        rank_status="unavailable",
        known_rank=None,
    )
    point_records.extend(rows)
    group_records.append(group)

    for k, (particular, nullspace) in enumerate(spaces, start=1):
        parameter_sets = [[0] * len(nullspace)]
        for _ in range(1, variants):
            parameter_sets.append([rng.randint(-radius, radius) for _ in nullspace])
        for variant, parameters in enumerate(parameter_sets):
            lifted_curve = corrected_curve(
                p,
                finite_curve.a,
                finite_curve.b,
                particular,
                nullspace,
                parameters,
            )
            validate_reduction(
                lifted_curve,
                rational_points[:k],
                p,
                finite_curve.a,
                finite_curve.b,
            )
            rows, group = measure_group(
                family="random_general",
                curve_id=f"p{p}-t{trial}-k{k}-v{variant}",
                curve=lifted_curve,
                points=rational_points[:k],
                p=p,
                bits=bits,
                trial=trial,
                k=k,
                variant=variant,
                seed=seed,
                iterations=iterations,
                rank_status="total rank unavailable; lifted-point span rank unmeasured",
                known_rank=None,
            )
            point_records.extend(rows)
            group_records.append(group)
    return point_records, group_records


def control_groups(
    primes_and_bits: Sequence[tuple[int, int]], seed: int, iterations: int
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    controls = [
        (
            "fixed_rank1_37a1",
            WeierstrassCurveQ.from_coefficients([0, 0, 1, -1, 0]),
            (Fraction(0), Fraction(0)),
            1,
            "LMFDB 37.a1 rank 1",
            False,
        ),
        (
            "fixed_rank0_11a2_torsion",
            WeierstrassCurveQ.from_coefficients([0, -1, 1, -10, -20]),
            (Fraction(5), Fraction(5)),
            0,
            "LMFDB 11.a2 rank 0; base point has order 5",
            True,
        ),
    ]
    point_records: list[dict[str, object]] = []
    group_records: list[dict[str, object]] = []
    for family, curve, base_point, rank, rank_status, torsion in controls:
        multiples = [curve.scalar_mul(index, base_point) for index in range(1, 5)]
        if torsion and curve.scalar_mul(5, base_point) is not None:
            raise AssertionError("11.a2 control point did not have order five")
        for p, bits in primes_and_bits:
            if curve.discriminant.denominator % p == 0 or curve.discriminant.numerator % p == 0:
                continue
            reduced = [
                fraction_mod(value, p)
                for value in (curve.a1, curve.a2, curve.a3, curve.a4, curve.a6)
            ]
            validate_reduction(
                curve,
                multiples,
                p,
                reduced[3],
                reduced[4],
                expected_coefficients=reduced,
            )
            for k in range(1, 5):
                exact = [0.0] * k if torsion else None
                rows, group = measure_group(
                    family=family,
                    curve_id=family,
                    curve=curve,
                    points=multiples[:k],
                    p=p,
                    bits=bits,
                    trial=0,
                    k=k,
                    variant=0,
                    seed=seed,
                    iterations=iterations,
                    rank_status=rank_status,
                    known_rank=rank,
                    exact_heights=exact,
                )
                point_records.extend(rows)
                group_records.append(group)
    return point_records, group_records


def analysis_groups(group_records: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    buckets: dict[tuple[int, int, int], list[dict[str, object]]] = defaultdict(list)
    for row in group_records:
        family = str(row["family"])
        if family == "random_general":
            key = int(row["bits"]), int(row["trial"]), int(row["k"])
            buckets[key].append(row)
            if int(row["variant"]) == 0:
                copy = dict(row)
                copy["analysis_family"] = "random_general_min_norm"
                selected.append(copy)
        else:
            copy = dict(row)
            copy["analysis_family"] = family
            selected.append(copy)
    for rows in buckets.values():
        best = min(rows, key=lambda row: float(row["max_canonical_height"]))
        copy = dict(best)
        copy["analysis_family"] = "random_general_best_sampled"
        selected.append(copy)
    return selected


def summarize(rows: Sequence[dict[str, object]]) -> list[dict[str, object]]:
    ordered = sorted(
        rows,
        key=lambda row: (str(row["analysis_family"]), int(row["k"]), int(row["bits"])),
    )
    output: list[dict[str, object]] = []
    for key, items_iter in groupby(
        ordered,
        key=lambda row: (str(row["analysis_family"]), int(row["k"]), int(row["bits"])),
    ):
        items = list(items_iter)
        values = np.array([float(row["max_canonical_height"]) for row in items])
        family, k, bits = key
        output.append(
            {
                "analysis_family": family,
                "k": k,
                "bits": bits,
                "p": int(items[0]["p"]),
                "n": len(values),
                "mean_max_height": float(values.mean()),
                "median_max_height": float(np.median(values)),
                "q25_max_height": float(np.quantile(values, 0.25)),
                "q75_max_height": float(np.quantile(values, 0.75)),
                "min_max_height": float(values.min()),
                "max_max_height": float(values.max()),
                "rank_status": items[0]["rank_status"],
                "known_rank": items[0]["known_rank"],
            }
        )
    return output


def _ols(
    x_values: Sequence[float], y_values: Sequence[float]
) -> tuple[float, float, list[float], float, float, float, float, float]:
    x = np.asarray(x_values, dtype=float)
    y = np.asarray(y_values, dtype=float)
    design = np.column_stack([np.ones(len(x)), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    predicted = intercept + slope * x
    residuals = y - predicted
    squared_error = float(np.sum(residuals**2))
    rmse = float(sqrt(squared_error / len(y)))
    total = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1.0 - squared_error / total if total > 1e-24 else 1.0
    degrees_of_freedom = len(x) - 2
    centered_x = float(np.sum((x - x.mean()) ** 2))
    if degrees_of_freedom > 0 and centered_x > 0:
        slope_se = sqrt((squared_error / degrees_of_freedom) / centered_x)
        critical = float(student_t.ppf(0.975, degrees_of_freedom))
        ci_low = float(slope - critical * slope_se)
        ci_high = float(slope + critical * slope_se)
    else:
        slope_se = float("nan")
        ci_low = float("nan")
        ci_high = float("nan")
    return (
        float(intercept),
        float(slope),
        predicted.tolist(),
        rmse,
        r_squared,
        slope_se,
        ci_low,
        ci_high,
    )


def fit_models(
    rows: Sequence[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    ordered = sorted(rows, key=lambda row: (str(row["analysis_family"]), int(row["k"])))
    fits: list[dict[str, object]] = []
    residual_rows: list[dict[str, object]] = []
    for (family, k), items_iter in groupby(
        ordered, key=lambda row: (str(row["analysis_family"]), int(row["k"]))
    ):
        items = list(items_iter)
        if len({int(row["bits"]) for row in items}) < 3:
            continue
        models: list[tuple[str, list[dict[str, object]], str, str]] = [
            ("logarithmic", items, "ln(p)", "height"),
        ]
        positive_items = [row for row in items if float(row["max_canonical_height"]) > 0]
        if len({int(row["bits"]) for row in positive_items}) >= 3:
            models.append(("power", positive_items, "ln(p)", "ln(height)"))
        for model, model_items, x_name, y_name in models:
            x = [log(int(row["p"])) for row in model_items]
            heights = [float(row["max_canonical_height"]) for row in model_items]
            response = heights if model == "logarithmic" else [log(value) for value in heights]
            (
                intercept,
                slope,
                predicted,
                rmse,
                r_squared,
                slope_se,
                ci_low,
                ci_high,
            ) = _ols(x, response)
            height_predictions = predicted if model == "logarithmic" else [exp(value) for value in predicted]
            height_squared_error = sum(
                (observed - fitted) ** 2
                for observed, fitted in zip(heights, height_predictions, strict=True)
            )
            rmse_height = sqrt(height_squared_error / len(model_items))
            aic_height = len(model_items) * log(max(height_squared_error / len(model_items), 1e-300)) + 4
            fits.append(
                {
                    "analysis_family": family,
                    "k": k,
                    "model": model,
                    "n": len(model_items),
                    "p_min": min(int(row["p"]) for row in model_items),
                    "p_max": max(int(row["p"]) for row in model_items),
                    "x_variable": x_name,
                    "y_variable": y_name,
                    "intercept": intercept,
                    "slope": slope,
                    "slope_standard_error": slope_se,
                    "slope_ci95_low": ci_low,
                    "slope_ci95_high": ci_high,
                    "rmse_response_scale": rmse,
                    "rmse_height_scale": rmse_height,
                    "aic_height_scale": aic_height,
                    "r_squared": r_squared,
                }
            )
            for item, observed, fitted, height_fitted in zip(
                model_items, response, predicted, height_predictions, strict=True
            ):
                residual_rows.append(
                    {
                        "analysis_family": family,
                        "k": k,
                        "model": model,
                        "p": item["p"],
                        "bits": item["bits"],
                        "trial": item["trial"],
                        "observed_response": observed,
                        "predicted_response": fitted,
                        "residual_response": observed - fitted,
                        "observed_height": item["max_canonical_height"],
                        "predicted_height": height_fitted,
                    }
                )
    return fits, residual_rows


def write_csv(path: Path, rows: Sequence[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_figure(path: Path, summaries: Sequence[dict[str, object]]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    families = ["random_general_best_sampled", "fixed_rank1_37a1"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
    for axis, family in zip(axes, families, strict=True):
        selected = [row for row in summaries if row["analysis_family"] == family]
        for k in range(1, 5):
            rows = sorted((row for row in selected if int(row["k"]) == k), key=lambda row: int(row["p"]))
            if rows:
                axis.plot(
                    [log(int(row["p"])) for row in rows],
                    [float(row["median_max_height"]) for row in rows],
                    marker="o",
                    label=f"k={k}",
                )
        axis.set_title(family.replace("_", " "))
        axis.set_xlabel("ln p")
        axis.set_ylabel("median max canonical height")
        axis.grid(alpha=0.25)
        axis.legend()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170)
    plt.close(fig)


def run(
    *,
    bits_values: Sequence[int],
    trials: int,
    variants: int,
    radius: int,
    iterations: int,
    seed: int,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    if trials < 1 or variants < 1 or iterations < 1:
        raise ValueError("trials, variants, and iterations must be positive")
    rng = Random(seed)
    primes_and_bits = [
        (prime_below_power_of_two(bits, residue_mod_4=3), bits) for bits in bits_values
    ]
    point_records: list[dict[str, object]] = []
    group_records: list[dict[str, object]] = []
    for p, bits in primes_and_bits:
        for trial in range(trials):
            points, groups = construct_random_groups(
                p,
                bits,
                trial,
                rng,
                seed,
                variants,
                radius,
                iterations,
            )
            point_records.extend(points)
            group_records.extend(groups)
    control_points, control_group_rows = control_groups(primes_and_bits, seed, iterations)
    point_records.extend(control_points)
    group_records.extend(control_group_rows)
    analysis = analysis_groups(group_records)
    summaries = summarize(analysis)
    fits, residuals = fit_models(analysis)
    return point_records, group_records, summaries, fits, residuals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", default="5,7,9,11,13,15")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--variants", type=int, default=3)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--seed", type=int, default=16062026)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bits_values = [int(value) for value in args.bits.split(",")]
    if args.smoke:
        bits_values = [5, 7, 9]
        args.trials = 1
        args.variants = 1
        args.iterations = min(args.iterations, 3)
    outputs = run(
        bits_values=bits_values,
        trials=args.trials,
        variants=args.variants,
        radius=args.radius,
        iterations=args.iterations,
        seed=args.seed,
    )
    tag = (
        f"b{'-'.join(map(str, bits_values))}_t{args.trials}_v{args.variants}"
        f"_i{args.iterations}_s{args.seed}_{DATE_STAMP}"
    )
    names = ("points", "groups", "summary", "fits", "residuals")
    for name, rows in zip(names, outputs, strict=True):
        path = args.output_dir / f"measure_height_growth_{tag}_{name}.csv"
        write_csv(path, rows)
        print(f"wrote {len(rows)} rows to {path}")
    figure = args.output_dir.parent / "figures" / f"measure_height_growth_{tag}.png"
    write_figure(figure, outputs[2])
    print(f"wrote figure to {figure}")


if __name__ == "__main__":
    main()
