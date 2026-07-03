import importlib.util
import json
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "leakage_checklist.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("leakage_checklist", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class LeakageChecklistTests(unittest.TestCase):
    def classify_fixture(self, name: str) -> dict[str, str]:
        fixture = Path(__file__).resolve().parents[1] / name
        raw = json.loads(fixture.read_text(encoding="utf-8"))
        return {
            item["case_id"]: MODULE.classify(
                MODULE.LeakageProfile.from_mapping(item)
            ).verdict.value
            for item in raw["cases"]
        }

    def test_protocol_classification(self) -> None:
        actual = self.classify_fixture("protocol_cases.json")
        self.assertEqual(actual["SIDH-p434-shaped-Bob"], "KEY_RECOVERY_POLYNOMIAL")
        self.assertEqual(actual["SIKEp434"], "KEY_RECOVERY_POLYNOMIAL")
        self.assertEqual(actual["CSIDH"], "NO_PUBLISHED_ROUTE")
        self.assertEqual(actual["SQIsign-2.0.1"], "NO_PUBLISHED_ROUTE")
        self.assertEqual(actual["SQIsign2D-West"], "NO_PUBLISHED_ROUTE")

    def test_boundary_classification(self) -> None:
        actual = self.classify_fixture("boundary_cases.json")
        self.assertEqual(actual["B1-rank-one"], "NO_PUBLISHED_ROUTE")
        self.assertEqual(actual["B2-one-unit-inside"], "KEY_RECOVERY_POLYNOMIAL")
        self.assertEqual(actual["B3-hidden-degree"], "NO_PUBLISHED_ROUTE")
        self.assertEqual(actual["B4-below-boundary"], "WITNESS_DEPENDENT")
        self.assertEqual(actual["B5-large-prime-torsion"], "ALGEBRAIC_ONLY")
        self.assertEqual(actual["B6-same-secret-CRT"], "KEY_RECOVERY_POLYNOMIAL")
        self.assertEqual(actual["B6-distinct-secret-no-CRT"], "NO_PUBLISHED_ROUTE")
        self.assertEqual(actual["B7-endring-without-images"], "NO_PUBLISHED_ROUTE")

    def test_rejects_invalid_numeric_profile(self) -> None:
        raw = {
            "case_id": "invalid",
            "target_endpoints_public": True,
            "degree_visibility": "exact",
            "degree": 0,
            "degree_factorization_known": True,
            "torsion_order": 1,
            "torsion_factorization_known": True,
            "torsion_rank": 2,
            "target_action_derivable": True,
            "torsion_access": "base_field",
            "smooth_arithmetic": True,
            "kernel_recovery": "available",
            "surface_construction": "unavailable",
            "surface_certificate": None,
        }
        with self.assertRaises(ValueError):
            MODULE.classify(MODULE.LeakageProfile.from_mapping(raw))

    def test_k2_requires_validated_numerics_and_construction(self) -> None:
        certificate = {
            "route": "K2-MM",
            "secret_prime": 3,
            "secret_exponent": 6,
            "secret_degree": 729,
            "torsion_prime": 2,
            "torsion_exponent": 4,
            "torsion_order": 16,
            "removed_secret_steps": 0,
            "removed_torsion_levels": 0,
            "reduced_secret_degree": 729,
            "reduced_torsion_order": 16,
            "multiplier": 46,
            "multiplier_factorization": [[2, 1], [23, 1]],
            "cofactor": 7,
            "cofactor_factorization": [[7, 1]],
            "smoothness_bound": 23,
            "multiplier_bound": 46,
            "secret_guess_bound": 0,
            "torsion_drop_bound": 0,
        }
        raw = {
            "case_id": "K2-below-R8",
            "target_endpoints_public": True,
            "degree_visibility": "exact",
            "degree": 729,
            "degree_factorization_known": True,
            "torsion_order": 16,
            "torsion_factorization_known": True,
            "torsion_rank": 2,
            "target_action_derivable": True,
            "torsion_access": "base_field",
            "smooth_arithmetic": True,
            "kernel_recovery": "available",
            "surface_construction": "available",
            "surface_certificate": certificate,
        }
        result = MODULE.classify(MODULE.LeakageProfile.from_mapping(raw))
        self.assertEqual(result.verdict, MODULE.Verdict.KEY_RECOVERY_WITH_SURFACE_WITNESS)
        self.assertEqual(result.route, "K2-MM")

        raw["surface_construction"] = "unavailable"
        result = MODULE.classify(MODULE.LeakageProfile.from_mapping(raw))
        self.assertEqual(result.verdict, MODULE.Verdict.ALGEBRAIC_ONLY)

        raw["surface_construction"] = "available"
        raw["surface_certificate"] = dict(certificate, cofactor=8)
        result = MODULE.classify(MODULE.LeakageProfile.from_mapping(raw))
        self.assertEqual(result.verdict, MODULE.Verdict.WITNESS_DEPENDENT)


if __name__ == "__main__":
    unittest.main()
