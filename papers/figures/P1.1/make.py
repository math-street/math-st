"""Figures for the P1.1 paper (generic lower bounds beyond the GGM)."""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)


def fig_bypass():
    """Charged group operations: oracle spelling vs coordinate-compiled spelling."""
    labels = ["Charged\ngroup ops", "Coordinate\narith. events", "Equality\ntests"]
    oracle = [17, 17, 7]
    coord = [0, 17, 7]
    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(5.4, 3.1))
    b1 = ax.bar(x - w/2, oracle, w, label="charged group oracle",
                color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=1.2)
    b2 = ax.bar(x + w/2, coord, w, label="free coordinate formula",
                color=F.PALETTE[1], edgecolor=F.SURFACE, linewidth=1.2)
    ax.bar_label(b1, padding=2, fontsize=9, color=F.INK_SECOND)
    ax.bar_label(b2, padding=2, fontsize=9, color=F.INK_SECOND)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel("count (single fixed instance)")
    ax.set_title(r"Recovering $[7](5,1)$ on $y^2=x^3+2x+2$ over $\mathbb{F}_{17}$")
    ax.set_ylim(0, 20)
    ax.legend(loc="upper right")
    F.finish(fig, os.path.join(OUT, "bypass.svg"))


def fig_taxonomy():
    """Operation-requirement matrix as a categorical grid (SG-01)."""
    attacks = ["BSGS", "Pollard rho", "Pohlig–Hellman",
               "SSSA anomalous", "MOV / Frey–Rück", "GHS Weil descent",
               "Semaev over $\\mathbb{F}_p$", "Gaudry/Diem over $\\mathbb{F}_{q^n}$"]
    prims = ["Group\nlaw", "Equality", "Coord.\narith.", "$p$-adic\nlift",
             "Pairing", "Poly.\nsolving", "EXT /\nsubfield", "AUX-\nDLP", "Linear\nalg."]
    # R=2 required, I=1 impl choice, 0 = not used
    M = np.array([
        [2,2,0,0,0,0,0,0,0],  # BSGS
        [2,2,1,0,0,0,0,0,0],  # Pollard rho
        [2,2,0,0,0,0,0,0,0],  # Pohlig-Hellman
        [2,0,2,2,0,0,0,0,0],  # SSSA
        [2,2,2,0,2,0,2,2,0],  # MOV
        [2,2,2,0,0,0,2,2,2],  # GHS
        [2,2,2,0,0,2,0,0,2],  # Semaev Fp
        [2,2,2,0,0,2,2,0,2],  # Gaudry/Diem
    ])
    cmap = {0: F.SURFACE, 1: F.PALETTE[3], 2: F.PALETTE[0]}
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            ax.add_patch(plt.Rectangle((j, i), 0.92, 0.92, facecolor=cmap[v],
                         edgecolor=F.GRID, linewidth=0.8))
            if v == 2:
                ax.text(j+0.46, i+0.46, "R", ha="center", va="center",
                        color=F.SURFACE, fontsize=8.5, weight="bold")
            elif v == 1:
                ax.text(j+0.46, i+0.46, "I", ha="center", va="center",
                        color=F.INK, fontsize=8.5, weight="bold")
    ax.set_xlim(0, M.shape[1]); ax.set_ylim(0, M.shape[0])
    ax.set_xticks(np.arange(M.shape[1])+0.46)
    ax.set_xticklabels(prims, fontsize=8)
    ax.set_yticks(np.arange(M.shape[0])+0.46)
    ax.set_yticklabels(attacks, fontsize=8.5)
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_axisbelow(False); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    # legend
    from matplotlib.patches import Patch
    leg = [Patch(facecolor=F.PALETTE[0], label="R — required"),
           Patch(facecolor=F.PALETTE[3], label="I — implementation choice"),
           Patch(facecolor=F.SURFACE, edgecolor=F.GRID, label="— not used")]
    ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0, -0.04),
              ncol=3, fontsize=8.5)
    F.finish(fig, os.path.join(OUT, "taxonomy.svg"))


def fig_shoup():
    """Shoup success bound O(m^2/r) vs charged cost 0 in CCA_0, log-scaled."""
    r = 2**20
    m = np.linspace(1, 2000, 400)
    succ = np.minimum(1.0, (m*(m+1)/2 + 1) / r)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    ax.plot(m, succ, color=F.PALETTE[0], label=r"GGM: $\binom{m+2}{2}/r$ (opaque encoding)")
    ax.axhline(1.0, color=F.PALETTE[7], lw=1.4, ls="--",
               label=r"$\mathsf{CCA}_0$: success $1$ at $0$ charged ops")
    ax.axvline(np.sqrt(r), color=F.MUTED, lw=1.0, ls=":")
    ax.text(np.sqrt(r)+20, 0.12, r"$m\approx\sqrt{r}$", color=F.MUTED, fontsize=9)
    ax.set_xlabel("charged group-oracle queries $m$")
    ax.set_ylabel("success probability")
    ax.set_title(r"Opacity is load-bearing: group order $r=2^{20}$")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="center right", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "shoup.svg"))


if __name__ == "__main__":
    fig_bypass()
    fig_taxonomy()
    fig_shoup()
    print("P1.1 figures written")
