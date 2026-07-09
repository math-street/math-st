"""Measure curve and target variants of the quadratic Semaev descent.

Sub-goals: P1.3 / SG-08 and SG-09
Inputs: --q <odd primes> and bounded curve/target enumeration controls
Outputs: data/measure_quadratic_variants_<date>.csv unless overridden
Runtime: independently bounded by --case-timeout for every explicit case
Validated against: known decompositions, exact top-shape checks, and core-ideal reduction
"""

from __future__ import annotations

import argparse
import csv
import multiprocessing
import time
from datetime import date
from pathlib import Path
from typing import Sequence

import sympy

from measure_toy_degrees import polynomial_degree
from measure_weil_degrees import (
    FIELDS as BASE_FIELDS,
    degree_of_regularity_exact,
    field_equations,
    homogeneous_top,
    measure_case,
    solving_degree_exact,
    sympy_groebner,
)
from sparse_weil import (
    FiniteField,
    PrimePolynomial,
    build_weil_coordinate_system,
    curve_is_nonsingular,
    find_irreducible_modulus,
    known_decomposition_candidates,
)


EXTRA_FIELDS = [
    "case_id",
    "quadratic_top_shape_verified",
    "core_field_equations_redundant",
    "core_field_equation_remainders",
    "core_gb_size",
    "core_gb_max_degree",
    "core_solving_degree",
    "core_field_remainder_max_degree",
    "mutant_degree_of_regularity",
    "mutant_solving_degree",
]
FIELDS = EXTRA_FIELDS + [field for field in BASE_FIELDS if field not in EXTRA_FIELDS]


def _to_sympy(
    polynomial: PrimePolynomial, variables: Sequence[sympy.Symbol]
) -> sympy.Expr:
    return sympy.Add(
        *(
            coefficient
            * sympy.prod(variable**exponent for variable, exponent in zip(variables, monomial))
            for monomial, coefficient in polynomial.items()
        )
    )


def _from_sympy(
    expression: sympy.Expr, variables: Sequence[sympy.Symbol], q: int
) -> PrimePolynomial:
    return {
        tuple(monomial): int(coefficient) % q
        for monomial, coefficient in sympy.Poly(
            expression, *variables, modulus=q
        ).terms()
        if int(coefficient) % q
    }


def analyze_core(
    q: int,
    curve_a: Sequence[int],
    curve_b: Sequence[int],
    target: Sequence[int],
) -> dict[str, object]:
    """Check the proved top shape and whether field equations change the core ideal."""
    _, coordinates, _ = build_weil_coordinate_system(
        q, 2, 2, tuple(target), tuple(curve_a), tuple(curve_b)
    )
    core = [polynomial for polynomial in coordinates if polynomial]
    expected_c = (-2 * int(target[1])) % q
    expected_tops = [
        {(2, 2): 1},
        {(2, 1): expected_c, (1, 2): expected_c},
    ]
    tops = [homogeneous_top(polynomial) for polynomial in core]
    top_shape_verified = tops == expected_tops

    x1, x2 = sympy.symbols("x1 x2")
    variables = (x1, x2)
    basis = sympy.groebner(
        [_to_sympy(polynomial, variables) for polynomial in core],
        *variables,
        modulus=q,
        order="grevlex",
    )
    remainders = [
        sympy.expand(basis.reduce(_to_sympy(equation, variables))[1])
        for equation in field_equations(2, q)
    ]
    redundant = all(remainder == 0 for remainder in remainders)
    core_basis = [_from_sympy(item.as_expr(), variables, q) for item in basis.polys]
    core_solving, _, _, _ = solving_degree_exact(
        core,
        core_basis,
        2,
        q,
        5,
        10_000,
        10_000,
    )
    remainder_polynomials = [
        _from_sympy(remainder, variables, q)
        for remainder in remainders
        if remainder != 0
    ]
    mutant_family = [*core_basis, *remainder_polynomials]
    mutant_regularity, _ = degree_of_regularity_exact(
        mutant_family,
        2,
        q,
        5,
        10_000,
        10_000,
    )
    mutant_basis, _ = sympy_groebner(mutant_family, 2, q)
    mutant_solving, _, _, _ = solving_degree_exact(
        mutant_family,
        mutant_basis,
        2,
        q,
        5,
        10_000,
        10_000,
    )
    return {
        "quadratic_top_shape_verified": top_shape_verified,
        "core_field_equations_redundant": redundant,
        "core_field_equation_remainders": ";".join(str(item) for item in remainders),
        "core_gb_size": len(basis.polys),
        "core_gb_max_degree": max(
            sympy.Poly(polynomial, *variables, modulus=q).total_degree()
            for polynomial in basis.polys
        ),
        "core_solving_degree": core_solving,
        "core_field_remainder_max_degree": max(
            (polynomial_degree(item) for item in remainder_polynomials),
            default=0,
        ),
        "mutant_degree_of_regularity": mutant_regularity,
        "mutant_solving_degree": mutant_solving,
    }


