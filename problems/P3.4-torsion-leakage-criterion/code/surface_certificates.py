"""
surface_certificates.py -- check numerical K2-CD and K2-MM certificates.
Sub-goal: P3.4 / SG-09
Inputs:   --input <JSON>; --output <JSON>; --smoke
Outputs:  data/surface_certificates_<case-set>_20260703.json
Runtime:  <1 second for the bundled fixtures
Validated by: code/tests/test_surface_certificates.py

This checker verifies integer identities, exact small-prime factorizations, and
declared search bounds.  It does not construct or evaluate an auxiliary
isogeny, so a numerically valid result is not by itself a complete K2 witness.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from math import gcd, isqrt
from pathlib import Path
from typing import Any


MAX_EXACT_PRIME_CHECK = 1_000_000


class CertificateStatus(str, Enum):
    NUMERICALLY_VALID = "NUMERICALLY_VALID"
    INVALID = "INVALID"
    UNSUPPORTED_ROUTE = "UNSUPPORTED_ROUTE"


@dataclass(frozen=True)
class CertificateResult:
    case_id: str
    status: CertificateStatus
    route: str | None
    derived: dict[str, int]
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "status": self.status.value,
            "route": self.route,
            "derived": self.derived,
            "reasons": list(self.reasons),
        }


def _is_prime_exact_small(value: int) -> bool:
    if value < 2 or value > MAX_EXACT_PRIME_CHECK:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def _validate_factorization(
    value: int,
    raw_factors: list[list[int]],
    smoothness_bound: int,
    label: str,
) -> list[str]:
    errors: list[str] = []
    product = 1
    seen: set[int] = set()
    for pair in raw_factors:
        if len(pair) != 2:
            errors.append(f"{label} factorization entries must be [prime, exponent].")
            continue
        prime, exponent = int(pair[0]), int(pair[1])
        if prime in seen:
            errors.append(f"{label} factorization repeats prime {prime}.")
        seen.add(prime)
        if exponent <= 0:
            errors.append(f"{label} factor exponents must be positive.")
        if not _is_prime_exact_small(prime):
            errors.append(
                f"{label} factor {prime} is not an exactly checked prime at most "
                f"{MAX_EXACT_PRIME_CHECK}."
            )
        if prime > smoothness_bound:
            errors.append(f"{label} factor {prime} exceeds smoothness bound {smoothness_bound}.")
        if exponent > 0:
            product *= prime**exponent
    if product != value:
        errors.append(f"{label} factorization multiplies to {product}, not {value}.")
    return errors


def _invalid(
    case_id: str, route: str, derived: dict[str, int], errors: list[str]
) -> CertificateResult:
    return CertificateResult(
        case_id,
        CertificateStatus.INVALID,
        route,
        derived,
        tuple(errors),
    )


def validate_cd(case_id: str, certificate: dict[str, Any]) -> CertificateResult:
    """Check the basic Castryck--Decru degree relation N = d + c."""
    route = "K2-CD"
    torsion_order = int(certificate["torsion_order"])
    target_degree = int(certificate["target_degree"])
    auxiliary_degree = int(certificate["auxiliary_degree"])
    smoothness_bound = int(certificate["smoothness_bound"])
    derived = {"expected_auxiliary_degree": torsion_order - target_degree}
    errors: list[str] = []
    if torsion_order <= target_degree:
        errors.append("K2-CD requires a positive difference N - d.")
    if gcd(torsion_order, target_degree) != 1:
        errors.append("The encoded coprime K2-CD template requires gcd(N, d) = 1.")
    if auxiliary_degree != torsion_order - target_degree:
        errors.append("The auxiliary degree does not equal N - d.")
    if auxiliary_degree <= 0:
        errors.append("The auxiliary degree must be positive.")
    if smoothness_bound < 2:
        errors.append("The smoothness bound must be at least two.")
    errors.extend(
        _validate_factorization(
            auxiliary_degree,
            certificate["auxiliary_factorization"],
            smoothness_bound,
            "auxiliary degree",
        )
    )
    if errors:
        return _invalid(case_id, route, derived, errors)
    return CertificateResult(
        case_id,
        CertificateStatus.NUMERICALLY_VALID,
        route,
        derived,
        ("The coprimality, positivity, degree relation, and smooth factorization checks pass.",),
    )


def validate_mm(case_id: str, certificate: dict[str, Any]) -> CertificateResult:
    """Check the Maino--Martindale relation e B' = f + A'."""
    route = "K2-MM"
    secret_prime = int(certificate["secret_prime"])
    secret_exponent = int(certificate["secret_exponent"])
    torsion_prime = int(certificate["torsion_prime"])
    torsion_exponent = int(certificate["torsion_exponent"])
    secret_degree = int(certificate["secret_degree"])
    torsion_order = int(certificate["torsion_order"])
    removed_secret_steps = int(certificate["removed_secret_steps"])
    removed_torsion_levels = int(certificate["removed_torsion_levels"])
    reduced_secret_degree = int(certificate["reduced_secret_degree"])
    reduced_torsion_order = int(certificate["reduced_torsion_order"])
    multiplier = int(certificate["multiplier"])
    cofactor = int(certificate["cofactor"])
    smoothness_bound = int(certificate["smoothness_bound"])
    multiplier_bound = int(certificate["multiplier_bound"])
    secret_guess_bound = int(certificate["secret_guess_bound"])
    torsion_drop_bound = int(certificate["torsion_drop_bound"])
    expected_secret_degree = secret_prime**secret_exponent if secret_exponent >= 0 else 0
    expected_torsion_order = torsion_prime**torsion_exponent if torsion_exponent >= 0 else 0
    expected_reduced_secret = secret_prime ** (secret_exponent - removed_secret_steps) if 0 <= removed_secret_steps <= secret_exponent else 0
    expected_reduced_torsion = torsion_prime ** (torsion_exponent - removed_torsion_levels) if 0 <= removed_torsion_levels <= torsion_exponent else 0
    derived = {
        "expected_secret_degree": expected_secret_degree,
        "expected_torsion_order": expected_torsion_order,
        "expected_reduced_secret_degree": expected_reduced_secret,
        "expected_reduced_torsion_order": expected_reduced_torsion,
        "relation_left": multiplier * reduced_torsion_order,
        "relation_right": cofactor + reduced_secret_degree,
    }
    errors: list[str] = []
    if not _is_prime_exact_small(secret_prime):
        errors.append("The secret base is not an exactly checked small prime.")
    if not _is_prime_exact_small(torsion_prime):
        errors.append("The torsion base is not an exactly checked small prime.")
    if secret_exponent <= 0 or torsion_exponent <= 0:
        errors.append("Prime-power exponents must be positive.")
    if secret_degree != expected_secret_degree:
        errors.append("A does not equal the declared secret prime power.")
    if torsion_order != expected_torsion_order:
        errors.append("B does not equal the declared torsion prime power.")
    if gcd(secret_degree, torsion_order) != 1:
        errors.append("The encoded K2-MM template requires gcd(A, B) = 1.")
    if not 0 <= removed_secret_steps <= secret_exponent:
        errors.append("The removed secret-step count is outside [0, a].")
    if not 0 <= removed_torsion_levels <= torsion_exponent:
        errors.append("The removed torsion-level count is outside [0, b].")
    if removed_secret_steps > secret_guess_bound:
        errors.append("The removed secret-step count exceeds its declared search bound.")
    if removed_torsion_levels > torsion_drop_bound:
        errors.append("The removed torsion-level count exceeds its declared search bound.")
    if reduced_secret_degree != expected_reduced_secret:
        errors.append("A' does not equal A with the declared secret steps removed.")
    if reduced_torsion_order != expected_reduced_torsion:
        errors.append("B' does not equal B with the declared torsion levels removed.")
    if multiplier <= 0 or multiplier > multiplier_bound:
        errors.append("The multiplier e is nonpositive or exceeds its declared bound.")
    if cofactor <= 0:
        errors.append("The cofactor f must be positive.")
    if multiplier * reduced_torsion_order != cofactor + reduced_secret_degree:
        errors.append("The relation e B' = f + A' does not hold.")
    if smoothness_bound < 2:
        errors.append("The smoothness bound must be at least two.")
    errors.extend(
        _validate_factorization(
            multiplier,
            certificate["multiplier_factorization"],
            smoothness_bound,
            "multiplier",
        )
    )
    errors.extend(
        _validate_factorization(
            cofactor,
            certificate["cofactor_factorization"],
            smoothness_bound,
            "cofactor",
        )
    )
    if errors:
        return _invalid(case_id, route, derived, errors)
    return CertificateResult(
        case_id,
        CertificateStatus.NUMERICALLY_VALID,
        route,
        derived,
        ("The prime powers, removals, search bounds, smooth factorizations, and e B' = f + A' relation check.",),
    )


def validate_certificate(case_id: str, certificate: dict[str, Any]) -> CertificateResult:
    route = certificate.get("route")
    try:
        if route == "K2-CD":
            return validate_cd(case_id, certificate)
        if route == "K2-MM":
            return validate_mm(case_id, certificate)
    except (KeyError, TypeError, ValueError) as error:
        return CertificateResult(
            case_id,
            CertificateStatus.INVALID,
            str(route) if route is not None else None,
            {},
            (f"Malformed certificate: {error}",),
        )
    return CertificateResult(
        case_id,
        CertificateStatus.UNSUPPORTED_ROUTE,
        str(route) if route is not None else None,
        {},
        ("Only K2-CD and K2-MM numerical certificates are supported.",),
    )


def validate_file(input_path: Path) -> list[CertificateResult]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    return [validate_certificate(case["case_id"], case["certificate"]) for case in raw["cases"]]


def main() -> None:
    problem_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("surface_certificate_cases.json"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    results = validate_file(args.input)
    if args.smoke:
        results = results[:1]
    output = args.output
    if output is None:
        stem = args.input.stem
        if args.smoke:
            stem = f"{stem}_smoke"
        output = problem_dir / "data" / f"surface_certificates_{stem}_20260703.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps([result.as_dict() for result in results], indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
