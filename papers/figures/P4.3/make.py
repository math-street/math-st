"""Figures for the P4.3 paper (rigorous complexity for exTNFS).

The toy-experiment figures load the real exhaustive-enumeration summary CSV
from problems/P4.3-rigorous-extnfs/data/. The audit map and the
degree-uniformity barrier are reconstructed from the proved statements in
SMOOTHNESS_ASSUMPTIONS.md and attempt A003.
"""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P4.3-rigorous-extnfs", "data")
SUMMARY = "measure_norm_smoothness_p5_A4_B7-13-31-61_all_s4304_20260702_summary.csv"


def load_summary():
    with open(os.path.join(DATA, SUMMARY), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_toyrates():
    """Actual joint-smooth rates vs the dyadic random-integer baseline."""
    rows = load_summary()
    bounds = [7, 13, 31, 61]
    act, base, blo, bhi = [], [], [], []
    for b in bounds:
        for r in rows:
            if int(r["bound"]) == b and r["metric"] == "joint":
                if r["source"] == "actual":
                    act.append(float(r["rate"]))
                else:
                    base.append(float(r["rate"]))
                    blo.append(float(r["ci_low"]))
                    bhi.append(float(r["ci_high"]))
    x = np.arange(len(bounds))
    w = 0.36
    fig, ax = plt.subplots(figsize=(5.8, 3.1))
    b1 = ax.bar(x - w / 2, act, w, color=F.PALETTE[0],
                edgecolor=F.SURFACE, linewidth=0.8,
                label="actual joint rate (exact population)")
    err = [np.array(base) - np.array(blo), np.array(bhi) - np.array(base)]
    ax.bar(x + w / 2, base, w, color=F.PALETTE[1], edgecolor=F.SURFACE,
           linewidth=0.8, label="dyadic baseline (95% Wilson CI)")
    ax.errorbar(x + w / 2, base, yerr=err, fmt="none", ecolor=F.INK,
                elinewidth=1.1, capsize=3)
    for xi, (a, bb) in enumerate(zip(act, base)):
        ax.text(xi - w / 2, a * 1.12, f"×{a / bb:.2f}", ha="center",
                fontsize=8.6, color=F.INK_SECOND)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f"$B={b}$" for b in bounds])
    ax.set_ylabel("joint $B$-smooth rate")
    ax.set_title("Tower norms are not random integers "
                 r"($p=5$, $\eta=2$, $\kappa=3$, 5,856 vectors)")
    ax.legend(fontsize=8.4, loc="upper left")
    F.finish(fig, os.path.join(OUT, "toyrates.svg"))


def fig_dependence():
    """Joint/product-of-marginals dependence ratio versus the bound."""
    rows = load_summary()
    bounds = [7, 13, 31, 61]
    dep, ratio = [], []
    for b in bounds:
        for r in rows:
            if int(r["bound"]) == b and r["metric"] == "joint":
                if r["source"] == "actual":
                    dep.append(float(r["dependence_ratio"]))
                    ratio.append(float(r["rate_ratio_vs_baseline"]))
    fig, ax = plt.subplots(figsize=(5.6, 2.9))
    ax.plot(bounds, ratio, marker="o", color=F.PALETTE[0],
            label="actual / baseline joint rate")
    ax.plot(bounds, dep, marker="s", color=F.PALETTE[4],
            label="actual joint / product of actual marginals")
    ax.axhline(1.0, color=F.MUTED, lw=1.0, ls=":")
    ax.text(52, 1.12, "independence = 1", color=F.MUTED, fontsize=8.6)
    ax.set_xscale("log")
    ax.set_xticks(bounds)
    ax.set_xticklabels([str(b) for b in bounds])
    ax.set_xlabel("smoothness bound $B$")
    ax.set_ylabel("ratio")
    ax.set_ylim(0, 9.5)
    ax.set_title("Positive side dependence at every tested bound")
    ax.legend(fontsize=8.6, loc="upper right")
    F.finish(fig, os.path.join(OUT, "dependence.svg"))


