from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from audit_quartic_small_gaps import audit_small_gaps  # noqa: E402


class QuarticSmallGapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = audit_small_gaps(106)

    def test_every_pair_and_small_even_gap_is_audited(self) -> None:
        cases = {
            (row.degree_e1, row.degree_e2, row.gap_c) for row in self.rows
        }
        self.assertEqual(len(cases), 16 * 53)
        self.assertEqual(len(self.rows), 16 * 53)

    def test_unique_exact_cycle(self) -> None:
        exact = [row for row in self.rows if row.status == "exact_cycle"]
        self.assertEqual(len(exact), 1)
        row = exact[0]
        self.assertEqual(
            (
                row.degree_e1,
                row.degree_e2,
                row.gap_c,
                row.field_p,
                row.field_q,
            ),
            (12, 10, 2, 11, 13),
        )


if __name__ == "__main__":
    unittest.main()
