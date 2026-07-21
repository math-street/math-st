"""Figures for the P5.4 paper (toy hash-to-curve compile-time family)."""
import os, sys, csv
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                    "problems", "P5.4-hash-to-curve", "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_pipeline():
    """Schematic of the RFC 9380-shaped two-map pipeline (from SPEC.md)."""
    fig, ax = plt.subplots(figsize=(6.8, 2.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.4)
    ax.axis("off")

    def box(x, y, w, h, text, color, tcolor=None, fs=9.5):
        ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color,
                                   edgecolor=F.AXIS, linewidth=0.9))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center",
                fontsize=fs, color=tcolor or F.INK)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=F.INK_SECOND,
                                    linewidth=1.3))

    # message -> hash_to_field
    box(0.1, 1.7, 1.15, 1.0, "msg", "#e8eef8")
    arrow(1.25, 2.2, 1.75, 2.2)
    box(1.75, 1.45, 2.15, 1.5,
        "hash_to_field\n(XMD SHA-256,\nsuite DST)", "#e8eef8")
    # two field elements
    arrow(3.9, 2.55, 4.5, 3.25)
    arrow(3.9, 1.85, 4.5, 1.15)
    ax.text(4.18, 2.95, "$u_0$", fontsize=10.5, color=F.INK)
    ax.text(4.18, 1.28, "$u_1$", fontsize=10.5, color=F.INK)
    # two map boxes
    box(4.5, 2.85, 1.95, 0.95, "map_to_curve", "#e2f3ec")
    box(4.5, 0.55, 1.95, 0.95, "map_to_curve", "#e2f3ec")
    ax.text(5.475, 2.55, "$Q_0$", fontsize=10.5, color=F.INK, ha="center")
    ax.text(5.475, 1.78, "$Q_1$", fontsize=10.5, color=F.INK, ha="center")
    # add
    arrow(6.45, 3.3, 7.05, 2.5)
    arrow(6.45, 1.05, 7.05, 1.9)
    box(7.05, 1.7, 1.0, 1.0, "$+$", "#fdf1e2", fs=13)
    # clear cofactor
    arrow(8.05, 2.2, 8.5, 2.2)
    box(8.5, 1.7, 1.4, 1.0, "$[h]\\,\\cdot$", "#fdf1e2", fs=12)
    ax.text(9.2, 1.4, "clear cofactor", ha="center", fontsize=8.5,
            color=F.INK_SECOND)
    ax.text(9.2, 3.0, "$P \\in$ subgroup\nof order $r$", ha="center",
            fontsize=9.5, color=F.INK)
    # compile-time dispatch note
    ax.text(5.475, 4.15,
            "compile-time map choice: SSWU | SSWU$\\circ$isogeny | SvdW | "
            "Elligator 2 | char-2/3 routes",
            ha="center", fontsize=9, color=F.INK_SECOND)
    ax.plot([4.5, 6.45, 6.45, 4.5, 4.5], [0.4, 0.4, 3.95, 3.95, 0.4],
            color=F.MUTED, linewidth=0.7, linestyle=":")
    ax.set_title("The registered two-map interface (RFC 9380 Section 3 shape)")
    F.finish(fig, os.path.join(OUT, "pipeline.svg"))


