"""Figures for the P1.4 paper (classifying binary GHS Weil-descent genus).

All three figures are grounded in the real census CSVs written by
problems/P1.4-weil-descent-classification/code/sweep_ghs_genus.py.
"""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..",
                    "problems", "P1.4-weil-descent-classification", "data")

DEG_COLOR = {4: F.PALETTE[0], 6: F.PALETTE[1], 8: F.PALETTE[6]}
B_N = {4: 4, 6: 8, 8: 16}  # experimental low-genus slice B_n = 2^(n/2)


def load_distribution():
    """Return {n: [(genus, magic, rank, one_in_span, count), ...]} sorted by genus."""
    path = os.path.join(DATA, "ghs_genus_distribution_n4-6-8_20260623.csv")
    by_deg = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            n = int(row["absolute_degree"])
            by_deg.setdefault(n, []).append((
                int(row["genus"]),
                int(row["magic_number"]),
                int(row["conjugate_rank"]),
                int(row["one_in_conjugate_span"]),
                int(row["count"]),
            ))
    for n in by_deg:
        by_deg[n].sort()
    return by_deg


def load_locus():
    """Return {n: dict} from the low-genus locus CSV."""
    path = os.path.join(DATA, "ghs_low_genus_locus_n4-6-8_20260623.csv")
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[int(row["absolute_degree"])] = row
    return out


def fig_distribution():
    """Grouped bars: parameter count per genus value, one colour per degree."""
    dist = load_distribution()
    genera = sorted({g for rows in dist.values() for (g, *_ ) in rows})
    gpos = {g: i for i, g in enumerate(genera)}
    degrees = [4, 6, 8]
    x = np.arange(len(genera))
    w = 0.26
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for k, n in enumerate(degrees):
        counts = np.zeros(len(genera))
        for (g, _m, _r, _s, c) in dist[n]:
            counts[gpos[g]] = c
        bars = ax.bar(x + (k - 1) * w, counts, w, label=f"n = {n}",
                      color=DEG_COLOR[n], edgecolor=F.SURFACE, linewidth=0.8)
        for xi, ci in zip(x + (k - 1) * w, counts):
            if ci > 0:
                ax.text(xi, ci + 1.5, f"{int(ci)}", ha="center", va="bottom",
                        fontsize=7.0, color=F.INK_SECOND)
    ax.set_yscale("log")
    ax.set_ylim(0.7, 260)
    ax.set_xticks(x)
    ax.set_xticklabels([str(g) for g in genera], fontsize=8.5)
    ax.set_xlabel("GHS genus $g$")
    ax.set_ylabel("number of $b \\neq 0$ (log scale)")
    ax.set_title("Exact GHS genus census over $\\mathbb{F}_{2^n}$, all $b \\neq 0$")
    ax.legend(loc="upper left", ncol=3)
    ax.grid(axis="x", visible=False)
    F.finish(fig, os.path.join(OUT, "distribution.svg"))


def fig_cumulative():
    """Cumulative fraction of parameters with genus <= g, per degree; mark B_n."""
    dist = load_distribution()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for n in (4, 6, 8):
        rows = dist[n]
        total = (1 << n) - 1
        gs = [g for (g, *_ ) in rows]
        cum = np.cumsum([c for (_g, _m, _r, _s, c) in rows]) / total
        # step plot in log2 genus
        xs = [1] + gs
        ys = [0.0] + list(cum)
        ax.step(np.log2(xs), ys, where="post", color=DEG_COLOR[n],
                lw=2.0, label=f"n = {n}")
        ax.scatter(np.log2(gs), cum, s=18, color=DEG_COLOR[n], zorder=3)
        # mark the B_n = 2^(n/2) slice
        bn = B_N[n]
        frac = sum(c for (g, _m, _r, _s, c) in rows if g <= bn) / total
        ax.axvline(np.log2(bn), color=DEG_COLOR[n], lw=0.9, ls=":", alpha=0.7)
        ax.annotate(f"$B_{{{n}}}={bn}$: {frac:.3f}",
                    xy=(np.log2(bn), frac), xytext=(np.log2(bn) + 0.15, frac - 0.08),
                    fontsize=8.0, color=DEG_COLOR[n])
    ax.set_xlabel("$\\log_2 g$ (genus threshold)")
    ax.set_ylabel("fraction of $b \\neq 0$ with genus $\\leq g$")
    ax.set_title("Genus is heavy-tailed: low-genus parameters are rare")
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right")
    F.finish(fig, os.path.join(OUT, "cumulative.svg"))


def fig_branch():
    """Genus vs magic number m, showing Hess's two branches 2^(m-1) and 2^(m-1)-1."""
    dist = load_distribution()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    # theoretical upper envelope g = 2^(m-1)
    ms = np.arange(1, 9)
    ax.plot(ms, 2.0 ** (ms - 1), color=F.MUTED, lw=1.1, ls="--", zorder=1,
            label="$g = 2^{m-1}$ (upper branch)")
    ax.plot(ms, 2.0 ** (ms - 1) - 1, color=F.INK_SECOND, lw=1.0, ls=":", zorder=1,
            label="$g = 2^{m-1}-1$ (lower branch)")
    seen_labels = set()
    for n in (4, 6, 8):
        for (g, m, r, s, c) in dist[n]:
            upper = (s == 1)
            marker = "o" if upper else "s"
            lbl = None
            key = (n,)
            if key not in seen_labels:
                lbl = f"n = {n}"
                seen_labels.add(key)
            ax.scatter([m], [g], s=30 + 3 * np.log2(c + 1), marker=marker,
                       color=DEG_COLOR[n], edgecolor=F.SURFACE, linewidth=0.6,
                       zorder=3, label=lbl)
    ax.set_yscale("log", base=2)
    ax.set_xlabel("magic number $m = \\dim_{\\mathbb{F}_2}\\,\\mathrm{span}\\{(1,\\sigma^i\\sqrt{b})\\}$")
    ax.set_ylabel("GHS genus $g$ (log$_2$)")
    ax.set_title("Genus grows as $2^{m-1}$; the branch is set by $1 \\in \\mathrm{span}$")
    ax.set_xticks(range(1, 9))
    # combined legend: degree colours + branch markers
    handles, labels = ax.get_legend_handles_labels()
    marker_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=F.MUTED,
               markersize=7, label="upper branch ($1 \\in$ span)"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=F.MUTED,
               markersize=7, label="lower branch ($1 \\notin$ span)"),
    ]
    ax.legend(handles + marker_handles, labels + [h.get_label() for h in marker_handles],
              loc="upper left", fontsize=8.0, ncol=1)
    F.finish(fig, os.path.join(OUT, "branch.svg"))


if __name__ == "__main__":
    fig_distribution()
    fig_cumulative()
    fig_branch()
    print("P1.4 figures written")
