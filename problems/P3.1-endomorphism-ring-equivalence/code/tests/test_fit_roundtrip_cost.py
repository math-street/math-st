"""Known-answer tests for the P3.1 toy timing fit."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "fit_roundtrip_cost.py"
SPEC = importlib.util.spec_from_file_location("fit_roundtrip_cost", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_exact_three_halves_power_law() -> None:
    observations = [
        (parameter, 2.0 * parameter**1.5)
        for parameter in (2.0, 3.0, 5.0, 7.0, 11.0)
    ]
    fit = MODULE.fit_power_law(observations)
    assert fit.exponent == pytest.approx(1.5)
    assert fit.prefactor == pytest.approx(2.0)
    assert fit.r_squared == pytest.approx(1.0)


def test_residual_rows_preserve_all_observations() -> None:
    observations = [(11, 3, 0.1), (23, 3, 0.4), (47, 3, 1.6)]
    rows = MODULE.residual_rows(observations)
    assert [row["p"] for row in rows] == [11, 23, 47]
    assert all(row["sample_count"] == 3 for row in rows)
