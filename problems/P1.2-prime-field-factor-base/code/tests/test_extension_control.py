from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]
for directory in (str(CODE_DIR), str(REPO_ROOT)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

from run_extension_control import run_control, solve_full_rank


class ExtensionControlTests(unittest.TestCase):
    def test_linear_solver(self) -> None:
        solution = solve_full_rank([[1, 2], [3, 2]], [0, 4], 5)
        self.assertEqual(solution, [2, 4])

    def test_planted_dlog_is_recovered(self) -> None:
        result = run_control(q=5, secret=37, max_attempts=1000, seed=12022027)
        self.assertEqual(result.summary["planted_secret"], result.summary["recovered_secret"])
        self.assertEqual(result.summary["full_rank"], 1)
        self.assertLessEqual(result.summary["attempts_used"], 1000)


if __name__ == "__main__":
    unittest.main()
