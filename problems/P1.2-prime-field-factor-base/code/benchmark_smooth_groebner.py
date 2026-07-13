"""
benchmark_smooth_groebner.py — Benchmark subgroup constraints with SymPy.
Sub-goal: P1.2 / SG-11
Inputs:   --timeout, --include-large, --smoke; worker fixture arguments
Outputs:  data/benchmark_smooth_groebner_<params>_<date>.csv
Runtime:  about 12 s by default or 24 s with --include-large at --timeout 5
Validated against: a known p=17 solution annihilating every direct/chain equation
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

import sympy

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import AffinePoint, Curve
from lib.semaev import f4_value
from measure_smooth_subgroup import factor_base_from_x, subgroup_elements


FIELDS = (
    "date",
    "sympy_version",
    "p",
    "a",
    "b",
    "r",
    "subgroup_order",
    "encoding",
    "status",
    "timeout_s",
    "system_build_s",
    "variables",
    "equations",
    "input_max_total_degree",
    "input_terms",
    "basis_polynomials",
    "basis_max_total_degree",
    "basis_terms",
    "elapsed_s",
    "target_x",
)


FIXTURES = (
    (17, 2, 11, 11, 4),
    (257, 127, 216, 241, 16),
)
LARGE_FIXTURE = (65537, 31771, 14358, 65809, 64)


def symbolic_f4(x1: Any, x2: Any, x3: Any, x4: int, a: int, b: int) -> Any:
    first_a = (x1 - x2) ** 2
    first_b = -2 * ((x1 + x2) * (x1 * x2 + a) + 2 * b)
    first_c = (x1 * x2 - a) ** 2 - 4 * b * (x1 + x2)
    second_a = (x3 - x4) ** 2
    second_b = -2 * ((x3 + x4) * (x3 * x4 + a) + 2 * b)
    second_c = (x3 * x4 - a) ** 2 - 4 * b * (x3 + x4)
    return sympy.expand(
        (first_a * second_c - first_c * second_a) ** 2
        - (first_a * second_b - first_b * second_a)
        * (first_b * second_c - first_c * second_b)
    )


def first_affine_target(curve: Curve, factor_base: list[AffinePoint]) -> tuple[tuple[AffinePoint, ...], AffinePoint]:
    for terms in itertools.product(factor_base, repeat=3):
        target = curve.add(curve.add(terms[0], terms[1]), terms[2])
        if target is not None:
            return terms, target
    raise ArithmeticError("factor base produced no affine three-sum target")


def build_system(
    p: int,
    a: int,
    b: int,
    subgroup_order: int,
    encoding: str,
) -> tuple[list[Any], tuple[Any, ...], int]:
    curve = Curve(p, a, b)
    factor_base = factor_base_from_x(curve, subgroup_elements(p, subgroup_order))
    terms, target = first_affine_target(curve, factor_base)
    assert target is not None
    if f4_value(
        terms[0][0], terms[1][0], terms[2][0], target[0], a, b, p
    ) != 0:
        raise ArithmeticError("known decomposition did not satisfy f4")

    x_variables = sympy.symbols("x1 x2 x3")
    equations: list[Any] = [symbolic_f4(*x_variables, target[0], a, b)]
    generators: list[Any] = list(x_variables)
    if encoding == "direct":
        equations.extend(variable**subgroup_order - 1 for variable in x_variables)
    elif encoding == "chain":
        chain_length = subgroup_order.bit_length() - 1
        if 1 << chain_length != subgroup_order:
            raise ValueError("chain encoding requires a power-of-two subgroup order")
        for variable_index, variable in enumerate(x_variables, start=1):
            current = variable
            for step in range(1, chain_length):
                next_variable = sympy.Symbol(f"z{variable_index}_{step}")
                equations.append(next_variable - current**2)
                generators.append(next_variable)
                current = next_variable
            equations.append(current**2 - 1)
    else:
        raise ValueError("unknown encoding")
    return equations, tuple(generators), target[0]


def polynomial_stats(polynomials: list[Any], generators: tuple[Any, ...], p: int) -> tuple[int, int]:
    converted = [sympy.Poly(polynomial, *generators, modulus=p) for polynomial in polynomials]
    return max(polynomial.total_degree() for polynomial in converted), sum(
        len(polynomial.terms()) for polynomial in converted
    )


def worker(args: argparse.Namespace) -> None:
    equations, generators, target_x = build_system(
        args.p, args.a, args.b, args.subgroup_order, args.encoding
    )
    input_degree, input_terms = polynomial_stats(equations, generators, args.p)
    started = time.perf_counter()
    basis = sympy.groebner(
        equations,
        *generators,
        modulus=args.p,
        order="grevlex",
    )
    elapsed_s = time.perf_counter() - started
    basis_expressions = list(basis)
    basis_degree, basis_terms = polynomial_stats(basis_expressions, generators, args.p)
    print(
        json.dumps(
            {
                "variables": len(generators),
                "equations": len(equations),
                "input_max_total_degree": input_degree,
                "input_terms": input_terms,
                "basis_polynomials": len(basis_expressions),
                "basis_max_total_degree": basis_degree,
                "basis_terms": basis_terms,
                "elapsed_s": elapsed_s,
                "target_x": target_x,
            }
        )
    )


def benchmark_fixture(
    fixture: tuple[int, int, int, int, int],
    encoding: str,
    timeout_s: float,
) -> dict[str, Any]:
    p, a, b, order, subgroup_order = fixture
    build_started = time.perf_counter()
    equations, generators, target_x = build_system(p, a, b, subgroup_order, encoding)
    input_degree, input_terms = polynomial_stats(equations, generators, p)
    precomputed: dict[str, Any] = {
        "system_build_s": time.perf_counter() - build_started,
        "variables": len(generators),
        "equations": len(equations),
        "input_max_total_degree": input_degree,
        "input_terms": input_terms,
        "target_x": target_x,
    }
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker",
        "--p",
        str(p),
        "--a",
        str(a),
        "--b",
        str(b),
        "--order",
        str(order),
        "--subgroup-order",
        str(subgroup_order),
        "--encoding",
        encoding,
    ]
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            creationflags=creationflags,
        )
        measured = {**precomputed, **json.loads(completed.stdout.strip().splitlines()[-1])}
        status = "completed"
    except subprocess.TimeoutExpired:
        measured = precomputed
        status = "timeout"
    except subprocess.CalledProcessError as error:
        measured = {**precomputed, "error": error.stderr.strip()}
        status = "error"
    row: dict[str, Any] = {
        "date": date.today().isoformat(),
        "sympy_version": sympy.__version__,
        "p": p,
        "a": a,
        "b": b,
        "r": order,
        "subgroup_order": subgroup_order,
        "encoding": encoding,
        "status": status,
        "timeout_s": timeout_s,
    }
    for field in FIELDS[10:]:
        row[field] = measured.get(field, "")
    if "error" in measured:
        row["elapsed_s"] = measured["error"]
    return row


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--p", type=int)
    parser.add_argument("--a", type=int)
    parser.add_argument("--b", type=int)
    parser.add_argument("--order", type=int)
    parser.add_argument("--subgroup-order", type=int)
    parser.add_argument("--encoding", choices=("direct", "chain"))
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--include-large", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.worker:
        worker(args)
        return
    fixtures = FIXTURES[:1] if args.smoke else FIXTURES
    if args.include_large:
        fixtures = fixtures + (LARGE_FIXTURE,)
    rows: list[dict[str, Any]] = []
    for fixture in fixtures:
        for encoding in ("direct", "chain"):
            row = benchmark_fixture(fixture, encoding, args.timeout)
            rows.append(row)
            print(" ".join(f"{field}={row[field]}" for field in FIELDS))
    if args.smoke:
        return
    largest = max(fixture[0] for fixture in fixtures)
    output = (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"benchmark_smooth_groebner_p17-{largest}_to{args.timeout:g}s_{date.today().strftime('%Y%m%d')}.csv"
    )
    write_rows(output, rows)
    print(f"output={output}")


if __name__ == "__main__":
    main()
