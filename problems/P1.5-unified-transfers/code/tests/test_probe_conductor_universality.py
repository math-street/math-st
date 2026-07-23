"""Regression tests for the A026 Gaussian conductor theorem."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "probe_conductor_universality.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("probe_conductor_universality", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_gaussian_order_formula_matches_complete_enumeration() -> None:
    for conductor in (3, 5, 9, 15, 25, 35):
        torus_order, class_number = MODULE.validate_order_formula(conductor)
        assert torus_order == 2 * class_number


def test_general_inverse_recovers_semisimple_residues() -> None:
    assert MODULE.validate_semisimple_inverse(43) == 44


def test_additive_forms_recover_every_principal_unit() -> None:
    p = 7
    forms = []
    for parameter in range(p):
        form = MODULE.additive_ring_class_form(p, parameter)
        residue = MODULE.gaussian_torus_residue_from_form(p * p, form)
        assert MODULE.gaussian_projectively_equivalent(
            residue, (1, p * parameter), p * p
        )
        assert MODULE.principal_unit_parameter(residue, p) == parameter
        forms.append(form)
    assert len(set(forms)) == p


def test_anomalous_to_ordinary_ring_class_end_to_end() -> None:
    row = MODULE.run_additive_case(101, 37, 20260723)
    assert row["recovered"] == 37
    assert row["image_size"] == 101
    assert row["class_number"] % 101 == 0


def test_intrinsic_source_characteristic_branch_forces_trace_two() -> None:
    for p, r in ((47, 23), (59, 29), (83, 41)):
        row = MODULE.intrinsic_source_characteristic_verdict(p, r, 2)
        assert row["curve_order"] == p - 1
        assert row["embedding_degree_one"]
