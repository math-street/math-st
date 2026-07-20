"""Known-answer tests for the P1.5 transfer experiment driver."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "run_transfers.py"
SPEC = importlib.util.spec_from_file_location("run_transfers", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
RUN_TRANSFERS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN_TRANSFERS)


class TransferDriverTests(unittest.TestCase):
    def test_additive_known_log(self) -> None:
        row = RUN_TRANSFERS.run_additive_case(101, 15072026, 37, 1)
        self.assertEqual(row["recovered"], 37)
        self.assertEqual((row["curve_a"], row["curve_b"]), (56, 48))

    def test_pairing_known_log(self) -> None:
        row = RUN_TRANSFERS.run_mov_case(43, 11, 7, 1, 15072026)
        self.assertEqual(row["recovered"], 7)
        self.assertEqual(row["embedding_degree"], 2)


if __name__ == "__main__":
    unittest.main()

