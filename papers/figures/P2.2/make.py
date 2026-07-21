"""Figures for the P2.2 paper (q-type assumptions: catalogue and separations).

All three figures are honest schematics reconstructed from the recorded
research content (NOTES.md sections 1-2 and 13, attempts A002/A006/A007).
P2.2 has no data/ CSVs and no empirical measurements; nothing drawn here is
presented as measured data.
"""
import os, sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
# On this machine matplotlib resolves the shared serif list to Cambria, which
# ships as a .ttc collection that Agg fails to draw (plain text silently
# vanishes while mathtext survives).  Skip it; keep the rest of the style.
mpl.rcParams["font.serif"] = ["Georgia", "DejaVu Serif", "Times New Roman"]
OUT = os.path.dirname(__file__)

HW, HH = 1.13, 0.47  # node half-extents incl. box padding


def _node(ax, x, y, text, w=2.1, h=0.78, ec=None, fc=None, fs=9.5, lw=1.4):
    ec = ec or F.PALETTE[0]
    fc = fc or F.SURFACE
    box = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                         boxstyle="round,pad=0.08,rounding_size=0.12",
                         linewidth=lw, edgecolor=ec, facecolor=fc, zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            color=F.INK, zorder=4)


def _edge(ax, p, q, rad=0.0, color=None, lw=1.5, double=False):
    color = color or F.INK_SECOND
    arrow = FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                            arrowstyle="<|-|>" if double else "-|>",
                            mutation_scale=12, lw=lw, color=color,
                            shrinkA=2, shrinkB=2, zorder=2)
    ax.add_patch(arrow)


def _elabel(ax, x, y, text, fs=8.0):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=F.MUTED,
            zorder=5, bbox=dict(boxstyle="round,pad=0.16", fc=F.SURFACE,
                                ec="none", alpha=0.92))


def fig_implication_graph():
    """SG-02: the audited hardness-implication graph (NOTES.md section 2).

    An arrow A -> B means hardness of A implies hardness of B; every edge is
    one oracle call and success-preserving, with the annotated extra work.
    """
    fig, ax = plt.subplots(figsize=(7.6, 4.25))
    ax.set_xlim(0, 12.3)
    ax.set_ylim(-0.15, 6.45)
    ax.axis("off")

    P = {
        "BDHI":   (1.5, 5.5),
        "wBDHIs": (5.0, 5.5),
        "wBDHI":  (8.5, 5.5),
        "BDHE":   (1.5, 3.4),
        "DHE":    (5.0, 3.4),
        "DHI":    (8.5, 3.4),
        "aBDH":   (1.5, 1.3),
        "SDH":    (5.0, 1.3),
        "DDHI":   (8.5, 1.3),
        "DBDHI":  (11.05, 1.3),
    }
    comp = F.PALETTE[0]
    deci = F.PALETTE[6]

    _node(ax, *P["BDHI"], "$q$-BDHI", ec=comp)
    _node(ax, *P["wBDHIs"], "$q$-wBDHI$^{*}$", ec=comp)
    _node(ax, *P["wBDHI"], "$q$-wBDHI", ec=comp)
    _node(ax, *P["BDHE"], "$(q{+}1)$-BDHE", ec=comp)
    _node(ax, *P["DHE"], "$q$-DHE", ec=comp)
    _node(ax, *P["DHI"], "$q$-DHI", ec=comp)
    _node(ax, *P["aBDH"], "$q$-aBDH", ec=comp)
    _node(ax, *P["SDH"], "$q$-SDH", ec=F.PALETTE[1], fc=F.SEQ[0], lw=1.8)
    _node(ax, *P["DDHI"], "$q$-DDHI", ec=deci)
    _node(ax, *P["DBDHI"], "$q$-DBDHI", ec=deci, w=2.0)

    # row 1
    _edge(ax, (P["BDHI"][0] + HW, 5.5), (P["wBDHIs"][0] - HW, 5.5))
    _elabel(ax, 3.25, 5.82, "one call, tight")
    _edge(ax, (P["wBDHIs"][0] + HW, 5.5), (P["wBDHI"][0] - HW, 5.5), double=True)
    _elabel(ax, 6.75, 5.82, "one call each way")
    # wBDHI* -> DHE (vertical)
    _edge(ax, (5.0, 5.5 - HH), (5.0, 3.4 + HH))
    _elabel(ax, 6.25, 4.62, "DHE call, pair $h_2$")
    # BDHI -> DHI (curved, one pairing)
    _edge(ax, (1.5, 5.5 - HH), (8.5, 3.4 + HH), rad=-0.08)
    _elabel(ax, 2.78, 4.62, "one pairing")
    # row 2
    _edge(ax, (P["BDHE"][0] + HW, 3.4), (P["DHE"][0] - HW, 3.4))
    _elabel(ax, 3.25, 3.72, "prefix, one pairing")
    _edge(ax, (P["DHE"][0] + HW, 3.4), (P["DHI"][0] - HW, 3.4))
    _elabel(ax, 6.75, 3.72, "reverse ladder, tight")
    # row 3
    _edge(ax, (P["aBDH"][0] + HW, 1.3), (P["SDH"][0] - HW, 1.3))
    _elabel(ax, 3.25, 1.62, "one call, $O(q)$ ops")
    _edge(ax, (5.95, 1.3 + HH), (7.62, 3.4 - HH))
    _elabel(ax, 7.25, 2.05, "$c := 0$")
    _edge(ax, (P["DDHI"][0] + HW, 1.3), (P["DBDHI"][0] - 1.08, 1.3),
          color=deci)
    _elabel(ax, 9.82, 1.62, "pair with $[1]_2$")

    ax.text(6.15, 0.14,
            "family truncation (not drawn): $H(q\\mathrm{-}X) \\to "
            "H(k\\mathrm{-}X)$ for $k \\leq q$, "
            "$X \\in \\{$SDH, DHI, DDHI, BDHI, DBDHI, wBDHI$\\}$",
            ha="center", va="center", fontsize=8.2, color=F.MUTED)
    ax.set_title("Audited hardness-implication graph "
                 "($H(A) \\to H(B)$: a breaker for $B$ becomes a breaker for $A$)",
                 fontsize=11)
    F.finish(fig, os.path.join(OUT, "implication_graph.svg"))