def enumerate_cases(
    q: int,
    a0_count: int,
    a1_values: Sequence[int],
    b0_count: int,
    b1_values: Sequence[int],
    targets_per_curve: int,
) -> list[dict[str, object]]:
    field = FiniteField(q, find_irreducible_modulus(q, 2))
    cases: list[dict[str, object]] = []
    for a0 in range(min(a0_count, q)):
        for a1 in a1_values:
            for b0 in range(min(b0_count, q)):
                for b1 in b1_values:
                    curve_a = (a0 % q, a1 % q)
                    curve_b = (b0 % q, b1 % q)
                    if not curve_is_nonsingular(field, curve_a, curve_b):
                        continue
                    candidates = known_decomposition_candidates(
                        field,
                        2,
                        curve_a,
                        curve_b,
                        require_nonbase_target=True,
                        limit=targets_per_curve,
                    )
                    for target_index, (values, target) in enumerate(candidates):
                        cases.append(
                            {
                                "case_id": (
                                    f"q{q}-a{a0}_{a1}-b{b0}_{b1}-t{target_index}"
                                ),
                                "q": q,
                                "curve_a": curve_a,
                                "curve_b": curve_b,
                                "target": target,
                                "known_values": values,
                            }
                        )
    return cases


def measure_variant(
    case: dict[str, object],
    degree_ceiling: int,
    column_ceiling: int,
    row_ceiling: int,
    case_timeout: float,
) -> dict[str, object]:
    q = int(case["q"])
    curve_a = tuple(case["curve_a"])  # type: ignore[arg-type]
    curve_b = tuple(case["curve_b"])  # type: ignore[arg-type]
    target = tuple(case["target"])  # type: ignore[arg-type]
    row = measure_case(
        q,
        2,
        2,
        "known_variant",
        degree_ceiling,
        column_ceiling,
        row_ceiling,
        case_timeout,
        curve_a_coordinates=curve_a,
        curve_b_coordinates=curve_b,
        target_coordinates=target,
        known_values_override=case["known_values"],  # type: ignore[arg-type]
    )
    row.update(analyze_core(q, curve_a, curve_b, target))
    row["case_id"] = case["case_id"]
    return row


def _worker(
    case: dict[str, object],
    degree_ceiling: int,
    column_ceiling: int,
    row_ceiling: int,
    case_timeout: float,
    queue: multiprocessing.Queue,  # type: ignore[type-arg]
) -> None:
    try:
        queue.put(
            measure_variant(
                case,
                degree_ceiling,
                column_ceiling,
                row_ceiling,
                case_timeout,
            )
        )
    except Exception as error:
        queue.put(
            {
                "case_id": case["case_id"],
                "q": case["q"],
                "n": 2,
                "m": 2,
                "target_mode": "known_variant",
                "status": f"error: {type(error).__name__}: {error}",
            }
        )


def run_with_timeout(
    case: dict[str, object],
    degree_ceiling: int,
    column_ceiling: int,
    row_ceiling: int,
    case_timeout: float,
) -> dict[str, object]:
    if case_timeout <= 0:
        return measure_variant(
            case,
            degree_ceiling,
            column_ceiling,
            row_ceiling,
            case_timeout,
        )
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    process = context.Process(
        target=_worker,
        args=(
            case,
            degree_ceiling,
            column_ceiling,
            row_ceiling,
            case_timeout,
            queue,
        ),
    )
    started = time.perf_counter()
    process.start()
    process.join(case_timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "case_id": case["case_id"],
            "q": case["q"],
            "n": 2,
            "m": 2,
            "target_mode": "known_variant",
            "status": f"censored: wall clock exceeded {case_timeout:g}s",
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "case_timeout_seconds": case_timeout,
        }
    if process.exitcode != 0:
        raise RuntimeError(f"variant worker exited with code {process.exitcode}")
    return queue.get()


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=int, nargs="+", default=[5, 7])
    parser.add_argument("--a0-count", type=int, default=3)
    parser.add_argument("--a1-values", type=int, nargs="+", default=[1])
    parser.add_argument("--b0-count", type=int, default=3)
    parser.add_argument("--b1-values", type=int, nargs="+", default=[0, 1])
    parser.add_argument("--targets-per-curve", type=int, default=2)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--degree-ceiling", type=int, default=12)
    parser.add_argument("--column-ceiling", type=int, default=20_000)
    parser.add_argument("--row-ceiling", type=int, default=80_000)
    parser.add_argument("--case-timeout", type=float, default=30.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.smoke:
        args.q = [5]
        args.a0_count = 1
        args.a1_values = [1]
        args.b0_count = 2
        args.b1_values = [0]
        args.targets_per_curve = 1
        args.max_cases = 1
    cases = [
        case
        for q in args.q
        for case in enumerate_cases(
            q,
            args.a0_count,
            args.a1_values,
            args.b0_count,
            args.b1_values,
            args.targets_per_curve,
        )
    ]
    if args.max_cases > 0:
        cases = cases[: args.max_cases]
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"measure_quadratic_variants_{date.today():%Y%m%d}.csv"
    )
    rows: list[dict[str, object]] = []
    for case in cases:
        row = run_with_timeout(
            case,
            args.degree_ceiling,
            args.column_ceiling,
            args.row_ceiling,
            args.case_timeout,
        )
        rows.append(row)
        write_rows(rows, output)
        print(ascii(row), flush=True)
    print(f"wrote {len(rows)} variant rows to {output}")


if __name__ == "__main__":
    main()
