from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from random import Random

from lib.curves import Curve, curve_order, curve_order_bsgs, is_prime

SCRIPT = Path(__file__).resolve().parents[1] / "reproduce_cm_table.py"
SPEC = importlib.util.spec_from_file_location("reproduce_cm_table", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_sum_of_two_squares_and_cm_trace_against_exhaustive_counts() -> None:
    flags = MODULE.prime_flags(1_000)
    for prime in range(5, 1_001):
        if not flags[prime]:
            continue
        if prime % 4 == 1:
            first, second = MODULE.sum_of_two_squares_prime(prime)
            assert first * first + second * second == prime
        expected = curve_order(Curve(prime, -1 % prime, 0))
        assert MODULE.cm_curve_order(prime) == expected


def test_cm_prime_pair_reduction_and_unique_one_mod_eight_event() -> None:
    flags = MODULE.prime_flags(100_000)
    one_mod_eight_events: list[tuple[int, int]] = []
    for prime in MODULE.primes_from_flags(flags):
        if prime <= 2 or prime % 4 != 1:
            continue
        first, second = MODULE.sum_of_two_squares_prime(prime)
        a = first if first % 2 else second
        b = second if first % 2 else first
        if a % 4 != 1:
            a = -a
        epsilon = 1 if prime % 8 == 1 else -1
        order = MODULE.cm_curve_order(prime)
        assert order == (a - epsilon) ** 2 + b**2
        assert order % 8 == 0
        quotient = order // 8
        if prime % 8 == 1 and is_prime(quotient):
            one_mod_eight_events.append((prime, quotient))
    assert one_mod_eight_events == [(17, 2)]


def test_published_integral_predictor() -> None:
    predicted = MODULE.published_integral_prediction(MODULE.PUBLISHED_X)
    assert round(predicted) == MODULE.PUBLISHED_EXPECTED_ROUNDED
    assert abs(predicted - 50_062.77360219449) < 1e-8


def test_segmented_split_sieve_matches_full_sieve() -> None:
    limit = 100_000
    flags = MODULE.prime_flags(limit)
    expected = [prime for prime in range(5, limit + 1, 4) if flags[prime]]
    measured = list(MODULE.segmented_split_primes(limit, segment_size=7_777))
    assert measured == expected


def test_cm_trace_against_generic_bsgs_at_large_primes() -> None:
    for prime in (1_000_033, 100_000_037, 900_000_041):
        curve = Curve(prime, -1 % prime, 0)
        generic = curve_order_bsgs(curve, Random(0xC0FFEE ^ prime), max_points=96)
        assert MODULE.cm_curve_order(prime) == generic


def test_published_fixture_is_not_an_input_to_counting(monkeypatch) -> None:
    monkeypatch.setitem(MODULE.PUBLISHED_TABLE, 10_000, (999_999, 888_888))
    row = MODULE.measure(10_000, [10_000], seed=51012026)[0]
    assert row["quotient_prime_count"] == 105
    assert row["published_actual_difference"] == 105 - 999_999


def test_cm_table_smoke_measurement() -> None:
    rows = MODULE.measure(10_000, [1_000, 5_000, 10_000], seed=51012026)
    assert len(rows) == 3
    assert [int(row["cutoff"]) for row in rows] == [1_000, 5_000, 10_000]
    assert all(int(row["quotient_prime_count"]) > 0 for row in rows)
    assert all(row["point_counter"] == "cornacchia_walsh_j1728_exact_trace" for row in rows)
