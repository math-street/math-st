from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
SCRIPT = Path(__file__).resolve().parents[1] / "measure_corrected_cases.py"
SPEC = importlib.util.spec_from_file_location("measure_corrected_cases", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_lmfdb_adelic_group_and_finite_level_density() -> None:
    certificate = MODULE.torsion_3_finite_level_certificate()
    assert certificate.group_order_mod_30 == 8_640
    assert certificate.group_order_mod_90 == 699_840
    assert certificate.favorable_mod_90 == 98_280
    assert certificate.density == MODULE.Fraction(91, 648)
    assert certificate.low_prime_multiplier == MODULE.Fraction(455, 864)
    assert certificate.universal_correction == MODULE.Fraction(5_824, 5_913)


def test_cm_constant_reproduces_zywina() -> None:
    constant = MODULE.cm_qi_t8_constant(1_000_000)
    assert abs(constant - MODULE.PUBLISHED_CM_CONSTANT) < 1e-7
    generic = MODULE.generic_full_gl2_t8_constant(1_000_000)
    expected = (21 / 64) * MODULE.universal_koblitz_product(1_000_000)
    assert abs(generic - expected) < 1e-15


def test_cm_inert_orders_and_split_divisibility() -> None:
    for prime in (7, 11, 19, 23, 31, 43):
        order, _ = MODULE.exact_order(MODULE.CM_CURVE, prime, 51012026, 3)
        assert order == prime + 1
    for prime in (5, 13, 17, 29, 37, 41):
        order, _ = MODULE.exact_order(MODULE.CM_CURVE, prime, 51012026, 3)
        assert order % 8 == 0


def test_corrected_cases_smoke_measurement() -> None:
    rows = MODULE.measure(
        limit=128,
        checkpoints=[64, 128],
        product_limit=10_000,
        seed=51012026,
    )
    assert len(rows) == 4
    assert {row["case_key"] for row in rows} == {
        "torsion_3_quotient",
        "cm_qi_split_t8",
    }
    for row in rows:
        assert float(row["predicted_constant"]) > 0.0
        assert float(row["predicted_count"]) > 0.0
    cm_rows = [row for row in rows if row["case_key"] == "cm_qi_split_t8"]
    assert all(row["invalid_pool_count"] != "" for row in cm_rows)
