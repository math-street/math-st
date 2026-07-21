from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from torus_alternative import (
    enumerate_norm_one_torus,
    torus_embed,
    torus_extract,
    torus_mul,
    torus_on_curve,
)


class TorusAlternativeTests(unittest.TestCase):
    def test_parametrization_and_extraction_are_exhaustive(self) -> None:
        for prime, nonsquare in ((7, 3), (11, 2), (13, 2), (17, 3)):
            torus = enumerate_norm_one_torus(prime, nonsquare)
            self.assertEqual(len(torus), prime + 1)
            embedded = {torus_embed(prime, nonsquare, t) for t in range(prime)}
            self.assertEqual(len(embedded), prime)
            self.assertEqual(embedded, torus - {((-1) % prime, 0)})
            for t in range(prime):
                point = torus_embed(prime, nonsquare, t)
                self.assertTrue(torus_on_curve(prime, nonsquare, point))
                self.assertEqual(torus_extract(prime, point), t)

    def test_group_law_is_closed_and_has_identity(self) -> None:
        prime, nonsquare = 11, 2
        torus = enumerate_norm_one_torus(prime, nonsquare)
        identity = (1, 0)
        for left in torus:
            self.assertEqual(torus_mul(prime, nonsquare, left, identity), left)
            for right in torus:
                self.assertIn(
                    torus_mul(prime, nonsquare, left, right),
                    torus,
                )


if __name__ == "__main__":
    unittest.main()
