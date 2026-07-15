from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class SearchFamiliesTests(unittest.TestCase):
    def test_smoke_outputs_known_toy_fixture_and_all_targets(self) -> None:
        repository = Path(__file__).resolve().parents[4]
        script = repository / "problems" / "P4.1-extnfs-optimal-families" / "code" / "search_families.py"
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--smoke",
                    "--date",
                    "20260626",
                    "--output-dir",
                    str(output),
                ],
                cwd=repository,
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            toy_path = output / "search_families_m100_100_20260626.csv"
            with toy_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(any(row["family"] == "BLS12" and row["seed"] == "-2" for row in rows))
            self.assertTrue(all(int(row["p_bits"]) <= 60 for row in rows))

            extrapolation_path = output / "optimization_extrapolated_20260715.csv"
            with extrapolation_path.open(newline="", encoding="utf-8") as handle:
                extrapolation = list(csv.DictReader(handle))
            self.assertEqual({int(row["target_bits"]) for row in extrapolation}, {128, 192, 256})

            summary_path = output / "search_summary_m100_100_20260626.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["toy"]["seed_interval_inclusive"], [-100, 100])
            self.assertEqual(summary["extrapolation"]["row_count"], 36)


if __name__ == "__main__":
    unittest.main()
