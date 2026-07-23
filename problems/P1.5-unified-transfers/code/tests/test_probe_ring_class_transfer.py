"""Known-answer tests for the pairing-to-ring-class transfer."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "probe_ring_class_transfer.py"
SPEC = importlib.util.spec_from_file_location("probe_ring_class_transfer", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RingClassTransferTests(unittest.TestCase):
    def test_projective_residues_exhaust_ring_class_group(self) -> None:
        observed, expected = MODULE.validate_exact_sequence(43)
        self.assertEqual(observed, 22)
        self.assertEqual(observed, expected)

    def test_unit_orbit_has_one_class(self) -> None:
        p = 43
        for t in range(1, p):
            inverse_orbit = -pow(t, -1, p) % p
            self.assertEqual(
                MODULE.ring_class_form_from_parameter(p, t),
                MODULE.ring_class_form_from_parameter(p, inverse_orbit),
            )
        self.assertEqual(
            MODULE.ring_class_form_from_parameter(p, 0),
            MODULE.ring_class_form_from_parameter(p, None),
        )

    def test_complete_pairing_to_class_transfer(self) -> None:
        row = MODULE.run_case(43, 11, 7)
        self.assertEqual(row["recovered"], 7)
        self.assertEqual(row["image_size"], 11)
        self.assertEqual(row["class_number"], 22)
        self.assertEqual(row["discriminant"], -4 * 43 * 43)

    def test_gaussian_gcd_recovers_torus_class(self) -> None:
        field = MODULE.ExtensionField(43, (1, 0, 1))
        for t in range(43):
            form = MODULE.ring_class_form_from_parameter(43, t)
            observed = MODULE.torus_invariant_from_form(43, form, field)
            residue = field.element((1, t))
            self.assertEqual(observed, residue ** (2 * (43 - 1)))


if __name__ == "__main__":
    unittest.main()
