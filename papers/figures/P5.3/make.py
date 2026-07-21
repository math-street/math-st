"""Figures for the P5.3 paper (formalizing curve-generation rigidity)."""
import os, sys, csv
from collections import Counter
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
# On this machine "Libertinus Serif" is absent and the fallback "Cambria"
# (a .ttc) silently drops glyph runs at many sizes; skip it in the chain.
mpl.rcParams["font.serif"] = ["Libertinus Serif", "Georgia", "DejaVu Serif",
                              "Times New Roman"]
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P5.3-rigidity-formalization", "data")


def read_rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fig_game():
    """Schematic of the selective-generation game RigSel (from DEFINITIONS.md)."""
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.9)
    ax.axis("off")
    ax.grid(False)

    def box(x, y, w, h, step, title, lines, fc, ec):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                                   linewidth=1.1, zorder=2))
        ax.text(x + 0.13, y + h - 0.30, step, ha="left", va="center",
                fontsize=8, weight="bold", color=F.SEQ[9], zorder=3)
        ax.text(x + w / 2, y + h - 0.68, title, ha="center", va="center",
                fontsize=9.0, weight="bold", color=F.INK, zorder=3)
        for k, ln in enumerate(lines):
            ax.text(x + w / 2, y + h - 1.12 - 0.40 * k, ln, ha="center",
                    va="center", fontsize=7.8, color=F.INK_SECOND, zorder=3)

    W, H, Y = 1.86, 2.55, 3.05
    xs = [0.12, 2.18, 4.24, 6.30, 8.36]
    box(xs[0], Y, W, H, "1", "Auditor", [
        r"fixes contract $\mathcal{A}$:",
        r"$\Omega$, $\mathsf{Safe}$, index set $I$,",
        r"experiment $(X_i)_{i\in I}$, $\nu$,",
        "audit projection"], F.SEQ[0], F.SEQ[9])
    box(xs[1], Y, W, H, "2", "Weakness source", [
        r"commits $\mathcal{B}\subseteq\Omega$",
        r"(may depend on $\mathcal{A}$;",
        "designer knows it;",
        "fixed before the tape)"], "#fdecd2", F.PALETTE[1])
    box(xs[2], Y, W, H, "3", "Challenger", [
        "samples the joint",
        r"experiment $(X_i)_{i\in I}$",
        "with fresh",
        "randomness"], F.SEQ[0], F.SEQ[9])
    box(xs[3], Y, W, H, "4", "Designer", [
        r"screens all $X_i$",
        r"against hidden $\mathcal{B}$,",
        r"publishes one $i^{*}$",
        "(or fails)"], "#fdecd2", F.PALETTE[1])
    box(xs[4], Y, W, H, "5", "Win condition", [
        r"$X_{i^*}\in\mathcal{B}$  and",
        r"$\mathsf{Safe}(X_{i^*})=1$"], F.SEQ[0], F.SEQ[9])
    for k in range(4):
        ax.annotate("", xy=(xs[k + 1] - 0.04, Y + H / 2),
                    xytext=(xs[k] + W + 0.04, Y + H / 2),
                    arrowprops=dict(arrowstyle="-|>", color=F.INK_SECOND,
                                    lw=1.3, shrinkA=0, shrinkB=0))

    # designer's screenable menu strip under box 4
    mx, my, mw, mh, M = xs[3] + 0.06, 1.62, W - 0.12, 0.52, 8
    for j in range(M):
        cx = mx + j * mw / M
        fc = F.PALETTE[1] if j == 5 else F.SURFACE
        ax.add_patch(plt.Rectangle((cx, my), mw / M * 0.86, mh, facecolor=fc,
                                   edgecolor=F.MUTED, linewidth=0.8, zorder=2))
    ax.annotate("", xy=(xs[3] + W / 2, my + mh + 0.05),
                xytext=(xs[3] + W / 2, Y - 0.05),
                arrowprops=dict(arrowstyle="-|>", color=F.MUTED, lw=1.0))
    ax.text(mx + mw / 2, my - 0.30, r"menu of $M$ screenable executions",
            ha="center", va="center", fontsize=7.8, color=F.INK_SECOND)

    # bottom accounting band
    ax.add_patch(plt.Rectangle((0.12, 0.10), 10.1, 0.92, facecolor="#f2f1ec",
                               edgecolor=F.AXIS, linewidth=0.9, zorder=1))
    ax.text(0.35, 0.56, r"selection capacity  $b=\log_2 M$", ha="left",
            va="center", fontsize=9.5, color=F.INK)
    ax.text(10.0, 0.56,
            r"$\mathrm{Pr}[\mathrm{win}]\;\leq\;\min(1,\,2^{b}\kappa\epsilon)$"
            + "   (no candidate independence used)",
            ha="right", va="center", fontsize=9.5, color=F.INK)
    F.finish(fig, os.path.join(OUT, "game.svg"))