def fig_coverage():
    """Preimage spread and total-variation distance of the six SW suites."""
    rows = read_csv("validate_hash_pipeline_full_20260712.csv")
    labels, lo, hi, tv, orders = [], [], [], [], []
    for r in rows:
        pairs = int(r["field_pairs"])
        order = int(r["subgroup_order"])
        uniform = pairs / order
        short = (r["suite_id"].replace("TOY-", "").replace("-SHA256", "")
                 .replace("-RO", ""))
        labels.append(short)
        lo.append(int(r["minimum_preimages"]) / uniform)
        hi.append(int(r["maximum_preimages"]) / uniform)
        tv.append(float(r["tv_distance_decimal"]))
        orders.append(order)
    y = np.arange(len(labels))[::-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.0),
                                   gridspec_kw={"width_ratios": [1.25, 1.0]})
    ax1.axvline(1.0, color=F.MUTED, linewidth=1.0, linestyle="--")
    for yi, a, b in zip(y, lo, hi):
        ax1.plot([a, b], [yi, yi], color=F.PALETTE[0], linewidth=5,
                 solid_capstyle="round", alpha=0.85)
    ax1.scatter(lo, y, color=F.PALETTE[0], zorder=3, s=22)
    ax1.scatter(hi, y, color=F.PALETTE[6], zorder=3, s=22)
    ax1.set_yticks(y)
    ax1.set_yticklabels(labels, fontsize=8.5)
    ax1.set_xlabel("preimage count / uniform expectation")
    ax1.set_title("Fiber spread over the subgroup")
    bars = ax2.barh(y, tv, color=F.PALETTE[1], height=0.55,
                    edgecolor=F.SURFACE)
    for yi, t, n in zip(y, tv, orders):
        ax2.text(t + 0.004, yi, f"{t:.4f}  (r={n})", va="center",
                 fontsize=8, color=F.INK_SECOND)
    ax2.set_yticks(y)
    ax2.set_yticklabels([])
    ax2.set_xlim(0, 0.27)
    ax2.set_xlabel("exact TV distance from uniform")
    ax2.set_title("Exhaustive output histograms")
    F.finish(fig, os.path.join(OUT, "coverage.svg"))


def fig_timing():
    """Forest plot of every recorded paired timing ratio and its 95% CI."""
    rows = []  # (label, ratio, lo, hi, group)
    for r in read_csv("measure_map_timing_p11_s240_b100_seed5402_20260704_summary.csv"):
        name = {"elligator2": "Elligator 2 (p=11)",
                "simple_swu": "SSWU (p=11)"}[r["mapping"]]
        rows.append((name, float(r["mean_ratio_exceptional_over_ordinary"]),
                     float(r["ratio_ci95_low"]), float(r["ratio_ci95_high"]), 0))
    ext_names = {
        "elligator2_edwards": "Elligator 2 to Edwards (p=7)",
        "sswu_isogeny_j0": "SSWU-isogeny j=0 (p=29)",
        "sswu_isogeny_j1728": "SSWU-isogeny j=1728 (p=59)",
        "svdw_j0": "SvdW j=0 (p=11)",
        "svdw_j1728": "SvdW j=1728 (p=11)",
        "svdw_montgomery_transport": "SvdW to Montgomery (p=11)",
    }
    for r in read_csv("measure_extended_timing_s160_b80_seed5408_20260712_summary.csv"):
        rows.append((ext_names[r["mapping"]], float(r["mean_ratio_a_over_b"]),
                     float(r["ratio_ci95_low"]), float(r["ratio_ci95_high"]), 1))
    for r in read_csv("measure_compiled_timing_p11_s400_b1000_seed5409_20260720_summary.csv"):
        rows.append(("Rust u64 pipeline (p=11)",
                     float(r["mean_ratio_a_over_b"]),
                     float(r["paired_bootstrap_ci_low"]),
                     float(r["paired_bootstrap_ci_high"]), 2))

    fig, ax = plt.subplots(figsize=(6.9, 3.9))
    ypos, ylab, seen_groups = [], [], {}
    y = 0
    group_span = defaultdict(list)
    for label, ratio, lo, hi, g in rows:
        if g not in seen_groups:
            y -= 0.5  # gap between groups
            seen_groups[g] = True
        ax.errorbar(ratio, y, xerr=[[ratio - lo], [hi - ratio]],
                    fmt="o", color=F.PALETTE[g], ecolor=F.PALETTE[g],
                    elinewidth=2.0, capsize=3, markersize=5.5)
        group_span[g].append(y)
        ypos.append(y)
        ylab.append(label)
        y -= 1
    bands = {0: (0.9, 1.1), 1: (0.8, 1.25), 2: (0.9, 1.1)}
    for g, ys in group_span.items():
        b = bands[g]
        ax.add_patch(plt.Rectangle((b[0], min(ys) - 0.42),
                                   b[1] - b[0], max(ys) - min(ys) + 0.84,
                                   facecolor=F.PALETTE[g], alpha=0.08,
                                   edgecolor="none", zorder=0))
    ax.axvline(1.0, color=F.MUTED, linewidth=1.0, linestyle="--")
    ax.set_yticks(ypos)
    ax.set_yticklabels(ylab, fontsize=8.5)
    ax.set_xlabel("class-A / class-B mean-time ratio (paired bootstrap 95% CI)")
    ax.set_xlim(0.78, 1.27)
    ax.set_title("All nine preregistered timing screens")
    labels = ["Python map screen (240 rounds)",
              "Python extended screen (160 rounds)",
              "Compiled screen (400 rounds)"]
    handles = [plt.Line2D([], [], color=F.PALETTE[g], marker="o",
                          linestyle="none", label=labels[g]) for g in range(3)]
    ax.legend(handles=handles, loc="lower left", fontsize=8)
    F.finish(fig, os.path.join(OUT, "timing.svg"))


