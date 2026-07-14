from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = Path(__file__).resolve().parents[1] / "sample_rigid_curve.py"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lib.curves import Curve, curve_order, square_root_multiplicities


def load_script():
    spec = importlib.util.spec_from_file_location("p53_sample_rigid_curve", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def independent_curve_order(curve: Curve) -> int:
    return 1 + sum(
        1
        for x in range(curve.p)
        for y in range(curve.p)
        if (y * y - (x * x * x + curve.a * x + curve.b)) % curve.p == 0
    )


def test_known_curve_order() -> None:
    curve = Curve(5, 1, 1)
    assert curve_order(curve) == 9
    assert independent_curve_order(curve) == 9


def test_generator_is_deterministic_safe_and_first_passing() -> None:
    module = load_script()
    bits = 7
    beacon = "test-beacon"
    sample = 0
    profile = module.default_profile(bits)

    first = module.generate_curve(bits, beacon, sample, 10_000, profile)
    second = module.generate_curve(bits, beacon, sample, 10_000, profile)
    assert first == second

    curve = Curve(first.p, first.a, first.b)
    roots = square_root_multiplicities(first.p)
    assert curve_order(curve, roots) == first.order
    assert independent_curve_order(curve) == first.order
    assert module.evaluate_safety(curve, roots, profile) == (
        first.order,
        first.subgroup_order,
        first.cofactor,
        first.twist_order,
        first.twist_subgroup_order,
        first.twist_cofactor,
        first.trace,
        first.frobenius_discriminant,
    )
    base = (first.base_x, first.base_y)
    assert curve.contains(base)
    assert curve.scalar_mul(first.subgroup_order, base) is None

    for counter in range(first.counter):
        a = module.sample_field_element(first.p, beacon, sample, counter, "a")
        b = module.sample_field_element(first.p, beacon, sample, counter, "b")
        try:
            rejected = Curve(first.p, a, b)
        except ValueError:
            continue
        assert module.evaluate_safety(rejected, roots, profile) is None


def test_field_sampler_is_in_range_and_domain_separated() -> None:
    module = load_script()
    values_a = [
        module.sample_field_element(127, "test-beacon", 0, counter, "a")
        for counter in range(16)
    ]
    values_b = [
        module.sample_field_element(127, "test-beacon", 0, counter, "b")
        for counter in range(16)
    ]
    assert all(0 <= value < 127 for value in values_a + values_b)
    assert values_a != values_b
