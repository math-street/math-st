"""Figures for the P2.4 paper (fixed-argument pairing inversion)."""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "problems", "P2.4-pairing-inversion", "data"))


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


STAGES = rows("measure_pairing_stages_p43-59-83-103-131-163_20260624.csv")
MILLER = rows("analyze_miller_function_p43_r11_20260624.csv")
SATOH = rows("reproduce_satoh_mi_p43-59-83-103-131-163_20260627.csv")
BOUND = rows("verify_generic_oracle_bound_p5-7-11_t4_20260702.csv")


def fig_stages():
    """Stage inversion timings across the six toy curves (log scale)."""
    labels = [f"$p={r['p']}$\n$r={r['subgroup_order_r']}$" for r in STAGES]
    dlog = np.array([float(r["final_target_dlog_mean_ns"]) for r in STAGES]) / 1e3
    dlog_ci = np.array([float(r["final_target_dlog_ci95_halfwidth_ns"]) for r in STAGES]) / 1e3
    mill = np.array([float(r["miller_inverse_mean_ns"]) for r in STAGES]) / 1e3
    mill_ci = np.array([float(r["miller_inverse_ci95_halfwidth_ns"]) for r in STAGES]) / 1e3
    pair = np.array([float(r["pairing_inverse_mean_ns"]) for r in STAGES]) / 1e3
    pair_ci = np.array([float(r["pairing_inverse_ci95_halfwidth_ns"]) for r in STAGES]) / 1e3

    x = np.arange(len(labels))
    w = 0.27
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    ax.bar(x - w, dlog, w, yerr=dlog_ci, capsize=2,
           label="final-exp. root via target-subgroup DLP",
           color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=0.8)
    ax.bar(x, mill, w, yerr=mill_ci, capsize=2,
           label="naive raw Miller inversion",
           color=F.PALETTE[1], edgecolor=F.SURFACE, linewidth=0.8)
    ax.bar(x + w, pair, w, yerr=pair_ci, capsize=2,
           label="composed pairing inversion",
           color=F.PALETTE[2], edgecolor=F.SURFACE, linewidth=0.8)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel(r"mean time per target ($\mu$s, log)")
    ax.set_title("Measured inversion cost of the two pairing stages (50 seeded trials each)")
    ax.legend(loc="upper left", fontsize=8.8)
    for xi, (lo, hi) in zip(x, zip(dlog, mill)):
        ax.annotate(f"$\\times{hi / lo:.0f}$", (xi, hi * 1.9),
                    ha="center", fontsize=8.2, color=F.INK_SECOND)
    ax.set_ylim(top=max(pair) * 12)
    F.finish(fig, os.path.join(OUT, "stages.svg"))


def fig_degrees():
    """Fixed-argument Miller factor-degree growth (r-2, r-3) vs measured rows."""
    gen = [r for r in MILLER if r["row_type"] == "generic_degree_growth"]
    rs = np.array([int(r["order_r"]) for r in gen])
    num = np.array([int(r["numerator_factor_degree"]) for r in gen])
    den = np.array([int(r["denominator_factor_degree"]) for r in gen])
    line = np.linspace(3, 41, 50)
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    ax.plot(line, line - 2, ls="--", lw=1.3, color=F.PALETTE[0],
            label="proved $r-2$ (numerator lines)")
    ax.plot(line, line - 3, ls="--", lw=1.3, color=F.PALETTE[1],
            label="proved $r-3$ (denominator verticals)")
    ax.plot(rs, num, "o", ms=6.5, color=F.PALETTE[0],
            label="binary-loop count, numerator")
    ax.plot(rs, den, "s", ms=6, color=F.PALETTE[1],
            label="binary-loop count, denominator")
    ax.plot([11], [9], "o", ms=13, mfc="none", mec=F.PALETTE[7], mew=1.6)
    ax.annotate("exact $p=43$, $r=11$ expansion\n(degrees $9/8$; "
                "$\\deg A=13$, $\\deg B=12$)",
                (11, 9), xytext=(14, 2.5), fontsize=8.8, color=F.INK_SECOND,
                arrowprops=dict(arrowstyle="-", color=F.MUTED, lw=0.8))
    ax.set_xlabel("odd subgroup order $r$")
    ax.set_ylabel("affine line / vertical factors")
    ax.set_title("Fixed-argument Miller factor counts after final cancellation")
    ax.legend(loc="upper left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "miller_degrees.svg"))


def fig_satoh():
    """Naive Miller-inversion scan vs the transferred Satoh inverse."""
    labels = [f"$p={r['p']}$\n$r={r['subgroup_order_r']}$" for r in SATOH]
    naive = np.array([float(r["miller_inverse_mean_ns"]) for r in STAGES]) / 1e6
    naive_ci = np.array([float(r["miller_inverse_ci95_halfwidth_ns"]) for r in STAGES]) / 1e6
    satoh = np.array([float(r["raw_mi_mean_ns"]) for r in SATOH]) / 1e6
    satoh_ci = np.array([float(r["raw_mi_ci95_halfwidth_ns"]) for r in SATOH]) / 1e6
    cand = [float(r["raw_mi_mean_candidates"]) for r in SATOH]

    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.bar(x - w / 2, naive, w, yerr=naive_ci, capsize=2,
           label="naive scan over the cyclic domain",
           color=F.PALETTE[1], edgecolor=F.SURFACE, linewidth=0.8)
    ax.bar(x + w / 2, satoh, w, yerr=satoh_ci, capsize=2,
           label="transferred Satoh inverse ($\\leq 4$ candidates)",
           color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=0.8)
    for xi, (s, c) in enumerate(zip(satoh, cand)):
        ax.annotate(f"{c:.1f}", (xi + w / 2, s + 1.2), ha="center",
                    fontsize=8.2, color=F.INK_SECOND)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("mean time per raw target (ms)")
    ax.set_title("Raw Miller inversion: scan vs distortion-transferred Satoh algorithm")
    ax.legend(loc="upper left", fontsize=9)
    F.finish(fig, os.path.join(OUT, "satoh.svg"))


def fig_bound():
    """Exhaustive affine-collision audit vs the proved union bound."""
    labels = [f"$p={r['p']}$\n$t={r['handles_t']}$" for r in BOUND]
    bound = np.array([min(int(r["field_size_bound"]), int(r["pair_union_bound"]))
                      for r in BOUND])
    seen = np.array([int(r["maximum_bad_challenges"]) for r in BOUND])
    mean = np.array([float(r["mean_bad_challenges"]) for r in BOUND])
    sampled = [r["mode"] != "exhaustive" for r in BOUND]

    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    ax.bar(x - w / 2, bound, w, label="proved bound $\\min(p,\\binom{t}{2})$",
           color=F.SEQ[2], edgecolor=F.SURFACE, linewidth=0.8)
    ax.bar(x + w / 2, seen, w, label="maximum bad set observed",
           color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=0.8)
    ax.plot(x + w / 2, mean, "o", ms=5, color=F.PALETTE[1],
            label="mean bad-set size", zorder=5)
    for xi, flag in zip(x, sampled):
        if flag:
            ax.text(xi, max(bound) + 0.3, "seeded\nsample", ha="center",
                    va="bottom", fontsize=8.0, color=F.MUTED)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("informative challenges $|R_F|$")
    ax.set_title("Collision core of the oracle bound: 541,966 exact sets, zero violations")
    ax.set_ylim(0, max(bound) + 1.6)
    ax.legend(loc="upper left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "oracle_bound.svg"))


if __name__ == "__main__":
    fig_stages()
    fig_degrees()
    fig_satoh()
    fig_bound()
    print("P2.4 figures written")