def fig_audit():
    """Status map of the ten smoothness inputs S-01..S-10."""
    items = [
        ("S-01", "first-side relation density", "open"),
        ("S-02", "second-side relation density", "open"),
        ("S-03", "joint density (RC)", "open"),
        ("S-04", "JLSV2 initial split (IS-J)", "open"),
        ("S-05", "Conj./Waterloo split (IS-C)", "open"),
        ("S-06", "squarefree co-condition", "open"),
        ("S-07", "one special-q step (SQ)", "open"),
        ("S-08", "adaptive descent uniformity", "open"),
        ("S-09", "smooth detection/factoring", "known"),
        ("S-10", "random-integer benchmark (CEP)", "known"),
    ]
    extra = [
        ("PS", "polynomial-selection irreducibility", "open"),
        ("RK", "relation-matrix rank escape (R2)", "open"),
    ]
    col = {"open": F.PALETTE[7], "known": F.PALETTE[5]}
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    allrows = items + extra
    for i, (code, desc, status) in enumerate(allrows):
        y = len(allrows) - 1 - i
        ax.add_patch(plt.Rectangle((0, y + 0.08), 0.62, 0.84,
                     facecolor=col[status], edgecolor=F.SURFACE, lw=0.8))
        ax.text(0.31, y + 0.5, code, ha="center", va="center",
                color=F.SURFACE, fontsize=8.2, weight="bold")
        ax.text(0.75, y + 0.5, desc, ha="left", va="center",
                color=F.INK, fontsize=9.2)
        ax.text(6.9, y + 0.5, "known" if status == "known" else "OPEN",
                ha="right", va="center", fontsize=8.6, weight="bold",
                color=col[status])
    ax.axhline(1.98, color=F.MUTED, lw=0.9, ls=":")
    ax.text(6.9, 2.12, "adjacent non-smoothness gaps (A004)", ha="right",
            fontsize=7.8, color=F.MUTED)
    ax.set_xlim(0, 7.0)
    ax.set_ylim(0, len(allrows) + 0.1)
    ax.axis("off")
    ax.set_title("The exTNFS dependency audit: 10 of 12 inputs remain unproved")
    F.finish(fig, os.path.join(OUT, "audit.svg"))


def fig_barrier():
    """Degree-uniformity barrier: eta required to keep the L_Q(2/3) norm scale."""
    # PROVED scaling (A003 eq. 11): eta = Theta((log Q/loglog Q)^{2/3-l_p});
    # constants suppressed, so the plot shows the pure scaling shape.
    logq = np.linspace(2 ** 6, 2 ** 14, 400)  # log Q in nats
    fig, ax = plt.subplots(figsize=(5.9, 3.0))
    for lp, colidx in ((0.40, 0), (0.50, 2), (0.60, 4)):
        eta = (logq / np.log(logq)) ** (2.0 / 3.0 - lp)
        ax.plot(np.log2(np.e) * logq, eta, color=F.PALETTE[colidx],
                label=rf"$\ell_p={lp:.2f}$")
    ax.axhline(2, color=F.PALETTE[7], lw=1.5, ls="--",
               label=r"fixed $\eta=2$ (quadratic-form theorems)")
    ax.set_xscale("log")
    ax.set_xlabel(r"field size $\log_2 Q$")
    ax.set_ylabel(r"required tower degree $\eta$ (scaling, constants suppressed)")
    ax.set_title("Optimized interior exTNFS forces "
                 r"$\eta=\Theta((\log Q/\log\log Q)^{2/3-\ell_p})$")
    ax.legend(fontsize=8.6, loc="upper left")
    F.finish(fig, os.path.join(OUT, "barrier.svg"))


if __name__ == "__main__":
    fig_toyrates()
    fig_dependence()
    fig_audit()
    fig_barrier()
    print("P4.3 figures written")
