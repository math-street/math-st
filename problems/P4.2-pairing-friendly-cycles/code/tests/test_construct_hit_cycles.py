from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from construct_hit_cycles import (  # noqa: E402
    construct_hit_cycles,
    filter_hits_by_minimum_field,
    verify_prime_order_in_hasse_interval,
)
from lib.curves import Curve, curve_order  # noqa: E402


class ConstructHitCycleTests(unittest.TestCase):
    def test_minimum_field_filter_selects_only_extension_hits(self) -> None:
        hits = [
            {"field_prime_e1": "37", "field_prime_e2": "43"},
            {"field_prime_e1": "341057", "field_prime_e2": "341641"},
        ]
        self.assertEqual(
            filter_hits_by_minimum_field(hits, 1 << 18),
            [hits[1]],
        )

    def test_tiny_non_mnt_degree_pair_is_explicitly_constructed(self) -> None:
        hit = {
            "field_prime_e1": "7",
            "field_prime_e2": "11",
            "cm_fundamental_discriminant": "-19",
            "cm_conductor": "1",
            "embedding_degree_e1": "10",
            "embedding_degree_e2": "3",
        }
        rows = construct_hit_cycles([hit], seed=4203, max_attempts=100)

        self.assertEqual([row.field_prime for row in rows], [7, 11])
        self.assertEqual([row.exhaustive_order for row in rows], [11, 7])
        self.assertEqual([row.bsgs_order for row in rows], [11, 7])
        self.assertEqual([row.embedding_degree for row in rows], [10, 3])
        self.assertEqual([row.cm_radicand for row in rows], [19, 19])
        self.assertTrue(all(row.bsgs_isolation_failures >= 0 for row in rows))

    def test_prime_point_hasse_certificate_matches_exhaustive_count(self) -> None:
        fixtures = (
            (Curve(37, 24, 16), 43),
            (Curve(43, 36, 5), 37),
        )
        for curve, target_order in fixtures:
            verified_order, method, witness = verify_prime_order_in_hasse_interval(
                curve,
                target_order,
                exhaustive_limit=0,
            )
            self.assertEqual(method, "prime_point_hasse_certificate")
            self.assertEqual(verified_order, target_order)
            self.assertEqual(curve_order(curve), verified_order)
            self.assertIsNotNone(witness)
            self.assertTrue(curve.contains(witness))
            self.assertIsNone(curve.scalar_mul(verified_order, witness))

    def test_every_24bit_certificate_witness_verifies(self) -> None:
        ledger = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "construct_hit_cycles_n54_s8207_20260708.csv"
        )
        with ledger.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 108)
        self.assertEqual(len({row["cycle"] for row in rows}), 54)
        for row in rows:
            field_prime = int(row["field_prime"])
            target_order = int(row["expected_order"])
            curve = Curve(field_prime, int(row["a"]), int(row["b"]))
            witness = (int(row["witness_x"]), int(row["witness_y"]))
            self.assertEqual(row["verification_method"], "prime_point_hasse_certificate")
            self.assertEqual(int(row["bsgs_order"]), target_order)
            self.assertEqual(int(row["independently_verified_order"]), target_order)
            self.assertTrue(curve.contains(witness))
            self.assertIsNone(curve.scalar_mul(target_order, witness))


if __name__ == "__main__":
    unittest.main()
