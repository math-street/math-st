from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "sample_family_norms.py"
SPEC = importlib.util.spec_from_file_location("sample_family_norms", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AdditionalFamilyNormSamplerTests(unittest.TestCase):
    def test_all_profiles_sample_deterministically(self) -> None:
        for profile in MODULE.PROFILES.values():
            with self.subTest(profile=profile.name):
                first, first_attempts = MODULE.sample_profile(profile, samples=2, rng_seed=9)
                second, second_attempts = MODULE.sample_profile(profile, samples=2, rng_seed=9)
                self.assertEqual(first, second)
                self.assertEqual(first_attempts, second_attempts)
                self.assertTrue(all(row.norm_f > 0 and row.norm_g > 0 for row in first))

    def test_paper_code_distribution_is_separate_and_deterministic(self) -> None:
        profile = MODULE.PROFILES["kss16-128"]
        exact, _ = MODULE.sample_profile(
            profile, samples=2, rng_seed=9, distribution="exact-domain"
        )
        paper, _ = MODULE.sample_profile(
            profile, samples=2, rng_seed=9, distribution="paper-code"
        )
        self.assertNotEqual(exact, paper)

    def test_profile_metadata_matches_expected_dimensions(self) -> None:
        self.assertEqual(MODULE.PROFILES["bn-128"].eta, 6)
        self.assertEqual(MODULE.PROFILES["kss16-128"].roots_of_unity_index, 17)
        self.assertEqual(MODULE.PROFILES["bls24-192"].eta, 24)

    def test_sampling_bound_override_changes_draws_without_mutating_profile(self) -> None:
        profile = MODULE.PROFILES["bls24-192"]
        baseline, _ = MODULE.sample_profile(
            profile, samples=2, rng_seed=9, distribution="paper-code"
        )
        sensitivity, _ = MODULE.sample_profile(
            profile,
            samples=2,
            rng_seed=9,
            distribution="paper-code",
            sampling_coefficient_bound=10,
        )
        self.assertNotEqual(baseline, sensitivity)
        self.assertEqual(profile.coefficient_bound, 9)


if __name__ == "__main__":
    unittest.main()
