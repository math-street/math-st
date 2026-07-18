"""
classify_mixed_degree_pairs.py - exhaust mixed quadratic/quartic 2-cycle pairs.
Sub-goal: P4.2 / SG-16
Inputs:   [--smoke]
Outputs:  data/classify_mixed_degree_pairs_<date>.csv
Runtime:  <1 s
Validated against: the exact (10,3) cycle over fields 7 and 11
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CODE_ROOT = Path(__file__).resolve().parent
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from lib.curves import is_prime  # noqa: E402
from search_two_cycles import multiplicative_order_up_to  # noqa: E402

PROBLEM_ROOT = Path(__file__).resolve().parents[1]
QUADRATIC_DEGREES = (3, 4, 6)
QUARTIC_DEGREES = (5, 8, 10, 12)
PHI: dict[int, tuple[int, ...]] = {
    3: (1, 1, 1),
    4: (1, 0, 1),
    5: (1, 1, 1, 1, 1),
    6: (1, -1, 1),
    8: (1, 0, 0, 0, 1),
    10: (1, -1, 1, -1, 1),
    12: (1, 0, -1, 0, 1),
}


@dataclass(frozen=True, slots=True)
class MixedCaseRow:
    degree_e1: int
    degree_e2: int
    bounded_side: str
    bounded_multiplier: int
    divisor_linear_coefficient: int
    remainder_linear_coefficient: int
    remainder_constant: int
    exhaustive_gap_bound: int | None
    gap_c: int | None
    field_p: int | None
    field_q: int | None
    implicit_multiplier: int | None
    status: str
    rejection_reason: str


def _at_negative(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        coefficient if exponent % 2 == 0 else -coefficient
        for exponent, coefficient in enumerate(coefficients)
    )


def _scale(coefficients: tuple[int, ...], scalar: int) -> list[int]:
    return [scalar * coefficient for coefficient in coefficients]


def _evaluate(coefficients: tuple[int, ...] | list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def _remainder_mod_monic_quadratic(
    coefficients: list[int],
    linear_coefficient: int,
) -> tuple[int, int]:
    """Reduce modulo X^2 + linear_coefficient*X + 1."""

    work = coefficients[:]
    for exponent in range(len(work) - 1, 1, -1):
        leading = work[exponent]
        if not leading:
            continue
        work[exponent] = 0
        work[exponent - 1] -= leading * linear_coefficient
        work[exponent - 2] -= leading
    return work[0], work[1]


def _safe_gap_bound(divisor_linear: int, remainder: tuple[int, int]) -> int:
    constant, linear = remainder
    return abs(divisor_linear) + abs(linear) + abs(constant) + 2


def _classify_candidate(
    *,
    degree_e1: int,
    degree_e2: int,
    bounded_side: str,
    bounded_multiplier: int,
    divisor_linear: int,
    remainder: tuple[int, int],
    gap_bound: int,
    gap: int,
) -> MixedCaseRow:
    first_polynomial = _at_negative(PHI[degree_e1])
    second_polynomial = PHI[degree_e2]
    first_value = _evaluate(first_polynomial, gap)
    second_value = _evaluate(second_polynomial, gap)
    divisor_value = gap * gap + divisor_linear * gap + 1
    if bounded_side == "e2":
        if second_value % bounded_multiplier:
            fields = None
            rejection = "bounded quadratic quotient is not integral"
        else:
            field_p = second_value // bounded_multiplier
            field_q = field_p + gap
            fields = (field_p, field_q)
            rejection = ""
        scaled_target = bounded_multiplier * first_value
    else:
        if first_value % bounded_multiplier:
            fields = None
            rejection = "bounded quadratic quotient is not integral"
        else:
            field_q = first_value // bounded_multiplier
            field_p = field_q - gap
            fields = (field_p, field_q)
            rejection = ""
        scaled_target = bounded_multiplier * second_value

    implicit_multiplier = (
        scaled_target // divisor_value
        if divisor_value and scaled_target % divisor_value == 0
        else None
    )
    if fields is None:
        status = "candidate_rejected"
        field_p = None
        field_q = None
    elif implicit_multiplier is None or implicit_multiplier <= 0:
        status = "candidate_rejected"
        rejection = "quartic divisibility failed"
    elif field_p < 5 or not is_prime(field_p) or not is_prime(field_q):
        status = "candidate_rejected"
        rejection = "fields are not distinct primes at least 5"
    elif (gap - 1) ** 2 > 4 * field_p or (gap + 1) ** 2 > 4 * field_q:
        status = "candidate_rejected"
        rejection = "Hasse inequality failed"
    else:
        exact = (
            multiplicative_order_up_to(field_p, field_q, 12),
            multiplicative_order_up_to(field_q, field_p, 12),
        )
        if exact == (degree_e1, degree_e2):
            status = "exact_cycle"
            rejection = "none"
        else:
            status = "candidate_rejected"
            rejection = f"exact degrees are {exact}"
    return MixedCaseRow(
        degree_e1,
        degree_e2,
        bounded_side,
        bounded_multiplier,
        divisor_linear,
        remainder[1],
        remainder[0],
        gap_bound,
        gap,
        field_p,
        field_q,
        implicit_multiplier,
        status,
        rejection,
    )


def classify_mixed_cases() -> list[MixedCaseRow]:
    """Return a complete certificate for all 108 bounded multiplier cases."""

    rows: list[MixedCaseRow] = []
    for degree_e1 in QUARTIC_DEGREES:
        for degree_e2 in QUADRATIC_DEGREES:
            first = _at_negative(PHI[degree_e1])
            second = PHI[degree_e2]
            for multiplier in range(1, 7):
                divisor_linear = second[1] + multiplier
                remainder = _remainder_mod_monic_quadratic(
                    _scale(first, multiplier),
                    divisor_linear,
                )
                if remainder == (0, 0):
                    rows.append(
                        MixedCaseRow(
                            degree_e1,
                            degree_e2,
                            "e2",
                            multiplier,
                            divisor_linear,
                            0,
                            0,
                            None,
                            None,
                            None,
                            None,
                            None,
                            "identity_remainder",
                            "requires symbolic family analysis",
                        )
                    )
                    continue
                bound = _safe_gap_bound(divisor_linear, remainder)
                candidates = []
                for gap in range(2, bound + 1, 2):
                    divisor_value = gap * gap + divisor_linear * gap + 1
                    remainder_value = remainder[1] * gap + remainder[0]
                    if divisor_value and remainder_value % divisor_value == 0:
                        candidates.append(gap)
                if not candidates:
                    rows.append(
                        MixedCaseRow(
                            degree_e1,
                            degree_e2,
                            "e2",
                            multiplier,
                            divisor_linear,
                            remainder[1],
                            remainder[0],
                            bound,
                            None,
                            None,
                            None,
                            None,
                            "finite_case_empty",
                            "no allowable even gap",
                        )
                    )
                else:
                    rows.extend(
                        _classify_candidate(
                            degree_e1=degree_e1,
                            degree_e2=degree_e2,
                            bounded_side="e2",
                            bounded_multiplier=multiplier,
                            divisor_linear=divisor_linear,
                            remainder=remainder,
                            gap_bound=bound,
                            gap=gap,
                        )
                        for gap in candidates
                    )

    for degree_e1 in QUADRATIC_DEGREES:
        for degree_e2 in QUARTIC_DEGREES:
            first = _at_negative(PHI[degree_e1])
            second = PHI[degree_e2]
            for multiplier in range(1, 4):
                divisor_linear = first[1] - multiplier
                remainder = _remainder_mod_monic_quadratic(
                    _scale(second, multiplier),
                    divisor_linear,
                )
                if remainder == (0, 0):
                    rows.append(
                        MixedCaseRow(
                            degree_e1,
                            degree_e2,
                            "e1",
                            multiplier,
                            divisor_linear,
                            0,
                            0,
                            None,
                            None,
                            None,
                            None,
                            None,
                            "identity_remainder",
                            "requires symbolic family analysis",
                        )
                    )
                    continue
                bound = _safe_gap_bound(divisor_linear, remainder)
                candidates = []
                for gap in range(2, bound + 1, 2):
                    divisor_value = gap * gap + divisor_linear * gap + 1
                    remainder_value = remainder[1] * gap + remainder[0]
                    if divisor_value and remainder_value % divisor_value == 0:
                        candidates.append(gap)
                if not candidates:
                    rows.append(
                        MixedCaseRow(
                            degree_e1,
                            degree_e2,
                            "e1",
                            multiplier,
                            divisor_linear,
                            remainder[1],
                            remainder[0],
                            bound,
                            None,
                            None,
                            None,
                            None,
                            "finite_case_empty",
                            "no allowable even gap",
                        )
                    )
                else:
                    rows.extend(
                        _classify_candidate(
                            degree_e1=degree_e1,
                            degree_e2=degree_e2,
                            bounded_side="e1",
                            bounded_multiplier=multiplier,
                            divisor_linear=divisor_linear,
                            remainder=remainder,
                            gap_bound=bound,
                            gap=gap,
                        )
                        for gap in candidates
                    )
    return rows


def write_rows(rows: list[MixedCaseRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MixedCaseRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = classify_mixed_cases()
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"classify_mixed_degree_pairs_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    identities = sum(row.status == "identity_remainder" for row in rows)
    exact = [row for row in rows if row.status == "exact_cycle"]
    print(
        f"recorded {len(rows)} certificate rows; identities={identities}; "
        f"exact cycles={len(exact)}"
    )
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
