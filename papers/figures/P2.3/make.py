"""Figures for the P2.3 paper (Cheon divisor-case reproduction and scaling).

All figures are generated from the real experiment artifacts under
problems/P2.3-cheon-generalization/data/: the two seeded scaling sweeps
(hb4-7 t3, hb8-22 t41) with their summary CSVs and bootstrap fit JSONs.
"""
import os, sys, csv, json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                    "problems", "P2.3-cheon-generalization", "data")

STAMP = "hb8-22_t41_s2303_20260713"
STAMP_SMOKE = "hb4-7_t3_s2303_20260713"


def load_summary(stamp):
    path = os.path.join(DATA, f"run_scaling_summary_{stamp}.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    cols = {}
    for key in rows[0]:
        vals = []
        for r in rows:
            v = r[key]
            try:
                vals.append(float(v))
            except ValueError:
                vals.append(v)
        cols[key] = np.array(vals)
    return cols


def load_fit(stamp):
    path = os.path.join(DATA, f"run_scaling_fit_{stamp}.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


MAIN = load_summary(STAMP)
SMOKE = load_summary(STAMP_SMOKE)
FIT = load_fit(STAMP)
FIT_SMOKE = load_fit(STAMP_SMOKE)


# --------------------------------------------------------------------------
def fig_scaling():
    """Median oracle exponentiations vs n on log-log, with the fitted slope."""
    fig, ax = plt.subplots(figsize=(6.0, 3.7))

    n_main = MAIN["order"]
    y_main = MAIN["median_scalar_multiplications"]
    n_smoke = SMOKE["order"]
    y_smoke = SMOKE["median_scalar_multiplications"]

    slope = FIT["slope"]
    inter = FIT["intercept"]
    lo, hi = FIT["slope_ci_95"]

    # Fitted power law and CI fan, anchored at the geometric mean of n.
    xs = np.geomspace(n_smoke.min() * 0.7, n_main.max() * 1.4, 200)
    pivot = np.exp(np.mean(np.log(n_main)))
    ypivot = np.exp(inter + slope * np.log(pivot))
    fit_line = ypivot * (xs / pivot) ** slope
    band_lo = ypivot * (xs / pivot) ** lo
    band_hi = ypivot * (xs / pivot) ** hi
    ax.fill_between(xs, band_lo, band_hi, color=F.PALETTE[0], alpha=0.14, lw=0,
                    label=f"95% CI on slope [{lo:.4f}, {hi:.4f}]")
    ax.plot(xs, fit_line, color=F.PALETTE[0], lw=1.6,
            label=f"fit: slope {slope:.4f}")

    # Reference quarter-power line (slope exactly 1/4).
    ref = ypivot * (xs / pivot) ** 0.25
    ax.plot(xs, ref, color=F.MUTED, lw=1.0, ls=":", label=r"reference $n^{1/4}$")

    ax.scatter(n_main, y_main, s=42, color=F.PALETTE[0], zorder=5,
               edgecolor=F.SURFACE, linewidth=0.8,
               label="hb8-22 sweep (41 trials/size)")
    ax.scatter(n_smoke, y_smoke, s=42, marker="s", color=F.PALETTE[1], zorder=5,
               edgecolor=F.SURFACE, linewidth=0.8,
               label="hb4-7 sweep (3 trials/size)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("prime group order $n$")
    ax.set_ylabel("median oracle exponentiations")
    ax.set_title("Divisor-case recovery cost tracks a quarter power of $n$")
    ax.legend(loc="upper left", fontsize=8.4)
    F.finish(fig, os.path.join(OUT, "scaling.svg"))


# --------------------------------------------------------------------------
def fig_metrics():
    """Two cost metrics: oracle exponentiations vs primitive double-and-add ops."""
    fig, ax = plt.subplots(figsize=(6.0, 3.7))

    n = MAIN["order"]
    scal = MAIN["median_scalar_multiplications"]
    grp = MAIN["median_group_operations"]
    shape = MAIN["theory_shape"]

    def slope_of(y):
        a, b = np.polyfit(np.log(n), np.log(y), 1)
        return a

    s_scal = slope_of(scal)
    s_grp = slope_of(grp)

    ax.plot(n, scal, "o-", color=F.PALETTE[0], lw=1.6, ms=6,
            label=f"oracle exponentiations  (slope {s_scal:.2f})")
    ax.plot(n, grp, "s-", color=F.PALETTE[1], lw=1.6, ms=6,
            label=f"primitive group ops  (slope {s_grp:.2f})")
    # Theory shape sqrt(n/d)+sqrt(d), scaled to the exponentiation series.
    scale = np.median(scal / shape)
    ax.plot(n, scale * shape, ls="--", color=F.PALETTE[2], lw=1.4,
            label=r"$\sqrt{(n-1)/d}+\sqrt{d}$ (scaled)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("prime group order $n$")
    ax.set_ylabel("median count")
    ax.set_title(r"The $\log n$ factor separates the two cost metrics")
    ax.legend(loc="upper left", fontsize=8.6)
    F.finish(fig, os.path.join(OUT, "metrics.svg"))


# --------------------------------------------------------------------------
def fig_residuals():
    """Log residuals of the power-law fit + measured/theory ratio, two panels."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.1))

    bits = MAIN["order_bits"]
    resid = MAIN["log_residual"]
    ratio = MAIN["median_scalar_multiplications"] / MAIN["theory_shape"]

    # Panel 1: residuals about the fitted line.
    ax1.axhline(0.0, color=F.MUTED, lw=1.0)
    ax1.axhline(0.1, color=F.GRID, lw=0.8, ls=":")
    ax1.axhline(-0.1, color=F.GRID, lw=0.8, ls=":")
    ax1.vlines(bits, 0, resid, color=F.PALETTE[0], lw=1.4, alpha=0.6)
    ax1.scatter(bits, resid, s=40, color=F.PALETTE[0], zorder=5,
                edgecolor=F.SURFACE, linewidth=0.8)
    ax1.set_xlabel(r"$\log_2 n$ (bits)")
    ax1.set_ylabel("log residual")
    ax1.set_title("No systematic size trend")
    ax1.set_ylim(-0.16, 0.16)

    # Panel 2: measured / theory shape ratio.
    mean_ratio = np.mean(ratio)
    ax2.axhline(mean_ratio, color=F.MUTED, lw=1.0, ls="--",
                label=f"mean {mean_ratio:.2f}")
    ax2.plot(bits, ratio, "o-", color=F.PALETTE[1], lw=1.4, ms=6,
             markeredgecolor=F.SURFACE, markeredgewidth=0.8)
    ax2.set_xlabel(r"$\log_2 n$ (bits)")
    ax2.set_ylabel(r"measured $/\ (\sqrt{(n-1)/d}+\sqrt{d})$")
    ax2.set_title("Constant multiple of the model")
    ax2.set_ylim(1.0, 2.0)
    ax2.legend(loc="lower right", fontsize=9)

    F.finish(fig, os.path.join(OUT, "residuals.svg"))


# --------------------------------------------------------------------------
def fig_structure():
    """Schematic of the two-stage orbit search and the divisor dependency."""
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")

    def box(x, y, w, h, text, fc, ec, tc=F.INK, fs=9.0, weight="normal"):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.12",
                           facecolor=fc, edgecolor=ec, linewidth=1.2)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=tc, weight=weight)

    def arrow(x1, y1, x2, y2, color=F.INK_SECOND):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                     mutation_scale=13, color=color, lw=1.5,
                     shrinkA=2, shrinkB=2))

    # Header banner: the multiplicative-group decomposition (needs d | n-1).
    box(0.2, 5.55, 9.6, 0.85,
        r"$\mathbb{F}_n^{*}=\langle\zeta\rangle$,   order $n-1=d\cdot q$,"
        r"   with the divisor condition $d\mid n-1$",
        "#fbe9df", F.PALETTE[1], fs=9.6, weight="bold")

    # Flow row: inputs -> Stage 1 -> Stage 2.
    box(0.2, 3.55, 2.4, 1.35,
        r"inputs" + "\n\n" + r"$g,\ g^{x},\ g^{x^{d}}$", F.SEQ[0], F.PALETTE[0],
        fs=10, weight="bold")
    box(3.15, 3.55, 3.15, 1.35,
        "Stage 1: BSGS in\n"
        r"$\langle\zeta^{d}\rangle$ of order $q=(n-1)/d$" + "\n"
        r"recovers $x^{d}=(\zeta^{d})^{k_1}$", F.SURFACE, F.PALETTE[0], fs=8.6)
    box(6.85, 3.55, 3.05, 1.35,
        "Stage 2: BSGS in\n"
        r"$\langle\zeta^{q}\rangle$ of order $d$" + "\n"
        r"recovers $x=\zeta^{k_1}(\zeta^{q})^{k_2}$", F.SURFACE, F.PALETTE[2], fs=8.6)
    arrow(2.65, 4.22, 3.1, 4.22)
    arrow(6.35, 4.22, 6.8, 4.22)

    # Cost summary line.
    ax.text(5.0, 2.75,
            r"cost $\approx 2\,(\sqrt{q}+\sqrt{d})$ exponentiations,"
            r" minimized at $d\approx\sqrt{n}\ \Rightarrow\ \Theta(n^{1/4})$",
            ha="center", va="center", fontsize=9.4, color=F.INK)

    # Obstruction banner (SG-04 open): the two orbits disappear off the divisor set.
    box(0.9, 0.55, 8.2, 1.35,
        r"$d\nmid n\pm 1$:  no pair of exact multiplicative orbits of orders"
        + "\n" + r"$q$ and $d$ exists $-$ both search sets vanish."
        + "\n" + r"SG-04 open: no falsifiable non-divisor adaptation found.",
        "#f7e2e2", F.PALETTE[7], tc="#8a2b2b", fs=9.2, weight="bold")
    ax.scatter([0.5, 9.5], [1.22, 1.22], marker="x", s=150,
               color="#a03a3a", linewidth=2.6, zorder=6)

    F.finish(fig, os.path.join(OUT, "structure.svg"))


if __name__ == "__main__":
    fig_scaling()
    fig_metrics()
    fig_residuals()
    fig_structure()
    print("P2.3 figures written")
