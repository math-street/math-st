"""Figures for the P1.6 paper (the height obstruction to lifting)."""
import csv
import os, sys
from math import log
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems", "P1.6-height-obstruction", "data")

GROWTH_STEM = "measure_height_growth_b5-7-9-11-13-15_t3_v3_i5_s16062026_20260703"
RELATIONS_STEM = "analyze_lift_relations_b5-7-9-11_B8_allv_20260714"

PRIMES = [31, 127, 503, 2039, 8191, 32719]


def read_rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fig_growth():
    """Per-trial max canonical heights vs ln p with the stored logarithmic fits."""
    groups = read_rows(GROWTH_STEM + "_groups.csv")
    fits = read_rows(GROWTH_STEM + "_fits.csv")

    # least-norm (variant 0) general lifts, per k, and the direct single lift
    general = {k: ([], []) for k in (1, 2, 3, 4)}
    direct = ([], [])
    for row in groups:
        p = int(row["p"])
        h = float(row["max_canonical_height"])
        if row["family"] == "random_general" and row["variant"] == "0":
            k = int(row["k"])
            general[k][0].append(log(p))
            general[k][1].append(h)
        elif row["family"] == "random_short_single":
            direct[0].append(log(p))
            direct[1].append(h)

    line = {}
    for row in fits:
        if row["model"] != "logarithmic":
            continue
        key = (row["analysis_family"], int(row["k"]))
        line[key] = (float(row["intercept"]), float(row["slope"]))

    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    xs = np.linspace(log(PRIMES[0]), log(PRIMES[-1]), 50)
    k_colors = {1: F.SEQ[3], 2: F.SEQ[6], 3: F.SEQ[9], 4: F.SEQ[12]}
    for k in (1, 2, 3, 4):
        b, a = line[("random_general_min_norm", k)]
        ax.plot(xs, b + a * xs, color=k_colors[k], lw=1.8, zorder=2)
        ax.scatter(general[k][0], general[k][1], s=22, color=k_colors[k],
                   edgecolor=F.SURFACE, linewidth=0.6, zorder=3,
                   label=rf"general lift, $k={k}$  ($\alpha_{k}={a:.2f}$)")
    b, a = line[("random_short_single", 1)]
    ax.plot(xs, b + a * xs, color=F.PALETTE[1], lw=1.8, ls="--", zorder=2)
    ax.scatter(direct[0], direct[1], s=22, marker="D", color=F.PALETTE[1],
               edgecolor=F.SURFACE, linewidth=0.6, zorder=3,
               label=rf"direct short lift  ($\alpha={a:.2f}$)")
    # fixed controls: 37.a1 k=4 multiples (flat) and 11.a2 torsion (zero)
    ax.axhline(0.8176547198523896, color=F.MUTED, lw=1.2, ls=":", zorder=1)
    ax.text(log(30000), 1.9, "37.a1 control, $k=4$ (0.818)", color=F.MUTED,
            fontsize=8.7, ha="right")
    ax.set_xticks([log(p) for p in PRIMES])
    ax.set_xticklabels([str(p) for p in PRIMES], fontsize=9.5)
    ax.set_xlabel(r"prime $p$ (log axis)")
    ax.set_ylabel(r"max canonical height $\max_i \hat{h}(\tilde P_i)$")
    ax.set_title("Least-norm lift heights grow like $\\log p$, not like a power of $p$")
    ax.legend(loc="upper left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "growth.svg"))


def fig_fits():
    """Fitted logarithmic slopes with CIs; log-fit vs power-fit height-scale RMSE."""
    fits = read_rows(GROWTH_STEM + "_fits.csv")
    slope, ci_lo, ci_hi, rmse_log, rmse_pow = {}, {}, {}, {}, {}
    for row in fits:
        fam, k, model = row["analysis_family"], int(row["k"]), row["model"]
        if fam == "random_general_min_norm" and model == "logarithmic":
            slope[k] = float(row["slope"])
            ci_lo[k] = float(row["slope_ci95_low"])
            ci_hi[k] = float(row["slope_ci95_high"])
            rmse_log[k] = float(row["rmse_height_scale"])
        elif fam == "random_general_min_norm" and model == "power":
            rmse_pow[k] = float(row["rmse_height_scale"])
        elif fam == "random_short_single" and model == "logarithmic":
            slope[0] = float(row["slope"])
            ci_lo[0] = float(row["slope_ci95_low"])
            ci_hi[0] = float(row["slope_ci95_high"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
    order = [0, 1, 2, 3, 4]
    labels = ["direct\nshort", "$k=1$", "$k=2$", "$k=3$", "$k=4$"]
    x = np.arange(len(order))
    vals = [slope[k] for k in order]
    err_low = [slope[k] - ci_lo[k] for k in order]
    err_high = [ci_hi[k] - slope[k] for k in order]
    colors = [F.PALETTE[1], F.SEQ[3], F.SEQ[6], F.SEQ[9], F.SEQ[12]]
    ax1.bar(x, vals, 0.62, color=colors, edgecolor=F.SURFACE, linewidth=1.0)
    ax1.errorbar(x, vals, yerr=[err_low, err_high], fmt="none",
                 ecolor=F.INK_SECOND, elinewidth=1.3, capsize=3)
    ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=9)
    ax1.set_ylabel(r"logarithmic slope $\alpha_k$")
    ax1.set_title("OLS slope, 95% CI")

    ks = [1, 2, 3, 4]
    x2 = np.arange(len(ks)); w = 0.38
    b1 = ax2.bar(x2 - w / 2, [rmse_log[k] for k in ks], w,
                 label=r"logarithmic fit", color=F.PALETTE[0],
                 edgecolor=F.SURFACE, linewidth=1.0)
    b2 = ax2.bar(x2 + w / 2, [rmse_pow[k] for k in ks], w,
                 label=r"power fit", color=F.PALETTE[7],
                 edgecolor=F.SURFACE, linewidth=1.0)
    ax2.bar_label(b1, fmt="%.1f", padding=2, fontsize=8, color=F.INK_SECOND)
    ax2.bar_label(b2, fmt="%.1f", padding=2, fontsize=8, color=F.INK_SECOND)
    ax2.set_xticks(x2); ax2.set_xticklabels([f"$k={k}$" for k in ks], fontsize=9)
    ax2.set_ylabel("height-scale RMSE")
    ax2.set_ylim(0, 10.6)
    ax2.set_title("Log fit vs power fit")
    ax2.legend(loc="upper left", fontsize=8.6)
    F.finish(fig, os.path.join(OUT, "fits.svg"))


def fig_relations():
    """SG-08 exact bounded-relation audit: finite vs rational relations by (k, bits)."""
    rows = [row for row in read_rows(RELATIONS_STEM + "_summary.csv")
            if row["variant_kind"] == "all"]
    bits = [5, 7, 9, 11]
    ks = [1, 2, 3, 4]
    finite = np.zeros((4, 4)); rational = np.zeros((4, 4)); n = np.zeros((4, 4))
    for row in rows:
        i = ks.index(int(row["k"])); j = bits.index(int(row["bits"]))
        finite[i, j] = int(row["finite_relation_count"])
        rational[i, j] = int(row["rational_relation_count"])
        n[i, j] = int(row["n"])

    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    for i in range(4):
        for j in range(4):
            rate = finite[i, j] / n[i, j]
            shade = F.SEQ[int(round(rate * (len(F.SEQ) - 4)))]
            ax.add_patch(plt.Rectangle((j, i), 0.94, 0.94, facecolor=shade,
                         edgecolor=F.GRID, linewidth=0.8))
            ink = F.SURFACE if rate > 0.55 else F.INK
            ax.text(j + 0.47, i + 0.40, f"{int(finite[i, j])}/{int(n[i, j])}",
                    ha="center", va="center", color=ink, fontsize=10, weight="bold")
            if rational[i, j] > 0:
                ax.add_patch(plt.Rectangle((j + 0.03, i + 0.03), 0.88, 0.88,
                             facecolor="none", edgecolor=F.PALETTE[7], linewidth=2.0))
                ax.text(j + 0.47, i + 0.72, f"{int(rational[i, j])} rational",
                        ha="center", va="center", color=F.PALETTE[7], fontsize=8,
                        weight="bold")
    ax.set_xlim(0, 4); ax.set_ylim(0, 4)
    ax.set_xticks(np.arange(4) + 0.47)
    ax.set_xticklabels([f"$b={b}$\n($p={p}$)" for b, p in
                        zip(bits, [31, 127, 503, 2039])], fontsize=9)
    ax.set_yticks(np.arange(4) + 0.47)
    ax.set_yticklabels([f"$k={k}$" for k in ks], fontsize=10)
    ax.invert_yaxis()
    ax.set_axisbelow(False); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Finite-field relations through bound 8 (count/variants); "
                 "rational relations outlined", fontsize=11)
    F.finish(fig, os.path.join(OUT, "relations.svg"))


if __name__ == "__main__":
    fig_growth()
    fig_fits()
    fig_relations()
    print("P1.6 figures written")
