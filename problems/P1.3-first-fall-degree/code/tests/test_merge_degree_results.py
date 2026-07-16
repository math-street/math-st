"""Tests for deterministic selection of canonical experiment rows."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))

from merge_degree_results import merge_rows  # noqa: E402


class MergeDegreeResultsTests(unittest.TestCase):
    def test_later_stage_replaces_timeout_and_legacy_stage_is_inferred(self) -> None:
        fields = [
            "q", "n", "m", "target_mode", "status", "stage_completed",
            "first_fall_degree", "degree_of_regularity", "solving_degree",
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = root / "old.csv"
            new = root / "new.csv"
            with old.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerow({
                    "q": 5, "n": 2, "m": 4, "target_mode": "known",
                    "status": "censored", "stage_completed": "system_build",
                })
            with new.open("w", newline="", encoding="utf-8") as handle:
                legacy_fields = [field for field in fields if field != "stage_completed"]
                writer = csv.DictWriter(handle, fieldnames=legacy_fields)
                writer.writeheader()
                writer.writerow({
                    "q": 5, "n": 2, "m": 4, "target_mode": "known",
                    "status": "censored", "first_fall_degree": 16,
                    "degree_of_regularity": 16,
                })
            rows = merge_rows([old, new])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["stage_completed"], "degree_of_regularity")
        self.assertEqual(rows[0]["degree_of_regularity"], "16")


if __name__ == "__main__":
    unittest.main()
