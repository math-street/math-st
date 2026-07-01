"""Build tiny Weil systems and compare exact first-fall, regularity, and solving degrees.

Sub-goals: P1.3 / SG-03 through SG-06
Inputs:   --q <primes> --n <2 3> --m <2 3 4> --modes <known external>
Outputs:  data/measure_weil_degrees_<date>.csv unless --output is supplied
Runtime:  bounded per case by --case-timeout; --smoke runs one small case
Validated against: constructed elliptic-curve decompositions and exact Macaulay tests
"""

from __future__ import annotations

import argparse
import csv
import multiprocessing
import platform
import queue as queue_module
import sys
import time
from datetime import date
from pathlib import Path
from typing import Sequence

import sympy

from measure_toy_degrees import (
    MacaulaySpace,
    closed_macaulay_space,
    in_rowspace,
    monomials_exact_degree,
    polynomial_degree,
    rref_mod_prime,
)
from sparse_weil import (
    FiniteField,
    PrimePolynomial,
    build_weil_coordinate_system,
    curve_is_nonsingular,
    evaluate_prime_polynomial,
    find_irreducible_modulus,
    first_nonbase_target_x,
    known_decomposition,
)


FIELDS = [
    "q",
    "n",
    "m",
    "target_mode",
    "status",
    "stage_completed",
    "modulus",
    "curve_a_coordinates",
    "curve_b_coordinates",
    "target_coordinates",
    "known_solution",
    "known_solution_verified",
    "core_equation_count",
    "core_degrees",
    "core_term_counts",
    "first_fall_degree",
    "first_fall_status",
    "degree_of_regularity",
    "regularity_status",
    "solving_degree",
    "solving_status",
    "solving_minus_first_fall",
    "gb_size",
    "gb_max_degree",
    "max_macaulay_columns",
    "max_macaulay_rank",
    "order",
    "engine",
    "engine_version",
    "field_equations_in_solving_system",
    "function_reduction",
    "degree_ceiling",
    "column_ceiling",
    "row_ceiling",
    "elapsed_seconds",
    "case_timeout_seconds",
    "python_version",
    "platform",
]


class DegreeResourceLimit(RuntimeError):
    """Raised when an exact degree computation crosses a declared size ceiling."""


def homogeneous_top(poly: PrimePolynomial) -> PrimePolynomial:
    degree = polynomial_degree(poly)
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if sum(monomial) == degree
    }


def bounded_monomials(nvars: int, degree: int, q: int) -> list[tuple[int, ...]]:
    return [
        monomial
        for monomial in monomials_exact_degree(nvars, degree)
        if all(exponent < q for exponent in monomial)
    ]


def multiply_in_truncated_ring(
    left: PrimePolynomial, right: PrimePolynomial, q: int
) -> PrimePolynomial:
    result: PrimePolynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left + right
                for left, right in zip(left_monomial, right_monomial, strict=True)
            )
            if any(exponent >= q for exponent in monomial):
                continue
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            ) % q
            if result[monomial] == 0:
                del result[monomial]
    return result


def power_in_truncated_ring(poly: PrimePolynomial, exponent: int, q: int) -> PrimePolynomial:
    if not poly:
        return {}
    nvars = len(next(iter(poly)))
    result: PrimePolynomial = {(0,) * nvars: 1}
    base = poly
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = multiply_in_truncated_ring(result, base, q)
        base = multiply_in_truncated_ring(base, base, q)
        remaining >>= 1
    return result


def multiply_by_bounded_monomial(
    poly: PrimePolynomial, multiplier: tuple[int, ...], q: int
) -> PrimePolynomial:
    return multiply_in_truncated_ring(poly, {multiplier: 1}, q)


