import importlib.util
import json
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "surface_certificates.py"
SPEC = importlib.util.spec_from_file_location("surface_certificates", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SurfaceCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = Path(__file__).resolve().parents[1] / "surface_certificate_cases.json"
        raw = json.loads(fixture.read_text(encoding="utf-8"))
        cls.results = {
            case["case_id"]: MODULE.validate_certificate(case["case_id"], case["certificate"])
            for case in raw["cases"]
        }

    def test_valid_cd_certificate(self) -> None:
        result = self.results["S1-valid-cd"]
        self.assertEqual(result.status, MODULE.CertificateStatus.NUMERICALLY_VALID)
        self.assertEqual(result.derived["expected_auxiliary_degree"], 7)

    def test_invalid_cd_difference(self) -> None:
        self.assertEqual(
            self.results["S2-invalid-cd-difference"].status,
            MODULE.CertificateStatus.INVALID,
        )

    def test_valid_mm_certificate(self) -> None:
        result = self.results["S3-valid-mm"]
        self.assertEqual(result.status, MODULE.CertificateStatus.NUMERICALLY_VALID)
        self.assertEqual(result.derived["relation_left"], 32)
        self.assertEqual(result.derived["relation_right"], 32)

    def test_invalid_mm_relation_and_bound(self) -> None:
        self.assertEqual(
            self.results["S4-invalid-mm-relation"].status,
            MODULE.CertificateStatus.INVALID,
        )
        self.assertEqual(
            self.results["S5-invalid-mm-search-bound"].status,
            MODULE.CertificateStatus.INVALID,
        )

    def test_factorization_must_be_exact(self) -> None:
        certificate = {
            "route": "K2-CD",
            "torsion_order": 16,
            "target_degree": 9,
            "auxiliary_degree": 7,
            "auxiliary_factorization": [[5, 1]],
            "smoothness_bound": 7,
        }
        result = MODULE.validate_certificate("bad-factorization", certificate)
        self.assertEqual(result.status, MODULE.CertificateStatus.INVALID)


if __name__ == "__main__":
    unittest.main()
