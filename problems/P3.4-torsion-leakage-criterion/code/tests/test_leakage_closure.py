import importlib.util
import json
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "leakage_closure.py"
SPEC = importlib.util.spec_from_file_location("leakage_closure", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class LeakageClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = Path(__file__).resolve().parents[1] / "leakage_records.json"
        raw = json.loads(fixture.read_text(encoding="utf-8"))
        cls.results = {case["case_id"]: MODULE.analyze_case(case) for case in raw["cases"]}

    def test_collective_span_without_a_basis_pair(self) -> None:
        result = self.results["L1-composite-collective-span"]
        self.assertEqual(result.status, MODULE.ClosureStatus.FULL_ACTION)
        self.assertIsNotNone(result.certificate)
        assert result.certificate is not None
        self.assertEqual(result.certificate.minors, (2, 3, 0))
        self.assertEqual(result.certificate.span_gcd, 1)
        self.assertEqual(result.certificate.action, ((2, 1), (1, 3)))
        self.assertTrue(all(MODULE.gcd(6, abs(minor)) != 1 for minor in (2, 3, 0)))

    def test_rank_one_is_rejected(self) -> None:
        result = self.results["L2-rank-one"]
        self.assertEqual(result.status, MODULE.ClosureStatus.PARTIAL_SPAN)
        self.assertIsNone(result.certificate)

    def test_inconsistent_image_equations_are_rejected(self) -> None:
        result = self.results["L3-inconsistent-images"]
        self.assertEqual(result.status, MODULE.ClosureStatus.INCONSISTENT_IMAGES)
        self.assertIsNone(result.certificate)

    def test_same_secret_certificates_combine_by_crt(self) -> None:
        result = self.results["L4-same-secret-crt"]
        self.assertEqual(result.status, MODULE.ClosureStatus.FULL_ACTION)
        assert result.certificate is not None
        self.assertEqual(result.certificate.modulus, 36)
        self.assertEqual(result.certificate.action, ((1, 1), (1, 2)))

    def test_mixed_secrets_and_bases_are_rejected(self) -> None:
        self.assertEqual(
            self.results["L5-mixed-secrets"].status,
            MODULE.ClosureStatus.MIXED_TARGET_MAPS,
        )
        self.assertEqual(
            self.results["L6-incompatible-bases"].status,
            MODULE.ClosureStatus.INCOMPATIBLE_BASES,
        )

    def test_generalized_crt_checks_overlap(self) -> None:
        certificate_a = MODULE.ActionCertificate(
            "phi", "bases", 4, ((1, 1), (1, 2)), 2, (1,), 1
        )
        certificate_b = MODULE.ActionCertificate(
            "phi", "bases", 6, ((1, 1), (1, 2)), 2, (1,), 1
        )
        combined = MODULE.combine_certificates([certificate_a, certificate_b])
        self.assertEqual(combined.modulus, 12)
        incompatible = MODULE.ActionCertificate(
            "phi", "bases", 6, ((2, 1), (1, 2)), 2, (1,), 1
        )
        with self.assertRaises(ValueError):
            MODULE.combine_certificates([certificate_a, incompatible])


if __name__ == "__main__":
    unittest.main()
