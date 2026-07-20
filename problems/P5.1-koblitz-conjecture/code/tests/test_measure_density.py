from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from random import Random

from lib.curves import Curve, curve_order_bsgs

SCRIPT = Path(__file__).resolve().parents[1] / "measure_density.py"
SPEC = importlib.util.spec_from_file_location("measure_density", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_published_constants() -> None:
    universal = MODULE.universal_koblitz_product(1_000_000)
    assert abs(universal - MODULE.PUBLISHED_UNIVERSAL_CONSTANT) < 1e-7
    serre = MODULE.corrected_constant(MODULE.CURVES[0], 1_000_000)
    assert abs(serre - MODULE.PUBLISHED_SERRE_CONSTANT) < 1e-7


def test_lmfdb_1728_w1_point_counts() -> None:
    # LMFDB q-expansion coefficients give #E(F_p) = p + 1 - a_p.
    expected = {5: 4, 7: 7, 11: 10, 13: 15, 17: 24, 19: 15, 23: 18}
    for prime, order in expected.items():
        curve = Curve(prime, 6 % prime, -2 % prime)
        assert curve_order_bsgs(curve, Random(prime)) == order


def test_rational_torsion_points() -> None:
    for prime in (11, 13, 17, 19, 23):
        curve_2 = Curve(prime, 1, -2 % prime)
        assert curve_2.contains((1, 0))
        assert curve_2.scalar_mul(2, (1, 0)) is None

        curve_3 = Curve(prime, 3, -11 % prime)
        point = (3 % prime, 5 % prime)
        assert curve_3.contains(point)
        assert curve_3.scalar_mul(3, point) is None
        assert point is not None


def test_validation_and_smoke_measurement() -> None:
    validation = MODULE.validate_orders(seed=51012026, validation_limit=43)
    assert validation["comparisons"] > 20
    assert validation["bsgs"] > 0
    rows = MODULE.measure(
        limit=128,
        checkpoints=[64, 128],
        product_limit=1_000,
        seed=51012026,
    )
    assert len(rows) == 6
    assert {row["curve_key"] for row in rows} == {
        "serre_trivial",
        "torsion_2",
        "torsion_3",
    }
    for row in rows:
        if row["curve_key"] != "serre_trivial":
            assert float(row["predicted_constant"]) == 0.0
