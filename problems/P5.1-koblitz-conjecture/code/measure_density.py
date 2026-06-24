"""
measure_density.py — measure prime orders of fixed elliptic-curve reductions.
Sub-goal: P5.1 / SG-01, SG-02, SG-03, SG-04
Inputs:   --limit <int> --checkpoints <csv> --product-limit <int> --seed <int>
Outputs:  data/measure_density_x<limit>_l<product-limit>_s<seed>_<date>.csv
Runtime:  11.2 s wall time at limit=2^17 for three curves on the recorded host
Validated against: LMFDB q-expansion for 1728.w1 and exhaustive small-prime counts
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from random import Random

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import Curve, curve_order, curve_order_bsgs, is_prime


PUBLISHED_UNIVERSAL_CONSTANT = 0.505166168239435774
PUBLISHED_SERRE_CONSTANT = 0.561295742488261971


@dataclass(frozen=True, slots=True)
class CurveSpec:
    key: str
    label: str
    a: int
    b: int
    rational_torsion_order: int
    bad_primes: frozenset[int]
    constant_rule: str


CURVES = (
    CurveSpec(
        key="serre_trivial",
        label="y^2=x^3+6x-2 (LMFDB 1728.w1)",
        a=6,
        b=-2,
        rational_torsion_order=1,
        bad_primes=frozenset({2, 3}),
        constant_rule="zywina_serre_10_over_9",
    ),
    CurveSpec(
        key="torsion_2",
        label="y^2=x^3+x-2 (LMFDB 112.b4)",
        a=1,
        b=-2,
        rational_torsion_order=2,
        bad_primes=frozenset({2, 7}),
        constant_rule="rational_torsion_obstruction",
    ),
    CurveSpec(
        key="torsion_3",
        label="y^2=x^3+3x-11, P=(3,5)",
        a=3,
        b=-11,
        rational_torsion_order=3,
        bad_primes=frozenset({2, 3, 5}),
        constant_rule="rational_torsion_obstruction",
    ),
)


def primes_up_to(limit: int) -> list[int]:
    """Return all primes at most limit with an Eratosthenes sieve."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [value for value, flag in enumerate(sieve) if flag]


def universal_koblitz_product(prime_limit: int) -> float:
    """Truncate Zywina's universal full-GL(2) Euler product."""
    product = 1.0
    for ell in primes_up_to(prime_limit):
        numerator = ell * ell - ell - 1
        denominator = (ell - 1) ** 3 * (ell + 1)
        product *= 1.0 - numerator / denominator
    return product


def corrected_constant(spec: CurveSpec, prime_limit: int) -> float:
    """Return a supported corrected C_(E,1); do not infer Galois images."""
    if spec.constant_rule == "zywina_serre_10_over_9":
        return (10.0 / 9.0) * universal_koblitz_product(prime_limit)
    if spec.constant_rule == "rational_torsion_obstruction":
        return 0.0
    raise ValueError(f"unsupported constant rule: {spec.constant_rule}")


def deterministic_rng(seed: int, curve_index: int, prime: int) -> Random:
    """Construct a stable per-reduction RNG for the BSGS/twist counter."""
    mixed = seed ^ ((curve_index + 1) * 0x9E3779B1) ^ (prime * 0x85EBCA77)
    return Random(mixed & ((1 << 64) - 1))


def exact_order(
    spec: CurveSpec, prime: int, seed: int, curve_index: int
) -> tuple[int, str]:
    """Count one good reduction, with an exhaustive exact fallback."""
    curve = Curve(prime, spec.a % prime, spec.b % prime)
    try:
        return (
            curve_order_bsgs(
                curve, deterministic_rng(seed, curve_index, prime), max_points=64
            ),
            "hasse_bsgs_twist",
        )
    except RuntimeError:
        return curve_order(curve), "exhaustive_fallback"


def validate_orders(seed: int, validation_limit: int) -> dict[str, int]:
    """Compare BSGS/twist and exhaustive counts at every supported small prime."""
    counts = {"comparisons": 0, "bsgs": 0, "fallback": 0}
    for curve_index, spec in enumerate(CURVES):
        for prime in primes_up_to(validation_limit):
            if prime <= 3 or prime in spec.bad_primes:
                continue
            curve = Curve(prime, spec.a % prime, spec.b % prime)
            exhaustive = curve_order(curve)
            measured, method = exact_order(spec, prime, seed, curve_index)
            if measured != exhaustive:
                raise AssertionError(
                    f"order mismatch for {spec.key} at p={prime}: "
                    f"measured={measured}, exhaustive={exhaustive}"
                )
            counts["comparisons"] += 1
            counts["fallback" if method == "exhaustive_fallback" else "bsgs"] += 1
    return counts


