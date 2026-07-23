"""Regression tests for the A029 uniform SG-30 constructor."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from lib.isogeny import reduced_positive_forms

MODULE_PATH = Path(__file__).parents[1] / "construct_sg30_ring_class_target.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location(
    "construct_sg30_ring_class_target", MODULE_PATH
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_constructor_certifies_every_full_fixture() -> None:
    for r in MODULE.FULL_PRIMES:
        row = MODULE.construct_target(r)
        assert row["exact_order_r_certified"]
        assert row["inside_sg25_lower_scale"]
        assert row["under_60_bit_ceiling"]
        assert row["class_number"] % r == 0
        assert row["discriminant"] == -4 * r**4
        assert (
            row["reduced_a"],
            row["reduced_b"],
            row["reduced_c"],
        ) == (r * r, 2 * r, r * r + 1)


def test_principal_unit_law_is_additive() -> None:
    for r in MODULE.SMOKE_PRIMES:
        modulus = r * r
        for left in range(r):
            for right in range(r):
                product = MODULE.gaussian_multiply_mod(
                    (1, r * left), (1, r * right), modulus
                )
                assert MODULE.wild_parameter(product, r) == (left + right) % r


def test_forms_give_r_distinct_canonical_classes() -> None:
    for r in MODULE.SMOKE_PRIMES:
        forms = {MODULE.reduced_parameter_form(r, value) for value in range(r)}
        assert len(forms) == r
        assert MODULE.reduced_parameter_form(r, 0) == (1, 0, r**4)


def test_small_class_numbers_match_complete_enumeration() -> None:
    for r in (3, 5, 7):
        row = MODULE.construct_target(r)
        forms = reduced_positive_forms(row["discriminant"])
        assert len(forms) == row["class_number"]
        assert (
            row["reduced_a"],
            row["reduced_b"],
            row["reduced_c"],
        ) in forms


def test_invalid_inputs_are_rejected() -> None:
    for value in (2, 9, 15):
        try:
            MODULE.construct_target(value)
        except ValueError:
            pass
        else:
            raise AssertionError("non-odd-prime input was accepted")
