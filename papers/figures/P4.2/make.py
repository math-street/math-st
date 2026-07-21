"""Figures for the P4.2 paper (pairing-friendly cycles of elliptic curves).

Census data are loaded from the real search summary JSONs and classification
CSVs in problems/P4.2-pairing-friendly-cycles/data/.
"""
import os, sys, csv, json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P4.2-pairing-friendly-cycles", "data")

TWO_CYCLE_SUMMARIES = [
    (16, "search_two_cycles_p5-65535_k3-12_20260708_summary.json"),
    (18, "search_two_cycles_p5-262143_k3-12_20260708_summary.json"),
    (20, "search_two_cycles_p5-1048575_k3-12_20260708_summary.json"),
    (22, "search_two_cycles_targeted_p5-4194303_k3-12_20260708_summary.json"),
    (24, "search_two_cycles_targeted_p5-16777215_k3-12_20260708_summary.json"),
    (26, "search_two_cycles_roots_p5-67108863_k3-12_20260708_summary.json"),
    (28, "search_two_cycles_roots_p5-268435455_k3-12_20260708_summary.json"),
]
THREE_CYCLE_SUMMARIES = [
    (16, "search_three_cycles_p5-65535_k3-12_20260708_summary.json"),
    (18, "search_three_cycles_p5-262143_k3-12_20260708_summary.json"),
    (20, "search_three_cycles_targeted_p5-1048575_k3-12_20260708_summary.json"),
    (22, "search_three_cycles_targeted_p5-4194303_k3-12_20260708_summary.json"),
    (24, "search_three_cycles_targeted_p5-16777215_k3-12_20260708_summary.json"),
    (26, "search_three_cycles_roots_p5-67108863_k3-12_20260708_summary.json"),
    (28, "search_three_cycles_roots_p5-268435455_k3-12_20260708_summary.json"),
]


def load(name):
    with open(os.path.join(DATA, name)) as fh:
        return json.load(fh)


def fig_census():
    """Growth of the verified cycle census from 16 to 28 bits."""
    bits, mnt, exc = [], [], []
    for b, name in TWO_CYCLE_SUMMARIES:
        d = load(name)
        pairs = d["hit_degree_pair_counts"]
        m = pairs.get("6,4", 0) + pairs.get("4,6", 0)
        bits.append(b)
        mnt.append(m)
        exc.append(d["hit_count"] - m)
    three_hits, three_nm = [], []
    for b, name in THREE_CYCLE_SUMMARIES:
        d = load(name)
        three_hits.append(d["hit_count"])
        three_nm.append(d["two_of_three_near_miss_count"])

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9))
    ax = axes[0]
    x = np.arange(len(bits))
    b1 = ax.bar(x, mnt, 0.6, color=F.PALETTE[0], edgecolor=F.SURFACE,
                linewidth=0.6, label="MNT pattern (6,4)/(4,6)")
    ax.bar(x, exc, 0.6, bottom=mnt, color=F.PALETTE[7], edgecolor=F.SURFACE,
           linewidth=0.6, label="exceptional (5 total, all $q\\leq 31$)")
    for xi, (m, e) in enumerate(zip(mnt, exc)):
        ax.text(xi, m + e + 4, str(m + e), ha="center", fontsize=8.4,
                color=F.INK_SECOND)
    ax.set_xticks(x)
    ax.set_xticklabels([f"$2^{{{b}}}$" for b in bits], fontsize=9)
    ax.set_xlabel("prime bound")
    ax.set_ylabel("verified 2-cycles")
    ax.set_ylim(0, 375)
    ax.set_title("2-cycle hits, exact degrees 3–12")
    ax.legend(fontsize=8.0, loc="upper left")

    ax = axes[1]
    ax.plot(bits, three_nm, marker="o", color=F.PALETTE[1],
            label="two-of-three near-misses")
    ax.plot(bits, three_hits, marker="s", color=F.PALETTE[5],
            label="full directed 3-cycles")
    ax.annotate("stays at 5 (all fields $\\leq 43$)", (22, 8),
                fontsize=8.4, color=F.INK_SECOND)
    ax.set_xlabel("prime bound (bits)")
    ax.set_ylabel("count")
    ax.set_ylim(0, 70)
    ax.set_title("Directed 3-cycle ledger")
    ax.legend(fontsize=8.0, loc="upper left")
    F.finish(fig, os.path.join(OUT, "census.svg"))


