"""Integration tests for the exhaustive toy CSIDH action."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "verify_toy_action.py"
SPEC = importlib.util.spec_from_file_location("verify_toy_action", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ToyActionTests(unittest.TestCase):
    def test_smoke_instance_is_regular_and_matches_class_number(self) -> None:
        report = MODULE.build_report(59, (3, 5))
        self.assertTrue(report["matches_class_number"])
        self.assertTrue(report["generators_commute"])
        self.assertTrue(report["transitive"])
        self.assertTrue(report["free"])
        self.assertTrue(report["regular"])


if __name__ == "__main__":
    unittest.main()
