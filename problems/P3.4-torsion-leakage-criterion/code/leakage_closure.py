"""
leakage_closure.py -- derive a torsion action from point-image records.
Sub-goal: P3.4 / SG-08
Inputs:   --input <JSON>; --output <JSON>; --smoke
Outputs:  data/leakage_closure_<case-set>_20260703.json
Runtime:  <1 second for the bundled fixtures
Validated by: code/tests/test_leakage_closure.py

The coordinates in one record are relative to fixed source and target bases of
E_0[N] and E_1[N].  A ``basis_family_id`` asserts that bases used at different
orders are compatible under the relevant CRT projections.  A ``map_id`` names
one target homomorphism; records with different identifiers are never merged.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from math import gcd
from pathlib import Path
from typing import Any, Iterable


Vector = tuple[int, int]
Matrix = tuple[Vector, Vector]


class ClosureStatus(str, Enum):
    FULL_ACTION = "FULL_ACTION"
    PARTIAL_SPAN = "PARTIAL_SPAN"
    INCONSISTENT_IMAGES = "INCONSISTENT_IMAGES"
    MIXED_TARGET_MAPS = "MIXED_TARGET_MAPS"
    INCOMPATIBLE_BASES = "INCOMPATIBLE_BASES"


@dataclass(frozen=True)
class LeakageRecord:
    map_id: str
    basis_family_id: str
    modulus: int
    source: Vector
    image: Vector

    @classmethod
    def from_mapping(cls, raw: dict[str, Any]) -> "LeakageRecord":
        source = tuple(int(x) for x in raw["source"])
        image = tuple(int(x) for x in raw["image"])
        if len(source) != 2 or len(image) != 2:
            raise ValueError("source and image coordinates must have length two")
        modulus = int(raw["modulus"])
        if modulus <= 1:
            raise ValueError("modulus must be greater than one")
        return cls(
            map_id=str(raw["map_id"]),
            basis_family_id=str(raw["basis_family_id"]),
            modulus=modulus,
            source=(source[0] % modulus, source[1] % modulus),
            image=(image[0] % modulus, image[1] % modulus),
        )


@dataclass(frozen=True)
class ActionCertificate:
    map_id: str
    basis_family_id: str
    modulus: int
    action: Matrix
    record_count: int
    minors: tuple[int, ...]
    span_gcd: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "map_id": self.map_id,
            "basis_family_id": self.basis_family_id,
            "effective_order": self.modulus,
            "action": [list(row) for row in self.action],
            "record_count": self.record_count,
            "source_minors": list(self.minors),
            "span_gcd": self.span_gcd,
        }


@dataclass(frozen=True)
class ClosureResult:
    case_id: str
    status: ClosureStatus
    certificate: ActionCertificate | None
    reasons: tuple[str, ...]
    group_statuses: tuple[dict[str, Any], ...] = ()

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "case_id": self.case_id,
            "status": self.status.value,
            "reasons": list(self.reasons),
            "groups": list(self.group_statuses),
        }
        if self.certificate is not None:
            result["certificate"] = self.certificate.as_dict()
        return result


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return nonnegative g and coefficients x,y with ax + by = g."""
    aa, bb = abs(a), abs(b)
    old_r, r = aa, bb
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    sign_a = -1 if a < 0 else 1
    sign_b = -1 if b < 0 else 1
    return old_r, old_s * sign_a, old_t * sign_b


def bezout_many(values: Iterable[int]) -> tuple[int, tuple[int, ...]]:
    """Return the gcd and one Bezout coefficient for every supplied integer."""
    items = tuple(values)
    if not items:
        raise ValueError("at least one integer is required")
    running_gcd = items[0]
    coefficients = [1]
    for value in items[1:]:
        next_gcd, left, right = _extended_gcd(running_gcd, value)
        coefficients = [left * coefficient for coefficient in coefficients]
        coefficients.append(right)
        running_gcd = next_gcd
    if running_gcd < 0:
        running_gcd = -running_gcd
        coefficients = [-coefficient for coefficient in coefficients]
    return running_gcd, tuple(coefficients)


