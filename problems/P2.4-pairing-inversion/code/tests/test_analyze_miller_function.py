from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "analyze_miller_function.py"
SPEC = importlib.util.spec_from_file_location("analyze_miller_function", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class MillerFunctionAnalysisTests(unittest.TestCase):
    def test_exact_vector_matches_all_nonidentity_g2_points(self) -> None:
        row = MODULE.exact_row(43, 11, (23, 8), seed=2404, trials=1)
        self.assertEqual(row["validated_G2_points"], 10)
        self.assertEqual(row["numerator_factor_degree"], 9)
        self.assertEqual(row["denominator_factor_degree"], 8)

    def test_generic_degree_growth(self) -> None:
        for order in (3, 5, 7, 11, 41):
            self.assertEqual(MODULE.factor_degree_growth(order), (order - 2, order - 3))


if __name__ == "__main__":
    unittest.main()

