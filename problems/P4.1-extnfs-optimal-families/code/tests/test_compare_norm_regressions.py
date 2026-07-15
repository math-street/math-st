from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "compare_norm_regressions.py"
SPEC = importlib.util.spec_from_file_location("compare_norm_regressions", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class NormRegressionComparisonTests(unittest.TestCase):
    def test_checked_in_artifacts_form_the_expected_matrix(self) -> None:
        data_dir = Path(__file__).resolve().parents[2] / "data"
        rows = MODULE.build_rows(data_dir, "20260715")
        self.assertEqual(len(rows), 8)
        self.assertEqual({row["profile"] for row in rows}, {
            "BN-128", "BLS12-128", "KSS16-128", "BLS24-192"
        })
        self.assertLess(
            abs(next(row for row in rows if row["profile"] == "BN-128")[
                "sampled_minus_paper_security_bits"
            ]),
            0.1,
        )


if __name__ == "__main__":
    unittest.main()
