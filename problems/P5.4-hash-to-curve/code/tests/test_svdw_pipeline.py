from __future__ import annotations

import ast
import inspect
import sys
import textwrap
import unittest
from pathlib import Path

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = PROBLEM_ROOT.parents[1]
for path in (REPOSITORY_ROOT, PROBLEM_ROOT / "code"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from lib.curves import (
    BinaryField,
    Curve,
    TwistedEdwardsCurve,
    find_svdw_z,
    map_to_curve_svdw,
    map_to_curve_svdw_montgomery,
    montgomery_to_twisted_edwards,
    svdw_parameters_are_valid,
    weierstrass_to_montgomery,
)
from lib.small_characteristic import (
    BinaryWeierstrassCurve,
    CharacteristicThreeCurve,
    add_complete_binary,
    add_complete_characteristic_three,
    map_binary_shallue_van_de_woestijne,
    map_characteristic_three_square_discriminant,
)
from lib.isogeny import velu_map_affine_nonkernel
from lib.finite_fields import add_complete_extension_weierstrass
from hash_pipeline import (
    TOY_EDWARDS_SUITE,
    TOY_MONTGOMERY_SUITE,
    TOY_SUITES,
    expand_message_xmd_sha256,
    hash_to_field_sha256,
)
from measure_extended_timing import measure_rows as measure_extended_rows
from measure_extended_timing import summarize_rows as summarize_extended_rows
from search_exceptional_isogenies import search
from validate_curve_transports import validate as validate_transports
from validate_compiled_backend import validate as validate_compiled
from validate_extension_svdw import (
    CURVE as EXTENSION_CURVE,
    FIELD as EXTENSION_FIELD,
    Z as EXTENSION_Z,
    svdw_extension_oracle,
    validate as validate_extension,
)
from validate_extension_pipeline import validate as validate_extension_pipeline
from validate_hash_pipeline import RFC_XMD_DST, RFC_XMD_VECTORS, validate as validate_hash
from validate_isogeny_workarounds import FIXTURES, map_via_isogeny, validate
from validate_small_characteristic import validate as validate_small_characteristic
from validate_small_characteristic_pipelines import validate as validate_small_pipelines
from validate_svdw import SVDW_CASES, svdw_oracle, validate_primes


class SvdwMapTests(unittest.TestCase):
    def test_fixed_known_outputs(self) -> None:
        self.assertEqual(map_to_curve_svdw(Curve(11, 0, 1), 0, 1), (5, 4))
        self.assertEqual(map_to_curve_svdw(Curve(11, 1, 0), 0, 10), (8, 6))

    def test_finder_uses_rfc_candidate_order(self) -> None:
        self.assertEqual(find_svdw_z(Curve(11, 1, 1)), 1)
        self.assertEqual(find_svdw_z(Curve(11, 1, 0)), 10)

    def test_source_has_no_input_dependent_branch_or_indexing(self) -> None:
        tree = ast.parse(inspect.getsource(map_to_curve_svdw))
        function_node = tree.body[0]
        self.assertIsInstance(function_node, ast.FunctionDef)
        for statement in function_node.body:
            for node in ast.walk(statement):
                if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                    referenced = {
                        child.id
                        for child in ast.walk(node.test)
                        if isinstance(child, ast.Name)
                    }
                    self.assertNotIn("u", referenced)
                self.assertNotIsInstance(node, ast.Subscript)

    def test_exhaustive_oracle_on_all_three_families(self) -> None:
        for p, cases in SVDW_CASES.items():
            for _family, a, b in cases:
                curve = Curve(p, a, b)
                z = find_svdw_z(curve)
                self.assertTrue(svdw_parameters_are_valid(curve, z))
                schedules = set()
                for u in range(p):
                    trace: list[str] = []
                    actual = map_to_curve_svdw(curve, u, z, trace=trace)
                    self.assertEqual(actual, svdw_oracle(curve, u, z))
                    self.assertTrue(curve.contains(actual))
                    schedules.add(tuple(trace))
                self.assertEqual(len(schedules), 1)

    def test_invalid_z_is_rejected(self) -> None:
        curve = Curve(11, 0, 1)
        self.assertFalse(svdw_parameters_are_valid(curve, 0))
        with self.assertRaisesRegex(ValueError, "SvdW parameter predicates"):
            map_to_curve_svdw(curve, 3, 0)

    def test_smoke_summary_has_no_failures(self) -> None:
        rows = validate_primes([11, 13], seed=5403)
        self.assertEqual(len(rows), 6)
        for row in rows:
            self.assertEqual(row["inputs_tested"], row["on_curve"])
            self.assertEqual(row["inputs_tested"], row["oracle_matches"])
            self.assertEqual(row["schedule_variants"], 1)


class ExtensionSvdwTests(unittest.TestCase):
    def test_exhaustive_f_7_cubed_oracle(self) -> None:
        from lib.finite_fields import map_to_curve_svdw_extension

        schedules = set()
        for value in EXTENSION_FIELD.elements():
            trace: list[str] = []
            actual = map_to_curve_svdw_extension(
                EXTENSION_CURVE,
                EXTENSION_Z,
                value,
                trace=trace.append,
            )
            self.assertEqual(
                actual,
                svdw_extension_oracle(EXTENSION_CURVE, EXTENSION_Z, value),
            )
            self.assertTrue(EXTENSION_CURVE.contains(actual))
            schedules.add(tuple(trace))
        self.assertEqual(len(schedules), 1)

    def test_extension_validation_summary(self) -> None:
        row = validate_extension(seed=5404)
        self.assertEqual(row["inputs_tested"], 343)
        self.assertEqual(row["inverse_checks"], 342)
        self.assertEqual(row["on_curve"], 343)
        self.assertEqual(row["oracle_matches"], 343)
        self.assertEqual(row["schedule_variants"], 1)

    def test_extension_complete_pipeline_smoke(self) -> None:
        row = validate_extension_pipeline(seed=5411, smoke=True)
        self.assertEqual(row["group_pairs"], 1024)
        self.assertEqual(row["group_pairs"], row["group_law_matches"])
        self.assertEqual(row["schedule_variants"], 1)

    def test_extension_complete_add_has_no_point_dependent_branch(self) -> None:
        tree = ast.parse(inspect.getsource(add_complete_extension_weierstrass))
        function_node = tree.body[0]
        self.assertIsInstance(function_node, ast.FunctionDef)
        for statement in function_node.body:
            for node in ast.walk(statement):
                if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                    referenced = {
                        child.id
                        for child in ast.walk(node.test)
                        if isinstance(child, ast.Name)
                    }
                    self.assertTrue(
                        referenced.isdisjoint(
                            {"left", "right", "x1", "y1", "x2", "y2"}
                        )
                    )


class SmallCharacteristicTests(unittest.TestCase):
    def test_characteristic_three_fixed_outputs(self) -> None:
        curve = CharacteristicThreeCurve(1, 2)
        self.assertEqual(
            [map_characteristic_three_square_discriminant(curve, t) for t in range(3)],
            [(1, 2), (1, 1), (1, 2)],
        )

    def test_binary_fixed_outputs(self) -> None:
        field = BinaryField(3, 0b1011)
        curve = BinaryWeierstrassCurve(field, 1, 1)
        self.assertEqual(
            [map_binary_shallue_van_de_woestijne(curve, t) for t in range(8)],
            [(0, 1), (0, 1), (3, 0), (7, 0), (5, 0), (3, 0), (7, 0), (5, 0)],
        )

    def test_small_characteristic_exhaustive_summaries(self) -> None:
        rows = validate_small_characteristic([3, 5, 7], seed=5408)
        self.assertEqual(sum(int(row["inputs_tested"]) for row in rows), 174)
        for row in rows:
            self.assertEqual(row["inputs_tested"], row["on_curve"])
            self.assertEqual(row["inputs_tested"], row["oracle_matches"])
            self.assertEqual(row["schedule_variants"], 1)
            self.assertLessEqual(int(row["maximum_preimage"]), 6)

    def test_mapping_sources_have_no_input_branch_or_index(self) -> None:
        for function, secret in (
            (map_characteristic_three_square_discriminant, "t"),
            (map_binary_shallue_van_de_woestijne, "t"),
        ):
            tree = ast.parse(inspect.getsource(function))
            function_node = tree.body[0]
            self.assertIsInstance(function_node, ast.FunctionDef)
            for statement in function_node.body:
                for node in ast.walk(statement):
                    if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                        referenced = {
                            child.id
                            for child in ast.walk(node.test)
                            if isinstance(child, ast.Name)
                        }
                        self.assertNotIn(secret, referenced)
                    if isinstance(node, ast.Subscript):
                        referenced = {
                            child.id
                            for child in ast.walk(node.slice)
                            if isinstance(child, ast.Name)
                        }
                        self.assertNotIn(secret, referenced)

    def test_small_characteristic_complete_pipeline_smoke(self) -> None:
        rows = validate_small_pipelines([3], seed=5410)
        self.assertEqual(sum(int(row["field_pairs"]) for row in rows), 73)
        for row in rows:
            self.assertEqual(row["group_pairs"], row["group_law_matches"])
            self.assertEqual(row["field_pairs"], row["pipeline_oracle_matches"])
            self.assertEqual(row["field_pairs"], row["subgroup_checks"])
            self.assertEqual(row["subgroup_order"], row["subgroup_support"])
            self.assertEqual(row["schedule_variants"], 1)

    def test_complete_add_sources_have_no_point_dependent_branch(self) -> None:
        for function in (add_complete_characteristic_three, add_complete_binary):
            tree = ast.parse(inspect.getsource(function))
            function_node = tree.body[0]
            self.assertIsInstance(function_node, ast.FunctionDef)
            for statement in function_node.body:
                for node in ast.walk(statement):
                    if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                        referenced = {
                            child.id
                            for child in ast.walk(node.test)
                            if isinstance(child, ast.Name)
                        }
                        self.assertTrue(
                            referenced.isdisjoint(
                                {"left", "right", "x1", "y1", "x2", "y2"}
                            )
                        )


class CompiledBackendTests(unittest.TestCase):
    def test_rust_backend_matches_all_toy_oracles(self) -> None:
        row = validate_compiled(seed=5409)
        self.assertEqual(row["map_inputs"], row["map_matches"])
        self.assertEqual(row["group_pairs"], row["group_law_matches"])
        self.assertEqual(row["hash_pairs"], row["hash_matches"])
        self.assertEqual(row["hash_pairs"], row["subgroup_checks"])
        self.assertEqual(row["support_size"], 3)
        self.assertEqual(row["source_branch_violations"], 0)
        self.assertEqual(row["source_index_violations"], 0)
        self.assertEqual(row["assembly_divides"], 0)
        self.assertEqual(row["assembly_non_loop_jumps"], 0)
        self.assertEqual(row["compile_warnings"], 0)


class ExceptionalIsogenyTests(unittest.TestCase):
    def test_exhaustive_workaround_fixtures(self) -> None:
        rows = validate(seed=5405)
        self.assertEqual({row["family"] for row in rows}, {"j0", "j1728"})
        for row in rows:
            self.assertEqual(row["source_order"], row["target_order"])
            self.assertEqual(row["map_inputs"], row["nonidentity_outputs"])
            self.assertEqual(row["schedule_variants"], 1)

    def test_isogeny_workaround_fixed_outputs(self) -> None:
        self.assertEqual(map_via_isogeny(FIXTURES[0], 0), (27, 1))
        self.assertEqual(map_via_isogeny(FIXTURES[1], 0), (32, 24))

    def test_affine_velu_source_has_no_point_dependent_branch_or_indexing(self) -> None:
        tree = ast.parse(inspect.getsource(velu_map_affine_nonkernel))
        function_node = tree.body[0]
        self.assertIsInstance(function_node, ast.FunctionDef)
        for statement in function_node.body:
            for node in ast.walk(statement):
                if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                    referenced = {
                        child.id
                        for child in ast.walk(node.test)
                        if isinstance(child, ast.Name)
                    }
                    self.assertTrue(referenced.isdisjoint({"point", "x", "y"}))
                self.assertNotIsInstance(node, ast.Subscript)

    def test_smoke_search_finds_both_exceptional_families(self) -> None:
        rows, counters = search(bound=20, seed=5404)
        self.assertEqual(
            {str(row["target_family"]) for row in rows},
            {"j0", "j1728"},
        )
        self.assertGreater(counters["curves"], 0)
        self.assertGreater(counters["kernels"], 0)


class HashPipelineTests(unittest.TestCase):
    def test_rfc_expand_message_xmd_vectors(self) -> None:
        for message, length, expected_hex in RFC_XMD_VECTORS:
            self.assertEqual(
                expand_message_xmd_sha256(message, RFC_XMD_DST, length).hex(),
                expected_hex,
            )

    def test_hash_to_field_returns_two_field_elements(self) -> None:
        values = hash_to_field_sha256(b"abc", 2, 13, TOY_SUITES[0].dst)
        self.assertEqual(len(values), 2)
        self.assertTrue(all(0 <= value < 13 for value in values))

    def test_all_compile_time_suite_cases_clear_to_subgroup(self) -> None:
        rows = validate_hash(seed=5406)
        self.assertEqual(len(rows), 6)
        self.assertEqual(
            {str(row["method"]) for row in rows},
            {"sswu", "svdw", "sswu_isogeny"},
        )
        for row in rows:
            self.assertEqual(row["field_pairs"], row["subgroup_checks"])
            self.assertEqual(row["support_size"], row["subgroup_order"])
            self.assertEqual(row["map_schedule_variants"], 1)

    def test_montgomery_and_edwards_transport_pipelines(self) -> None:
        rows = validate_transports(seed=5407)
        self.assertEqual(
            {str(row["form"]) for row in rows},
            {"montgomery", "twisted_edwards"},
        )
        for row in rows:
            self.assertEqual(row["inputs_tested"], row["on_curve"])
            self.assertEqual(row["inputs_tested"], row["oracle_matches"])
            self.assertEqual(row["schedule_variants"], 1)
        self.assertEqual(TOY_MONTGOMERY_SUITE.hash_to_curve(b"abc"), (3, 6))
        self.assertEqual(TOY_EDWARDS_SUITE.hash_to_curve(b"abc"), (4, 4))

    def test_transport_and_edwards_add_sources_do_not_branch_on_points(self) -> None:
        audited = (
            montgomery_to_twisted_edwards,
            weierstrass_to_montgomery,
            map_to_curve_svdw_montgomery,
            TwistedEdwardsCurve.add,
        )
        for function in audited:
            tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
            function_node = tree.body[0]
            self.assertIsInstance(function_node, ast.FunctionDef)
            for statement in function_node.body:
                for node in ast.walk(statement):
                    if isinstance(node, (ast.If, ast.IfExp, ast.While)):
                        referenced = {
                            child.id
                            for child in ast.walk(node.test)
                            if isinstance(child, ast.Name)
                        }
                        self.assertTrue(
                            referenced.isdisjoint(
                                {"point", "left", "right", "u", "v1", "w1", "v2", "w2"}
                            )
                        )
                    self.assertNotIsInstance(node, ast.Subscript)

    def test_extended_timing_smoke_has_all_classes(self) -> None:
        rows = measure_extended_rows(samples=2, batch=1, seed=5408)
        summaries = summarize_extended_rows(
            rows,
            bootstrap_resamples=10,
            seed=5408,
        )
        self.assertEqual(len(summaries), 6)
        self.assertTrue(all(float(row["mean_ratio_a_over_b"]) > 0 for row in summaries))


if __name__ == "__main__":
    unittest.main()
