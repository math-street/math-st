from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "certify_kss16_ceiling.py"
SPEC = importlib.util.spec_from_file_location("certify_kss16_ceiling", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class KSS16CeilingCertificateTests(unittest.TestCase):
    def test_analytic_cutoff_exceeds_the_ceiling(self) -> None:
        bound = MODULE.kss16_numerator_absolute_lower_bound(256)
        self.assertGreater(bound, 980 * (1 << 60))

    def test_exhaustive_certificate_has_no_valid_candidate(self) -> None:
        certificate = MODULE.build_certificate()
        self.assertEqual(certificate["enumerated_seed_count"], 511)
        self.assertEqual(certificate["valid_candidate_count"], 0)
        self.assertEqual(certificate["integral_parameters_below_ceiling"], 8)
        self.assertEqual(
            [row["seed"] for row in certificate["parameters_below_ceiling"]],
            [-115, -95, -45, -25, 25, 45, 95, 115],
        )


if __name__ == "__main__":
    unittest.main()
