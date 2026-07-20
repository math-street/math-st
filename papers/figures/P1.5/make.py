"""Figures for the P1.5 paper (a unified theory of transfers)."""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems", "P1.5-unified-transfers", "data")


def _read(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_scaling():
    """Measured evaluator cost vs explicit work predictor, with recorded power-law fits.

    Source: run_transfers_full_20260626_scaling.csv (observed medians, fitted
    exponents and intercepts exactly as stored by the experiment driver).
    """
    rows = _read("run_transfers_full_20260626_scaling.csv")
    panels = [
        ("additive_transfer", "Additive lift map", "lifted group operations"),
        ("pairing_transfer", "Affine Tate (Miller) map", r"Miller lines $\times$ field bits"),
        ("target_bsgs", "Toy target BSGS dlog", r"BSGS width $\lceil\sqrt{r}\,\rceil$"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.0))
    for ax, (model, title, xlabel) in zip(axes, panels):
        sel = [r for r in rows if r["model"] == model]
        x = np.array([float(r["predictor"]) for r in sel])
        y = np.array([float(r["observed_ns"]) for r in sel]) / 1000.0  # microseconds
        expo = float(sel[0]["fitted_exponent"])
        icpt = float(sel[0]["log2_intercept"])
        xs = np.linspace(x.min() * 0.9, x.max() * 1.1, 200)
        ys = (2.0 ** icpt) * xs ** expo / 1000.0
        ax.plot(xs, ys, color=F.MUTED, lw=1.3, ls="--", zorder=2)
        ax.plot(x, y, "o", color=F.PALETTE[0], ms=6, zorder=3)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_title(title, fontsize=10.5)
        ax.set_xlabel(xlabel, fontsize=9.5)
        ax.text(0.05, 0.86, f"fit exponent {expo:.4f}",
                transform=ax.transAxes, fontsize=9, color=F.INK_SECOND)
        ax.tick_params(labelsize=8.5)
    axes[0].set_ylabel(r"median time ($\mu$s)")
    F.finish(fig, os.path.join(OUT, "scaling.svg"))


def fig_taxonomy():
    """Candidate-target verdict grid (SG-05/SG-06/SG-22)."""
    targets = [
        "Local formal groups",
        "Drinfeld-module targets",
        "Tori (global maps / $E[r]$ pairing)",
        "Additive char-$p$ ring groups",
        "Endomorphism-order class group",
        r"Ray class groups $(\mathrm{mod}\ r,\ r^2)$",
        "Jacobians of covers / Weil descent",
        "Weil-restriction abelian varieties",
        "Other elliptic curves / AVs",
        "Separately built number-field class group",
    ]
    cols = ["Excluded", "Known\nmechanism", "Conditional /\nneutral", "Open\n(Q004)"]
    # 1 = excluded (proved), 2 = known mechanism (cited), 3 = conditional, 4 = open
    M = np.zeros((len(targets), 4), dtype=int)
    M[0, 0] = 1; M[0, 1] = 2       # formal groups: excluded r!=p, known r=p (Semaev)
    M[1, 0] = 1                    # Drinfeld
    M[2, 0] = 1; M[2, 1] = 2       # tori: SG-07 excl., pairing route known
    M[3, 0] = 1                    # additive char-p rings
    M[4, 0] = 1                    # endomorphism class group (orientation + size)
    M[5, 0] = 1                    # ray class groups (A004/A022)
    M[6, 1] = 2; M[6, 2] = 3       # covers / descent: known + EGT-conditional
    M[7, 2] = 3                    # Weil restriction: neutral until composed
    M[8, 0] = 1                    # other EC/AV: no new mechanism (SG-07)
    M[9, 0] = 1; M[9, 3] = 4       # number-field Cl: natural branches dead, Q004 open
    cmap = {0: F.SURFACE, 1: F.PALETTE[7], 2: F.PALETTE[0], 3: F.PALETTE[3], 4: F.PALETTE[6]}
    letter = {1: "E", 2: "K", 3: "C", 4: "O"}
    fig, ax = plt.subplots(figsize=(6.8, 4.1))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.add_patch(plt.Rectangle((j, i), 0.92, 0.92, facecolor=cmap[v],
                         edgecolor=F.GRID, linewidth=0.8))
            if v:
                ax.text(j + 0.46, i + 0.46, letter[v], ha="center", va="center",
                        color=F.SURFACE if v != 3 else F.INK,
                        fontsize=9, weight="bold")
    ax.set_xlim(0, M.shape[1]); ax.set_ylim(0, M.shape[0])
    ax.set_xticks(np.arange(M.shape[1]) + 0.46)
    ax.set_xticklabels(cols, fontsize=8.5)
    ax.set_yticks(np.arange(M.shape[0]) + 0.46)
    ax.set_yticklabels(targets, fontsize=8.5)
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_axisbelow(False); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    from matplotlib.patches import Patch
    leg = [Patch(facecolor=F.PALETTE[7], label="E — excluded (proved)"),
           Patch(facecolor=F.PALETTE[0], label="K — known mechanism (cited)"),
           Patch(facecolor=F.PALETTE[3], label="C — conditional / neutral"),
           Patch(facecolor=F.PALETTE[6], label="O — open residual")]
    ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0, -0.02),
              ncol=2, fontsize=8.5)
    F.finish(fig, os.path.join(OUT, "taxonomy.svg"))


