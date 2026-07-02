"""
measure_norm_smoothness.py - compare exTNFS tower norms with matched random integers.
Sub-goal: P4.3 / SG-04
Inputs:   --p <prime> --trials <int> --seed <int> [--a-bound <int>] [--bounds <csv>]
Outputs:  data/measure_norm_smoothness_<params>_<date>_{raw,summary}.csv
Runtime:  ~0.6 s at p=5, A=4, 5,856 exhaustive primitive pairs on Python 3.13.
Validated against: hand-computed nested norms and exact trial-division factorizations.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from datetime import date
from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import Iterable


QuadraticElement = tuple[int, int]


@dataclass(frozen=True)
class Instance:
    p: int = 5
    h_constant: int = 2
    f_constant: int = 1
    g_constant: int = -4


INSTANCE = Instance()


def quadratic_add(*values: QuadraticElement) -> QuadraticElement:
    return sum(value[0] for value in values), sum(value[1] for value in values)


def quadratic_scale(scalar: int, value: QuadraticElement) -> QuadraticElement:
    return scalar * value[0], scalar * value[1]


def quadratic_mul(left: QuadraticElement, right: QuadraticElement) -> QuadraticElement:
    """Multiply in Z[iota] with iota^2 = -2."""
    a, b = left
    c, d = right
    return a * c - 2 * b * d, a * d + b * c


def quadratic_norm(value: QuadraticElement) -> int:
    a, b = value
    return a * a + 2 * b * b


def tower_norm(a: QuadraticElement, b: QuadraticElement, constant: int) -> int:
    """Compute |Res_t(Res_x(a-b*x, x^3+x+constant), t^2+2)|."""
    a_cubed = quadratic_mul(quadratic_mul(a, a), a)
    a_b_squared = quadratic_mul(a, quadratic_mul(b, b))
    b_cubed = quadratic_mul(quadratic_mul(b, b), b)
    relative_norm = quadratic_add(
        a_cubed,
        a_b_squared,
        quadratic_scale(constant, b_cubed),
    )
    return quadratic_norm(relative_norm)


def validate_instance(instance: Instance = INSTANCE) -> None:
    if instance != INSTANCE:
        raise ValueError("Only the validated p=5 toy instance is implemented")

    # h=t^2+2 has no root in F_5; a cubic is irreducible iff it has no root.
    if any((r * r + instance.h_constant) % instance.p == 0 for r in range(instance.p)):
        raise AssertionError("h is reducible modulo p")
    if any((r**3 + r + instance.f_constant) % instance.p == 0 for r in range(instance.p)):
        raise AssertionError("the common cubic is reducible modulo p")
    if (instance.f_constant - instance.g_constant) % instance.p != 0:
        raise AssertionError("f and g do not have the same reduction modulo p")


@lru_cache(maxsize=None)
def factor_integer(value: int) -> tuple[tuple[int, int], ...]:
    """Return the complete prime factorization of a nonzero integer."""
    n = abs(value)
    if n == 0:
        raise ValueError("zero has no prime factorization")
    factors: list[tuple[int, int]] = []
    for prime in (2,):
        exponent = 0
        while n % prime == 0:
            n //= prime
            exponent += 1
        if exponent:
            factors.append((prime, exponent))
    divisor = 3
    while divisor * divisor <= n:
        exponent = 0
        while n % divisor == 0:
            n //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def largest_prime_factor(factors: tuple[tuple[int, int], ...]) -> int:
    return factors[-1][0] if factors else 1


def format_factorization(factors: tuple[tuple[int, int], ...]) -> str:
    if not factors:
        return "1"
    return "*".join(f"{prime}^{exponent}" for prime, exponent in factors)


def is_primitive(coefficients: tuple[int, int, int, int]) -> bool:
    return math.gcd(*(abs(value) for value in coefficients)) == 1


def candidate_coefficients(a_bound: int) -> list[tuple[int, int, int, int]]:
    values = range(-a_bound, a_bound + 1)
    return [coefficients for coefficients in product(values, repeat=4) if is_primitive(coefficients)]


def matched_random_integer(value: int, rng: random.Random) -> int:
    """Sample uniformly from the dyadic interval containing value."""
    n = abs(value)
    if n <= 1:
        return 1
    lower = 1 << (n.bit_length() - 1)
    upper = (lower << 1) - 1
    return rng.randint(lower, upper)


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return math.nan, math.nan
    rate = successes / total
    denominator = 1.0 + z * z / total
    centre = (rate + z * z / (2.0 * total)) / denominator
    radius = z * math.sqrt(rate * (1.0 - rate) / total + z * z / (4.0 * total * total)) / denominator
    return centre - radius, centre + radius


def choose_candidates(
    population: list[tuple[int, int, int, int]], trials: int, seed: int
) -> tuple[list[tuple[int, int, int, int]], bool]:
    if trials <= 0 or trials >= len(population):
        return population, True
    selection_rng = random.Random(seed)
    selected_indices = sorted(selection_rng.sample(range(len(population)), trials))
    return [population[index] for index in selected_indices], False


def write_raw(
    path: Path,
    rows: Iterable[dict[str, object]],
    bounds: list[int],
) -> None:
    fixed_fields = [
        "candidate_id",
        "a0",
        "a1",
        "b0",
        "b1",
        "norm_f",
        "factorization_f",
        "largest_prime_f",
        "norm_g",
        "factorization_g",
        "largest_prime_g",
        "baseline_f",
        "baseline_factorization_f",
        "baseline_largest_prime_f",
        "baseline_g",
        "baseline_factorization_g",
        "baseline_largest_prime_g",
    ]
    smooth_fields = [f"{source}_{side}_B{bound}" for bound in bounds for source in ("actual", "baseline") for side in ("f", "g", "joint")]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fixed_fields + smooth_fields)
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(
    *,
    a_bound: int,
    bounds: list[int],
    trials: int,
    seed: int,
    output_dir: Path,
    instance: Instance = INSTANCE,
) -> tuple[Path, Path, int]:
    validate_instance(instance)
    population = candidate_coefficients(a_bound)
    candidates, exhaustive = choose_candidates(population, trials, seed)
    baseline_rng = random.Random(seed ^ 0x5EED43)

    raw_rows: list[dict[str, object]] = []
    counts: dict[tuple[str, str, int], int] = {}

    for candidate_id, coefficients in enumerate(candidates):
        a0, a1, b0, b1 = coefficients
        a = (a0, a1)
        b = (b0, b1)
        norm_f = tower_norm(a, b, instance.f_constant)
        norm_g = tower_norm(a, b, instance.g_constant)
        factors_f = factor_integer(norm_f)
        factors_g = factor_integer(norm_g)
        baseline_f = matched_random_integer(norm_f, baseline_rng)
        baseline_g = matched_random_integer(norm_g, baseline_rng)
        baseline_factors_f = factor_integer(baseline_f)
        baseline_factors_g = factor_integer(baseline_g)
        largest = {
            ("actual", "f"): largest_prime_factor(factors_f),
            ("actual", "g"): largest_prime_factor(factors_g),
            ("baseline", "f"): largest_prime_factor(baseline_factors_f),
            ("baseline", "g"): largest_prime_factor(baseline_factors_g),
        }
        row: dict[str, object] = {
            "candidate_id": candidate_id,
            "a0": a0,
            "a1": a1,
            "b0": b0,
            "b1": b1,
            "norm_f": norm_f,
            "factorization_f": format_factorization(factors_f),
            "largest_prime_f": largest[("actual", "f")],
            "norm_g": norm_g,
            "factorization_g": format_factorization(factors_g),
            "largest_prime_g": largest[("actual", "g")],
            "baseline_f": baseline_f,
            "baseline_factorization_f": format_factorization(baseline_factors_f),
            "baseline_largest_prime_f": largest[("baseline", "f")],
            "baseline_g": baseline_g,
            "baseline_factorization_g": format_factorization(baseline_factors_g),
            "baseline_largest_prime_g": largest[("baseline", "g")],
        }
        for bound in bounds:
            for source in ("actual", "baseline"):
                f_smooth = largest[(source, "f")] <= bound
                g_smooth = largest[(source, "g")] <= bound
                flags = {"f": f_smooth, "g": g_smooth, "joint": f_smooth and g_smooth}
                for metric, flag in flags.items():
                    row[f"{source}_{metric}_B{bound}"] = int(flag)
                    counts[(source, metric, bound)] = counts.get((source, metric, bound), 0) + int(flag)
        raw_rows.append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    mode = "all" if exhaustive else f"t{len(candidates)}"
    bound_label = "-".join(str(bound) for bound in bounds)
    stem = f"measure_norm_smoothness_p{instance.p}_A{a_bound}_B{bound_label}_{mode}_s{seed}_{date.today():%Y%m%d}"
    raw_path = output_dir / f"{stem}_raw.csv"
    summary_path = output_dir / f"{stem}_summary.csv"
    write_raw(raw_path, raw_rows, bounds)

    total = len(candidates)
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        fields = [
            "p",
            "a_bound",
            "bound",
            "source",
            "metric",
            "successes",
            "total",
            "rate",
            "ci_low",
            "ci_high",
            "ci_method",
            "baseline_rate",
            "difference_vs_baseline",
            "rate_ratio_vs_baseline",
            "dependence_ratio",
            "exhaustive_actual_box",
            "seed",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for bound in bounds:
            rates = {
                (source, metric): counts[(source, metric, bound)] / total
                for source in ("actual", "baseline")
                for metric in ("f", "g", "joint")
            }
            for source in ("actual", "baseline"):
                dependence_denominator = rates[(source, "f")] * rates[(source, "g")]
                dependence_ratio = rates[(source, "joint")] / dependence_denominator if dependence_denominator else math.nan
                for metric in ("f", "g", "joint"):
                    successes = counts[(source, metric, bound)]
                    rate = rates[(source, metric)]
                    if source == "actual" and exhaustive:
                        ci_low, ci_high, ci_method = rate, rate, "population_exact"
                    else:
                        ci_low, ci_high = wilson_interval(successes, total)
                        ci_method = "wilson_95"
                    baseline_rate = rates[("baseline", metric)]
                    writer.writerow(
                        {
                            "p": instance.p,
                            "a_bound": a_bound,
                            "bound": bound,
                            "source": source,
                            "metric": metric,
                            "successes": successes,
                            "total": total,
                            "rate": f"{rate:.12g}",
                            "ci_low": f"{ci_low:.12g}",
                            "ci_high": f"{ci_high:.12g}",
                            "ci_method": ci_method,
                            "baseline_rate": f"{baseline_rate:.12g}",
                            "difference_vs_baseline": f"{rate - baseline_rate:.12g}",
                            "rate_ratio_vs_baseline": f"{rate / baseline_rate:.12g}" if baseline_rate else "nan",
                            "dependence_ratio": f"{dependence_ratio:.12g}" if metric == "joint" else "",
                            "exhaustive_actual_box": int(exhaustive),
                            "seed": seed,
                        }
                    )
    return raw_path, summary_path, total


def parse_bounds(value: str) -> list[int]:
    bounds = sorted({int(item) for item in value.split(",")})
    if not bounds or bounds[0] < 2:
        raise argparse.ArgumentTypeError("bounds must be comma-separated integers at least 2")
    return bounds


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=5, help="validated toy characteristic (only 5 is supported)")
    parser.add_argument("--a-bound", type=int, default=4, help="coefficient box radius A")
    parser.add_argument("--bounds", type=parse_bounds, default=parse_bounds("7,13,31,61"), help="smoothness bounds")
    parser.add_argument("--trials", type=int, default=0, help="0 enumerates the whole primitive box")
    parser.add_argument("--seed", type=int, default=4304, help="selection and independent-baseline seed")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--smoke", action="store_true", help="use A=2 and bounds 7,13")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.p != INSTANCE.p:
        raise ValueError("only the validated p=5 exTNFS instance is implemented")
    if args.a_bound < 1:
        raise ValueError("a-bound must be positive")
    if args.trials < 0:
        raise ValueError("trials must be nonnegative")
    a_bound = 2 if args.smoke else args.a_bound
    bounds = [7, 13] if args.smoke else args.bounds
    raw_path, summary_path, total = run_experiment(
        a_bound=a_bound,
        bounds=bounds,
        trials=args.trials,
        seed=args.seed,
        output_dir=args.output_dir,
    )
    print(f"candidates={total}")
    print(f"raw={raw_path}")
    print(f"summary={summary_path}")


if __name__ == "__main__":
    main()
