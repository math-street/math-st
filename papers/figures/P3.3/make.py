"""Figures for the P3.3 paper (ideal-to-isogeny translation norm gaps)."""
import csv
import os, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..",
                    "problems", "P3.3-ideal-to-isogeny-norms", "data")

NORMGAP_RAW = os.path.join(
    DATA, "measure_norm_gap_p2203-245000047x18_t6_s33032028_enearp_20260701_raw.csv")
SHAPE_SUMMARY = os.path.join(
    DATA, "measure_shape_gap_p7-223x14_t5_m16_b5_s33032030_20260713_summary.csv")
POWER_RAW = os.path.join(
    DATA, "measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713_raw.csv")
POWER_SUMMARY = os.path.join(
    DATA, "measure_power_targets_p2203-245000047x18_t6_m4_s33032028_20260713_summary.csv")


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def fig_normgap():
    """Unconstrained exact equivalent-ideal norms across the 12/20/28-bit bands."""
    rows = read_rows(NORMGAP_RAW)
    p = np.array([int(r["p"]) for r in rows])
    expo = np.array([float(r["exact_log_p_norm"]) for r in rows])
    ratio = np.array([float(r["exact_norm_over_sqrt_p"]) for r in rows])
    bits = np.array([int(r["p_bits"]) for r in rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.1))

    ax1.scatter(p, expo, s=18, color=F.PALETTE[0], alpha=0.55, linewidths=0)
    for band in (12, 20, 28):
        mask = bits == band
        lo, hi = p[mask].min(), p[mask].max()
        mean = expo[mask].mean()
        ax1.hlines(mean, lo, hi, color=F.PALETTE[7], lw=2.2, zorder=5)
    ax1.axhline(0.5, color=F.MUTED, lw=1.1, ls="--")
    ax1.text(2400, 0.512, r"Minkowski target $\log_p N(J)=1/2$",
             color=F.MUTED, fontsize=8.6)
    ax1.set_xscale("log")
    ax1.set_xlabel(r"quaternion prime $p$ (log scale)")
    ax1.set_ylabel(r"$\log_p N(J)$")
    ax1.set_ylim(0.05, 0.58)
    ax1.set_title("Exact exponent (band means in red)", fontsize=11)

    ax2.scatter(p, ratio, s=18, color=F.PALETTE[2], alpha=0.55, linewidths=0)
    med = np.median(ratio)
    ax2.axhline(med, color=F.PALETTE[7], lw=1.6)
    ax2.text(2400, med + 0.02, f"median {med:.5f}", color=F.PALETTE[7], fontsize=8.6)
    ax2.axhline(1.0, color=F.MUTED, lw=1.1, ls="--")
    ax2.text(2400, 1.02, r"$N(J)=\sqrt{p}$", color=F.MUTED, fontsize=8.6)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"quaternion prime $p$ (log scale)")
    ax2.set_ylabel(r"$N(J)/\sqrt{p}$")
    ax2.set_ylim(0, 1.12)
    ax2.set_title("Normalized ratio (108 rows, LLL = exact on all)", fontsize=11)

    F.finish(fig, os.path.join(OUT, "normgap.svg"))


def fig_shapegap():
    """Small-p exact spectrum: mean exponent per prime for each norm shape."""
    rows = [r for r in read_rows(SHAPE_SUMMARY) if r["group_family"] == "p"]
    rows.sort(key=lambda r: int(r["group_value"]))
    p = np.array([int(r["group_value"]) for r in rows])
    series = [
        ("unconstrained", "unconstrained_log_p_norm_mean", F.PALETTE[0], "o"),
        (r"power of 2",   "power2_log_p_norm_mean",        F.PALETTE[1], "s"),
        (r"power of 3",   "power3_log_p_norm_mean",        F.PALETTE[6], "^"),
        (r"5-smooth",     "smooth_log_p_norm_mean",        F.PALETTE[2], "D"),
    ]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for label, key, color, marker in series:
        y = np.array([float(r[key]) for r in rows])
        ax.plot(p, y, color=color, marker=marker, ms=4.5, lw=1.8, label=label)
    ax.axhline(0.5, color=F.MUTED, lw=1.1, ls="--")
    ax.text(7.2, 0.515, r"$\log_p N(J) = 1/2$", color=F.MUTED, fontsize=8.6)
    ax.set_xscale("log")
    ax.set_xticks([7, 11, 19, 31, 59, 103, 151, 223])
    ax.set_xticklabels(["7", "11", "19", "31", "59", "103", "151", "223"])
    ax.set_xlabel(r"quaternion prime $p$")
    ax.set_ylabel(r"mean $\log_p N(J)$ over 5 ideals")
    ax.set_ylim(-0.03, 0.75)
    ax.set_title("Exact spectrum through cutoff $p$: shape costs at small $p$",
                 fontsize=11.5)
    ax.legend(loc="upper left", ncol=2, fontsize=9)
    F.finish(fig, os.path.join(OUT, "shapegap.svg"))


