"""search_families.py — bounded family enumeration and labelled extrapolation.
Sub-goal: P4.1 / SG-03 through SG-07
Inputs:   --min-seed <int> --max-seed <int> --targets <bits...> --mode <mode>
Outputs:  data/search_families_<range>_<date>.csv and extrapolation CSV/JSON
Runtime:  ~3 s for --smoke; the default range depends on host primality speed
Validated against: BN(-2), BLS12(-2), BLS24(-5), BLS12-381, BD19 BN estimate
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import date
from math import ceil, log2
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import (  # noqa: E402
    PAIRING_FAMILIES,
    evaluate_pairing_family,
    validate_pairing_family,
)
from lib.tnfs_cost import (  # noqa: E402
    pollard_security_bits,
    pollard_security_from_order_bits,
    tnfs_model_preset,
)


@dataclass(frozen=True, slots=True)
class FamilyGrowth:
    family: str
    embedding_degree: int
    p_degree: int
    p_leading_coefficient: float
    r_degree: int
    r_leading_coefficient: float
    miller_seed_multiplier: int

    def bit_estimates(self, log2_abs_seed: float) -> tuple[float, float]:
        p_bits = self.p_degree * log2_abs_seed + log2(self.p_leading_coefficient)
        r_bits = self.r_degree * log2_abs_seed + log2(self.r_leading_coefficient)
        return p_bits, r_bits

    def pairing_proxy(self, log2_abs_seed: float) -> float:
        miller_bits = log2_abs_seed + log2(self.miller_seed_multiplier)
        return self.embedding_degree * miller_bits


GROWTH = {
    "BN": FamilyGrowth("BN", 12, 4, 36.0, 4, 36.0, 6),
    "BLS12": FamilyGrowth("BLS12", 12, 6, 1.0 / 3.0, 4, 1.0, 1),
    "BLS24": FamilyGrowth("BLS24", 24, 10, 1.0 / 3.0, 8, 1.0, 1),
    "KSS16": FamilyGrowth("KSS16", 16, 10, 1.0 / 980.0, 8, 1.0 / 61_250.0, 1),
}


def pairing_proxy(family: str, seed: int, embedding_degree: int) -> int:
    scalar = abs(6 * seed + 2) if family == "BN" else abs(seed)
    return embedding_degree * max(1, scalar.bit_length())


def enumerate_toy_candidates(
    minimum_seed: int,
    maximum_seed: int,
    maximum_p_bits: int,
    model_name: str,
    rng_seed: int,
) -> tuple[list[dict[str, object]], dict[str, int]]:
    if minimum_seed > maximum_seed:
        raise ValueError("minimum_seed must not exceed maximum_seed")
    if maximum_p_bits > 60:
        raise ValueError("the project scaffold caps toy searches at 60 p bits")
    model = tnfs_model_preset(model_name)
    rows: list[dict[str, object]] = []
    counts = {family: 0 for family in PAIRING_FAMILIES}
    for family in PAIRING_FAMILIES:
        for seed in range(minimum_seed, maximum_seed + 1):
            if abs(seed) < 2:
                continue
            try:
                parameters = evaluate_pairing_family(family, seed)
            except ValueError:
                continue
            if parameters.p.bit_length() > maximum_p_bits:
                continue
            validation = validate_pairing_family(parameters)
            if not validation.valid:
                continue
            counts[family] += 1
            rows.append(
                {
                    "family": family,
                    "seed": seed,
                    "p": parameters.p,
                    "r": parameters.r,
                    "embedding_degree": parameters.embedding_degree,
                    "cofactor": parameters.cofactor,
                    "p_bits": parameters.p.bit_length(),
                    "r_bits": parameters.r.bit_length(),
                    "rho": f"{parameters.rho:.12f}",
                    "extnfs_security_bits": f"{model.security_bits(parameters.p, parameters.embedding_degree):.6f}",
                    "pollard_security_bits": f"{pollard_security_bits(parameters.r):.6f}",
                    "pairing_proxy": pairing_proxy(family, seed, parameters.embedding_degree),
                    "model": model_name,
                    "rng_seed": rng_seed,
                }
            )
    rows.sort(key=lambda row: (str(row["family"]), int(row["seed"])))
    return rows, counts


def _meets_target(profile: FamilyGrowth, log_seed: float, target: float, model_name: str) -> bool:
    model = tnfs_model_preset(model_name)
    p_bits, r_bits = profile.bit_estimates(log_seed)
    if p_bits <= 1 or r_bits <= 0:
        return False
    field_security = model.security_bits_from_field_bits(profile.embedding_degree * p_bits)
    pollard_security = pollard_security_from_order_bits(r_bits)
    return min(field_security, pollard_security) >= target


def minimum_log2_seed(profile: FamilyGrowth, target: float, model_name: str) -> float:
    """Solve the monotone leading-term model to about 2^-60 bits."""
    lower = 2.0
    upper = 4.0
    while not _meets_target(profile, upper, target, model_name):
        upper *= 2.0
        if upper > 4096:
            raise RuntimeError("target exceeds extrapolator search ceiling")
    for _ in range(80):
        midpoint = (lower + upper) / 2.0
        if _meets_target(profile, midpoint, target, model_name):
            upper = midpoint
        else:
            lower = midpoint
    return upper


def extrapolation_rows(targets: list[int], model_names: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for model_name in model_names:
        model = tnfs_model_preset(model_name)
        for target in targets:
            target_rows: list[dict[str, object]] = []
            for family in PAIRING_FAMILIES:
                profile = GROWTH[family]
                log_seed = minimum_log2_seed(profile, target, model_name)
                p_bits, r_bits = profile.bit_estimates(log_seed)
                target_rows.append(
                    {
                        "target_bits": target,
                        "model": model_name,
                        "l_constant": model.l_constant,
                        "log2_prefactor": f"{model.log2_prefactor:.9f}",
                        "l_exponent": f"{model.l_exponent:.9f}",
                        "notation_denominator": model.notation_denominator,
                        "polynomial_selection": model.polynomial_selection,
                        "calibration": model.calibration,
                        "family": family,
                        "minimum_log2_abs_seed": f"{log_seed:.6f}",
                        "minimum_seed_bits": ceil(log_seed),
                        "estimated_p_bits": f"{p_bits:.3f}",
                        "estimated_r_bits": f"{r_bits:.3f}",
                        "estimated_field_bits": f"{profile.embedding_degree * p_bits:.3f}",
                        "extnfs_security_bits": f"{model.security_bits_from_field_bits(profile.embedding_degree * p_bits):.6f}",
                        "pollard_security_bits": f"{pollard_security_from_order_bits(r_bits):.6f}",
                        "rho_estimate": f"{p_bits / r_bits:.9f}",
                        "rho_limit": f"{profile.p_degree / profile.r_degree:.6f}",
                        "pairing_proxy": f"{profile.pairing_proxy(log_seed):.3f}",
                        "concrete_prime_seed": "not searched (model extrapolation)",
                        "optimal_for_rho": False,
                    }
                )
            best = min(
                target_rows,
                key=lambda row: (
                    float(row["rho_estimate"]),
                    float(row["pairing_proxy"]),
                    float(row["estimated_p_bits"]),
                    str(row["family"]),
                ),
            )
            best["optimal_for_rho"] = True
            rows.extend(target_rows)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        if not rows:
            raise ValueError("fieldnames are required for an empty CSV")
        fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-seed", type=int, default=-10_000)
    parser.add_argument("--max-seed", type=int, default=10_000)
    parser.add_argument("--max-p-bits", type=int, default=60)
    parser.add_argument("--targets", type=int, nargs="+", default=[128, 192, 256])
    parser.add_argument(
        "--models",
        nargs="+",
        default=["bn254-calibrated", "sextnfs-o1less", "extnfs-composite"],
    )
    parser.add_argument("--mode", choices=("toy", "extrapolate", "all"), default="all")
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
        arguments.min_seed = -100
        arguments.max_seed = 100

    summary: dict[str, object] = {
        "date": arguments.date,
        "rng_seed": arguments.rng_seed,
        "targets": arguments.targets,
        "mode": arguments.mode,
        "toy_ceiling_p_bits": arguments.max_p_bits,
    }
    range_label = f"m{abs(arguments.min_seed)}_{arguments.max_seed}"
    if arguments.mode in ("toy", "all"):
        toy_rows, counts = enumerate_toy_candidates(
            arguments.min_seed,
            arguments.max_seed,
            arguments.max_p_bits,
            arguments.models[0],
            arguments.rng_seed,
        )
        toy_path = arguments.output_dir / f"search_families_{range_label}_{arguments.date}.csv"
        toy_fields = [
            "family",
            "seed",
            "p",
            "r",
            "embedding_degree",
            "cofactor",
            "p_bits",
            "r_bits",
            "rho",
            "extnfs_security_bits",
            "pollard_security_bits",
            "pairing_proxy",
            "model",
            "rng_seed",
        ]
        write_csv(toy_path, toy_rows, toy_fields)
        feasible = {
            str(target): min(
                (
                    row
                    for row in toy_rows
                    if min(
                        float(row["extnfs_security_bits"]),
                        float(row["pollard_security_bits"]),
                    )
                    >= target
                ),
                key=lambda row: (float(row["rho"]), int(row["pairing_proxy"])),
                default=None,
            )
            for target in arguments.targets
        }
        summary["toy"] = {
            "seed_interval_inclusive": [arguments.min_seed, arguments.max_seed],
            "families": list(PAIRING_FAMILIES),
            "accepted_counts": counts,
            "candidate_count": len(toy_rows),
            "optima": feasible,
            "proof_scope": (
                "Exhaustive over every integer seed in the interval; acceptance requires "
                "integral family polynomials, deterministic p/r primality below 2^60, "
                "r | p+1-t, and least multiplicative order k."
            ),
            "csv": toy_path.name,
        }

    if arguments.mode in ("extrapolate", "all"):
        rows = extrapolation_rows(arguments.targets, arguments.models)
        extrapolation_path = arguments.output_dir / f"optimization_extrapolated_{arguments.date}.csv"
        write_csv(extrapolation_path, rows)
        summary["extrapolation"] = {
            "models": arguments.models,
            "row_count": len(rows),
            "csv": extrapolation_path.name,
            "status": "HEURISTIC MODEL EXTRAPOLATION; no concrete prime seeds generated",
            "objective": "minimum estimated rho, pairing proxy used only as a tie-breaker",
            "growth_profiles": {name: asdict(profile) for name, profile in GROWTH.items()},
        }

    summary_path = arguments.output_dir / f"search_summary_{range_label}_{arguments.date}.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(summary_path)


if __name__ == "__main__":
    main()