def fig_buell():
    """Distinct lifted discriminants under the canonical Buell reduction.

    Source: probe_buell_reduction_full_20260710.csv — every nonzero point of
    ten toy prime-order subgroups produced its own lifted discriminant.
    """
    rows = _read("probe_buell_reduction_full_20260710.csv")
    labels = [f"p={r['p']}\nr={r['r']}" for r in rows]
    distinct = [int(r["distinct_lifted_discriminants"]) for r in rows]
    fixed = [int(r["fixed_discriminant_points"]) for r in rows]
    x = np.arange(len(rows))
    w = 0.4
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    b1 = ax.bar(x - w / 2, distinct, w, label="distinct lifted discriminants",
                color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=1.0)
    b2 = ax.bar(x + w / 2, fixed, w, label="points hitting the model discriminant",
                color=F.PALETTE[1], edgecolor=F.SURFACE, linewidth=1.0)
    ax.bar_label(b1, padding=2, fontsize=8, color=F.INK_SECOND)
    ax.bar_label(b2, padding=2, fontsize=8, color=F.INK_SECOND)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("count per subgroup")
    ax.set_title("Canonical Buell reduction: one lifted discriminant per point")
    ax.set_ylim(0, 40)
    ax.legend(loc="upper left", fontsize=8.5)
    F.finish(fig, os.path.join(OUT, "buell.svg"))


def fig_window():
    """Succinct census targets vs the self-certifying A019 family.

    Source: probe_exact_order_targets_full_20260710.csv — least discriminant
    with r | h(Delta) for each prime 3 <= r <= 43, against the Theta(r)-bit
    discriminant 1 - 4*2^r.
    """
    rows = _read("probe_exact_order_targets_full_20260710.csv")
    r = np.array([int(x["r"]) for x in rows])
    census_bits = np.array([int(x["discriminant_bits"]) for x in rows])
    a019_bits = np.array([int(x["a019_bits"]) for x in rows])
    guide = 2 * np.log2(r) + 1
    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(r, a019_bits, "s-", color=F.PALETTE[7], ms=5, lw=1.6,
            label=r"$1-4\cdot 2^r$ family: $\Theta(r)$ bits (fails SG-01)")
    ax.plot(r, census_bits, "o-", color=F.PALETTE[0], ms=5, lw=1.6,
            label=r"census least $|\Delta|$ with $r \mid h(\Delta)$")
    ax.plot(r, guide, ls="--", lw=1.2, color=F.MUTED,
            label=r"$2\log_2 r + 1$ (SG-25 window floor)")
    ax.set_xlabel(r"prime $r$")
    ax.set_ylabel(r"target discriminant bits")
    ax.set_title("Exact-order class targets: succinct census vs certified family")
    ax.legend(loc="upper left", fontsize=8.5)
    F.finish(fig, os.path.join(OUT, "window.svg"))


if __name__ == "__main__":
    fig_scaling()
    fig_taxonomy()
    fig_buell()
    fig_window()
    print("P1.5 figures written")
