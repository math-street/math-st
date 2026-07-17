from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lib.curves import Curve


class FormalSupportBoundTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curve = Curve(17, 2, 2)
        self.generator = (5, 1)

    def sum_tuple(self, points: tuple) -> object:
        total = None
        for point in points:
            total = self.curve.add(total, point)
        return total

    def reachable_exactly(self, base: list, length: int) -> set:
        return {
            self.sum_tuple(points)
            for points in itertools.product(base, repeat=length)
        }

    def test_exact_and_at_most_support_bounds_exhaustively(self) -> None:
        # This curve is cyclic of order 19.  The test covers 20 base/length
        # combinations and enumerates ordered tuples with repetition, the
        # largest representation space among the usual variants.
        for base_size in range(1, 6):
            base = [
                self.curve.scalar_mul(index, self.generator)
                for index in range(1, base_size + 1)
            ]
            reachable_at_most: set = set()
            for length in range(0, 5):
                reachable_exactly = self.reachable_exactly(base, length)
                self.assertLessEqual(len(reachable_exactly), base_size**length)
                reachable_at_most.update(reachable_exactly)
                geometric_bound = sum(base_size**index for index in range(length + 1))
                self.assertLessEqual(len(reachable_at_most), geometric_bound)

    def test_support_can_be_strictly_smaller_than_tuple_count(self) -> None:
        base = [
            self.curve.scalar_mul(index, self.generator)
            for index in (1, 2, 3, 4, 5)
        ]
        reachable = self.reachable_exactly(base, 3)
        self.assertLess(len(reachable), len(base) ** 3)
        self.assertEqual(len(reachable), 13)


if __name__ == "__main__":
    unittest.main()