def source_minors(records: list[LeakageRecord]) -> tuple[int, ...]:
    """Compute all 2-by-2 minors of the matrix of source columns."""
    return tuple(
        records[i].source[0] * records[j].source[1]
        - records[j].source[0] * records[i].source[1]
        for i in range(len(records))
        for j in range(i + 1, len(records))
    )


def _right_inverse_from_minors(
    records: list[LeakageRecord], minors: tuple[int, ...]
) -> list[list[int]]:
    """Construct R with V R = I using a Bezout combination of the minors."""
    modulus = records[0].modulus
    span_gcd, coefficients = bezout_many((modulus, *minors))
    if span_gcd != 1:
        raise ValueError("the source columns do not span the full module")

    right_inverse = [[0, 0] for _ in records]
    minor_index = 0
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            coefficient = coefficients[minor_index + 1]
            xi, yi = records[i].source
            xj, yj = records[j].source
            # The embedded adjugate of [v_i v_j].
            right_inverse[i][0] += coefficient * yj
            right_inverse[i][1] -= coefficient * xj
            right_inverse[j][0] -= coefficient * yi
            right_inverse[j][1] += coefficient * xi
            minor_index += 1
    return [[entry % modulus for entry in row] for row in right_inverse]


def _apply(action: Matrix, vector: Vector, modulus: int) -> Vector:
    return (
        (action[0][0] * vector[0] + action[0][1] * vector[1]) % modulus,
        (action[1][0] * vector[0] + action[1][1] * vector[1]) % modulus,
    )


def derive_action(records: list[LeakageRecord]) -> tuple[ClosureStatus, ActionCertificate | None]:
    """Derive and verify the unique action matrix for one order, if it exists."""
    if not records:
        raise ValueError("at least one leakage record is required")
    map_ids = {record.map_id for record in records}
    basis_ids = {record.basis_family_id for record in records}
    moduli = {record.modulus for record in records}
    if len(map_ids) != 1:
        return ClosureStatus.MIXED_TARGET_MAPS, None
    if len(basis_ids) != 1:
        return ClosureStatus.INCOMPATIBLE_BASES, None
    if len(moduli) != 1:
        raise ValueError("derive_action accepts records at exactly one modulus")

    modulus = records[0].modulus
    minors = source_minors(records)
    span_gcd = gcd(modulus, *(abs(minor) for minor in minors))
    if span_gcd != 1:
        return ClosureStatus.PARTIAL_SPAN, None

    right_inverse = _right_inverse_from_minors(records, minors)
    # W is the 2-by-k matrix of image columns; action = W R.
    action: Matrix = (
        (
            sum(records[index].image[0] * right_inverse[index][0] for index in range(len(records)))
            % modulus,
            sum(records[index].image[0] * right_inverse[index][1] for index in range(len(records)))
            % modulus,
        ),
        (
            sum(records[index].image[1] * right_inverse[index][0] for index in range(len(records)))
            % modulus,
            sum(records[index].image[1] * right_inverse[index][1] for index in range(len(records)))
            % modulus,
        ),
    )
    if any(_apply(action, record.source, modulus) != record.image for record in records):
        return ClosureStatus.INCONSISTENT_IMAGES, None

    return ClosureStatus.FULL_ACTION, ActionCertificate(
        map_id=records[0].map_id,
        basis_family_id=records[0].basis_family_id,
        modulus=modulus,
        action=action,
        record_count=len(records),
        minors=minors,
        span_gcd=span_gcd,
    )


