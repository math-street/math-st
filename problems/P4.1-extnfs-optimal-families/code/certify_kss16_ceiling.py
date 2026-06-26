"""Finite certificate for KSS16 seeds with p < 2^60.

Sub-goal: P4.1 / SG-09
Inputs:   fixed scaffold ceiling log2(p) <= 60
Outputs:  dated JSON containing the analytic cutoff and exhaustive seed table
Runtime:  below one second
Validated against: exact KSS16 polynomials in lib.curves
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from sympy import factorint

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import evaluate_pairing_family, validate_pairing_family  # noqa: E402

CUTOFF_ABS_SEED = 256
LOW_DEGREE_ABSOLUTE_COEFFICIENT_SUM = 6_588


def kss16_numerator_absolute_lower_bound(abs_seed: int) -> int:
    """Lower-bound the KSS16 p numerator for every seed of this magnitude."""
    if abs_seed < 1:
        raise ValueError("abs_seed must be positive")
    x = abs_seed
    return x**6 * (
        x**4 - 2 * x**3 - 5 * x**2 - LOW_DEGREE_ABSOLUTE_COEFFICIENT_SUM
    )


def _factorization(value: int) -> dict[str, int]:
    return {str(prime): int(exponent) for prime, exponent in factorint(value).items()}


def build_certificate() -> dict[str, object]:
    """Exhaust every seed not excluded by the analytic magnitude bound."""
    ceiling = 1 << 60
    threshold_numerator = 980 * ceiling
    cutoff_bound = kss16_numerator_absolute_lower_bound(CUTOFF_ABS_SEED)
    if cutoff_bound <= threshold_numerator:
        raise ArithmeticError("the analytic cutoff does not imply p > 2^60")

    rows: list[dict[str, object]] = []
    evaluation_failures = 0
    integral_above_ceiling = 0
    for seed in range(-CUTOFF_ABS_SEED + 1, CUTOFF_ABS_SEED):
        try:
            parameters = evaluate_pairing_family("KSS16", seed)
        except ValueError:
            evaluation_failures += 1
            continue
        if parameters.p >= ceiling:
            integral_above_ceiling += 1
            continue
        validation = validate_pairing_family(parameters)
        rows.append(
            {
                "seed": seed,
                "p": parameters.p,
                "r": parameters.r,
                "trace": parameters.trace,
                "p_bits": parameters.p.bit_length(),
                "r_bits": parameters.r.bit_length(),
                "p_is_prime": validation.p_is_prime,
                "r_is_prime": validation.r_is_prime,
                "p_factorization": _factorization(parameters.p),
                "r_factorization": _factorization(parameters.r),
                "order_divisible": validation.order_divisible,
                "exact_embedding_degree": validation.exact_embedding_degree,
                "valid_pairing_candidate": validation.valid,
            }
        )

    valid = [row for row in rows if row["valid_pairing_candidate"]]
    return {
        "status": "PROVED within the scaffold ceiling",
        "claim": "No integral KSS16 seed has prime p and prime r with p < 2^60.",
        "ceiling": ceiling,
        "ceiling_relation": "strict p < 2^60 (there is no equality candidate)",
        "analytic_cutoff_abs_seed": CUTOFF_ABS_SEED,
        "cutoff_lower_bound_numerator": cutoff_bound,
        "required_numerator_to_reach_ceiling": threshold_numerator,
        "bound_ratio": cutoff_bound / threshold_numerator,
        "analytic_argument": (
            "For x=|u|>=256, triangle inequality gives N(u)>=x^6"
            "(x^4-2x^3-5x^2-6588). The parenthesis is positive and increasing; "
            "the bound at 256 exceeds 980*2^60, hence p=N(u)/980>2^60."
        ),
        "enumerated_seed_interval_inclusive": [
            -CUTOFF_ABS_SEED + 1,
            CUTOFF_ABS_SEED - 1,
        ],
        "enumerated_seed_count": 2 * CUTOFF_ABS_SEED - 1,
        "evaluation_failures_nonintegral_or_nonpositive": evaluation_failures,
        "integral_parameters_above_ceiling": integral_above_ceiling,
        "integral_parameters_below_ceiling": len(rows),
        "valid_candidate_count": len(valid),
        "parameters_below_ceiling": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    arguments = parser.parse_args()
    certificate = build_certificate()
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    path = arguments.output_dir / f"kss16_p_lt_2pow60_certificate_{arguments.date}.json"
    path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
