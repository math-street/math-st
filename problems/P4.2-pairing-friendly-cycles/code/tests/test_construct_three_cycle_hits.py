from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from construct_three_cycle_hits import construct_three_cycle_hits  # noqa: E402


class ConstructThreeCycleHitTests(unittest.TestCase):
    def test_first_tiny_hit_is_fully_constructed(self) -> None:
        hit = {
            "field_prime_e1": "7",
            "field_prime_e2": "13",
            "field_prime_e3": "11",
            "embedding_degree_e1": "12",
            "embedding_degree_e2": "10",
            "embedding_degree_e3": "3",
            "cm_discriminant_e1": "-3",
            "cm_discriminant_e2": "-43",
            "cm_discriminant_e3": "-19",
            "cm_conductor_e1": "1",
            "cm_conductor_e2": "1",
            "cm_conductor_e3": "1",
        }
        rows = construct_three_cycle_hits([hit], seed=4303, max_attempts=1000)

        self.assertEqual([row.field_prime for row in rows], [7, 13, 11])
        self.assertEqual([row.exhaustive_order for row in rows], [13, 11, 7])
        self.assertEqual([row.bsgs_order for row in rows], [13, 11, 7])
        self.assertEqual([row.embedding_degree for row in rows], [12, 10, 3])
        self.assertEqual(sum(row.trace for row in rows), 3)


if __name__ == "__main__":
    unittest.main()