def first_fall_degree_exact(
    generators: Sequence[PrimePolynomial],
    nvars: int,
    q: int,
    degree_ceiling: int,
    column_ceiling: int,
) -> tuple[int | None, str]:
    """Compute Syz(F_top)_d / Triv(F_top)_d in B=F_q[x]/(x_i^q)."""
    tops = [homogeneous_top(poly) for poly in generators if poly]
    if not tops:
        return None, "undefined: no nonzero core equations"
    degrees = [polynomial_degree(poly) for poly in tops]
    quotient_syzygies = [power_in_truncated_ring(poly, q - 1, q) for poly in tops]
    for degree in range(min(degrees), degree_ceiling + 1):
        output_columns = bounded_monomials(nvars, degree, q)
        domain: list[tuple[int, tuple[int, ...]]] = []
        for generator_index, generator_degree in enumerate(degrees):
            if generator_degree <= degree:
                domain.extend(
                    (generator_index, monomial)
                    for monomial in bounded_monomials(
                        nvars, degree - generator_degree, q
                    )
                )
        if len(domain) > column_ceiling:
            raise DegreeResourceLimit(
                f"first-fall domain {len(domain)} exceeds {column_ceiling} at degree {degree}"
            )
        domain_index = {item: index for index, item in enumerate(domain)}
        map_rows: list[list[int]] = []
        for generator_index, multiplier in domain:
            product_poly = multiply_by_bounded_monomial(
                tops[generator_index], multiplier, q
            )
            map_rows.append(
                [product_poly.get(monomial, 0) % q for monomial in output_columns]
            )
        map_rank = len(rref_mod_prime(map_rows, q))
        syzygy_dimension = len(domain) - map_rank

        trivial_vectors: list[list[int]] = []
        for left in range(len(tops)):
            for right in range(left + 1, len(tops)):
                base_degree = degrees[left] + degrees[right]
                if base_degree > degree:
                    continue
                for multiplier in bounded_monomials(nvars, degree - base_degree, q):
                    vector = [0] * len(domain)
                    right_component = multiply_by_bounded_monomial(tops[left], multiplier, q)
                    left_component = multiply_by_bounded_monomial(tops[right], multiplier, q)
                    for monomial, coefficient in right_component.items():
                        key = (right, monomial)
                        if key in domain_index:
                            vector[domain_index[key]] = (
                                vector[domain_index[key]] + coefficient
                            ) % q
                    for monomial, coefficient in left_component.items():
                        key = (left, monomial)
                        if key in domain_index:
                            vector[domain_index[key]] = (
                                vector[domain_index[key]] - coefficient
                            ) % q
                    if any(vector):
                        trivial_vectors.append(vector)

        for generator_index, (generator_degree, quotient_syzygy) in enumerate(
            zip(degrees, quotient_syzygies, strict=True)
        ):
            base_degree = q * generator_degree
            if base_degree > degree or not quotient_syzygy:
                continue
            for multiplier in bounded_monomials(nvars, degree - base_degree, q):
                component = multiply_by_bounded_monomial(quotient_syzygy, multiplier, q)
                vector = [0] * len(domain)
                for monomial, coefficient in component.items():
                    key = (generator_index, monomial)
                    if key in domain_index:
                        vector[domain_index[key]] = coefficient % q
                if any(vector):
                    trivial_vectors.append(vector)

        trivial_rank = len(rref_mod_prime(trivial_vectors, q))
        if syzygy_dimension > trivial_rank:
            return degree, (
                f"exact: kernel dimension {syzygy_dimension}, "
                f"trivial rank {trivial_rank}"
            )
    return None, f"not found through degree {degree_ceiling}"


def degree_of_regularity_exact(
    generators: Sequence[PrimePolynomial],
    nvars: int,
    q: int,
    degree_ceiling: int,
    row_ceiling: int,
    column_ceiling: int,
) -> tuple[int | None, str]:
    tops = [homogeneous_top(poly) for poly in generators if poly]
    degrees = [polynomial_degree(poly) for poly in tops]
    for degree in range(min(degrees), degree_ceiling + 1):
        columns = monomials_exact_degree(nvars, degree)
        if len(columns) > column_ceiling:
            raise DegreeResourceLimit(
                f"regularity columns {len(columns)} exceed {column_ceiling} at degree {degree}"
            )
        rows: list[list[int]] = []
        for top, top_degree in zip(tops, degrees, strict=True):
            if top_degree > degree:
                continue
            for multiplier in monomials_exact_degree(nvars, degree - top_degree):
                product_poly: PrimePolynomial = {}
                for monomial, coefficient in top.items():
                    product_monomial = tuple(
                        left + right
                        for left, right in zip(monomial, multiplier, strict=True)
                    )
                    product_poly[product_monomial] = coefficient % q
                rows.append([product_poly.get(column, 0) for column in columns])
                if len(rows) > row_ceiling:
                    raise DegreeResourceLimit(
                        f"regularity rows exceed {row_ceiling} at degree {degree}"
                    )
        if len(rref_mod_prime(rows, q)) == len(columns):
            return degree, f"exact: homogeneous rank fills {len(columns)} columns"
    return None, f"not found through degree {degree_ceiling}"