def fig_metareduction():
    """A006: architecture of the bounded-fresh-label meta-reduction."""
    fig, ax = plt.subplots(figsize=(7.5, 4.7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.8)
    ax.axis("off")

    _node(ax, 2.65, 6.9, "fixed-size challenger $F^{G_*}$\nat most $n$ "
          "source-group labels", w=4.5, h=1.0, ec=F.PALETTE[0], fs=9.3)
    _node(ax, 9.25, 6.9, "native representation code\nvalidate / decompress / "
          "hash-to-group\nat most $s$ fresh source labels", w=4.7, h=1.25,
          ec=F.PALETTE[1], fs=9.0)
    _node(ax, 5.95, 4.95, "reduction $R$ — PPT, fully black-box, $s$-fresh",
          w=5.9, h=0.85, ec=F.PALETTE[6], fs=9.5, lw=1.7)
    _node(ax, 2.65, 3.0, "dictionary $D$: every typed source label\n"
          "$\\mapsto$ vector in $\\mathbb{Z}_r^{\\,n+s+1}$\n"
          "basis: $n$ challenger $+$ $s$ fresh $+$ generator",
          w=4.7, h=1.35, ec=F.PALETTE[2], fs=8.8)
    _node(ax, 9.25, 3.0, "simulated perfect $q$-SDH adversary\n"
          "root list from $M$ (Lu–Zhandry Lem. 5.1)\n"
          "check candidates, return $(c,\\,U^{1/(x+c)})$",
          w=4.7, h=1.35, ec=F.PALETTE[3], fs=8.8)
    _node(ax, 5.95, 0.85, "PPT attack on $F^{G_*}$ whenever $n+s<q-1$ — "
          "no additional success loss", w=7.6, h=0.8, ec=F.PALETTE[7], fs=9.3)

    _edge(ax, (2.65, 6.35), (4.35, 5.42))
    _elabel(ax, 2.9, 5.72, "challenge labels")
    _edge(ax, (9.25, 6.22), (7.55, 5.42))
    _elabel(ax, 9.05, 5.72, "fresh labels (budget $s$)")
    _edge(ax, (4.35, 4.48), (2.9, 3.72))
    _elabel(ax, 2.9, 4.28, "trace every typed label")
    _edge(ax, (7.55, 4.48), (9.0, 3.72), double=True)
    _elabel(ax, 9.15, 4.28, "$q$-SDH oracle calls / answers")
    _edge(ax, (5.95, 4.48), (5.95, 1.3))
    _edge(ax, (5.05, 3.0), (6.85, 3.0), color=F.PALETTE[2])
    _elabel(ax, 5.95, 3.0, "ladder rows form $M$\n($\\leq n+s+1$ columns)",
            fs=8.2)
    ax.set_title("A006 meta-reduction: one coordinate per native fresh label "
                 "restores the trace invariant", fontsize=10.5)
    F.finish(fig, os.path.join(OUT, "metareduction.svg"))


def fig_freshness():
    """A006 thresholds: the separation region and minimal ladder lengths."""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(7.7, 3.25))

    # Panel A: region n1 + s1 < q - 1 for concrete q.
    n = np.linspace(0, 70, 300)
    qs = [64, 32, 16, 8]
    fills = [F.SEQ[0], F.SEQ[1], F.SEQ[2], F.SEQ[3]]
    lines = [F.SEQ[11], F.SEQ[9], F.SEQ[7], F.SEQ[5]]
    for q, fc in zip(qs, fills):
        s = np.clip(q - 1 - n, 0, None)
        axa.fill_between(n, 0, s, color=fc, lw=0, zorder=1)
    for q, lc in zip(qs, lines):
        s = q - 1 - n
        m = s >= 0
        axa.plot(n[m], s[m], color=lc, lw=1.6, zorder=2)
        axa.annotate(f"$q={q}$", xy=(max(q - 1 - 3.5, 0.6), 2.1),
                     fontsize=8.5, color=lc, rotation=0,
                     bbox=dict(boxstyle="round,pad=0.12", fc=F.SURFACE,
                               ec="none", alpha=0.85))
    axa.text(6, 26, "separation applies:\nreduction impossible\nif $F^{G_*}$ "
             "is hard", fontsize=8.6, color=F.INK_SECOND)
    axa.text(40, 50, "outside the theorem\n(open residual class)",
             fontsize=8.6, color=F.MUTED)
    axa.set_xlim(0, 70)
    axa.set_ylim(0, 70)
    axa.set_xlabel("challenge labels reaching the source, $n_1$")
    axa.set_ylabel("fresh native source labels, $s_1$")
    axa.set_title("Source-valued region $n_1+s_1<q-1$", fontsize=10.5)

    # Panel B: minimal ladder length q for the separation to bite.
    k = np.arange(0, 31)
    lin = k + 2                      # smallest q with n1+s1 < q-1
    quad = (k + 2) * (k + 1) // 2 + 1  # smallest q with C(n+s+2,2) < q, t=0
    axb.plot(k, lin, color=F.PALETTE[0], lw=2.0,
             label="source-valued $q$-SDH: $q_{\\min}=n_1{+}s_1{+}2$")
    axb.plot(k, quad, color=F.PALETTE[1], lw=2.0,
             label="bilinear overcount, $t{=}0$:\n"
                   "$q_{\\min}=(n{+}s{+}2)(n{+}s{+}1)/2+1$")
    axb.set_yscale("log")
    axb.set_xlabel("$n+s$ (challenge $+$ fresh labels)")
    axb.set_ylabel("minimal ladder length $q$")
    axb.set_title("Ladder length needed for separation", fontsize=10.5)
    axb.legend(fontsize=7.8, loc="upper left")
    F.finish(fig, os.path.join(OUT, "freshness.svg"))


if __name__ == "__main__":
    fig_implication_graph()
    fig_metareduction()
    fig_freshness()
    print("P2.2 figures written")
