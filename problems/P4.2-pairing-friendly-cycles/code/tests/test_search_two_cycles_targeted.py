from __future__ import annotations

import sys
import unittest
from dataclasses import asdict
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_two_cycles import search_two_cycles  # noqa: E402
from search_two_cycles_targeted import (  # noqa: E402
    fundamental_discriminant_trial,
    search_two_cycles_targeted,
)


class TargetedTwoCycleSearchTests(unittest.TestCase):
    def test_trial_discriminant_decomposition(self) -> None:
        factor_primes = [2, 3, 5, 7, 11, 13]
        self.assertEqual(fundamental_discriminant_trial(123, factor_primes), (-123, 1))
        self.assertEqual(fundamental_discriminant_trial(20, factor_primes), (-20, 1))
        self.assertEqual(fundamental_discriminant_trial(48, factor_primes), (-3, 4))

    def test_candidate_ledger_matches_full_search(self) -> None:
        for limit in (128, 512):
            full = search_two_cycles(limit=limit, max_degree=12)
            targeted = search_two_cycles_targeted(limit=limit, max_degree=12)
            self.assertEqual(
                [asdict(row) for row in targeted.candidates],
                [asdict(row) for row in full.candidates],
            )
            self.assertEqual(
                targeted.summary["hasse_valid_pair_count"],
                full.summary["hasse_valid_pair_count"],
            )
            self.assertEqual(targeted.summary["hit_count"], full.summary["hit_count"])

    def test_root_generated_rows_match_hasse_scan(self) -> None:
        for limit in (128, 512, 2048):
            scanned = search_two_cycles_targeted(
                limit=limit,
                max_degree=12,
                pair_generator="hasse_scan",
            )
            generated = search_two_cycles_targeted(
                limit=limit,
                max_degree=12,
                pair_generator="cyclotomic_roots",
            )
            self.assertEqual(
                [asdict(row) for row in generated.candidates],
                [asdict(row) for row in scanned.candidates],
            )
            self.assertEqual(
                generated.summary["hit_count"],
                scanned.summary["hit_count"],
            )


if __name__ == "__main__":
    unittest.main()
