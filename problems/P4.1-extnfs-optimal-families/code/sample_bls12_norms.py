"""Exact nested-resultant sampler for the BLS12 SexTNFS construction.

Sub-goal: P4.1 / SG-08
Inputs:   BLS12 seed u, coefficient bound A, sample count, RNG seed
Outputs:  one CSV of exact norms and one JSON summary with uncertainty
Runtime:  about 1 s for --smoke and about 15 s for 256 production samples
Validated against: hand-computed nested resultants and BD19 Section 7.1.2
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from math import log2, sqrt
from pathlib import Path
from random import Random
from statistics import fmean, stdev

from sympy import Expr, Symbol, resultant, symbols

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.tnfs_cost import FiniteTNFSParameters, finite_tnfs_cost  # noqa: E402

PAPER_BLS12_SEED = -(1 << 77) + (1 << 50) + (1 << 33)
PAPER_NORM_F_BITS = 791.2
PAPER_NORM_G_BITS = 584.8


@dataclass(frozen=True, slots=True)
class NormSample:
    sample_index: int
    a_coefficients: tuple[int, ...]
    b_coefficients: tuple[int, ...]
    norm_f: int
    norm_g: int
    log2_norm_f: float
    log2_norm_g: float
    bit_length_f: int
    bit_length_g: int


def bls12_sextnfs_polynomials(seed: int) -> tuple[Symbol, Symbol, Expr, Expr, Expr]:
    """Return the exact h, f, g from BD19 Section 7.1.2."""
    x, t = symbols("x t")
    substitution = x**2 + t + t**2 + t**4 + 1
    p_numerator = (substitution - 1) ** 2 * (
        substitution**4 - substitution**2 + 1
    ) + 3 * substitution
    h = t**6 - t - 1
    g = substitution - seed
    return x, t, h, p_numerator, g


def nested_resultant_norm(
    a_coefficients: tuple[int, ...],
    b_coefficients: tuple[int, ...],
    f: Expr,
    h: Expr,
    x: Symbol,
    t: Symbol,
) -> int:
    """Compute |Res_t(Res_x(a(t)-x*b(t), f(t,x)), h(t))| exactly."""
    if len(a_coefficients) != len(b_coefficients) or not a_coefficients:
        raise ValueError("a and b must be nonempty coefficient tuples of equal length")
    a = sum(value * t**index for index, value in enumerate(a_coefficients))
    b = sum(value * t**index for index, value in enumerate(b_coefficients))
    inner = resultant(a - x * b, f, x)
    return abs(int(resultant(inner, h, t)))


def sample_bls12_norms(
    *,
    seed: int,
    coefficient_bound: int,
    samples: int,
    rng_seed: int,
) -> tuple[list[NormSample], int]:
    """Sample exact BLS12 norms, rejecting the zero polynomial or zero norms."""
    if coefficient_bound < 1:
        raise ValueError("coefficient_bound must be positive")
    if samples < 2:
        raise ValueError("samples must be at least two for uncertainty estimates")

    x, t, h, f, g = bls12_sextnfs_polynomials(seed)
    rng = Random(rng_seed)
    rows: list[NormSample] = []
    attempts = 0
    while len(rows) < samples:
        attempts += 1
        a = tuple(rng.randint(-coefficient_bound, coefficient_bound) for _ in range(6))
        b = tuple(rng.randint(-coefficient_bound, coefficient_bound) for _ in range(6))
        if not any(a) and not any(b):
            continue
        norm_f = nested_resultant_norm(a, b, f, h, x, t)
        norm_g = nested_resultant_norm(a, b, g, h, x, t)
        if norm_f == 0 or norm_g == 0:
            continue
        rows.append(
            NormSample(
                sample_index=len(rows),
                a_coefficients=a,
                b_coefficients=b,
                norm_f=norm_f,
                norm_g=norm_g,
                log2_norm_f=log2(norm_f),
                log2_norm_g=log2(norm_g),
                bit_length_f=norm_f.bit_length(),
                bit_length_g=norm_g.bit_length(),
            )
        )
    return rows, attempts


def summarize(
    samples: list[NormSample],
    *,
    paper_norm_f_bits: float = PAPER_NORM_F_BITS,
    paper_norm_g_bits: float = PAPER_NORM_G_BITS,
) -> dict[str, object]:
    """Return means, sample standard errors, and normal 95% intervals."""
    if len(samples) < 2:
        raise ValueError("at least two samples are required")
    summary: dict[str, object] = {"accepted_samples": len(samples)}
    for side in ("f", "g"):
        paper_value = paper_norm_f_bits if side == "f" else paper_norm_g_bits
        log_values = [getattr(row, f"log2_norm_{side}") for row in samples]
        bit_values = [float(getattr(row, f"bit_length_{side}")) for row in samples]
        log_mean = fmean(log_values)
        bit_mean = fmean(bit_values)
        log_standard_deviation = stdev(log_values)
        bit_standard_deviation = stdev(bit_values)
        log_standard_error = log_standard_deviation / sqrt(len(log_values))
        bit_standard_error = bit_standard_deviation / sqrt(len(bit_values))
        summary[side] = {
            "mean_log2_norm": log_mean,
            "log2_standard_error": log_standard_error,
            "log2_normal_95_interval": [
                log_mean - 1.96 * log_standard_error,
                log_mean + 1.96 * log_standard_error,
            ],
            "mean_integer_bit_length": bit_mean,
            "bit_length_sample_standard_deviation": bit_standard_deviation,
            "bit_length_standard_error": bit_standard_error,
            "bit_length_normal_95_interval": [
                bit_mean - 1.96 * bit_standard_error,
                bit_mean + 1.96 * bit_standard_error,
            ],
            "paper_value": paper_value,
            "bit_length_difference_from_paper": bit_mean - paper_value,
            "log2_difference_from_paper": log_mean - paper_value,
        }
    return summary


def write_outputs(
    rows: list[NormSample],
    attempts: int,
    *,
    seed: int,
    coefficient_bound: int,
    rng_seed: int,
    output_dir: Path,
    date_label: str,
) -> Path:
    """Write a reproducible sample table and summary; return the JSON path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"bls12_norms_n{len(rows)}_a{coefficient_bound}_s{rng_seed}_{date_label}"
    csv_path = output_dir / f"{stem}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "sample_index",
            "a_coefficients",
            "b_coefficients",
            "norm_f",
            "norm_g",
            "log2_norm_f",
            "log2_norm_g",
            "bit_length_f",
            "bit_length_g",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            record["a_coefficients"] = json.dumps(record["a_coefficients"])
            record["b_coefficients"] = json.dumps(record["b_coefficients"])
            writer.writerow(record)

    norm_summary = summarize(rows)
    finite_parameters = FiniteTNFSParameters(
        coefficient_bound=coefficient_bound,
        smoothness_bound_bits=73.5,
        eta=6,
        roots_of_unity_index=1,
        relation_automorphisms=2,
        linear_algebra_automorphisms=2,
    )
    sampled_cost = finite_tnfs_cost(
        float(norm_summary["f"]["mean_integer_bit_length"]),  # type: ignore[index]
        float(norm_summary["g"]["mean_integer_bit_length"]),  # type: ignore[index]
        finite_parameters,
    )
    report = {
        "status": "EMPIRICAL exact-integer nested-resultant sample",
        "construction": "Barbulescu--Duquesne 2019 Section 7.1.2 BLS12 SexTNFS",
        "seed": seed,
        "coefficient_bound": coefficient_bound,
        "rng_seed": rng_seed,
        "attempted_draws": attempts,
        "zero_norm_policy": "reject and resample",
        "coefficient_distribution": "independent discrete uniform integers on [-A,A]",
        "paper_metric_interpretation": (
            "The published 791.2 and 584.8 are reproduced by mean integer bit length "
            "floor(log2(N))+1; mean log2(N) is also reported to expose the convention."
        ),
        "summary": norm_summary,
        "finite_cost_from_mean_integer_bit_lengths": asdict(sampled_cost),
        "finite_cost_parameters": asdict(finite_parameters),
        "csv": csv_path.name,
    }
    json_path = output_dir / f"{stem}.json"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return json_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=PAPER_BLS12_SEED)
    parser.add_argument("--coefficient-bound", type=int, default=1169)
    parser.add_argument("--samples", type=int, default=256)
    parser.add_argument("--rng-seed", type=int, default=20260722)
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    if arguments.smoke:
        arguments.seed = -2
        arguments.coefficient_bound = 2
        arguments.samples = 8

    rows, attempts = sample_bls12_norms(
        seed=arguments.seed,
        coefficient_bound=arguments.coefficient_bound,
        samples=arguments.samples,
        rng_seed=arguments.rng_seed,
    )
    path = write_outputs(
        rows,
        attempts,
        seed=arguments.seed,
        coefficient_bound=arguments.coefficient_bound,
        rng_seed=arguments.rng_seed,
        output_dir=arguments.output_dir,
        date_label=arguments.date,
    )
    print(path)


if __name__ == "__main__":
    main()
