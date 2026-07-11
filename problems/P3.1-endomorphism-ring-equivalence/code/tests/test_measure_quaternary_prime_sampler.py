"""Known-invariant tests for the P3.1 direct quaternary sampler experiment."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "measure_quaternary_prime_sampler.py"
SPEC = importlib.util.spec_from_file_location("measure_quaternary_prime_sampler", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_known_discriminant_and_reciprocity_invariant() -> None:
    rows = MODULE.run_grid(max_p=11, ells=(3,), cutoff=500, trials=0, seed=0)
    row = next(row for row in rows if row["p"] == 11)
    assert row["discriminant"] == 11**2 * 24**6
    assert row["reciprocity_violations"] == 0
    assert row["ellipsoid_vectors"] > 0
    assert row["prime_vectors"] > 0
