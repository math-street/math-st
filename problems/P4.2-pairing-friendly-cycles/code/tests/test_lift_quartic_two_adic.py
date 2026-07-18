from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from lift_quartic_two_adic import audit_two_adic  # noqa: E402


class QuarticTwoAdicTests(unittest.TestCase):
    def test_all_47_odd_survivors_are_audited(self) -> None:
        rows = audit_two_adic(5, 251)
        self.assertEqual(len(rows), 47)
        self.assertTrue(all(row.certificate_exponent <= 5 for row in rows))


if __name__ == "__main__":
    unittest.main()