def field_equations(nvars: int, q: int) -> list[PrimePolynomial]:
    equations: list[PrimePolynomial] = []
    for variable in range(nvars):
        high = tuple(q if index == variable else 0 for index in range(nvars))
        low = tuple(1 if index == variable else 0 for index in range(nvars))
        equations.append({high: 1, low: -1})
    return equations


def sympy_groebner(
    generators: Sequence[PrimePolynomial], nvars: int, q: int
) -> tuple[list[PrimePolynomial], list[str]]:
    variables = sympy.symbols(" ".join(f"x{index + 1}" for index in range(nvars)))
    if nvars == 1:
        variables = (variables,)
    expressions = []
    for poly in generators:
        expression = 0
        for monomial, coefficient in poly.items():
            term = coefficient
            for variable, exponent in zip(variables, monomial, strict=True):
                term *= variable**exponent
            expression += term
        expressions.append(expression)
    basis = sympy.groebner(
        expressions, *variables, order="grevlex", modulus=q
    )
    dictionaries = [
        {
            tuple(monomial): int(coefficient) % q
            for monomial, coefficient in item.terms()
            if int(coefficient) % q
        }
        for item in basis.polys
    ]
    return dictionaries, [str(item.as_expr()) for item in basis.polys]


def solving_degree_exact(
    generators: Sequence[PrimePolynomial],
    target_basis: Sequence[PrimePolynomial],
    nvars: int,
    q: int,
    degree_ceiling: int,
    row_ceiling: int,
    column_ceiling: int,
) -> tuple[int | None, str, int, int]:
    start = max(polynomial_degree(poly) for poly in target_basis)
    maximum_columns = 0
    maximum_rank = 0
    for degree in range(start, degree_ceiling + 1):
        column_count = sum(
            len(monomials_exact_degree(nvars, value)) for value in range(degree + 1)
        )
        if column_count > column_ceiling:
            raise DegreeResourceLimit(
                f"Macaulay columns {column_count} exceed {column_ceiling} at degree {degree}"
            )
        estimated_rows = sum(
            sum(
                len(monomials_exact_degree(nvars, value))
                for value in range(degree - polynomial_degree(generator) + 1)
            )
            for generator in generators
            if polynomial_degree(generator) <= degree
        )
        if estimated_rows > row_ceiling:
            raise DegreeResourceLimit(
                f"initial Macaulay rows {estimated_rows} exceed {row_ceiling} at degree {degree}"
            )
        space: MacaulaySpace = closed_macaulay_space(
            list(generators), nvars, degree, q
        )
        maximum_columns = max(maximum_columns, len(space.columns))
        maximum_rank = max(maximum_rank, space.rank)
        if all(
            polynomial_degree(item) <= degree
            and in_rowspace(item, space.rows, space.columns, q)
            for item in target_basis
        ):
            return degree, f"exact: Gröbner basis contained at cutoff {degree}", maximum_columns, maximum_rank
    return (
        None,
        f"not found through degree {degree_ceiling}",
        maximum_columns,
        maximum_rank,
    )


