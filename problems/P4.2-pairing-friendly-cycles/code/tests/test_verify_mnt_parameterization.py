from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from verify_mnt_parameterization import verify_mnt_pair  # noqa: E402


class MntParameterizationTests(unittest.TestCase):
    def test_published_and_reverse_orientations(self) -> None:
        published = verify_mnt_pair(37, 43, 6, 4)
        reverse = verify_mnt_pair(31, 37, 4, 6)
        self.assertEqual(published.parameter_x, 3)
        self.assertEqual(reverse.parameter_x, 3)

    def test_non_mnt_fields_are_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            verify_mnt_pair(7, 11, 6, 4)


if __name__ == "__main__":
    unittest.main()

