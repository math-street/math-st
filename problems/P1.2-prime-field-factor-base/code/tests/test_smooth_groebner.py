from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from benchmark_smooth_groebner import build_system, polynomial_stats


class SmoothGroebnerTests(unittest.TestCase):
    def test_direct_and_chain_systems_contain_known_solution(self) -> None:
        direct_equations, direct_variables, direct_target = build_system(17, 2, 11, 4, "direct")
        chain_equations, chain_variables, chain_target = build_system(17, 2, 11, 4, "chain")
        self.assertEqual(direct_target, chain_target)
        self.assertEqual(len(direct_variables), 3)
        self.assertEqual(len(chain_variables), 6)
        direct_degree, _ = polynomial_stats(direct_equations, direct_variables, 17)
        chain_degree, _ = polynomial_stats(chain_equations, chain_variables, 17)
        self.assertGreaterEqual(direct_degree, 4)
        self.assertLessEqual(chain_degree, direct_degree)


if __name__ == "__main__":
    unittest.main()
