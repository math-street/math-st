"""Regression tests for the A028 Kummer class character."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "probe_kummer_class_character.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("probe_kummer_class_character", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_a019_forms_have_the_claimed_discriminants() -> None:
    for r in MODULE.SMOKE_PRIMES:
        row = MODULE.run_case(r)
        a, b, c = row["form_a"], row["form_b"], row["form_c"]
        assert b * b - 4 * a * c == row["discriminant"]
        assert row["discriminant_bits"] in (r + 1, r + 2)


def test_tonelli_shanks_handles_both_prime_classes() -> None:
    for prime, value in ((11, 9), (13, 10), (41, 9)):
        root = MODULE.modular_square_root(value, prime)
        assert root is not None
        assert root * root % prime == value
    assert MODULE.modular_square_root(2, 11) is None


def test_nontrivial_character_recovers_every_scalar() -> None:
    for r in MODULE.SMOKE_PRIMES:
        row = MODULE.run_case(r)
        assert row["character_order"] == r
        assert row["all_logs_recovered"]
        assert (row["auxiliary_prime"] - 1) % r == 0


def test_checked_family_includes_small_auxiliary_primes() -> None:
    rows = [MODULE.run_case(r) for r in MODULE.FULL_PRIMES]
    assert any(not row["q_exceeds_sqrt_abs_delta"] for row in rows)
    assert max(row["auxiliary_bits"] for row in rows) <= 10
