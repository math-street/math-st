"""Exact nested-resultant sampling for BN, KSS16, and BLS24 published rows.

Sub-goal: P4.1 / SG-10
Inputs:   named paper profile, sample count, RNG seed
Outputs:  exact per-sample CSV and uncertainty/cost JSON for each profile
Runtime:  about 90 seconds for all profiles at 512 samples each
Validated against: BD19 Sections 7.1.1, 7.1.3, and 7.2.2
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from math import log2
from pathlib import Path
from random import Random

from sympy import Expr, Symbol, symbols

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CODE_DIRECTORY = Path(__file__).resolve().parent
for import_path in (REPOSITORY_ROOT, CODE_DIRECTORY):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

from lib.tnfs_cost import FiniteTNFSParameters, finite_tnfs_cost  # noqa: E402
from sample_bls12_norms import (  # noqa: E402
    NormSample,
    nested_resultant_norm,
    summarize,
)


@dataclass(frozen=True, slots=True)
class PaperProfile:
    name: str
    family: str
    level: int
    seed: int
    eta: int
    coefficient_bound: int
    smoothness_bound_bits: float
    roots_of_unity_index: int
    automorphisms: int
    paper_norm_f_bits: float
    paper_norm_g_bits: float
    paper_security_bits: float
    citation_section: str


PROFILES = {
    "bn-128": PaperProfile(
        "bn-128",
        "BN",
        128,
        (1 << 114) + (1 << 101) - (1 << 14) - 1,
        6,
        1098,
        74.2,
        1,
        2,
        557.0,
        808.9,
        131.3,
        "7.1.1",
    ),
    "kss16-128": PaperProfile(
        "kss16-128",
        "KSS16",
        128,
        (1 << 35) - (1 << 32) - (1 << 18) + (1 << 8) + 1,
        16,
        12,
        80.0,
        17,
        16,
        920.4,
        628.9,
        139.0,
        "7.1.3",
    ),
    "bls24-192": PaperProfile(
        "bls24-192",
        "BLS24",
        192,
        -(1 << 56) - (1 << 43) + (1 << 9) - (1 << 6),
        24,
        9,
        109.8,
        1,
        1,
        1295.0,
        1460.0,
        203.72,
        "7.2.2",
    ),
}


def profile_polynomials(profile: PaperProfile) -> tuple[Symbol, Symbol, Expr, Expr, Expr]:
    """Return the exact `x,t,h,f,g` selection for a published profile."""
    x, t = symbols("x t")
    u = profile.seed
    if profile.name == "bn-128":
        h = t**6 - t**4 + t**2 + 1
        substitution = x**2 - t
        f = (
            36 * substitution**4
            + 36 * substitution**3
            + 24 * substitution**2
            + 6 * substitution
            + 1
        )
        g = substitution - u
    elif profile.name == "kss16-128":
        h = sum(t**index for index in range(17))
        substitution = x - 1
        f = (
            substitution**10
            + 2 * substitution**9
            + 5 * substitution**8
            + 48 * substitution**6
            + 152 * substitution**5
            + 240 * substitution**4
            + 625 * substitution**2
            + 2398 * substitution
            + 3125
        )
        g = x - u - 1
    elif profile.name == "bls24-192":
        h = t**24 + t**4 - t**3 - t - 1
        f = (x - 1) ** 2 * (x**8 - x**4 + 1) + 3 * x
        g = x - u
    else:
        raise ValueError(f"unsupported profile {profile.name!r}")
    return x, t, h, f, g


def sample_profile(
    profile: PaperProfile,
    *,
    samples: int,
    rng_seed: int,
    distribution: str = "exact-domain",
    sampling_coefficient_bound: int | None = None,
) -> tuple[list[NormSample], int]:
    """Draw deterministic coefficient tuples and compute both exact norms."""
    if samples < 2:
        raise ValueError("samples must be at least two")
    if distribution not in ("exact-domain", "paper-code"):
        raise ValueError("distribution must be exact-domain or paper-code")
    sample_bound = (
        profile.coefficient_bound
        if sampling_coefficient_bound is None
        else sampling_coefficient_bound
    )
    if sample_bound < 1:
        raise ValueError("sampling_coefficient_bound must be positive")
    x, t, h, f, g = profile_polynomials(profile)
    rng = Random(rng_seed)
    upper_coefficient = sample_bound + int(distribution == "paper-code")
    rows: list[NormSample] = []
    attempts = 0
    while len(rows) < samples:
        attempts += 1
        a = tuple(
            rng.randint(-sample_bound, upper_coefficient)
            for _ in range(profile.eta)
        )
        b = tuple(
            rng.randint(-sample_bound, upper_coefficient)
            for _ in range(profile.eta)
        )
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


def write_profile_outputs(
    profile: PaperProfile,
    rows: list[NormSample],
    attempts: int,
    *,
    rng_seed: int,
    distribution: str,
    sampling_coefficient_bound: int | None,
    date_label: str,
    output_dir: Path,
) -> Path:
    """Write the exact rows and a finite-cost comparison for one profile."""
    output_dir.mkdir(parents=True, exist_ok=True)
    sample_bound = (
        profile.coefficient_bound
        if sampling_coefficient_bound is None
        else sampling_coefficient_bound
    )
    bound_suffix = (
        ""
        if sample_bound == profile.coefficient_bound
        else f"_sampling-a{sample_bound}"
    )
    stem = (
        f"{profile.name}_norms_{distribution}{bound_suffix}_n{len(rows)}_"
        f"s{rng_seed}_{date_label}"
    )
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

    norm_summary = summarize(
        rows,
        paper_norm_f_bits=profile.paper_norm_f_bits,
        paper_norm_g_bits=profile.paper_norm_g_bits,
    )
    parameters = FiniteTNFSParameters(
        coefficient_bound=profile.coefficient_bound,
        smoothness_bound_bits=profile.smoothness_bound_bits,
        eta=profile.eta,
        roots_of_unity_index=profile.roots_of_unity_index,
        relation_automorphisms=profile.automorphisms,
        linear_algebra_automorphisms=profile.automorphisms,
    )
    sampled_cost = finite_tnfs_cost(
        float(norm_summary["f"]["mean_integer_bit_length"]),  # type: ignore[index]
        float(norm_summary["g"]["mean_integer_bit_length"]),  # type: ignore[index]
        parameters,
    )
    paper_input_cost = finite_tnfs_cost(
        profile.paper_norm_f_bits,
        profile.paper_norm_g_bits,
        parameters,
    )
    report = {
        "status": "EMPIRICAL exact-integer nested-resultant sample",
        "profile": asdict(profile),
        "sampling_coefficient_bound": sample_bound,
        "rng_seed": rng_seed,
        "attempted_draws": attempts,
        "coefficient_distribution": (
            f"independent discrete uniform integers on [-{sample_bound},{sample_bound}]"
            if distribution == "exact-domain"
            else (
                "author-code reproduction: randint(-A,A+1), inclusive "
                f"[-{sample_bound},{sample_bound + 1}]"
            )
        ),
        "distribution_mode": distribution,
        "zero_norm_policy": "reject and resample",
        "summary": norm_summary,
        "finite_cost_parameters": asdict(parameters),
        "finite_cost_from_sampled_mean_bit_lengths": asdict(sampled_cost),
        "finite_cost_from_paper_norm_inputs": asdict(paper_input_cost),
        "difference_sampled_cost_from_paper_security": (
            sampled_cost.total_cost_log2 - profile.paper_security_bits
        ),
        "difference_paper_input_cost_from_paper_security": (
            paper_input_cost.total_cost_log2 - profile.paper_security_bits
        ),
        "csv": csv_path.name,
    }
    json_path = output_dir / f"{stem}.json"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return json_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", nargs="+", choices=tuple(PROFILES), default=list(PROFILES))
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--rng-seed", type=int, default=20260722)
    parser.add_argument(
        "--sampling-bound",
        type=int,
        help=(
            "override only the coefficient draw bound; finite-cost parameters retain "
            "the profile's printed A"
        ),
    )
    parser.add_argument(
        "--distribution",
        choices=("exact-domain", "paper-code"),
        default="paper-code",
    )
    parser.add_argument("--date", default=date.today().strftime("%Y%m%d"))
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data",
    )
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    if arguments.sampling_bound is not None and len(arguments.profiles) != 1:
        parser.error("--sampling-bound requires exactly one --profiles value")
    if arguments.smoke:
        arguments.samples = 2

    for profile_name in arguments.profiles:
        profile = PROFILES[profile_name]
        rows, attempts = sample_profile(
            profile,
            samples=arguments.samples,
            rng_seed=arguments.rng_seed,
            distribution=arguments.distribution,
            sampling_coefficient_bound=arguments.sampling_bound,
        )
        path = write_profile_outputs(
            profile,
            rows,
            attempts,
            rng_seed=arguments.rng_seed,
            distribution=arguments.distribution,
            sampling_coefficient_bound=arguments.sampling_bound,
            date_label=arguments.date,
            output_dir=arguments.output_dir,
        )
        print(path)


if __name__ == "__main__":
    main()
