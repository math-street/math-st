"""Figures for the P5.1 paper (Koblitz's conjecture on prime curve orders)."""
import csv
import os, sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                    "problems", "P5.1-koblitz-conjecture", "data")

DENSITY_CSV = os.path.join(DATA, "measure_density_x131072_l1000000_s51012026_20260624.csv")
CORRECTED_CSV = os.path.join(DATA, "measure_corrected_cases_x131072_l1000000_s51012026_20260713.csv")
CM_TABLE_CSV = os.path.join(DATA, "reproduce_cm_table_x1000000000_s51012026_20260720.csv")


def read_rows(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def fig_serre_convergence():
    """Serre curve 1728.w1: refined vs raw-asymptotic ratio across cutoffs."""
    rows = [r for r in read_rows(DENSITY_CSV) if r["curve_key"] == "serre_trivial"]
    x = np.array([int(r["cutoff"]) for r in rows])
    refined = np.array([float(r["measured_over_predicted"]) for r in rows])
    raw = np.array([float(r["observed_over_asymptotic"]) for r in rows])
    pred_const = float(rows[-1]["predicted_constant"])
    lo = np.array([float(r["constant_ci95_low"]) for r in rows]) / pred_const
    hi = np.array([float(r["constant_ci95_high"]) for r in rows]) / pred_const

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.fill_between(x, lo, hi, color=F.PALETTE[0], alpha=0.14, linewidth=0,
                    label="heuristic 95% band (Poisson)")
    ax.plot(x, refined, marker="o", color=F.PALETTE[0],
            label="refined prime-sum predictor")
    ax.plot(x, raw, marker="s", color=F.PALETTE[1],
            label=r"raw $C_{E,1}\,x/(\log x)^2$")
    ax.axhline(1.0, color=F.MUTED, lw=1.0, ls="--")
    ax.set_xscale("log", base=2)
    ax.set_xticks(x)
    ax.set_xticklabels([f"$2^{{{int(np.log2(v))}}}$" for v in x])
    ax.set_xlabel("cutoff $x$")
    ax.set_ylabel("observed / predicted")
    ax.set_title(r"$y^2=x^3+6x-2$: prime-order counts vs. two predictors")
    ax.set_ylim(0.6, 1.8)
    ax.legend(loc="upper right", fontsize=9)
    F.finish(fig, os.path.join(OUT, "serre_convergence.svg"))


def fig_corrected_ratios():
    """Certified quotient predictors vs the deliberately invalid pooled model."""
    rows = read_rows(CORRECTED_CSV)
    t3 = [r for r in rows if r["case_key"] == "torsion_3_quotient"]
    cm = [r for r in rows if r["case_key"] == "cm_qi_split_t8"]
    x3 = np.array([int(r["cutoff"]) for r in t3])
    r3 = np.array([float(r["observed_over_predicted"]) for r in t3])
    xc = np.array([int(r["cutoff"]) for r in cm])
    rc = np.array([float(r["observed_over_predicted"]) for r in cm])
    rp = np.array([float(r["invalid_pool_observed_over_predicted"]) for r in cm])

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(x3, r3, marker="o", color=F.PALETTE[0],
            label=r"540.f2, $t=3$, certified $C_{E,3}$")
    ax.plot(xc, rc, marker="s", color=F.PALETTE[1],
            label=r"$y^2=x^3-x$, $t=8$, split primes, CM constant")
    ax.plot(xc, rp, marker="^", color=F.PALETTE[7], ls=":",
            label=r"invalid pooled full-$\mathrm{GL}_2$ control")
    ax.axhline(1.0, color=F.MUTED, lw=1.0, ls="--")
    ax.set_xscale("log", base=2)
    ax.set_xticks(x3)
    ax.set_xticklabels([f"$2^{{{int(np.log2(v))}}}$" for v in x3])
    ax.set_xlabel("cutoff $x$")
    ax.set_ylabel("observed / predicted")
    ax.set_title("Certified quotient constants track the data; the pooled model fails")
    ax.set_ylim(0.0, 4.5)
    ax.legend(loc="center left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "corrected_ratios.svg"))


def fig_cm_table():
    """Exact reproduction of Zywina's CM table through 10^9."""
    rows = read_rows(CM_TABLE_CSV)
    x = np.array([int(r["cutoff"]) for r in rows])
    observed = np.array([int(r["quotient_prime_count"]) for r in rows])
    predicted = np.array([float(r["integral_predicted_count"]) for r in rows])
    ratio = np.array([float(r["observed_over_integral_predicted"]) for r in rows])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax1.plot(x / 1e8, predicted / 1e3, color=F.PALETTE[1], lw=1.6,
             label="integral prediction (eq. 7.1)")
    ax1.plot(x / 1e8, observed / 1e3, marker="o", ms=3.2, lw=0,
             color=F.PALETTE[0], label="exact count")
    ax1.set_xlabel(r"cutoff $x$  ($\times 10^8$)")
    ax1.set_ylabel("prime-quotient events ($\\times 10^3$)")
    ax1.set_title("Counts, 50 checkpoints")
    ax1.legend(loc="upper left", fontsize=8.8)

    ax2.plot(x / 1e8, ratio, marker="o", ms=3.2, color=F.PALETTE[0])
    ax2.axhline(1.0, color=F.MUTED, lw=1.0, ls="--")
    ax2.set_xlabel(r"cutoff $x$  ($\times 10^8$)")
    ax2.set_ylabel("observed / predicted")
    ax2.set_title("Ratio at every checkpoint")
    ax2.set_ylim(0.9950, 1.0010)
    F.finish(fig, os.path.join(OUT, "cm_table.svg"))


def fig_constants():
    """Predicted constants vs measured constants with heuristic intervals."""
    density = read_rows(DENSITY_CSV)
    corrected = read_rows(CORRECTED_CSV)
    serre = [r for r in density if r["curve_key"] == "serre_trivial"][-1]
    t3 = [r for r in corrected if r["case_key"] == "torsion_3_quotient"][-1]
    cm = [r for r in corrected if r["case_key"] == "cm_qi_split_t8"][-1]

    labels = [r"1728.w1, $t=1$", r"540.f2, $t=3$", r"$y^2=x^3-x$, $t=8$"]
    predicted = [float(serre["predicted_constant"]),
                 float(t3["predicted_constant"]),
                 float(cm["predicted_constant"])]
    measured = [float(serre["measured_constant"]),
                float(t3["measured_constant"]),
                float(cm["measured_constant"])]
    lo = [float(serre["constant_ci95_low"]), float(t3["constant_ci95_low"]),
          float(cm["constant_ci95_low"])]
    hi = [float(serre["constant_ci95_high"]), float(t3["constant_ci95_high"]),
          float(cm["constant_ci95_high"])]

    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.axvline(0.505166168239435774, color=F.MUTED, lw=1.0, ls="--")
    ax.text(0.517, 1.5, "universal product $C$", color=F.MUTED, fontsize=9,
            ha="left", va="center")
    ax.errorbar(measured, y,
                xerr=[np.array(measured) - np.array(lo),
                      np.array(hi) - np.array(measured)],
                fmt="o", color=F.PALETTE[0], ecolor=F.PALETTE[0],
                elinewidth=1.6, capsize=4, ms=6,
                label=r"measured constant at $x=2^{17}$ (95% heuristic)")
    ax.plot(predicted, y, marker="D", ms=6.5, lw=0, mfc="none", mew=1.6,
            mec=F.PALETTE[7], label="certified predicted constant")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xlabel(r"constant $C_{E,t}$")
    ax.set_title("Certified constants vs. measured constants")
    ax.set_xlim(0.35, 1.25)
    ax.legend(loc="upper right", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "constants.svg"))


if __name__ == "__main__":
    fig_serre_convergence()
    fig_corrected_ratios()
    fig_cm_table()
    fig_constants()
    print("P5.1 figures written")
