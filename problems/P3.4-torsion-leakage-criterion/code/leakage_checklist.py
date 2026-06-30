"""
leakage_checklist.py — classify torsion leakage against published attack templates.
Sub-goal: P3.4 / SG-04 and SG-05
Inputs:   --input <JSON>; --output <JSON>; --smoke
Outputs:  data/leakage_checklist_<case-set>_20260630.json
Runtime:  <1 second for the bundled protocol and boundary fixtures
Validated against: Robert 2023, Theorem 1.1 and Section 6.4; the protocol
fixtures sourced in CHECKLIST.md Section 3.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from math import gcd
from pathlib import Path
from typing import Any

from surface_certificates import CertificateStatus, validate_certificate


class Verdict(str, Enum):
    KEY_RECOVERY_POLYNOMIAL = "KEY_RECOVERY_POLYNOMIAL"
    KEY_RECOVERY_WITH_SURFACE_WITNESS = "KEY_RECOVERY_WITH_SURFACE_WITNESS"
    ALGEBRAIC_ONLY = "ALGEBRAIC_ONLY"
    WITNESS_DEPENDENT = "WITNESS_DEPENDENT"
    NO_PUBLISHED_ROUTE = "NO_PUBLISHED_ROUTE"
    INSUFFICIENT_PROFILE = "INSUFFICIENT_PROFILE"


def parse_integer(value: int | str | None) -> int | None:
    """Parse an integer or a deliberately small ``base^exponent`` expression."""
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if value.count("^") == 1:
        base, exponent = value.split("^")
        return int(base) ** int(exponent)
    return int(value)


@dataclass(frozen=True)
class LeakageProfile:
    case_id: str
    target_endpoints_public: bool | None
    degree_visibility: str
    degree: int | None
    degree_factorization_known: bool | None
    torsion_order: int | None
    torsion_factorization_known: bool | None
    torsion_rank: int | None
    target_action_derivable: bool | None
    torsion_access: str
    smooth_arithmetic: bool | None
    kernel_recovery: str
    surface_construction: str
    surface_certificate: dict[str, Any] | None = None
    endomorphism_ring_known: bool | None = None
    same_secret_across_samples: bool | None = None

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "LeakageProfile":
        cooked = dict(raw)
        cooked["degree"] = parse_integer(cooked.get("degree"))
        cooked["torsion_order"] = parse_integer(cooked.get("torsion_order"))
        return cls(**cooked)


@dataclass(frozen=True)
class Classification:
    case_id: str
    verdict: Verdict
    route: str | None
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "verdict": self.verdict.value,
            "route": self.route,
            "reasons": list(self.reasons),
        }


def classify(profile: LeakageProfile) -> Classification:
    """Apply the ordered checklist in CHECKLIST.md Section 4."""
    reasons: list[str] = []
    hard_blockers: list[str] = []

    if profile.target_endpoints_public is False:
        hard_blockers.append("No public endpoints identify one target secret map (C0).")
    if profile.degree_visibility == "hidden":
        hard_blockers.append("The target degree is not polynomially enumerable (C1).")
    if profile.target_action_derivable is False:
        hard_blockers.append("The transcript does not determine the target map on torsion (C2).")
    if profile.torsion_rank is not None and profile.torsion_rank < 2:
        hard_blockers.append("The derivable target-map restriction has rank below two (C2).")
    if profile.same_secret_across_samples is False:
        hard_blockers.append("The proposed leakage aggregation mixes distinct secret maps.")
    if hard_blockers:
        return Classification(
            profile.case_id,
            Verdict.NO_PUBLISHED_ROUTE,
            None,
            tuple(hard_blockers),
        )

    unknown = (
        profile.target_endpoints_public is None
        or profile.degree_visibility == "unknown"
        or profile.target_action_derivable is None
        or profile.torsion_rank is None
        or profile.torsion_access == "unknown"
        or profile.kernel_recovery == "unknown"
    )
    if unknown:
        return Classification(
            profile.case_id,
            Verdict.INSUFFICIENT_PROFILE,
            None,
            ("At least one common template input is unknown.",),
        )

    if profile.degree is None or profile.torsion_order is None:
        return Classification(
            profile.case_id,
            Verdict.INSUFFICIENT_PROFILE,
            None,
            ("Numeric degree and effective torsion order are needed for the size test.",),
        )

    if profile.degree <= 0 or profile.torsion_order <= 1:
        raise ValueError(f"{profile.case_id}: degree must be positive and torsion order > 1")

    arithmetic_ready = (
        profile.degree_factorization_known is True
        and profile.torsion_factorization_known is True
        and profile.torsion_access in {"base_field", "polynomial_extension"}
        and profile.smooth_arithmetic is True
    )

    if gcd(profile.degree, profile.torsion_order) != 1:
        return Classification(
            profile.case_id,
            Verdict.WITNESS_DEPENDENT,
            None,
            ("The recorded profile has not supplied the common-factor peeling required before the coprime templates.",),
        )

    size_passes = profile.torsion_order**2 > profile.degree
    if size_passes and profile.kernel_recovery == "available":
        reasons.append("Full rank-two target action and N^2 > degree satisfy the R8 recovery boundary.")
        if arithmetic_ready:
            return Classification(
                profile.case_id,
                Verdict.KEY_RECOVERY_POLYNOMIAL,
                "R8",
                tuple(reasons),
            )
        reasons.append("At least one factorization, torsion-access, or smoothness cost is not polynomially available.")
        return Classification(
            profile.case_id,
            Verdict.ALGEBRAIC_ONLY,
            "R8",
            tuple(reasons),
        )

    certificate_result = None
    if profile.surface_certificate is not None:
        certificate_result = validate_certificate(profile.case_id, profile.surface_certificate)
    if (
        certificate_result is not None
        and certificate_result.status == CertificateStatus.NUMERICALLY_VALID
    ):
        reasons.append(f"A mechanically valid {certificate_result.route} numerical certificate is recorded.")
        if (
            profile.surface_construction == "available"
            and arithmetic_ready
            and profile.kernel_recovery == "available"
        ):
            return Classification(
                profile.case_id,
                Verdict.KEY_RECOVERY_WITH_SURFACE_WITNESS,
                certificate_result.route,
                tuple(reasons),
            )
        reasons.append(
            "The numerical certificate lacks a constructed auxiliary map or another polynomial-cost recovery condition."
        )
        return Classification(
            profile.case_id,
            Verdict.ALGEBRAIC_ONLY,
            certificate_result.route,
            tuple(reasons),
        )

    if certificate_result is not None:
        reasons.append(
            "The supplied surface certificate failed mechanical validation: "
            + "; ".join(certificate_result.reasons)
        )

    if size_passes and profile.kernel_recovery != "available":
        reasons.append("The R8 size condition passes, but conversion from evaluation to the protocol secret is absent.")
    else:
        reasons.append("N^2 <= degree, so the generic R8 direct-recovery leaf does not apply.")
    reasons.append("No mechanically valid K2 numerical certificate plus construction witness was supplied.")
    return Classification(
        profile.case_id,
        Verdict.WITNESS_DEPENDENT,
        None,
        tuple(reasons),
    )


def classify_file(input_path: Path) -> list[Classification]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    return [classify(LeakageProfile.from_mapping(item)) for item in raw["cases"]]


def main() -> None:
    problem_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("protocol_cases.json"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    results = classify_file(args.input)
    if args.smoke:
        results = results[:1]

    output = args.output
    if output is None:
        stem = args.input.stem.replace("_cases", "")
        if args.smoke:
            stem = f"{stem}_smoke"
        output = problem_dir / "data" / f"leakage_checklist_{stem}_20260630.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps([result.as_dict() for result in results], indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
