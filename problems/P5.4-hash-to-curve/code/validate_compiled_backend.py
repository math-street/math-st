"""
validate_compiled_backend.py - Compile and exhaust the Rust p=11 backend.
Sub-goal: P5.4 / SG-11
Inputs:   --seed <int> [--smoke] [--output <path>]
Outputs:  data/validate_compiled_backend_<params>_<date>.csv
Runtime:  about 3 seconds with rustc 1.93
Validated against: Python SvdW/group oracle, source audit, assembly audit
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from lib.curves import Curve, map_to_curve_svdw

SOURCE = Path(__file__).with_name("ct_backend_p11.rs")
CURVE = Curve(11, 0, 1)
Z = 1
SUBGROUP_ORDER = 3
COFACTOR = 4


def _function_body(source: str, signature: str) -> str:
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[opening + 1 : index]
    raise ValueError(f"unterminated function {signature}")


def _assembly_body(assembly: str, symbol: str) -> str:
    match = re.search(rf"(?m)^{re.escape(symbol)}:\s*$", assembly)
    if match is None:
        raise AssertionError(f"assembly symbol {symbol} not found")
    tail = assembly[match.end() :]
    end_markers = [
        position
        for marker in ("\t.seh_endproc", "\t.cfi_endproc")
        if (position := tail.find(marker)) >= 0
    ]
    if not end_markers:
        raise AssertionError(f"assembly end for {symbol} not found")
    return tail[: min(end_markers)]


def _decode_point(row: dict[str, str]) -> tuple[int, int] | None:
    if int(row["infinity"]):
        return None
    return int(row["x"]), int(row["y"])


def validate(seed: int) -> dict[str, int | str]:
    rustc = shutil.which("rustc")
    if rustc is None:
        raise RuntimeError("rustc is required for the compiled-backend validator")
    source_text = SOURCE.read_text(encoding="utf-8")
    audited_signatures = (
        'pub extern "C" fn map_svdw_p11',
        'pub extern "C" fn point_add_complete_p11',
        'pub extern "C" fn hash_field_pair_p11',
    )
    source_branch_violations = 0
    source_index_violations = 0
    for signature in audited_signatures:
        body = _function_body(source_text, signature)
        source_branch_violations += len(re.findall(r"\b(?:if|match|while)\b", body))
        source_index_violations += body.count("[") + body.count("]")
    pow_body = _function_body(source_text, "fn fpow")
    if "for bit_index in (0..64).rev()" not in pow_body:
        raise AssertionError("field exponentiation lost its fixed 64-round loop")
    if source_branch_violations or source_index_violations:
        raise AssertionError("secret-path Rust source audit failed")

    with tempfile.TemporaryDirectory(prefix="p54-ct-backend-") as temporary:
        temporary_path = Path(temporary)
        executable = temporary_path / "ct_backend_p11.exe"
        compile_result = subprocess.run(
            [
                rustc,
                "-C",
                "opt-level=3",
                "-C",
                "target-cpu=native",
                "--emit",
                f"link={executable},asm={executable.with_suffix('.s')}",
                str(SOURCE),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        assembly_path = executable.with_suffix(".s")
        assembly = assembly_path.read_text(encoding="utf-8")
        audited_symbols = (
            "map_svdw_p11",
            "point_add_complete_p11",
            "hash_field_pair_p11",
        )
        assembly_bodies = {
            symbol: _assembly_body(assembly, symbol) for symbol in audited_symbols
        }
        divide_instructions = sum(
            len(re.findall(r"\b(?:idiv|div)(?:b|w|l|q)?\b", body))
            for body in assembly_bodies.values()
        )
        if divide_instructions:
            raise AssertionError("integer divide found in audited assembly")
        jump_mnemonics = [
            match.group(1)
            for body in assembly_bodies.values()
            for match in re.finditer(r"(?m)^\s*(j(?!mp)[a-z]+)\s", body)
        ]
        conditional_jumps = len(jump_mnemonics)
        non_loop_jumps = sum(mnemonic != "jne" for mnemonic in jump_mnemonics)
        if non_loop_jumps:
            raise AssertionError("non-loop conditional jump found in audited assembly")
        execution = subprocess.run(
            [str(executable)],
            check=True,
            capture_output=True,
            text=True,
        )

    rows = list(csv.DictReader(execution.stdout.splitlines()))
    by_kind: dict[str, list[dict[str, str]]] = {
        kind: [row for row in rows if row["kind"] == kind]
        for kind in ("map", "hash", "add")
    }
    if tuple(map(len, by_kind.values())) != (11, 121, 144):
        raise AssertionError("compiled backend emitted an incomplete table")

    map_matches = 0
    for row in by_kind["map"]:
        u = int(row["left"])
        map_matches += _decode_point(row) == map_to_curve_svdw(CURVE, u, Z)

    points = [*CURVE.affine_points(), None]
    group_law_matches = 0
    for row in by_kind["add"]:
        left = points[int(row["left"])]
        right = points[int(row["right"])]
        group_law_matches += _decode_point(row) == CURVE.add(left, right)

    hash_matches = 0
    subgroup_checks = 0
    support: Counter[tuple[int, int] | None] = Counter()
    for row in by_kind["hash"]:
        u0 = int(row["left"])
        u1 = int(row["right"])
        actual = _decode_point(row)
        expected = CURVE.scalar_mul(
            COFACTOR,
            CURVE.add(
                map_to_curve_svdw(CURVE, u0, Z),
                map_to_curve_svdw(CURVE, u1, Z),
            ),
        )
        hash_matches += actual == expected
        subgroup_checks += CURVE.scalar_mul(SUBGROUP_ORDER, actual) is None
        support[actual] += 1

    if (map_matches, group_law_matches, hash_matches, subgroup_checks) != (
        11,
        144,
        121,
        121,
    ):
        raise AssertionError("compiled backend disagreed with Python oracle")
    rustc_version = subprocess.run(
        [rustc, "--version"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return {
        "backend": "rust-u64-p11",
        "compiler": rustc_version,
        "seed": seed,
        "map_inputs": 11,
        "map_matches": map_matches,
        "group_pairs": 144,
        "group_law_matches": group_law_matches,
        "hash_pairs": 121,
        "hash_matches": hash_matches,
        "subgroup_checks": subgroup_checks,
        "support_size": len(support),
        "source_branch_violations": source_branch_violations,
        "source_index_violations": source_index_violations,
        "assembly_divides": divide_instructions,
        "assembly_conditional_jumps": conditional_jumps,
        "assembly_non_loop_jumps": non_loop_jumps,
        "compile_warnings": int(bool(compile_result.stderr.strip())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=5409)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    row = validate(args.seed)
    output = args.output or (
        Path(__file__).resolve().parents[1]
        / "data"
        / f"validate_compiled_backend_p11_{date.today():%Y%m%d}.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(f"wrote 1 row to {output}")
    print(
        "validated "
        f"{row['map_inputs']} maps, {row['group_pairs']} group pairs, "
        f"and {row['hash_pairs']} hash pairs"
    )


if __name__ == "__main__":
    main()
