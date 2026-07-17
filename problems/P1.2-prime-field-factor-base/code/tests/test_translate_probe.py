from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from audit_translate_probe import audit_order_19


class TranslateProbeTests(unittest.TestCase):
    def test_all_small_shift_schedules_obey_union_bound(self) -> None:
        rows = audit_order_19(max_probes=4)
        self.assertEqual([row["probe_count"] for row in rows], [1, 2, 3, 4])
        self.assertTrue(all(row["violations"] == 0 for row in rows))
        self.assertTrue(all(row["maximum_support"] <= row["union_bound"] for row in rows))
        self.assertTrue(any(row["strict_schedules"] > 0 for row in rows[1:]))


if __name__ == "__main__":
    unittest.main()
