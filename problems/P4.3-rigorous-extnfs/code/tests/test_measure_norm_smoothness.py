import csv
import sys
import tempfile
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_DIR))
import measure_norm_smoothness as measure


class NormSmoothnessTests(unittest.TestCase):
    def test_validated_tower_instance_and_hand_norms(self):
        measure.validate_instance()
        self.assertEqual(measure.tower_norm((1, 0), (0, 0), 1), 1)
        self.assertEqual(measure.tower_norm((0, 0), (1, 0), 1), 1)
        self.assertEqual(measure.tower_norm((0, 0), (1, 0), -4), 16)
        self.assertEqual(measure.tower_norm((0, 1), (1, 0), 1), 3)
        self.assertEqual(measure.tower_norm((0, 1), (1, 0), -4), 18)

    def test_complete_factorization(self):
        self.assertEqual(measure.factor_integer(1), ())
        self.assertEqual(measure.factor_integer(360), ((2, 3), (3, 2), (5, 1)))
        self.assertEqual(measure.factor_integer(-97), ((97, 1),))

    def test_smoke_writes_factor_verified_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            raw_path, summary_path, total = measure.run_experiment(
                a_bound=1,
                bounds=[7],
                trials=0,
                seed=4304,
                output_dir=Path(directory),
            )
            self.assertEqual(total, 80)
            self.assertTrue(raw_path.exists())
            self.assertTrue(summary_path.exists())
            with raw_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), total)
            first = rows[0]
            self.assertIn("factorization_f", first)
            self.assertIn("baseline_factorization_g", first)


if __name__ == "__main__":
    unittest.main()
