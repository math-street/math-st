"""
sweep_ghs_genus.py — exhaust the classical binary GHS parameter locus.
Sub-goal: P1.4 / SG-02 through SG-05
Inputs:   --degrees <n...> --date <YYYYMMDD> [--smoke]
Outputs:  data/sweep_ghs_genus_n4-6-8_<date>.csv and an SVG distribution
Runtime:  ~0.64 seconds for the complete n in {4,6,8} sweep
Validated against: Hess's exact genus formula and the separate published-example test
"""

from __future__ import annotations

import argparse
import csv
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

from ghs import apply_frobenius_polynomial, format_binary_polynomial, ghs_profile
from lib.curves import BinaryField, find_irreducible_binary_polynomial


KNOWN_MODULI = {
    4: 0b1_0011,
    6: 0b1_000011,
    8: 0x11B,
}


def field_for_degree(degree: int) -> BinaryField:
    modulus = KNOWN_MODULI.get(degree)
    if modulus is None:
        modulus = find_irreducible_binary_polynomial(degree)
    return BinaryField(degree, modulus)


def enumerate_rows(degrees: list[int]) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for degree in degrees:
        field = field_for_degree(degree)
        for b in range(1, field.order):
            profile = ghs_profile(field, b, a=0, base_degree=1)
            j = field.inverse(b)
            frobenius_b = field.square(b)
            conjugate_profile = ghs_profile(field, frobenius_b, a=0, base_degree=1)
            invariant = (
                profile.conjugate_rank,
                profile.one_in_conjugate_span,
                profile.magic_number,
                profile.genus,
            )
            conjugate_invariant = (
                conjugate_profile.conjugate_rank,
                conjugate_profile.one_in_conjugate_span,
                conjugate_profile.magic_number,
                conjugate_profile.genus,
            )
            if invariant != conjugate_invariant:
                raise AssertionError("GHS invariants changed under Frobenius")
            if field.mul(b, j) != 1:
                raise AssertionError("j=1/b invariant failed")
            rows.append(
                {
                    "absolute_degree": degree,
                    "field_modulus_hex": hex(field.modulus),
                    "a_hex": "0x0",
                    "b_hex": hex(b),
                    "sqrt_b_hex": hex(profile.sqrt_b),
                    "j_hex": hex(j),
                    "frobenius_annihilator_hex": hex(profile.annihilator_polynomial),
                    "frobenius_annihilator": format_binary_polynomial(
                        profile.annihilator_polynomial
                    ),
                    "conjugate_rank": profile.conjugate_rank,
                    "one_in_conjugate_span": int(profile.one_in_conjugate_span),
                    "magic_number": profile.magic_number,
                    "genus": profile.genus,
                    "frobenius_orbit_size": profile.orbit_size,
                    "regularity_satisfied": int(profile.regularity_satisfied),
                    "seed": "none",
                }
            )
    return rows