def measure_case(
    q: int,
    n: int,
    m: int,
    target_mode: str,
    degree_ceiling: int,
    column_ceiling: int,
    row_ceiling: int,
    case_timeout: float,
    progress_queue: multiprocessing.Queue | None = None,  # type: ignore[type-arg]
    curve_a_coordinates: Sequence[int] | None = None,
    curve_b_coordinates: Sequence[int] | None = None,
    target_coordinates: Sequence[int] | None = None,
    known_values_override: Sequence[int] | None = None,
) -> dict[str, object]:
    started = time.perf_counter()
    field = FiniteField(q, find_irreducible_modulus(q, n))
    curve_a = field.element(
        curve_a_coordinates
        if curve_a_coordinates is not None
        else (0, 1, *([0] * (n - 2)))
    )
    curve_b = field.element(
        curve_b_coordinates if curve_b_coordinates is not None else field.one
    )
    if not curve_is_nonsingular(field, curve_a, curve_b):
        raise ValueError("singular short-Weierstrass curve")
    known_values: list[int] = []
    if target_coordinates is not None:
        target = field.element(target_coordinates)
        known_values = list(known_values_override or [])
    elif target_mode == "known":
        known_values, target = known_decomposition(
            field,
            m,
            curve_a,
            curve_b,
            require_nonbase_target=True,
        )
    elif target_mode == "external":
        target = first_nonbase_target_x(field, curve_a, curve_b)
    else:
        raise ValueError(f"unknown target mode {target_mode}")

    if progress_queue is not None:
        progress_queue.put(
            {
                "_progress": True,
                "stage_completed": "target_selection",
                "modulus": ";".join(str(value) for value in field.modulus),
                "curve_a_coordinates": ";".join(str(value) for value in curve_a),
                "curve_b_coordinates": ";".join(str(value) for value in curve_b),
                "target_coordinates": ";".join(str(value) for value in target),
                "known_solution": ";".join(str(value) for value in known_values),
            }
        )

    _, coordinates, extension_polynomial = build_weil_coordinate_system(
        q, n, m, target, curve_a, curve_b
    )
    core = [poly for poly in coordinates if poly]
    known_verified: bool | str = ""
    if known_values:
        known_verified = all(
            evaluate_prime_polynomial(poly, known_values, q) == 0 for poly in core
        ) and extension_polynomial.evaluate(
            [field.element(value) for value in known_values]
        ) == field.zero

    partial: dict[str, object] = {
        "stage_completed": "system_build",
        "modulus": ";".join(str(value) for value in field.modulus),
        "curve_a_coordinates": ";".join(str(value) for value in curve_a),
        "curve_b_coordinates": ";".join(str(value) for value in curve_b),
        "target_coordinates": ";".join(str(value) for value in target),
        "known_solution": ";".join(str(value) for value in known_values),
        "known_solution_verified": known_verified,
        "core_equation_count": len(core),
        "core_degrees": ";".join(str(polynomial_degree(poly)) for poly in core),
        "core_term_counts": ";".join(str(len(poly)) for poly in core),
    }
    if progress_queue is not None:
        progress_queue.put({"_progress": True, **partial})

    first_fall, first_fall_status = first_fall_degree_exact(
        core, m, q, degree_ceiling, column_ceiling
    )
    partial.update(
        {
            "stage_completed": "first_fall",
            "first_fall_degree": "" if first_fall is None else first_fall,
            "first_fall_status": first_fall_status,
        }
    )
    if progress_queue is not None:
        progress_queue.put({"_progress": True, **partial})
    full_system = [*core, *field_equations(m, q)]
    regularity, regularity_status = degree_of_regularity_exact(
        full_system, m, q, degree_ceiling, row_ceiling, column_ceiling
    )
    partial.update(
        {
            "stage_completed": "degree_of_regularity",
            "degree_of_regularity": "" if regularity is None else regularity,
            "regularity_status": regularity_status,
        }
    )
    if progress_queue is not None:
        progress_queue.put({"_progress": True, **partial})
    groebner_basis, _ = sympy_groebner(full_system, m, q)
    partial.update(
        {
            "stage_completed": "groebner_basis",
            "gb_size": len(groebner_basis),
            "gb_max_degree": max(polynomial_degree(poly) for poly in groebner_basis),
        }
    )
    if progress_queue is not None:
        progress_queue.put({"_progress": True, **partial})
    solving, solving_status, max_columns, max_rank = solving_degree_exact(
        full_system,
        groebner_basis,
        m,
        q,
        degree_ceiling,
        row_ceiling,
        column_ceiling,
    )
    difference: int | str = ""
    if first_fall is not None and solving is not None:
        difference = solving - first_fall
    return {
        "q": q,
        "n": n,
        "m": m,
        "target_mode": target_mode,
        "status": "complete",
        "stage_completed": "solving_degree",
        "modulus": ";".join(str(value) for value in field.modulus),
        "curve_a_coordinates": ";".join(str(value) for value in curve_a),
        "curve_b_coordinates": ";".join(str(value) for value in curve_b),
        "target_coordinates": ";".join(str(value) for value in target),
        "known_solution": ";".join(str(value) for value in known_values),
        "known_solution_verified": known_verified,
        "core_equation_count": len(core),
        "core_degrees": ";".join(str(polynomial_degree(poly)) for poly in core),
        "core_term_counts": ";".join(str(len(poly)) for poly in core),
        "first_fall_degree": "" if first_fall is None else first_fall,
        "first_fall_status": first_fall_status,
        "degree_of_regularity": "" if regularity is None else regularity,
        "regularity_status": regularity_status,
        "solving_degree": "" if solving is None else solving,
        "solving_status": solving_status,
        "solving_minus_first_fall": difference,
        "gb_size": len(groebner_basis),
        "gb_max_degree": max(polynomial_degree(poly) for poly in groebner_basis),
        "max_macaulay_columns": max_columns,
        "max_macaulay_rank": max_rank,
        "order": "grevlex(x1>...>xm)",
        "engine": "exact closed Macaulay + SymPy groebner target",
        "engine_version": sympy.__version__,
        "field_equations_in_solving_system": True,
        "function_reduction": "x_i^q=x_i applied to core during construction",
        "degree_ceiling": degree_ceiling,
        "column_ceiling": column_ceiling,
        "row_ceiling": row_ceiling,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "case_timeout_seconds": case_timeout,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }


