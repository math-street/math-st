"""Known-answer test for the P3.1 toy Deuring round trip."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "toy_deuring_roundtrip.py"
SPEC = importlib.util.spec_from_file_location("toy_deuring_roundtrip", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_p11_ell3_roundtrip_known_counts() -> None:
    row = MODULE.run(p=11, ell=3, trials=1, seed=3103)[0]
    assert row["source_order"] == 144
    assert row["torsion_points"] == 8
    assert row["neighbor_ideals"] == 4
    assert row["kernel_nonzero_points"] == 2
    assert row["roundtrip_match"] == 1
    assert row["target_order"] == 144
    assert row["right_order_discriminant"] == 121
    assert row["right_order_lookup_match"] == 1
    assert row["embedded_right_orders"] == 4
    assert row["target_curve_classes"] == 2
    assert row["dual_kernel_nonzero_points"] == 2
    assert row["dual_roundtrip_match"] == 1
    assert row["dual_ideal_product_match"] == 1
    assert row["chain_degree"] == 9
    assert row["velu_steps"] == 2
