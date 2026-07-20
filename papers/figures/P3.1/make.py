"""Figures for the P3.1 paper (GRH usage map / unconditional quaternary sampler)."""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P3.1-endomorphism-ring-equivalence", "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- GRH map ---
def fig_grh_map():
    """Dependency schematic of the four GRH leaves D1-D4 (plus removable D5)
    through Wesolowski 2022, following GRH_USAGE_MAP.md."""
    fig, ax = plt.subplots(figsize=(7.6, 4.9))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-0.4, 10.4)
    ax.axis("off")
    ax.grid(False)

    def box(x, y, text, fc, ec, tc=F.INK, fs=8.0, w=2.0, h=0.86, lw=1.1,
            style="round,pad=0.14", alpha=1.0):
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc,
                zorder=3, alpha=alpha,
                bbox=dict(boxstyle=style, facecolor=fc, edgecolor=ec,
                          linewidth=lw, alpha=alpha))
        return (x, y)

    def arrow(a, b, color=F.MUTED, ls="-", lw=1.2, alpha=0.95, shrink=16):
        ax.annotate("", xy=b, xytext=a, zorder=2,
                    arrowprops=dict(arrowstyle="-|>", color=color, ls=ls,
                                    lw=lw, alpha=alpha,
                                    shrinkA=shrink, shrinkB=shrink))

    ORANGE = F.PALETTE[1]; BLUE = F.PALETTE[0]; AQUA = F.PALETTE[2]
    VIOLET = F.PALETTE[6]
    leafc = "#fdece3"; midc = "#e8f1fb"; corec = "#dcE9f9"; finc = "#ece8f8"

    # column 1: analytic leaves
    d1 = box(1.15, 9.0, "D1\nsmall Frobenius\nprime $q_p$", leafc, ORANGE)
    d2 = box(1.15, 6.9, "D2\nfixed-form\nprime density", leafc, ORANGE)
    d3 = box(1.15, 4.6, "D3\nlarge-modulus\nTitchmarsh", leafc, ORANGE)
    d4 = box(1.15, 2.5, "D4\npolylog class\nexpansion", leafc, ORANGE)
    d5 = box(1.15, 0.5, "D5 (RH)\nremovable: PNT", "#f4f3ee", F.MUTED,
             tc=F.INK_SECOND, alpha=0.9)

    # column 2: first consumers
    l2 = box(3.85, 9.0, "Lem. 2.2--2.6\nspecial order,\ncurve + dictionary",
             midc, BLUE)
    t3 = box(3.85, 6.9, "Thm. 3.1 $\\to$ Prop. 3.8\nprime-norm\nequivalent ideal",
             midc, BLUE)
    t4 = box(3.85, 4.6, "Thm. 4.4 $\\to$ Cor. 4.3\nuniform repr.\ncounts", midc, BLUE)
    l5 = box(3.85, 2.5, "Lem. 5.3 / 5.4\nclass\nrandomization", midc, BLUE)
    a3 = box(3.85, 0.5, "A003 rank-4 sampler\n(unconditional, this audit)",
             "#e2f5ec", AQUA, fs=8.0)

    # column 3: quaternion core
    t51 = box(6.55, 3.4, "Thm. 5.1\nnorm equation", corec, BLUE)
    c58 = box(6.55, 5.3, "Cor. 5.8\nprescribed norms", corec, BLUE)
    t63 = box(6.55, 7.2, "Thm. 6.3\nEquivIdeal", corec, BLUE)
    t64 = box(6.55, 9.2, "Thm. 6.4\npowersmooth ideal", corec, BLUE)

    # column 4: final equivalences
    f72 = box(9.35, 8.9, "Thm. 7.2\nMaxOrder $\\leq$ Path", finc, VIOLET)
    f74 = box(9.35, 6.7, "Thm. 7.4\nPath $\\leq$ MaxOrder", finc, VIOLET)
    f81 = box(9.35, 4.5, "Thm. 8.1\nEndRing $\\leq$ MaxOrder", finc, VIOLET)
    f83 = box(9.35, 2.3, "Thm. 8.3\nMaxOrder $\\leq$ EndRing", finc, VIOLET)

    arrow(d1, l2, color=ORANGE)
    arrow(d2, t3, color=ORANGE, ls=":", alpha=0.7)   # bypassed by A003
    arrow(d3, t4, color=ORANGE)
    arrow(d4, l5, color=ORANGE)
    arrow(d5, (5.6, 8.9), color=F.MUTED, ls=":", alpha=0.6, shrink=18)

    arrow(t4, t51); arrow(l5, t51)
    arrow(l2, c58); arrow(t51, c58)
    arrow(t3, t63, ls=":", alpha=0.6)                # replaced route
    arrow(a3, t63, color=AQUA, lw=1.6)               # unconditional replacement
    arrow(c58, t63); arrow(t51, t63)
    arrow(t63, t64)
    arrow(t64, f72); arrow(t64, f81)
    arrow(t63, f74); arrow(t64, f74)
    arrow(t3, f83, ls=":", alpha=0.6); arrow(l2, f83)

    ax.set_title("GRH dependency closure of Wesolowski 2022 (audit A001);"
                 " dotted D2 route bypassed by A003", fontsize=10)
    F.finish(fig, os.path.join(OUT, "grh_map.svg"))


