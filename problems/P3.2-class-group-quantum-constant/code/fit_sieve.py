"""
fit_sieve.py — fit the simulated sieve's leading and lower-order terms.
Sub-goal: P3.2 / SG-03
Inputs:   --input <CSV> --bootstrap <int> --seed <int>
Outputs:  data/fit_sieve_n<MIN>-<MAX>_<YYYYMMDD>.json
Runtime:  under 2 seconds for 700 rows and 2000 bootstrap replicates
Validated against: exact recovery from synthetic noiseless log-cost data
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np


def design_matrix(log_n_values: np.ndarray) -> np.ndarray:
    """Return columns for sqrt(log N), log(log N), and the intercept."""
    if np.any(log_n_values <= 1.0):
        raise ValueError("all natural logarithms of N must exceed one")
    return np.column_stack(
        (np.sqrt(log_n_values), np.log(log_n_values), np.ones_like(log_n_values))
    )


def fit_parameters(log_n_values: np.ndarray, log_query_values: np.ndarray) -> np.ndarray:
    """Least-squares fit of log Q = c sqrt(log N) + d log log N + k."""
    if log_n_values.shape != log_query_values.shape:
        raise ValueError("predictor and response arrays must have equal shapes")
    parameters, _, _, _ = np.linalg.lstsq(
        design_matrix(log_n_values), log_query_values, rcond=None
    )
    return parameters


def regression_rmse(features: np.ndarray, response: np.ndarray) -> float:
    """Return in-sample least-squares RMSE for explicit feature columns."""
    design = np.column_stack((features, np.ones(len(response))))
    parameters, _, _, _ = np.linalg.lstsq(design, response, rcond=None)
    residuals = response - design @ parameters
    return float(np.sqrt(np.mean(residuals**2)))


def read_grouped(path: Path) -> dict[int, tuple[float, np.ndarray]]:
    """Read trial log-costs grouped by bit size."""
    grouped: dict[int, list[float]] = defaultdict(list)
    log_n_by_bits: dict[int, float] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            n_bits = int(row["n_bits"])
            grouped[n_bits].append(math.log(float(row["query_count"])))
            log_n_by_bits[n_bits] = float(row["log_natural_N"])
    return {
        n_bits: (log_n_by_bits[n_bits], np.asarray(values, dtype=float))
        for n_bits, values in sorted(grouped.items())
    }


def fit_report(
    grouped: dict[int, tuple[float, np.ndarray]],
    bootstrap: int,
    seed: int,
) -> dict[str, object]:
    """Fit geometric means and bootstrap trials within every size."""
    if len(grouped) < 5:
        raise ValueError("the fit requires at least five distinct sizes")
    if bootstrap < 1:
        raise ValueError("bootstrap must be positive")
    bits = np.asarray(list(grouped), dtype=int)
    log_n_values = np.asarray([grouped[int(n)][0] for n in bits])
    mean_log_queries = np.asarray([np.mean(grouped[int(n)][1]) for n in bits])
    parameters = fit_parameters(log_n_values, mean_log_queries)
    fitted = design_matrix(log_n_values) @ parameters
    residuals = mean_log_queries - fitted

    rng = np.random.default_rng(seed)
    samples = np.empty((bootstrap, 3), dtype=float)
    for index in range(bootstrap):
        bootstrap_means = []
        for n_bits in bits:
            observations = grouped[int(n_bits)][1]
            resample = rng.choice(observations, size=len(observations), replace=True)
            bootstrap_means.append(float(np.mean(resample)))
        samples[index] = fit_parameters(log_n_values, np.asarray(bootstrap_means))

    lower = np.quantile(samples, 0.025, axis=0)
    upper = np.quantile(samples, 0.975, axis=0)
    names = ("c_sqrt_log_N", "d_log_log_N", "k_intercept")
    parameter_report = {
        name: {
            "estimate": float(parameters[index]),
            "bootstrap_95_percent_ci": [float(lower[index]), float(upper[index])],
        }
        for index, name in enumerate(names)
    }
    return {
        "schema_version": 1,
        "model": "ln Q = c*sqrt(ln N) + d*ln(ln N) + k",
        "log_base": "natural",
        "sizes": [int(value) for value in bits],
        "size_count": len(bits),
        "trial_count": int(sum(len(grouped[int(n)][1]) for n in bits)),
        "bootstrap_replicates": bootstrap,
        "bootstrap_seed": seed,
        "parameters": parameter_report,
        "rmse_log_query": float(np.sqrt(np.mean(residuals**2))),
        "shape_comparison_in_sample_rmse": {
            "sqrt_log_N_plus_log_log_N": float(np.sqrt(np.mean(residuals**2))),
            "sqrt_log_N": regression_rmse(
                np.sqrt(log_n_values)[:, np.newaxis], mean_log_queries
            ),
            "log_N": regression_rmse(log_n_values[:, np.newaxis], mean_log_queries),
            "log_log_N": regression_rmse(
                np.log(log_n_values)[:, np.newaxis], mean_log_queries
            ),
        },
        "residuals": [
            {
                "n_bits": int(n_bits),
                "mean_log_query": float(observed),
                "fitted_log_query": float(predicted),
                "residual": float(residual),
            }
            for n_bits, observed, predicted, residual in zip(
                bits, mean_log_queries, fitted, residuals, strict=True
            )
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    if args.smoke:
        smoke_sizes = (8, 12, 16, 20, 24)
        grouped = {
            n_bits: (
                n_bits * math.log(2.0),
                np.asarray(
                    [
                        2.0 * math.sqrt(n_bits * math.log(2.0))
                        + 0.5 * math.log(n_bits * math.log(2.0))
                        + 1.0
                    ]
                    * 2
                ),
            )
            for n_bits in smoke_sizes
        }
        report = fit_report(grouped, min(args.bootstrap, 10), args.seed)
    else:
        if args.input is None:
            parser.error("--input is required unless --smoke is used")
        grouped = read_grouped(args.input)
        report = fit_report(grouped, args.bootstrap, args.seed)
    output = args.output
    if output is None:
        sizes = report["sizes"]
        assert isinstance(sizes, list)
        output = (
            Path(__file__).resolve().parents[1]
            / "data"
            / (
                f"fit_sieve_smoke_{date.today():%Y%m%d}.json"
                if args.smoke
                else f"fit_sieve_n{min(sizes)}-{max(sizes)}_{date.today():%Y%m%d}.json"
            )
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report["parameters"], sort_keys=True))
    print(output)


if __name__ == "__main__":
    main()
