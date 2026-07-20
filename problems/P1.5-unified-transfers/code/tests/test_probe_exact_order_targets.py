"""Known-answer tests for the toy exact-order target census."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "probe_exact_order_targets.py"
SPEC = importlib.util.spec_from_file_location("probe_exact_order_targets", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExactOrderTargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.counts = MODULE.class_numbers_through(1_000)

    def test_known_class_numbers(self) -> None:
        MODULE.validate_known_answers(self.counts)

    def test_batch_counts_match_shared_enumerator(self) -> None:
        for discriminant in MODULE.KNOWN_CLASS_NUMBERS:
            self.assertEqual(
                self.counts[discriminant],
                MODULE.class_number_from_reduced_forms(discriminant),
            )

    def test_smoke_primes_are_found(self) -> None:
        rows = MODULE.least_divisible_rows(1_000, MODULE.SMOKE_PRIMES)
        self.assertTrue(all(row["found"] for row in rows))
        self.assertTrue(all(row["class_number"] % row["r"] == 0 for row in rows))
        self.assertTrue(all(row["class_number_equals_r"] for row in rows))
        for row in rows:
            self.assertEqual(
                row["form_b"] ** 2 - 4 * row["form_a"] * row["form_c"],
                row["discriminant"],
            )


if __name__ == "__main__":
    unittest.main()
