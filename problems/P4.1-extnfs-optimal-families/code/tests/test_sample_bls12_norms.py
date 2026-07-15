from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from sympy import symbols

MODULE_PATH = Path(__file__).resolve().parents[1] / "sample_bls12_norms.py"
SPEC = importlib.util.spec_from_file_location("sample_bls12_norms", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BLS12NormSamplerTests(unittest.TestCase):
    def test_nested_resultant_matches_hand_computation(self) -> None:
        x, t = symbols("x t")
        h = t**2 + 1
        f = x**2 + 1
        # Res_x(2+t-x, x^2+1) = t^2+4t+5; its h-resultant is 32.
        norm = MODULE.nested_resultant_norm((2, 1), (1, 0), f, h, x, t)
        self.assertEqual(norm, 32)

    def test_sampler_is_deterministic_and_writes_outputs(self) -> None:
        first, first_attempts = MODULE.sample_bls12_norms(
            seed=-2,
            coefficient_bound=2,
            samples=3,
            rng_seed=17,
        )
        second, second_attempts = MODULE.sample_bls12_norms(
            seed=-2,
            coefficient_bound=2,
            samples=3,
            rng_seed=17,
        )
        self.assertEqual(first, second)
        self.assertEqual(first_attempts, second_attempts)
        self.assertTrue(all(row.norm_f > 0 and row.norm_g > 0 for row in first))
        self.assertTrue(all(row.bit_length_f == row.norm_f.bit_length() for row in first))

        with tempfile.TemporaryDirectory() as temporary:
            path = MODULE.write_outputs(
                first,
                first_attempts,
                seed=-2,
                coefficient_bound=2,
                rng_seed=17,
                output_dir=Path(temporary),
                date_label="test",
            )
            self.assertTrue(path.exists())
            self.assertTrue(path.with_suffix(".csv").exists())


if __name__ == "__main__":
    unittest.main()
