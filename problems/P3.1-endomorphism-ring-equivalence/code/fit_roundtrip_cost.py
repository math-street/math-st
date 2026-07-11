"""
fit_roundtrip_cost.py - fit a toy Deuring round-trip timing exponent.
Sub-goal: P3.1 / SG-04b
Inputs:   five data/toy_deuring_roundtrip_p*_ell3_20260711.csv files
Outputs:  data/fit_roundtrip_cost_ell3_p11-71_20260711.csv
Runtime:  under one second for the five recorded timing rows
Validated against: the exact synthetic relation t = 2 p^(3/2)
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from math import exp, log, sqrt
from pathlib import Path
from typing import Sequence


DEFAULT_PRIMES = (11, 23, 47, 59, 71)
T_CRITICAL_95 = {1: 12.706204736, 3: 3.182446305}


@dataclass(frozen=True)
class PowerLawFit:
    """Ordinary least-squares fit of log(time) on log(parameter)."""

    exponent: float
    log_prefactor: float
    r_squared: float
    exponent_standard_error: float
    exponent_ci_low_95: float
    exponent_ci_high_95: float

    @property
    def prefactor(self) -> float:
        return exp(self.log_prefactor)

    def predict(self, parameter: float) -> float:
        return self.prefactor * parameter**self.exponent


def fit_power_law(observations: Sequence[tuple[float, float]]) -> PowerLawFit:
    """Fit time = prefactor * parameter^exponent in logarithmic coordinates."""

    if len(observations) < 3:
        raise ValueError("at least three positive observations are required")
    degrees_of_freedom = len(observations) - 2
    if degrees_of_freedom not in T_CRITICAL_95:
        raise ValueError("the validated confidence interval supports 3 or 5 observations")
    if any(parameter <= 0 or elapsed <= 0 for parameter, elapsed in observations):
        raise ValueError("parameters and elapsed times must be positive")
    xs = [log(parameter) for parameter, _ in observations]
    ys = [log(elapsed) for _, elapsed in observations]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    sxx = sum((value - x_mean) ** 2 for value in xs)
    if sxx == 0:
        raise ValueError("parameters must not all be equal")
    exponent = sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(xs, ys)
    ) / sxx
    log_prefactor = y_mean - exponent * x_mean
    residuals = [
        y_value - (log_prefactor + exponent * x_value)
        for x_value, y_value in zip(xs, ys)
    ]
    residual_sum_squares = sum(value**2 for value in residuals)
    total_sum_squares = sum((value - y_mean) ** 2 for value in ys)
    r_squared = (
        1.0 if total_sum_squares == 0 else 1.0 - residual_sum_squares / total_sum_squares
    )
    residual_variance = residual_sum_squares / (len(observations) - 2)
    exponent_standard_error = sqrt(residual_variance / sxx)
    margin = T_CRITICAL_95[degrees_of_freedom] * exponent_standard_error
    return PowerLawFit(
        exponent=exponent,
        log_prefactor=log_prefactor,
        r_squared=r_squared,
        exponent_standard_error=exponent_standard_error,
        exponent_ci_low_95=exponent - margin,
        exponent_ci_high_95=exponent + margin,
    )


def read_timings(
    data_directory: Path, primes: Sequence[int]
) -> list[tuple[int, int, float]]:
    observations: list[tuple[int, int, float]] = []
    for prime in primes:
        path = data_directory / f"toy_deuring_roundtrip_p{prime}_ell3_20260711.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            row = next(csv.DictReader(handle))
        observations.append(
            (int(row["p"]), int(row["ell"]), float(row["seconds_per_trial"]))
        )
    return observations


def residual_rows(
    observations: Sequence[tuple[int, int, float]],
) -> list[dict[str, float | int]]:
    fit = fit_power_law(
        [(prime, elapsed) for prime, _, elapsed in observations]
    )
    rows: list[dict[str, float | int]] = []
    for prime, ell, elapsed in observations:
        predicted = fit.predict(prime)
        rows.append(
            {
                "p": prime,
                "ell": ell,
                "observed_seconds_per_trial": elapsed,
                "predicted_seconds_per_trial": predicted,
                "residual_seconds": elapsed - predicted,
                "residual_log_seconds": log(elapsed) - log(predicted),
                "sample_count": len(observations),
                "fit_exponent": fit.exponent,
                "fit_prefactor": fit.prefactor,
                "fit_r_squared": fit.r_squared,
                "exponent_standard_error": fit.exponent_standard_error,
                "exponent_ci_low_95": fit.exponent_ci_low_95,
                "exponent_ci_high_95": fit.exponent_ci_high_95,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    problem_directory = Path(__file__).resolve().parents[1]
    observations = read_timings(problem_directory / "data", DEFAULT_PRIMES)
    rows = residual_rows(observations[:3] if args.smoke else observations)
    output_name = (
        "fit_roundtrip_cost_smoke_20260711.csv"
        if args.smoke
        else "fit_roundtrip_cost_ell3_p11-71_20260711.csv"
    )
    output = problem_directory / "data" / output_name
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(output)
    print(rows[0])


if __name__ == "__main__":
    main()