def _crt_pair(a: int, modulus_a: int, b: int, modulus_b: int) -> tuple[int, int]:
    """Combine two compatible congruences, allowing non-coprime moduli."""
    common = gcd(modulus_a, modulus_b)
    if (b - a) % common:
        raise ValueError("incompatible action entries on overlapping primary parts")
    reduced_a = modulus_a // common
    reduced_b = modulus_b // common
    if reduced_b == 1:
        combined_modulus = modulus_a
        return a % combined_modulus, combined_modulus
    inverse = pow(reduced_a, -1, reduced_b)
    multiplier = ((b - a) // common * inverse) % reduced_b
    combined_modulus = modulus_a * reduced_b
    return (a + modulus_a * multiplier) % combined_modulus, combined_modulus


def combine_certificates(certificates: list[ActionCertificate]) -> ActionCertificate:
    """CRT-combine compatible full-action certificates for the same map."""
    if not certificates:
        raise ValueError("at least one action certificate is required")
    if len({certificate.map_id for certificate in certificates}) != 1:
        raise ValueError("cannot combine certificates for different target maps")
    if len({certificate.basis_family_id for certificate in certificates}) != 1:
        raise ValueError("cannot combine certificates in incompatible basis families")

    combined = certificates[0]
    for certificate in certificates[1:]:
        entries: list[int] = []
        combined_modulus: int | None = None
        for row in range(2):
            for column in range(2):
                entry, entry_modulus = _crt_pair(
                    combined.action[row][column],
                    combined.modulus,
                    certificate.action[row][column],
                    certificate.modulus,
                )
                entries.append(entry)
                if combined_modulus is None:
                    combined_modulus = entry_modulus
                elif combined_modulus != entry_modulus:
                    raise AssertionError("CRT produced inconsistent moduli")
        assert combined_modulus is not None
        combined = ActionCertificate(
            map_id=combined.map_id,
            basis_family_id=combined.basis_family_id,
            modulus=combined_modulus,
            action=((entries[0], entries[1]), (entries[2], entries[3])),
            record_count=combined.record_count + certificate.record_count,
            minors=combined.minors + certificate.minors,
            span_gcd=1,
        )
    return combined


def analyze_case(raw: dict[str, Any]) -> ClosureResult:
    """Analyze one fixture and return a machine-readable closure result."""
    case_id = str(raw["case_id"])
    records = [LeakageRecord.from_mapping(item) for item in raw["records"]]
    if not records:
        raise ValueError(f"{case_id}: records must not be empty")
    if len({record.map_id for record in records}) != 1:
        return ClosureResult(
            case_id,
            ClosureStatus.MIXED_TARGET_MAPS,
            None,
            ("Records name more than one target homomorphism and were not aggregated.",),
        )
    if len({record.basis_family_id for record in records}) != 1:
        return ClosureResult(
            case_id,
            ClosureStatus.INCOMPATIBLE_BASES,
            None,
            ("Records do not use one declared CRT-compatible source/target basis family.",),
        )

    grouped: dict[int, list[LeakageRecord]] = {}
    for record in records:
        grouped.setdefault(record.modulus, []).append(record)

    certificates: list[ActionCertificate] = []
    group_statuses: list[dict[str, Any]] = []
    for modulus in sorted(grouped):
        status, certificate = derive_action(grouped[modulus])
        group_statuses.append(
            {
                "modulus": modulus,
                "status": status.value,
                "record_count": len(grouped[modulus]),
            }
        )
        if status == ClosureStatus.INCONSISTENT_IMAGES:
            return ClosureResult(
                case_id,
                status,
                None,
                (f"Image records at modulus {modulus} are not values of one linear map.",),
                tuple(group_statuses),
            )
        if certificate is not None:
            certificates.append(certificate)

    if not certificates:
        return ClosureResult(
            case_id,
            ClosureStatus.PARTIAL_SPAN,
            None,
            ("No modulus group determines a full rank-two action.",),
            tuple(group_statuses),
        )
    try:
        combined = combine_certificates(certificates)
    except ValueError as error:
        return ClosureResult(
            case_id,
            ClosureStatus.INCONSISTENT_IMAGES,
            None,
            (str(error),),
            tuple(group_statuses),
        )
    return ClosureResult(
        case_id,
        ClosureStatus.FULL_ACTION,
        combined,
        ("The source columns span at each retained order and all image equations verify.",),
        tuple(group_statuses),
    )


def analyze_file(input_path: Path) -> list[ClosureResult]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    return [analyze_case(case) for case in raw["cases"]]


def main() -> None:
    problem_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).with_name("leakage_records.json"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    results = analyze_file(args.input)
    if args.smoke:
        results = results[:1]
    output = args.output
    if output is None:
        stem = args.input.stem
        if args.smoke:
            stem = f"{stem}_smoke"
        output = problem_dir / "data" / f"leakage_closure_{stem}_20260703.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps([result.as_dict() for result in results], indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