# ------------------------------------------------------------ sampler grid --
def fig_sampler_grid():
    """22-case refutation grid: scaled prime density and progression coverage
    from measure_quaternary_prime_sampler_p31_ells3-5_x3000_20260711.csv."""
    rows = read_csv("measure_quaternary_prime_sampler_p31_ells3-5_x3000_20260711.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.2))

    def jitter(p, ell, maximal):
        base = -0.55 if ell == 3 else 0.55
        return p + base + (0.0 if maximal else 0.28)

    seen = set()
    for r in rows:
        p, ell = int(r["p"]), int(r["ell"])
        maximal = r["ideal"] == "maximal_order"
        dens = float(r["prime_probability_times_log_cutoff"])
        cov = float(r["progression_coverage"])
        color = F.PALETTE[0] if ell == 3 else F.PALETTE[1]
        marker = "o" if maximal else "D"
        key = (ell, maximal)
        label = None
        if key not in seen:
            seen.add(key)
            kind = "maximal order" if maximal else "prime ideal"
            label = f"$\\ell={ell}$, {kind}"
        x = jitter(p, ell, maximal)
        ax1.scatter(x, dens, s=34, color=color, marker=marker, label=label,
                    edgecolor=F.SURFACE, linewidth=0.7, zorder=3)
        ax2.scatter(x, cov, s=34, color=color, marker=marker,
                    edgecolor=F.SURFACE, linewidth=0.7, zorder=3)

    mean = np.mean([float(r["prime_probability_times_log_cutoff"]) for r in rows])
    ax1.axhline(1.0, color=F.MUTED, lw=1.0, ls=":")
    ax1.axhline(mean, color=F.PALETTE[2], lw=1.3, ls="--")
    ax1.text(31.6, mean + 0.04, f"mean {mean:.3f}", color=F.PALETTE[2],
             fontsize=8.5, ha="right")
    ax1.set_xlabel("characteristic $p$")
    ax1.set_ylabel(r"$\Pr[Q_\Lambda(v)\ \mathrm{prime}]\cdot\log X$")
    ax1.set_title("Scaled prime density (22 cases)", fontsize=10.5)
    ax1.set_ylim(0, 2.0)
    ax1.legend(fontsize=7.6, loc="lower left", ncol=2, handletextpad=0.2,
               columnspacing=0.7)

    ax2.set_xlabel("characteristic $p$")
    ax2.set_ylabel("admissible-progression coverage")
    ax2.set_ylim(0, 1.0)
    ax2.set_title("Coverage below the crossover", fontsize=10.5)

    for ax in (ax1, ax2):
        ax.set_xticks([3, 7, 11, 19, 23, 31])
    F.finish(fig, os.path.join(OUT, "sampler_grid.svg"))


# ---------------------------------------------------------- cutoff scaling --
def fig_sampler_cutoff():
    """Approach of the scaled prime density toward ~1 as the cutoff X grows,
    from the five measure_quaternary_prime_sampler_p11_ells3_x*.csv files."""
    cutoffs = [250, 500, 1000, 2000, 4000]
    series = {}   # (p, ideal) -> list over cutoffs
    cov = {}
    for X in cutoffs:
        for r in read_csv(f"measure_quaternary_prime_sampler_p11_ells3_x{X}_20260711.csv"):
            key = (int(r["p"]), r["ideal"])
            series.setdefault(key, []).append(
                float(r["prime_probability_times_log_cutoff"]))
            cov.setdefault(key, []).append(float(r["progression_coverage"]))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.1))
    styles = {
        (7, "maximal_order"): (F.PALETTE[0], "-", "o", "$p=7$, maximal order"),
        (7, "prime_ideal_5_trial_0"): (F.PALETTE[0], "--", "D", "$p=7$, norm-5 ideal"),
        (11, "maximal_order"): (F.PALETTE[1], "-", "o", "$p=11$, maximal order"),
        (11, "prime_ideal_5_trial_0"): (F.PALETTE[1], "--", "D", "$p=11$, norm-5 ideal"),
    }
    for key, (c, ls, mk, lab) in styles.items():
        ax1.plot(cutoffs, series[key], color=c, ls=ls, marker=mk, ms=5,
                 lw=1.7, label=lab)
        ax2.plot(cutoffs, cov[key], color=c, ls=ls, marker=mk, ms=5, lw=1.7)
    ax1.axhline(1.0, color=F.MUTED, lw=1.0, ls=":")
    from matplotlib.ticker import NullLocator
    for ax in (ax1, ax2):
        ax.set_xscale("log")
        ax.set_xticks(cutoffs)
        ax.set_xticklabels([str(c) for c in cutoffs])
        ax.xaxis.set_minor_locator(NullLocator())
    ax1.set_xlabel("ellipsoid cutoff $X$")
    ax2.set_xlabel("ellipsoid cutoff $X$")
    ax1.set_ylabel(r"$\Pr[Q_\Lambda(v)\ \mathrm{prime}]\cdot\log X$")
    ax2.set_ylabel("admissible-progression coverage")
    ax1.set_ylim(0, 2.0); ax2.set_ylim(0, 1.0)
    ax1.set_title(r"Scaled density approaches $\approx 1$", fontsize=10.5)
    ax2.set_title("Coverage rises with the cutoff", fontsize=10.5)
    ax1.legend(fontsize=7.8, loc="lower left")
    F.finish(fig, os.path.join(OUT, "sampler_cutoff.svg"))


