from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
CODE = Path(__file__).resolve().parents[1]
SCRIPT = CODE / "class_uniform_kernel.py"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from lib.curves import Curve


def load_script():
    spec = importlib.util.spec_from_file_location("p53_class_uniform", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_exact_class_and_safety_counts_at_p127() -> None:
    module = load_script()
    summary = module.audit_summary(7)

    assert summary == {
        "bits": 7,
        "p": 127,
        "nonsingular_encodings": 16002,
        "all_classes": 258,
        "all_orbit_histogram": {"21": 6, "63": 252},
        "safe_encodings": 4179,
        "safe_classes": 67,
        "safe_orbit_histogram": {"21": 1, "63": 66},
        "coefficient_kernel_min_class_mass": "1/199",
        "coefficient_kernel_max_class_mass": "3/199",
        "class_uniform_mass": "1/67",
        "total_variation_from_class_uniform": "132/13333",
    }


def test_class_keys_equal_explicit_scaling_orbits() -> None:
    module = load_script()
    p = 127
    for key, recorded_size in module.coefficient_class_sizes(p):
        orbit = module.scaling_orbit(p, *key)
        assert len(orbit) == recorded_size
        assert min(orbit) == key
        for a, b in orbit:
            assert module.isomorphism_class_key(p, a, b) == key


def test_safe_class_unranking_boundaries_and_points() -> None:
    module = load_script()
    classes = module.enumerate_safe_classes(7)

    first = module.unrank_safe_class(classes, 0)
    last = module.unrank_safe_class(classes, len(classes) - 1)
    assert (first.a, first.b, first.orbit_size) == (0, 13, 21)
    assert (last.a, last.b, last.orbit_size) == (3, 123, 63)
    for row in (first, last):
        curve = Curve(row.p, row.a, row.b)
        point = (row.base_x, row.base_y)
        assert curve.contains(point)
        assert curve.scalar_mul(row.subgroup_order, point) is None


def test_uniform_rank_sampler_is_deterministic_and_domain_separated() -> None:
    module = load_script()
    first = module.choose_safe_class(7, "class-test-beacon", 0)
    second = module.choose_safe_class(7, "class-test-beacon", 0)
    assert first == second
    ranks_a = [
        module.sample_uniform_rank(67, "class-test-beacon", sample, "a")
        for sample in range(32)
    ]
    ranks_b = [
        module.sample_uniform_rank(67, "class-test-beacon", sample, "b")
        for sample in range(32)
    ]
    assert all(0 <= rank < 67 for rank in ranks_a + ranks_b)
    assert ranks_a != ranks_b


def test_reported_masses_are_exact() -> None:
    module = load_script()
    summary = module.audit_summary(7)
    assert Fraction(summary["coefficient_kernel_min_class_mass"]) == Fraction(1, 199)
    assert Fraction(summary["coefficient_kernel_max_class_mass"]) == Fraction(3, 199)
    assert Fraction(summary["class_uniform_mass"]) == Fraction(1, 67)
    assert Fraction(summary["total_variation_from_class_uniform"]) == Fraction(
        132, 13333
    )


def test_smoke_cli_uses_fixed_quick_profile(tmp_path: Path, capsys) -> None:
    module = load_script()
    prefix = tmp_path / "class-kernel-smoke"

    module.main(
        [
            "--smoke",
            "--bits",
            "8",
            "--output-prefix",
            str(prefix),
        ]
    )

    summary = json.loads(prefix.with_suffix(".json").read_text(encoding="utf-8"))
    assert summary["bits"] == 5
    assert summary["p"] == 31
    assert summary["safe_classes"] == 23
    assert prefix.with_suffix(".csv").is_file()
    assert "safe_classes=23" in capsys.readouterr().out
