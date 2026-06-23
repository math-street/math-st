"""Measure expanded term and degree statistics for Semaev f3 through f6.

Sub-goal: P1.3 / SG-02
Inputs:   --max-index <3..6> --term-limit <int> --output <CSV path>
Outputs:  data/measure_semaev_stats_<date>.csv unless --output is supplied
Runtime:  f3/f4 are subsecond; higher indices depend on the term ceiling
Validated against: published f3 formula, recursive resultants, and lib tests
"""

from __future__ import annotations

import argparse
import csv
import multiprocessing
import time
from datetime import date
from pathlib import Path

from sparse_weil import ExpansionLimit, generic_semaev_polynomial


FIELDS = [
    "index",
    "status",
    "term_count",
    "total_degree",
    "x_variable_degrees",
    "elapsed_seconds",
    "term_limit",
    "wall_timeout_seconds",
]


def measure_index(index: int, term_limit: int) -> dict[str, int | float | str]:
    started = time.perf_counter()
    try:
        polynomial = generic_semaev_polynomial(index, term_limit=term_limit)
    except ExpansionLimit as error:
        return {
            "index": index,
            "status": f"censored: {error}",
            "term_count": "",
            "total_degree": "",
            "x_variable_degrees": "",
            "elapsed_seconds": round(time.perf_counter() - started, 6),
            "term_limit": term_limit,
            "wall_timeout_seconds": "",
        }
    return {
        "index": index,
        "status": "complete",
        "term_count": polynomial.term_count,
        "total_degree": polynomial.degree,
        "x_variable_degrees": ";".join(
            str(polynomial.variable_degree(variable)) for variable in range(index)
        ),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "term_limit": term_limit,
        "wall_timeout_seconds": "",
    }


def _measurement_worker(
    index: int,
    term_limit: int,
    queue: multiprocessing.Queue,  # type: ignore[type-arg]
) -> None:
    queue.put(measure_index(index, term_limit))


def measure_index_with_timeout(
    index: int, term_limit: int, timeout_seconds: float
) -> dict[str, int | float | str]:
    if timeout_seconds <= 0:
        return measure_index(index, term_limit)
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()
    process = context.Process(
        target=_measurement_worker, args=(index, term_limit, queue)
    )
    process.start()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        return {
            "index": index,
            "status": f"censored: wall clock exceeded {timeout_seconds:g}s",
            "term_count": "",
            "total_degree": "",
            "x_variable_degrees": "",
            "elapsed_seconds": timeout_seconds,
            "term_limit": term_limit,
            "wall_timeout_seconds": timeout_seconds,
        }
    if process.exitcode != 0:
        raise RuntimeError(f"measurement worker exited with code {process.exitcode}")
    result = queue.get()
    result["wall_timeout_seconds"] = timeout_seconds
    return result


def write_rows(rows: list[dict[str, int | float | str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-index", type=int, default=6, choices=range(3, 7))
    parser.add_argument("--term-limit", type=int, default=250_000)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--per-index-timeout", type=float, default=0.0)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    maximum = 4 if args.smoke else args.max_index
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"measure_semaev_stats_{date.today():%Y%m%d}.csv"
    )
    rows: list[dict[str, int | float | str]] = []
    for index in range(3, maximum + 1):
        row = measure_index_with_timeout(
            index, args.term_limit, args.per_index_timeout
        )
        rows.append(row)
        write_rows(rows, output)
        print(row, flush=True)
    print(f"output: {output}")


if __name__ == "__main__":
    main()