# ------------------------------------------------------------- cost fit -----
def fig_roundtrip_fit():
    """Toy Deuring round-trip timing power-law fit and residuals from
    fit_roundtrip_cost_ell3_p11-71_20260711.csv."""
    rows = read_csv("fit_roundtrip_cost_ell3_p11-71_20260711.csv")
    ps = np.array([float(r["p"]) for r in rows])
    obs = np.array([float(r["observed_seconds_per_trial"]) for r in rows])
    logres = np.array([float(r["residual_log_seconds"]) for r in rows])
    expo = float(rows[0]["fit_exponent"])
    pref = float(rows[0]["fit_prefactor"])
    r2 = float(rows[0]["fit_r_squared"])
    lo = float(rows[0]["exponent_ci_low_95"])
    hi = float(rows[0]["exponent_ci_high_95"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.2),
                                   gridspec_kw={"width_ratios": [1.5, 1]})
    grid = np.geomspace(9, 90, 120)
    ax1.plot(grid, pref * grid**expo, color=F.PALETTE[0], lw=1.8,
             label=f"fit $T=%.4f\\,p^{{%.3f}}$ s" % (pref, expo))
    ax1.fill_between(grid, pref * grid**lo, pref * grid**hi,
                     color=F.PALETTE[0], alpha=0.12, linewidth=0,
                     label=f"exponent 95% CI [{lo:.3f}, {hi:.3f}]")
    ax1.scatter(ps, obs, s=42, color=F.PALETTE[1], zorder=3,
                edgecolor=F.SURFACE, linewidth=0.8, label="observed (1 trial per $p$)")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xticks([11, 23, 47, 59, 71])
    ax1.set_xticklabels(["11", "23", "47", "59", "71"])
    ax1.set_xlabel("characteristic $p$")
    ax1.set_ylabel("seconds per round trip")
    ax1.set_title(f"Exhaustive toy round trip, $R^2={r2:.4f}$", fontsize=10.5)
    ax1.legend(fontsize=7.8, loc="upper left")

    ax2.bar([str(int(p)) for p in ps], logres, color=F.PALETTE[4],
            edgecolor=F.SURFACE, linewidth=0.8, width=0.62)
    ax2.axhline(0, color=F.AXIS, lw=0.9)
    ax2.set_xlabel("characteristic $p$")
    ax2.set_ylabel("log residual")
    ax2.set_title("Stored fit residuals", fontsize=10.5)
    F.finish(fig, os.path.join(OUT, "roundtrip_fit.svg"))


if __name__ == "__main__":
    fig_grh_map()
    fig_sampler_grid()
    fig_sampler_cutoff()
    fig_roundtrip_fit()
    print("P3.1 figures written")