def fig_firstpass():
    """Forced first-passing search per beacon label (real SG-08 CSV)."""
    rows = read_rows("sample_rigid_curve_b7_n8_20260625.csv")
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    for r in rows:
        s, c = int(r["sample"]), int(r["counter"])
        if c > 0:
            ax.plot(range(c), [s] * c, marker="o", mfc="none", mec=F.MUTED,
                    ms=5, mew=1.1, ls="none")
        ax.plot([c], [s], marker="o", color=F.PALETTE[0], ms=7.5, ls="none")
        ax.annotate(f"$(a,b)=({r['a']},{r['b']})$,  $r={r['subgroup_order']}$",
                    (c, s), xytext=(8, 0), textcoords="offset points",
                    fontsize=8.0, color=F.INK_SECOND, va="center")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"label {i}" for i in range(len(rows))], fontsize=9)
    ax.invert_yaxis()
    ax.set_xticks(range(0, 15, 2))
    ax.set_xlim(-0.6, 19.5)
    ax.set_xlabel("candidate counter inside one forced execution")
    ax.set_title(r"First-passing search at $p=127$: eight beacon labels")
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], marker="o", mfc="none", mec=F.MUTED, ls="none",
               label="rejected by the public safety profile"),
        Line2D([], [], marker="o", color=F.PALETTE[0], ls="none",
               label="first passing candidate (forced publication)")],
        loc="center right", bbox_to_anchor=(1.0, 0.30), fontsize=8.2)
    F.finish(fig, os.path.join(OUT, "firstpass.svg"))


def fig_classkernel():
    """Coefficient-kernel vs class-uniform mass over the 67 safe classes."""
    rows = read_rows("class_kernel_b7_20260708.csv")
    orbit = np.array([int(r["orbit_size"]) for r in rows])
    total = int(orbit.sum())            # 4179 safe encodings
    N = len(rows)                       # 67 safe classes
    mass = orbit / total
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0),
                                   gridspec_kw={"width_ratios": [1.55, 1]})
    colors = [F.PALETTE[1] if o == 21 else F.PALETTE[0] for o in orbit]
    ax1.bar(range(N), mass, width=0.86, color=colors, linewidth=0)
    ax1.axhline(1 / N, color=F.INK, lw=1.2, ls="--")
    ax1.annotate(r"$(a,b)=(0,13)$, orbit 21: mass $1/199$", (0.6, mass[0]),
                 xytext=(4, 0.0215), textcoords="data", fontsize=8.6,
                 color=F.PALETTE[1], ha="left", va="center",
                 arrowprops=dict(arrowstyle="->", color=F.PALETTE[1], lw=1.0,
                                 connectionstyle="arc3,rad=-0.25"))
    ax1.text(4, 0.0196, r"66 generic classes: $63/4179=3/199$",
             fontsize=8.6, color=F.PALETTE[0], ha="left")
    ax1.text(4, 0.0177,
             r"dashed: class-uniform $1/67$;   "
             r"$d_{\mathrm{TV}}=132/13333\approx 0.0099$",
             fontsize=8.6, color=F.INK_SECOND, ha="left")
    ax1.set_xlabel("canonical safe-class rank (lexicographic)")
    ax1.set_ylabel("class probability")
    ax1.set_ylim(0, 0.0228)
    ax1.set_title("Coefficient kernel vs class-uniform")

    sub = Counter(int(r["subgroup_order"]) for r in rows)
    ks = sorted(sub)
    ax2.bar(range(len(ks)), [sub[k] for k in ks], color=F.PALETTE[2],
            width=0.72)
    ax2.set_xticks(range(len(ks)))
    ax2.set_xticklabels(ks, fontsize=7.6, rotation=60)
    ax2.set_xlabel("prime subgroup order $r$")
    ax2.set_ylabel("safe classes")
    ax2.set_title("Safe-class census by $r$")
    F.finish(fig, os.path.join(OUT, "classkernel.svg"))


def fig_auditbits():
    """A256 conditional selection-capacity caps across the five audited curves."""
    curves = ["NIST P-256", "Curve25519", "brainpoolP256r1",
              "secp256k1", "BLS12-381"]
    core = [161, 0, 0, None, None]
    pkg = [417, 1, 1, None, None]
    core_lab = [r"$\leq 161$", r"$0$ (given $p$)", r"$0$", None, None]
    pkg_lab = [r"$\leq 417$", r"$\leq 1$ (affine sign; 0 $u$-only)",
               r"$1$ (point sign)", None, None]
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    y = np.arange(len(curves))[::-1]
    h = 0.30
    for i, (c, p) in enumerate(zip(core, pkg)):
        yy = y[i]
        if c is None:
            ax.add_patch(plt.Rectangle((0, yy - 0.40), 470, 0.80,
                                       facecolor=F.GRID, edgecolor=F.MUTED,
                                       linewidth=0.7, hatch="///", zorder=1,
                                       alpha=0.55))
            ax.text(235, yy, r"$\perp$ — not identifiable from the cited "
                    "source record", ha="center", va="center", fontsize=8.8,
                    color=F.INK_SECOND, zorder=3)
        else:
            ax.barh(yy + h / 2 + 0.02, c, height=h, color=F.PALETTE[0])
            ax.barh(yy - h / 2 - 0.02, p, height=h, color=F.PALETTE[1])
            ax.text(c + 6, yy + h / 2 + 0.02, core_lab[i], va="center",
                    fontsize=8.6, color=F.INK_SECOND)
            ax.text(p + 6, yy - h / 2 - 0.02, pkg_lab[i], va="center",
                    fontsize=8.6, color=F.INK_SECOND)
    ax.set_yticks(y)
    ax.set_yticklabels(curves, fontsize=9.5)
    ax.set_xlim(0, 470)
    ax.set_xlabel("conditional cap on designer selection capacity $b$ (bits)")
    ax.set_title("A256 audit: curve-core and full-package caps")
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(facecolor=F.PALETTE[0], label="curve-core projection"),
        Patch(facecolor=F.PALETTE[1], label="full-package projection")],
        loc="center right", bbox_to_anchor=(1.0, 0.55), fontsize=8.6)
    F.finish(fig, os.path.join(OUT, "auditbits.svg"))


if __name__ == "__main__":
    fig_game()
    fig_firstpass()
    fig_classkernel()
    fig_auditbits()
    print("P5.3 figures written")
