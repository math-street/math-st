from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from audit_quartic_degenerate_cases import audit_degenerate_cases  # noqa: E402


class QuarticDegenerateAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = audit_degenerate_cases(24)

    def test_all_34_degenerate_reductions_are_closed(self) -> None:
        source_cases = {
            (
                row.degree_e1,
                row.degree_e2,
                row.quotient_difference_h,
                row.source_classification,
            )
            for row in self.rows
        }
        self.assertEqual(len(source_cases), 34)
        self.assertTrue(
            all(row.status in {"audited_empty", "exact_cycle"} for row in self.rows)
        )

    def test_only_exact_degenerate_cycle_is_11_13(self) -> None:
        exact = [row for row in self.rows if row.status == "exact_cycle"]
        self.assertEqual(len(exact), 1)
        row = exact[0]
        self.assertEqual(
            (
                row.degree_e1,
                row.degree_e2,
                row.quotient_difference_h,
                row.gap_c,
                row.field_p,
                row.field_q,
            ),
            (12, 10, 0, 2, 11, 13),
        )


if __name__ == "__main__":
    unittest.main()
