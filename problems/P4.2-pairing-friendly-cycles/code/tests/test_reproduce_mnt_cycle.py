from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from reproduce_mnt_cycle import reconstruct_cycle  # noqa: E402


class PublishedMntCycleTests(unittest.TestCase):
    def test_x3_cycle_matches_published_orders_and_degrees(self) -> None:
        rows = reconstruct_cycle(seed=4202)

        self.assertEqual([row.field_prime for row in rows], [37, 43])
        self.assertEqual([row.exhaustive_order for row in rows], [43, 37])
        self.assertEqual([row.bsgs_order for row in rows], [43, 37])
        self.assertEqual([row.computed_embedding_degree for row in rows], [6, 4])
        self.assertEqual([row.trace for row in rows], [-5, 7])
        self.assertEqual([row.cm_radicand for row in rows], [123, 123])
        self.assertEqual(sum(row.trace for row in rows), 2)

    def test_every_lower_embedding_exponent_is_rejected(self) -> None:
        rows = reconstruct_cycle(seed=4202)

        for row in rows:
            lower_residues = [int(value) for value in row.lower_degree_residues.split(";")]
            self.assertNotIn(1, lower_residues)
            self.assertEqual(row.target_degree_residue, 1)


if __name__ == "__main__":
    unittest.main()

