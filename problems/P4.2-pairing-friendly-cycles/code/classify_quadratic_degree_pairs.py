"""
classify_quadratic_degree_pairs.py - exhaust {3,4,6} multiplier equations.
Sub-goal: P4.2 / SG-15
Inputs:   [--smoke]
Outputs:  data/classify_quadratic_degree_pairs_k3-4-6_<date>.csv
Runtime:  <1 s
Validated against: the MNT multiplier-one families and direct exact orders
"""

from __future__ import annotations

import argparse
import csv
import math
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
DEGREES = (3, 4, 6)
FIRST_LINEAR = {3: -1, 4: 0, 6: 1}
SECOND_LINEAR = {3: 1, 4: 0, 6: -1}


@dataclass(frozen=True, slots=True)
class MultiplierRow:
    degree_e1: int
    degree_e2: int
    multiplier_m: int
    multiplier_n: int
    gap_c: int | None
    field_p: int | None
    field_q: int | None
    equation_a: int
    equation_b: int
    equation_c: int
    status: str
    rejection_reason: str


def _quadratic_roots(a: int, b: int, c: int) -> tuple[int, ...]:
    if a == 0:
        return ()
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return ()
    root = math.isqrt(discriminant)
    if root * root != discriminant:
        return ()
    values: set[int] = set()
    denominator = 2 * a
    for numerator in (-b + root, -b - root):
        if numerator % denominator == 0:
            value = numerator // denominator
            if value > 0:
                values.add(value)
    return tuple(sorted(values))


def _evaluate_factors(degree_e1: int, degree_e2: int, gap: int) -> tuple[int, int]:
    first = gap * gap + FIRST_LINEAR[degree_e1] * gap + 1
    second = gap * gap + SECOND_LINEAR[degree_e2] * gap + 1
    return first, second


def classify_multiplier_equations() -> list[MultiplierRow]:
    """Enumerate every bounded multiplier case from the Hasse proof."""

    rows: list[MultiplierRow] = []
    for degree_e1 in DEGREES:
        for degree_e2 in DEGREES:
            first_linear = FIRST_LINEAR[degree_e1]
            second_linear = SECOND_LINEAR[degree_e2]
            for multiplier_m in range(1, 4):
                for multiplier_n in range(1, 7):
                    equation_a = multiplier_n - multiplier_m
                    equation_b = (
                        multiplier_n * first_linear
                        - multiplier_m * second_linear
                        - multiplier_m * multiplier_n
                    )
                    equation_c = equation_a
                    if equation_a == 0 and equation_b == 0:
                        if (
                            (degree_e1, degree_e2, multiplier_m, multiplier_n)
                            in {(6, 4, 1, 1), (4, 6, 1, 1)}
                        ):
                            status = "infinite_mnt_family"
                            rejection = "none"
                        elif (
                            degree_e1,
                            degree_e2,
                            multiplier_m,
                            multiplier_n,
                        ) == (6, 6, 2, 2):
                            status = "identity_case_rejected"
                            rejection = "parity: odd cyclotomic value cannot equal 2 times odd prime"
                        else:
                            raise AssertionError("unexpected coefficient identity")
                        rows.append(
                            MultiplierRow(
                                degree_e1,
                                degree_e2,
                                multiplier_m,
                                multiplier_n,
                                None,
                                None,
                                None,
                                equation_a,
                                equation_b,
                                equation_c,
                                status,
                                rejection,
                            )
                        )
                        continue
                    for gap in _quadratic_roots(
                        equation_a,
                        equation_b,
                        equation_c,
                    ):
                        if gap % 2:
                            rejection = "gap is odd but odd-prime difference is even"
                            field_p = None
                            field_q = None
                            status = "finite_root_rejected"
                        else:
                            first, second = _evaluate_factors(
                                degree_e1,
                                degree_e2,
                                gap,
                            )
                            if (
                                first % multiplier_m
                                or second % multiplier_n
                            ):
                                rejection = "cyclotomic quotient is not integral"
                                field_p = None
                                field_q = None
                                status = "finite_root_rejected"
                            else:
                                field_q = first // multiplier_m
                                field_p = second // multiplier_n
                                if field_q - field_p != gap:
                                    raise AssertionError("multiplier equation failed")
                                if field_p < 5 or not is_prime(field_p) or not is_prime(field_q):
                                    rejection = "fields are not distinct primes at least 5"
                                    status = "finite_root_rejected"
                                elif (
                                    (gap - 1) ** 2 > 4 * field_p
                                    or (gap + 1) ** 2 > 4 * field_q
                                ):
                                    rejection = "Hasse inequality failed"
                                    status = "finite_root_rejected"
                                else:
                                    exact = (
                                        multiplicative_order_up_to(
                                            field_p,
                                            field_q,
                                            12,
                                        ),
                                        multiplicative_order_up_to(
                                            field_q,
                                            field_p,
                                            12,
                                        ),
                                    )
                                    if exact == (degree_e1, degree_e2):
                                        rejection = "none"
                                        status = "exact_finite_cycle"
                                    else:
                                        rejection = f"exact degrees are {exact}"
                                        status = "finite_root_rejected"
                        rows.append(
                            MultiplierRow(
                                degree_e1,
                                degree_e2,
                                multiplier_m,
                                multiplier_n,
                                gap,
                                field_p,
                                field_q,
                                equation_a,
                                equation_b,
                                equation_c,
                                status,
                                rejection,
                            )
                        )
    return rows


def write_rows(rows: list[MultiplierRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MultiplierRow.__dataclass_fields__))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = classify_multiplier_equations()
    output_path = args.output or (
        PROBLEM_ROOT
        / "data"
        / f"classify_quadratic_degree_pairs_k3-4-6_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output_path)
    exact_finite = sum(row.status == "exact_finite_cycle" for row in rows)
    print(
        f"recorded {len(rows)} identity/root rows; "
        f"exact finite cycles outside symbolic families={exact_finite}"
    )
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