def fig_powertargets():
    """Exact sparse pure-power optima vs the unconstrained optimum, 12-28 bits."""
    rows = read_rows(POWER_RAW)
    p = np.array([int(r["p"]) for r in rows])
    unc = np.array([float(r["unconstrained_log_p_norm"]) for r in rows])
    pw2 = np.array([float(r["power2_log_p_norm"]) for r in rows])
    pw3 = np.array([float(r["power3_log_p_norm"]) for r in rows])
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.scatter(p, unc, s=16, color=F.PALETTE[0], alpha=0.5, linewidths=0,
               label="unconstrained exact SVP")
    ax.scatter(p, pw2, s=18, color=F.PALETTE[1], alpha=0.6, linewidths=0,
               marker="s", label=r"least $2^e$ norm")
    ax.scatter(p, pw3, s=20, color=F.PALETTE[6], alpha=0.6, linewidths=0,
               marker="^", label=r"least $3^e$ norm")
    ax.axhline(0.5, color=F.MUTED, lw=1.1, ls="--")
    ax.axhline(1.0, color=F.MUTED, lw=1.1, ls=":")
    ax.text(2400, 0.512, r"$\log_p N(J)=1/2$", color=F.MUTED, fontsize=8.6)
    ax.text(2400, 1.012, r"$\log_p N(J)=1$", color=F.MUTED, fontsize=8.6)
    ax.set_xscale("log")
    ax.set_xlabel(r"quaternion prime $p$ (log scale)")
    ax.set_ylabel(r"$\log_p N(J)$")
    ax.set_ylim(0, 1.1)
    ax.set_title("Exact shaped optima stay below exponent 1.013 (108 ideals)",
                 fontsize=11.5)
    ax.legend(loc="lower right", fontsize=9)
    F.finish(fig, os.path.join(OUT, "powertargets.svg"))


def fig_penalty():
    """Median pure-power penalty over unconstrained SVP per bit band."""
    rows = [r for r in read_rows(POWER_SUMMARY) if r["group_family"] == "p_bits"]
    rows.sort(key=lambda r: int(r["group_value"]))
    bands = [r["group_value"] for r in rows]
    med2 = [float(r["power2_over_unconstrained_median"]) for r in rows]
    med3 = [float(r["power3_over_unconstrained_median"]) for r in rows]
    x = np.arange(len(bands))
    w = 0.36
    fig, ax = plt.subplots(figsize=(5.6, 3.3))
    b1 = ax.bar(x - w / 2, med2, w, label=r"$2^e$ constraint",
                color=F.PALETTE[1], edgecolor=F.SURFACE, linewidth=1.2)
    b2 = ax.bar(x + w / 2, med3, w, label=r"$3^e$ constraint",
                color=F.PALETTE[6], edgecolor=F.SURFACE, linewidth=1.2)
    for bars in (b1, b2):
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8.6,
                     color=F.INK_SECOND)
    ax.set_yscale("log")
    ax.set_ylim(1, 3e4)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{b}-bit $p$" for b in bands])
    ax.set_ylabel("median penalty over exact SVP (log)")
    ax.set_title("Pure-power shape penalty grows with the band", fontsize=11.5)
    ax.legend(loc="upper left", fontsize=9)
    F.finish(fig, os.path.join(OUT, "penalty.svg"))


if __name__ == "__main__":
    fig_normgap()
    fig_shapegap()
    fig_powertargets()
    fig_penalty()
    print("P3.3 figures written")