def write_csv(rows: list[dict[str, int | str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def distribution_rows(rows: list[dict[str, int | str]]) -> list[dict[str, int | str]]:
    counts: Counter[tuple[int, int, int, int, int, str, str, int]] = Counter()
    for row in rows:
        key = (
            int(row["absolute_degree"]),
            int(row["genus"]),
            int(row["magic_number"]),
            int(row["conjugate_rank"]),
            int(row["one_in_conjugate_span"]),
            str(row["frobenius_annihilator_hex"]),
            str(row["frobenius_annihilator"]),
            int(row["frobenius_orbit_size"]),
        )
        counts[key] += 1
    result: list[dict[str, int | str]] = []
    for key in sorted(counts):
        degree, genus, magic, rank, contains_one, ann_hex, ann, orbit_size = key
        count = counts[key]
        density = Fraction(count, (1 << degree) - 1)
        result.append(
            {
                "absolute_degree": degree,
                "genus": genus,
                "magic_number": magic,
                "conjugate_rank": rank,
                "one_in_conjugate_span": contains_one,
                "frobenius_annihilator_hex": ann_hex,
                "frobenius_annihilator": ann,
                "frobenius_orbit_size": orbit_size,
                "count": count,
                "density_exact": f"{density.numerator}/{density.denominator}",
                "density_decimal": f"{float(density):.12f}",
            }
        )
    return result


def is_additive_with_zero(values: set[int]) -> bool:
    return all(left ^ right in values for left in values for right in values)


def format_sparse_polynomial(exponents: list[int], variable: str) -> str:
    terms = []
    for exponent in sorted(exponents, reverse=True):
        if exponent == 0:
            terms.append("1")
        elif exponent == 1:
            terms.append(variable)
        else:
            terms.append(f"{variable}^{exponent}")
    return "+".join(terms)


def low_genus_locus_rows(
    rows: list[dict[str, int | str]], degrees: list[int]
) -> list[dict[str, int | str]]:
    result: list[dict[str, int | str]] = []
    for degree in sorted(degrees):
        degree_rows = [row for row in rows if int(row["absolute_degree"]) == degree]
        genus_bound = 1 << (degree // 2)
        low_rows = [row for row in degree_rows if int(row["genus"]) <= genus_bound]
        defining_row = max(
            low_rows,
            key=lambda row: int(row["frobenius_annihilator_hex"], 16).bit_length(),
        )
        defining_annihilator = int(defining_row["frobenius_annihilator_hex"], 16)
        annihilator_degree = defining_annihilator.bit_length() - 1
        frobenius_exponents = [
            1 << index
            for index in range(annihilator_degree + 1)
            if defining_annihilator >> index & 1
        ]
        reciprocal_exponents = [
            (1 << annihilator_degree) - exponent for exponent in frobenius_exponents
        ]
        field = field_for_degree(degree)
        kernel = {
            value
            for value in range(field.order)
            if apply_frobenius_polynomial(field, value, defining_annihilator, 1) == 0
        }
        b_values = {0} | {int(row["b_hex"], 16) for row in low_rows}
        if kernel != b_values:
            raise AssertionError("reported low-genus b-locus is not the claimed kernel")
        j_values = {0} | {int(row["j_hex"], 16) for row in low_rows}
        full_degree_rows = [
            row
            for row in degree_rows
            if int(row["frobenius_orbit_size"]) == degree
        ]
        count = len(low_rows)
        density = Fraction(count, (1 << degree) - 1)
        result.append(
            {
                "absolute_degree": degree,
                "genus_bound": genus_bound,
                "parameter_count": count,
                "density_exact": f"{density.numerator}/{density.denominator}",
                "density_decimal": f"{float(density):.12f}",
                "b_locus_with_zero_dimension": (len(b_values)).bit_length() - 1,
                "defining_annihilator_hex": hex(defining_annihilator),
                "defining_annihilator": format_binary_polynomial(defining_annihilator),
                "b_locus_equation": f"{format_sparse_polynomial(frobenius_exponents, 'b')}=0",
                "j_locus_equation_for_nonzero_j": f"{format_sparse_polynomial(reciprocal_exponents, 'j')}=0",
                "b_locus_additive_with_zero": int(is_additive_with_zero(b_values)),
                "j_locus_additive_with_zero": int(is_additive_with_zero(j_values)),
                "frobenius_stable": 1,
                "full_degree_count_within_bound": sum(
                    int(row["frobenius_orbit_size"]) == degree for row in low_rows
                ),
                "minimum_full_degree_genus": min(
                    int(row["genus"]) for row in full_degree_rows
                ),
            }
        )
    return result


def write_svg(rows: list[dict[str, int | str]], output: Path) -> None:
    degree_counts: dict[int, Counter[int]] = {}
    for row in rows:
        degree = int(row["absolute_degree"])
        degree_counts.setdefault(degree, Counter())[int(row["genus"])] += 1
    genera = sorted({genus for counts in degree_counts.values() for genus in counts})
    degrees = sorted(degree_counts)
    width, height = 920, 520
    left, top, plot_width, plot_height = 80, 60, 780, 360
    max_count = max(count for counts in degree_counts.values() for count in counts.values())
    group_width = plot_width / max(1, len(genera))
    bar_width = group_width / (len(degrees) + 1)
    colors = {degree: color for degree, color in zip(degrees, ("#255f85", "#d26a35", "#588157", "#7b2cbf"))}
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f7f3e8"/>',
        '<text x="80" y="32" font-family="Georgia,serif" font-size="22" fill="#18212b">Classical binary GHS genus distribution</text>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#18212b"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#18212b"/>',
    ]
    for index, genus in enumerate(genera):
        group_x = left + index * group_width
        for offset, degree in enumerate(degrees):
            count = degree_counts[degree][genus]
            bar_height = 0 if max_count == 0 else plot_height * count / max_count
            x = group_x + (offset + 0.5) * bar_width
            y = top + plot_height - bar_height
            svg.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width * 0.82:.2f}" height="{bar_height:.2f}" fill="{colors[degree]}"/>'
            )
            if count:
                svg.append(
                    f'<text x="{x + bar_width * 0.41:.2f}" y="{max(top + 12, y - 5):.2f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#18212b">{count}</text>'
                )
        svg.append(
            f'<text x="{group_x + group_width / 2:.2f}" y="{top + plot_height + 24}" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#18212b">g={genus}</text>'
        )
    for index, degree in enumerate(degrees):
        legend_x = left + 170 * index
        svg.append(f'<rect x="{legend_x}" y="470" width="16" height="16" fill="{colors[degree]}"/>')
        svg.append(
            f'<text x="{legend_x + 24}" y="483" font-family="Arial,sans-serif" font-size="14" fill="#18212b">n={degree}</text>'
        )
    svg.append('</svg>')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(svg) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degrees", nargs="+", type=int, default=[4, 6, 8])
    parser.add_argument("--date", default="20260623")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--locus", type=Path)
    parser.add_argument("--figure", type=Path)
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    degrees = [4] if args.smoke else args.degrees
    suffix = "-".join(str(degree) for degree in degrees)
    root = Path(__file__).resolve().parents[1]
    output = args.output or root / "data" / f"sweep_ghs_genus_n{suffix}_{args.date}.csv"
    summary = args.summary or root / "data" / f"ghs_genus_distribution_n{suffix}_{args.date}.csv"
    locus = args.locus or root / "data" / f"ghs_low_genus_locus_n{suffix}_{args.date}.csv"
    figure = args.figure or root / "figures" / f"sweep_ghs_genus_n{suffix}_{args.date}.svg"
    started = time.perf_counter()
    rows = enumerate_rows(degrees)
    expected = sum((1 << degree) - 1 for degree in degrees)
    if len(rows) != expected:
        raise AssertionError(f"expected {expected} rows, got {len(rows)}")
    write_csv(rows, output)
    write_csv(distribution_rows(rows), summary)
    write_csv(low_genus_locus_rows(rows, degrees), locus)
    write_svg(rows, figure)
    elapsed = time.perf_counter() - started
    print(f"rows={len(rows)} elapsed_seconds={elapsed:.6f}")
    print(f"csv={output}")
    print(f"summary={summary}")
    print(f"locus={locus}")
    print(f"figure={figure}")


if __name__ == "__main__":
    main()