def fig_classification():
    """Status of every ordered exact-degree pair (k1,k2) in {3..12}^2."""
    ks = list(range(3, 13))
    Q2 = {3, 4, 6}
    Q4 = {5, 8, 10, 12}
    # status codes: 0 open (involves 7,9,11), 1 impossible (proved),
    # 2 MNT family, 3 unique tiny cycle
    tiny = {(10, 3): "(7,11)", (12, 10): "(11,13)"}
    hits_open = {(9, 8): "(17,19)", (7, 11): "(23,29)", (10, 11): "(23,31)"}
    M = np.zeros((len(ks), len(ks)), dtype=int)
    for i, k1 in enumerate(ks):
        for j, k2 in enumerate(ks):
            if (k1, k2) in ((6, 4), (4, 6)):
                M[i, j] = 2
            elif (k1, k2) in tiny:
                M[i, j] = 3
            elif (k1 in Q2 | Q4) and (k2 in Q2 | Q4):
                M[i, j] = 1
            else:
                M[i, j] = 0
    cmap = {0: F.SURFACE, 1: F.SEQ[2], 2: F.PALETTE[0], 3: F.PALETTE[3]}
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    for i in range(len(ks)):
        for j in range(len(ks)):
            ax.add_patch(plt.Rectangle((j, i), 0.92, 0.92,
                         facecolor=cmap[M[i, j]], edgecolor=F.GRID,
                         linewidth=0.8))
            k1, k2 = ks[i], ks[j]
            if (k1, k2) in tiny:
                ax.text(j + 0.46, i + 0.46, tiny[(k1, k2)], ha="center",
                        va="center", fontsize=6.8, color=F.INK, weight="bold")
            elif (k1, k2) in ((6, 4), (4, 6)):
                ax.text(j + 0.46, i + 0.46, "MNT", ha="center", va="center",
                        fontsize=7.4, color=F.SURFACE, weight="bold")
            elif (k1, k2) in hits_open:
                ax.text(j + 0.46, i + 0.46, hits_open[(k1, k2)], ha="center",
                        va="center", fontsize=6.4, color=F.INK_SECOND)
    ax.set_xlim(0, len(ks))
    ax.set_ylim(0, len(ks))
    ax.set_xticks(np.arange(len(ks)) + 0.46)
    ax.set_xticklabels(ks, fontsize=9)
    ax.set_yticks(np.arange(len(ks)) + 0.46)
    ax.set_yticklabels(ks, fontsize=9)
    ax.set_xlabel("exact embedding degree $k_2$")
    ax.set_ylabel("exact embedding degree $k_1$")
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.set_axisbelow(False)
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    from matplotlib.patches import Patch
    leg = [Patch(facecolor=F.PALETTE[0], label="MNT family (all cycles)"),
           Patch(facecolor=F.PALETTE[3], label="unique tiny cycle"),
           Patch(facecolor=F.SEQ[2], label="proved impossible"),
           Patch(facecolor=F.SURFACE, edgecolor=F.GRID,
                 label="open globally (7, 9, or 11); labels = tiny hits")]
    ax.legend(handles=leg, loc="upper left", bbox_to_anchor=(0, -0.02),
              ncol=2, fontsize=8.2)
    F.finish(fig, os.path.join(OUT, "classification.svg"))


def fig_quartic():
    """Elimination funnel for the 750 quartic/quartic genus-one rows."""
    stages = ["750 genus-one\nrows ($|h|\\leq 24$)",
              "after congruence\nsieve mod $2^k$, odd $p\\leq 251$",
              "after exact\nreal-sign analysis",
              "after higher-power\nHensel lifting",
              "after exact global\ngenus-one closure"]
    counts = [750, 120, 51, 47, 0]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    x = np.arange(len(stages))
    cols = [F.PALETTE[0], F.SEQ[7], F.SEQ[5], F.SEQ[3], F.PALETTE[5]]
    bars = ax.bar(x, counts, 0.62, color=cols, edgecolor=F.SURFACE,
                  linewidth=0.8)
    ax.bar_label(bars, padding=3, fontsize=9.5, color=F.INK_SECOND)
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=7.8)
    ax.set_ylabel("surviving rows")
    ax.set_ylim(0, 820)
    ax.set_title("Quartic/quartic reduction: only $(11,13;12,10)$ survives")
    ax.annotate("47 rows = 29 normalized curves;\nMagma: 22 integral-point lists,\n5 empty fake 2-Selmer sets,\n1 symmetric rank-0 pair",
                xy=(3, 47), xytext=(2.45, 420), fontsize=8.2,
                color=F.INK_SECOND,
                arrowprops=dict(arrowstyle="->", color=F.MUTED, lw=1.0))
    F.finish(fig, os.path.join(OUT, "quartic.svg"))


def fig_nearmiss():
    """Directed 3-cycle near-misses below 2^28: MNT chains vs residual rows."""
    rows = list(csv.DictReader(open(os.path.join(
        DATA, "classify_three_cycle_near_misses_n61_20260718.csv"))))
    chains = [np.log2(float(r["maximum_field_prime"])) for r in rows
              if r["family"] == "consecutive_mnt_chain"]
    resid = [np.log2(float(r["maximum_field_prime"])) for r in rows
             if r["family"] == "unclassified_residual"]
    bins = np.arange(2, 29, 1)
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    ax.hist([chains, resid], bins=bins, stacked=True,
            color=[F.PALETTE[0], F.PALETTE[1]],
            edgecolor=F.SURFACE, linewidth=0.5,
            label=[f"consecutive MNT chain ({len(chains)}) — globally excluded",
                   f"unclassified residual ({len(resid)})"])
    ax.axvline(16, color=F.MUTED, lw=1.0, ls=":")
    ax.text(16.3, 10.3, "only 2 residual rows above $2^{16}$",
            fontsize=8.4, color=F.INK_SECOND)
    ax.set_xlabel("largest field prime in the near-miss (bits)")
    ax.set_ylabel("near-miss rows")
    ax.set_title("The 61 two-of-three near-misses below $2^{28}$")
    ax.legend(fontsize=8.4, loc="upper right")
    F.finish(fig, os.path.join(OUT, "nearmiss.svg"))


if __name__ == "__main__":
    fig_census()
    fig_classification()
    fig_quartic()
    fig_nearmiss()
    print("P4.2 figures written")
