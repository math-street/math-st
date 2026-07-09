"""Search the boundary of the quadratic solving-degree theorem.

The abstract search varies all lower coefficients while retaining the proved
top shape.  The actual search enumerates nonsingular curves and non-base target
x-coordinates on the curve over a quadratic extension.

Sub-goal: P1.3 / SG-09
Inputs: --q, --abstract-trials, and optionally --actual-exhaustive
Outputs: data/search_quadratic_counterexamples_<date>.csv unless overridden
Runtime: about one minute for the exhaustive q=5 search
Validated against: the fixed abstract q=5 counterexample regression test
"""

from __future__ import annotations

import argparse
import csv
import random
import time
from datetime import date
from pathlib import Path

import sympy

from measure_weil_degrees import (
    field_equations,
    solving_degree_exact,
    sympy_groebner,
)
from sparse_weil import (
    FiniteField,
    PrimePolynomial,
    build_weil_coordinate_system,
    curve_is_nonsingular,
    find_irreducible_modulus,
)


FIELDS = [
    "search_space",
    "q",
    "status",
    "candidates_checked",
    "eligible_cases",
    "solving_degree_q_cases",
    "solving_degree_q_plus_1_cases",
    "first_counterexample",
    "seed",
    "elapsed_seconds",
    "engine",
    "engine_version",
    "order",
]


def _from_sympy(expression: sympy.Expr, q: int) -> PrimePolynomial:
    x, y = sympy.symbols("x y")
    return {
        tuple(monomial): int(coefficient) % q
        for monomial, coefficient in sympy.Poly(
            sympy.expand(expression), x, y, modulus=q
        ).terms()
        if int(coefficient) % q
    }


def _solving_degree(core: list[PrimePolynomial], q: int) -> int | None:
    full = [*core, *field_equations(2, q)]
    basis, _ = sympy_groebner(full, 2, q)
    degree, _, _, _ = solving_degree_exact(
        full, basis, 2, q, q + 1, 100_000, 100_000
    )
    return degree


def abstract_core(q: int, coefficients: tuple[int, ...]) -> list[PrimePolynomial]:
    """Return the normalized symmetric core with the required top shape."""
    if len(coefficients) != 8:
        raise ValueError("the abstract core needs eight lower coefficients")
    b, c, d, e, f, g, h, i = coefficients
    x, y = sympy.symbols("x y")
    symmetric_sum = x + y
    symmetric_product = x * y
    return [
        _from_sympy(
            symmetric_product**2
            + b * symmetric_product
            + c * symmetric_sum**2
            + d * symmetric_sum
            + e,
            q,
        ),
        _from_sympy(
            symmetric_product * symmetric_sum
            + f * symmetric_product
            + g * symmetric_sum**2
            + h * symmetric_sum
            + i,
            q,
        ),
    ]


def abstract_search(q: int, trials: int, seed: int) -> dict[str, object]:
    started = time.perf_counter()
    random_source = random.Random(seed)
    q_cases = 0
    q_plus_1_cases = 0
    first_counterexample = ""
    checked = 0
    for index in range(trials):
        coefficients = tuple(random_source.randrange(q) for _ in range(8))
        degree = _solving_degree(abstract_core(q, coefficients), q)
        checked += 1
        if degree == q:
            q_cases += 1
        elif degree == q + 1:
            q_plus_1_cases += 1
            first_counterexample = f"trial={index};coefficients={coefficients}"
            break
    return {
        "search_space": "abstract normalized symmetric top shape",
        "q": q,
        "status": "counterexample found" if q_plus_1_cases else "no counterexample in range",
        "candidates_checked": checked,
        "eligible_cases": checked,
        "solving_degree_q_cases": q_cases,
        "solving_degree_q_plus_1_cases": q_plus_1_cases,
        "first_counterexample": first_counterexample,
        "seed": seed,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "engine": "exact closed Macaulay + SymPy Groebner target",
        "engine_version": sympy.__version__,
        "order": "grevlex(x>y)",
    }


def actual_exhaustive_search(q: int) -> dict[str, object]:
    started = time.perf_counter()
    field = FiniteField(q, find_irreducible_modulus(q, 2))
    elements = list(field.elements())
    nonbase_targets = [target for target in elements if target[1] != 0]
    checked = 0
    eligible = 0
    q_cases = 0
    q_plus_1_cases = 0
    first_counterexample = ""
    for curve_a in elements:
        for curve_b in elements:
            if not curve_is_nonsingular(field, curve_a, curve_b):
                continue
            for target in nonbase_targets:
                checked += 1
                right_hand_side = field.add(
                    field.add(
                        field.mul(field.mul(target, target), target),
                        field.mul(curve_a, target),
                    ),
                    curve_b,
                )
                if not any(field.mul(y_value, y_value) == right_hand_side for y_value in elements):
                    continue
                eligible += 1
                _, coordinates, _ = build_weil_coordinate_system(
                    q, 2, 2, target, curve_a, curve_b
                )
                degree = _solving_degree(
                    [polynomial for polynomial in coordinates if polynomial], q
                )
                if degree == q:
                    q_cases += 1
                elif degree == q + 1:
                    q_plus_1_cases += 1
                    first_counterexample = (
                        f"curve_a={curve_a};curve_b={curve_b};target={target}"
                    )
                    break
                if eligible % 500 == 0:
                    print(
                        f"actual q={q}: checked={checked}, eligible={eligible}",
                        flush=True,
                    )
            if first_counterexample:
                break
        if first_counterexample:
            break
    return {
        "search_space": "actual nonsingular curves and non-base on-curve targets",
        "q": q,
        "status": "counterexample found" if q_plus_1_cases else "exhaustive: no counterexample",
        "candidates_checked": checked,
        "eligible_cases": eligible,
        "solving_degree_q_cases": q_cases,
        "solving_degree_q_plus_1_cases": q_plus_1_cases,
        "first_counterexample": first_counterexample,
        "seed": "",
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "engine": "exact closed Macaulay + SymPy Groebner target",
        "engine_version": sympy.__version__,
        "order": "grevlex(x>y)",
    }


def write_rows(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=int, default=5)
    parser.add_argument("--abstract-trials", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=20_260_722)
    parser.add_argument("--actual-exhaustive", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = [abstract_search(args.q, args.abstract_trials, args.seed)]
    if args.actual_exhaustive:
        rows.append(actual_exhaustive_search(args.q))
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"search_quadratic_counterexamples_{date.today():%Y%m%d}.csv"
    )
    write_rows(rows, output)
    for row in rows:
        print(ascii(row))
    print(f"wrote {len(rows)} rows to {output}")


if __name__ == "__main__":
    main()