def fig_compiled():
    """Per-round distributions of the compiled p=11 timing screen."""
    rows = read_csv("measure_compiled_timing_p11_s400_b1000_seed5409_20260720.csv")
    a = np.array([float(r["class_a_ns"]) / float(r["batch"]) for r in rows])
    b = np.array([float(r["class_b_ns"]) / float(r["batch"]) for r in rows])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9))
    bins = np.linspace(min(a.min(), b.min()), max(a.max(), b.max()), 34)
    ax1.hist(a, bins=bins, color=F.PALETTE[0], alpha=0.65,
             label="class A: $(u_0,u_1)=(0,0)$")
    ax1.hist(b, bins=bins, color=F.PALETTE[1], alpha=0.65,
             label="class B: $(u_0,u_1)=(1,2)$")
    ax1.set_xlabel("ns per pipeline call (batch mean)")
    ax1.set_ylabel("rounds")
    ax1.set_title("400 randomized-order rounds")
    ax1.legend(fontsize=8.2)
    d = a - b
    ax2.hist(d, bins=30, color=F.PALETTE[2], alpha=0.85)
    ax2.axvline(0.0, color=F.MUTED, linewidth=1.0, linestyle="--")
    ax2.axvline(d.mean(), color=F.PALETTE[7], linewidth=1.4)
    ax2.text(d.mean() + 1.2, ax2.get_ylim()[1] * 0.9,
             f"mean {d.mean():+.2f} ns", fontsize=8.5, color=F.PALETTE[7])
    ax2.set_xlabel("paired difference A $-$ B (ns per call)")
    ax2.set_title("Paired round differences")
    F.finish(fig, os.path.join(OUT, "compiled.svg"))


def fig_isogeny():
    """Exceptional-invariant quotients found by the exhaustive Velu search."""
    rows = read_csv("search_exceptional_isogenies_b100_20260712.csv")
    counts = defaultdict(lambda: [0, 0])  # p -> [j0, j1728]
    for r in rows:
        p = int(r["p"])
        idx = 0 if r["target_family"] == "j0" else 1
        counts[p][idx] += 1
    primes = sorted(counts)
    j0 = np.array([counts[p][0] for p in primes])
    j1728 = np.array([counts[p][1] for p in primes])
    x = np.arange(len(primes))
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.bar(x, j0, color=F.PALETTE[0], label="$j=0$ target", width=0.72)
    ax.bar(x, j1728, bottom=j0, color=F.PALETTE[1],
           label="$j=1728$ target", width=0.72)
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) for p in primes], fontsize=8)
    ax.set_xlabel("prime $p$")
    ax.set_ylabel("degree-3/5 quotient hits")
    ax.set_title(
        "Exceptional-invariant isogeny targets: 1,492 hits over "
        "62,664 curves, 45,166 kernels")
    ax.legend(loc="upper left", fontsize=9)
    total = int(j0.sum() + j1728.sum())
    assert total == 1492, total
    F.finish(fig, os.path.join(OUT, "isogeny.svg"))


if __name__ == "__main__":
    fig_pipeline()
    fig_coverage()
    fig_timing()
    fig_compiled()
    fig_isogeny()
    print("P5.4 figures written")
