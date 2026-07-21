"""Figures for the P5.2 paper (small CM discriminant and ECDLP security).

All three figures are generated from the real measurement CSVs produced by
`problems/P5.2-cm-discriminant-security/code/{measure_unit_rho,measure_nonunit_orbits}.py`.
"""
import os, sys, csv, math
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                    "problems", "P5.2-cm-discriminant-security", "data")


def _read(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


TABLE = "measure_unit_rho_table_r20_b12-14-16-18_t200_s52022026_20260707_summary.csv"
FLOYD = "measure_unit_rho_b12-14-16-18_t200_s52022026_20260702_summary.csv"
ESCAPE = "measure_unit_rho_escape_b12-14-16-18_t200_s52022026_20260707_summary.csv"
NONUNIT = "measure_nonunit_orbits_b10-12-14-16-18_n16_s72022026_20260711_summary.csv"


def fig_ceiling():
    """Measured collision-table unit-orbit speedup vs the sqrt(m) ceiling."""
    rows = _read(TABLE)
    fig, ax = plt.subplots(figsize=(5.8, 3.4))
    styles = {
        "-3": (F.PALETTE[0], "o", r"$D=-3$ (unit order 6)"),
        "-4": (F.PALETTE[1], "s", r"$D=-4$ (unit order 4)"),
    }
    for disc, (color, marker, label) in styles.items():
        sub = [r for r in rows if r["discriminant"] == disc]
        sub.sort(key=lambda r: int(r["bits"]))
        x = [int(r["bits"]) for r in sub]
        y = [float(r["speedup_ratio_of_means"]) for r in sub]
        lo = [float(r["speedup_ratio_of_means"]) - float(r["speedup_ci95_low"]) for r in sub]
        hi = [float(r["speedup_ci95_high"]) - float(r["speedup_ratio_of_means"]) for r in sub]
        ax.errorbar(x, y, yerr=[lo, hi], fmt=marker + "-", color=color, capsize=3,
                    lw=1.8, markersize=6, markeredgecolor=F.SURFACE,
                    markeredgewidth=0.8, label=label)
    ax.axhline(math.sqrt(6), color=F.PALETTE[0], lw=1.1, ls="--")
    ax.axhline(2.0, color=F.PALETTE[1], lw=1.1, ls="--")
    ax.text(18.05, math.sqrt(6) + 0.02, r"$\sqrt{6}\approx2.449$",
            color=F.PALETTE[0], fontsize=9, ha="right", va="bottom")
    ax.text(18.05, 2.0 - 0.03, r"$2$", color=F.PALETTE[1], fontsize=9,
            ha="right", va="top")
    ax.set_xticks([12, 14, 16, 18])
    ax.set_xlabel("field size (bits of $p$)")
    ax.set_ylabel("mean-transition speedup ratio")
    ax.set_title("Unit-orbit quotient rho matches its constant ceiling")
    ax.set_ylim(1.6, 2.85)
    ax.legend(loc="lower left", fontsize=9)
    F.finish(fig, os.path.join(OUT, "ceiling.svg"))


def fig_variants():
    """Three cycle-handling variants: collision-table stays flat, the others collapse."""
    table = {r["bits"] + r["discriminant"]: r for r in _read(TABLE)}
    floyd = {r["bits"] + r["discriminant"]: r for r in _read(FLOYD)}
    escape = {r["bits"] + r["discriminant"]: r for r in _read(ESCAPE)}
    bits = [12, 14, 16, 18]
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3), sharey=True)
    panels = [("-3", math.sqrt(6), r"$D=-3$: ideal $\sqrt{6}$"),
              ("-4", 2.0, r"$D=-4$: ideal $2$")]
    for ax, (disc, ideal, title) in zip(axes, panels):
        def series(src):
            return [float(src[f"{b}{disc}"]["speedup_ratio_of_means"]) for b in bits]
        ax.plot(bits, series(table), "o-", color=F.PALETTE[2], lw=1.9,
                markeredgecolor=F.SURFACE, markeredgewidth=0.8,
                label="collision table")
        ax.plot(bits, series(floyd), "s-", color=F.PALETTE[3], lw=1.9,
                markeredgecolor=F.SURFACE, markeredgewidth=0.8,
                label="naive Floyd")
        ax.plot(bits, series(escape), "^-", color=F.PALETTE[7], lw=1.9,
                markeredgecolor=F.SURFACE, markeredgewidth=0.8,
                label="doubling escape")
        ax.axhline(ideal, color=F.MUTED, lw=1.0, ls=":")
        ax.axhline(1.0, color=F.INK_SECOND, lw=0.8, ls="-", alpha=0.4)
        ax.set_yscale("log")
        ax.set_xticks(bits)
        ax.set_xlabel("field size (bits of $p$)")
        ax.set_title(title, fontsize=11)
    axes[0].set_ylabel("speedup ratio (log scale)")
    axes[0].legend(loc="lower left", fontsize=8.6)
    F.finish(fig, os.path.join(OUT, "variants.svg"))


def fig_nonunit():
    """Non-unit D=-7 orbit: enumeration cost grows as m, ideal gain only as sqrt(m)."""
    rows = _read(NONUNIT)
    rows.sort(key=lambda r: int(r["subgroup_bits"]))
    xb = [int(r["subgroup_bits"]) for r in rows]
    m = [int(r["scalar_order"]) for r in rows]
    evals = [int(r["map_evaluations_per_normalization"]) for r in rows]
    ideal = [float(r["ideal_random_mapping_speedup"]) for r in rows]
    ratio = [float(r["enumeration_to_ideal_gain_ratio"]) for r in rows]

    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    ax.plot(xb, evals, "o-", color=F.PALETTE[7], lw=2.0,
            markeredgecolor=F.SURFACE, markeredgewidth=0.8,
            label=r"canonicalizer cost $m-1$ (map evals)")
    ax.plot(xb, ideal, "s-", color=F.PALETTE[2], lw=2.0,
            markeredgecolor=F.SURFACE, markeredgewidth=0.8,
            label=r"ideal orbit gain $\sqrt{m}$")
    ax.set_yscale("log")
    ax.set_xticks(xb)
    ax.set_xlabel("subgroup size (bits of $r$)")
    ax.set_ylabel("count (log scale)")
    ax.set_title("Non-unit orbit: enumeration outruns the collision gain")
    for xi, mi, ri in zip(xb, m, ratio):
        ax.annotate(f"m={mi}", (xi, mi), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7.6, color=F.INK_SECOND)
    ax.legend(loc="upper left", fontsize=9)
    F.finish(fig, os.path.join(OUT, "nonunit.svg"))


if __name__ == "__main__":
    fig_ceiling()
    fig_variants()
    fig_nonunit()
    print("P5.2 figures written")