def _case_worker(arguments: tuple[object, ...], queue: multiprocessing.Queue) -> None:  # type: ignore[type-arg]
    try:
        queue.put(measure_case(*arguments, progress_queue=queue))
    except Exception as error:  # exception text is data; errors are not silently ignored
        queue.put({"status": f"error: {type(error).__name__}: {error}"})


def run_case_with_timeout(
    q: int,
    n: int,
    m: int,
    target_mode: str,
    degree_ceiling: int,
    column_ceiling: int,
    row_ceiling: int,
    timeout_seconds: float,
) -> dict[str, object]:
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    arguments: tuple[object, ...] = (
        q,
        n,
        m,
        target_mode,
        degree_ceiling,
        column_ceiling,
        row_ceiling,
        timeout_seconds,
    )
    process = context.Process(target=_case_worker, args=(arguments, queue))
    process.start()
    process.join(timeout_seconds)
    prefix: dict[str, object] = {
        "q": q,
        "n": n,
        "m": m,
        "target_mode": target_mode,
        "degree_ceiling": degree_ceiling,
        "column_ceiling": column_ceiling,
        "row_ceiling": row_ceiling,
        "case_timeout_seconds": timeout_seconds,
        "order": "grevlex(x1>...>xm)",
        "engine": "exact closed Macaulay + SymPy groebner target",
        "engine_version": sympy.__version__,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }
    timed_out = process.is_alive()
    if timed_out:
        process.terminate()
        process.join()
    messages: list[dict[str, object]] = []
    while True:
        try:
            messages.append(queue.get_nowait())
        except queue_module.Empty:
            break
    progress: dict[str, object] = {}
    final: dict[str, object] | None = None
    for message in messages:
        if message.pop("_progress", False):
            progress.update(message)
        else:
            final = message
    if timed_out:
        return {
            **prefix,
            **progress,
            "status": f"censored: wall clock exceeded {timeout_seconds:g}s",
        }
    if final is None:
        return {
            **prefix,
            **progress,
            "status": f"error: worker exited with code {process.exitcode}",
        }
    return {**prefix, **final}


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=int, nargs="+", default=[3, 5, 7])
    parser.add_argument("--n", type=int, nargs="+", default=[2, 3])
    parser.add_argument("--m", type=int, nargs="+", default=[2, 3, 4])
    parser.add_argument("--modes", nargs="+", default=["known", "external"])
    parser.add_argument("--degree-ceiling", type=int, default=16)
    parser.add_argument("--column-ceiling", type=int, default=8_000)
    parser.add_argument("--row-ceiling", type=int, default=30_000)
    parser.add_argument("--case-timeout", type=float, default=30.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = [(3, 2, 2, "known")] if args.smoke else [
        (q, n, m, mode)
        for q in args.q
        for n in args.n
        for m in args.m
        for mode in args.modes
    ]
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"measure_weil_degrees_{date.today():%Y%m%d}.csv"
    )
    rows: list[dict[str, object]] = []
    for q, n, m, mode in cases:
        row = run_case_with_timeout(
            q,
            n,
            m,
            mode,
            args.degree_ceiling,
            args.column_ceiling,
            args.row_ceiling,
            args.case_timeout,
        )
        rows.append(row)
        write_rows(rows, output)
        print(ascii(row), flush=True)
    print(f"output: {output}")


if __name__ == "__main__":
    main()
