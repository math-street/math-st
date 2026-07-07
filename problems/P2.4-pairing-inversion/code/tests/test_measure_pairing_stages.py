from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "measure_pairing_stages.py"
SPEC = importlib.util.spec_from_file_location("measure_pairing_stages", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class PairingStageMeasurementTests(unittest.TestCase):
    def test_published_parameter_fibres_and_validation(self) -> None:
        row = MODULE.benchmark_parameter(43, trials=3, seed=2404)
        self.assertEqual(row["subgroup_order_r"], 11)
        self.assertEqual(row["final_exponent_d"], 168)
        self.assertEqual(row["final_fibre_min"], 168)
        self.assertEqual(row["final_fibre_max"], 168)
        self.assertEqual(row["pairing_image_size_nonidentity"], 10)
        self.assertTrue(row["nondegenerate"])


if __name__ == "__main__":
    unittest.main()