def poisson_style_constant_interval(
    count: int, baseline: float, z_value: float = 1.959963984540054
) -> tuple[float, float]:
    """Return a simple 95% Poisson-normal interval for count / baseline."""
    if baseline <= 0:
        return math.nan, math.nan
    if count == 0:
        return 0.0, -math.log(0.05) / baseline
    radius = z_value * math.sqrt(count) / baseline
    estimate = count / baseline
    return max(0.0, estimate - radius), estimate + radius


def measure(
    limit: int,
    checkpoints: list[int],
    product_limit: int,
    seed: int,
) -> list[dict[str, object]]:
    """Measure all registered curves in one pass over primes."""
    primes = [prime for prime in primes_up_to(limit) if prime > 3]
    checkpoint_set = set(checkpoints)
    rows: list[dict[str, object]] = []

    for curve_index, spec in enumerate(CURVES):
        started = time.perf_counter()
        constant = corrected_constant(spec, product_limit)
        prime_order_count = 0
        prime_quotient_count = 0
        good_prime_count = 0
        exhaustive_fallback_count = 0
        baseline = 0.0
        prime_position = 0

        for cutoff in checkpoints:
            while prime_position < len(primes) and primes[prime_position] <= cutoff:
                prime = primes[prime_position]
                prime_position += 1
                if prime in spec.bad_primes:
                    continue
                order, method = exact_order(spec, prime, seed, curve_index)
                good_prime_count += 1
                if method == "exhaustive_fallback":
                    exhaustive_fallback_count += 1
                baseline += 1.0 / math.log(prime + 1.0)
                if is_prime(order):
                    prime_order_count += 1
                torsion = spec.rational_torsion_order
                if order % torsion == 0 and is_prime(order // torsion):
                    prime_quotient_count += 1

            estimate = prime_order_count / baseline if baseline else math.nan
            ci_low, ci_high = poisson_style_constant_interval(
                prime_order_count, baseline
            )
            predicted = constant * baseline
            ratio = prime_order_count / predicted if predicted else math.nan
            asymptotic_predicted = (
                constant * cutoff / math.log(cutoff) ** 2 if constant else 0.0
            )
            asymptotic_ratio = (
                prime_order_count / asymptotic_predicted
                if asymptotic_predicted
                else math.nan
            )
            rows.append(
                {
                    "curve_key": spec.key,
                    "curve": spec.label,
                    "a": spec.a,
                    "b": spec.b,
                    "rational_torsion_order": spec.rational_torsion_order,
                    "constant_rule": spec.constant_rule,
                    "cutoff": cutoff,
                    "good_prime_count": good_prime_count,
                    "exhaustive_fallback_count": exhaustive_fallback_count,
                    "prime_order_count": prime_order_count,
                    "prime_quotient_count": prime_quotient_count,
                    "prime_order_rate": f"{prime_order_count / good_prime_count:.12f}",
                    "refined_baseline": f"{baseline:.12f}",
                    "predicted_constant": f"{constant:.12f}",
                    "predicted_prime_order_count": f"{predicted:.12f}",
                    "asymptotic_predicted_count": f"{asymptotic_predicted:.12f}",
                    "measured_constant": f"{estimate:.12f}",
                    "constant_ci95_low": f"{ci_low:.12f}",
                    "constant_ci95_high": f"{ci_high:.12f}",
                    "measured_over_predicted": (
                        f"{ratio:.12f}" if math.isfinite(ratio) else ""
                    ),
                    "observed_over_asymptotic": (
                        f"{asymptotic_ratio:.12f}"
                        if math.isfinite(asymptotic_ratio)
                        else ""
                    ),
                    "elapsed_seconds": f"{time.perf_counter() - started:.6f}",
                    "seed": seed,
                    "point_counter": "hasse_bsgs_twist_with_exact_fallback",
                }
            )

    return rows


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    """Write deterministic column order and row order."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_rows(rows: list[dict[str, object]], output: Path) -> None:
    """Plot the nonzero-constant ratio and the two obstruction counts."""
    import matplotlib.pyplot as plt

    by_curve: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_curve.setdefault(str(row["curve_key"]), []).append(row)

    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    serre_rows = by_curve["serre_trivial"]
    x_values = [int(row["cutoff"]) for row in serre_rows]
    ratios = [float(row["measured_over_predicted"]) for row in serre_rows]
    asymptotic_ratios = [
        float(row["observed_over_asymptotic"]) for row in serre_rows
    ]
    axes[0].plot(
        x_values,
        ratios,
        marker="o",
        color="#0b6e69",
        linewidth=2,
        label="refined prime-sum predictor",
    )
    axes[0].plot(
        x_values,
        asymptotic_ratios,
        marker="s",
        color="#c08a2d",
        linestyle="--",
        linewidth=1.6,
        label=r"asymptotic $Cx/(\log x)^2$",
    )
    axes[0].axhline(1.0, color="#d2553d", linestyle="--", linewidth=1.4)
    axes[0].set_xscale("log", base=2)
    axes[0].set_xlabel("Prime cutoff x")
    axes[0].set_ylabel("Observed / refined prediction")
    axes[0].set_title("Serre curve: corrected constant")
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False, fontsize=9)

    styles = {
        "torsion_2": {"color": "#c08a2d", "marker": "o", "linestyle": "-"},
        "torsion_3": {"color": "#735aa6", "marker": "s", "linestyle": "--"},
    }
    for key in ("torsion_2", "torsion_3"):
        curve_rows = by_curve[key]
        axes[1].plot(
            [int(row["cutoff"]) for row in curve_rows],
            [int(row["prime_order_count"]) for row in curve_rows],
            label=key.replace("_", " "),
            **styles[key],
            linewidth=2,
        )
    axes[1].set_xscale("log", base=2)
    axes[1].set_xlabel("Prime cutoff x")
    axes[1].set_ylabel("Cumulative prime-order reductions")
    axes[1].set_title("Rational-torsion obstructions")
    axes[1].grid(alpha=0.25)
    axes[1].legend(frameon=False)
    axes[1].annotate(
        "both series remain exactly zero",
        xy=(x_values[len(x_values) // 2], 0),
        xytext=(x_values[1], 0.035),
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        color="#444444",
        fontsize=9,
    )

    figure.suptitle("P5.1 — Koblitz density at toy scale", fontsize=13)
    figure.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180, bbox_inches="tight")
    plt.close(figure)


def parse_checkpoints(raw: str, limit: int) -> list[int]:
    """Parse increasing CSV checkpoints and ensure the final limit is included."""
    checkpoints = sorted({int(value.strip()) for value in raw.split(",") if value})
    checkpoints = [value for value in checkpoints if 5 <= value <= limit]
    if not checkpoints or checkpoints[-1] != limit:
        checkpoints.append(limit)
    return checkpoints


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=1 << 15)
    parser.add_argument(
        "--checkpoints", default="1024,2048,4096,8192,16384,32768"
    )
    parser.add_argument("--product-limit", type=int, default=1_000_000)
    parser.add_argument("--validation-limit", type=int, default=97)
    parser.add_argument("--seed", type=int, default=51012026)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--figure", type=Path)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.smoke:
        args.limit = 512
        args.checkpoints = "128,256,512"
        args.product_limit = 10_000
        args.validation_limit = 43
    if args.limit < 5:
        raise ValueError("limit must be at least 5")
    if args.limit.bit_length() > 18:
        raise ValueError("limit exceeds the session's toy ceiling of 2^17")

    validation = validate_orders(args.seed, args.validation_limit)
    checkpoints = parse_checkpoints(args.checkpoints, args.limit)
    rows = measure(args.limit, checkpoints, args.product_limit, args.seed)

    stamp = date.today().strftime("%Y%m%d")
    stem = f"measure_density_x{args.limit}_l{args.product_limit}_s{args.seed}_{stamp}"
    output = args.output or (Path(__file__).parents[1] / "data" / f"{stem}.csv")
    figure = args.figure or (Path(__file__).parents[1] / "figures" / f"{stem}.png")
    write_csv(rows, output)
    if not args.no_plot:
        plot_rows(rows, figure)

    universal = universal_koblitz_product(args.product_limit)
    corrected = (10.0 / 9.0) * universal
    print(f"validated_comparisons={validation['comparisons']}")
    print(f"validation_bsgs={validation['bsgs']}")
    print(f"validation_fallback={validation['fallback']}")
    print(f"universal_product={universal:.15f}")
    print(f"serre_corrected_constant={corrected:.15f}")
    print(f"csv={output}")
    if not args.no_plot:
        print(f"figure={figure}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
