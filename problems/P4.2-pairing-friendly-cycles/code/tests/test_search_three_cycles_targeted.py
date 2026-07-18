from __future__ import annotations

import sys
import unittest
from dataclasses import asdict
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from search_three_cycles import search_three_cycles  # noqa: E402
from search_three_cycles_targeted import (  # noqa: E402
    primitive_order_residues,
    search_three_cycles_targeted,
)


class TargetedThreeCycleSearchTests(unittest.TestCase):
    def test_primitive_order_residues_are_complete(self) -> None:
        for prime in (13, 43, 127):
            for order in range(3, 13):
                expected = tuple(
                    value
                    for value in range(1, prime)
                    if pow(value, order, prime) == 1
                    and all(
                        pow(value, exponent, prime) != 1
                        for exponent in range(1, order)
                    )
                )
                self.assertEqual(primitive_order_residues(prime, order), expected)

    def test_candidate_ledger_matches_exhaustive_search(self) -> None:
        for limit in (128, 512):
            exhaustive = search_three_cycles(limit=limit, max_degree=12)
            targeted = search_three_cycles_targeted(limit=limit, max_degree=12)

            self.assertEqual(
                [asdict(row) for row in targeted.candidates],
                [asdict(row) for row in exhaustive.candidates],
            )
            self.assertEqual(
                targeted.summary["directed_hasse_edge_count"],
                exhaustive.summary["directed_hasse_edge_count"],
            )
            self.assertEqual(targeted.summary["hit_count"], exhaustive.summary["hit_count"])
            self.assertEqual(
                targeted.summary["two_of_three_near_miss_count"],
                exhaustive.summary["two_of_three_near_miss_count"],
            )

    def test_root_generated_rows_match_hasse_scan(self) -> None:
        for limit in (128, 512, 2048):
            scanned = search_three_cycles_targeted(
                limit=limit,
                max_degree=12,
                edge_generator="hasse_scan",
            )
            generated = search_three_cycles_targeted(
                limit=limit,
                max_degree=12,
                edge_generator="cyclotomic_roots",
            )
            self.assertEqual(
                [asdict(row) for row in generated.candidates],
                [asdict(row) for row in scanned.candidates],
            )
            self.assertEqual(
                generated.summary["target_edge_count"],
                scanned.summary["target_edge_count"],
            )


if __name__ == "__main__":
    unittest.main()
