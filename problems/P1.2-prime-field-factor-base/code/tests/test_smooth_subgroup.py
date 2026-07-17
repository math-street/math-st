from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from lib.curves import Curve
from measure_smooth_subgroup import (
    factor_base_from_x,
    primitive_root,
    squaring_chain_accepts,
    subgroup_elements,
)


class SmoothSubgroupTests(unittest.TestCase):
    def test_primitive_root_and_subgroup_on_fermat_prime(self) -> None:
        p = 257
        root = primitive_root(p)
        self.assertEqual(pow(root, 128, p), p - 1)
        subgroup = subgroup_elements(p, 16)
        self.assertEqual(len(subgroup), 16)
        self.assertEqual(set(subgroup), {value for value in range(p) if pow(value, 16, p) == 1})

    def test_squaring_chain_matches_power_predicate(self) -> None:
        for value in range(257):
            self.assertEqual(
                squaring_chain_accepts(value, 257, 4),
                pow(value, 16, 257) == 1,
            )

    def test_factor_base_predicate_is_exact(self) -> None:
        curve = Curve(17, 2, 2)
        x_values = subgroup_elements(17, 4)
        factor_base = factor_base_from_x(curve, x_values)
        expected = {point for point in curve.affine_points() if pow(point[0], 4, 17) == 1}
        self.assertEqual(set(factor_base), expected)


if __name__ == "__main__":
    unittest.main()
