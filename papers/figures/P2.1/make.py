"""Figures for the P2.1 paper (uniform Maurer reduction: partial results).

Every figure is generated from the recorded CSVs under
problems/P2.1-maurer-reduction/data/ -- no synthetic numbers.
"""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "problems", "P2.1-maurer-reduction", "data"))


def rows(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_smoothness():
    """Blind-search success probability vs bit size, against the exact
    Hasse-interval integer baseline and the Dickman heuristic.
    Source: measure_smooth_orders ... _summary.csv (512 curves/prime)."""
    data = rows("measure_smooth_orders_b12-16-20-24-28-32-36-40_t512"
                "_e2-3_s21012026_20260629_summary.csv")
    fig, ax = plt.subplots(figsize=(5.9, 3.5))
    for exp, col, lbl in ((2, F.PALETTE[0], "$B=L^2$"),
                          (3, F.PALETTE[1], "$B=L^3$")):
        sel = [r for r in data if int(r["smoothness_exponent"]) == exp]
        bits = np.array([int(r["bits"]) for r in sel])
        rate = np.array([float(r["curve_rate"]) for r in sel])
        lo = rate - np.array([float(r["wilson_95_low"]) for r in sel])
        hi = np.array([float(r["wilson_95_high"]) for r in sel]) - rate
        base = np.array([float(r["integer_rate"]) for r in sel])
        dick = np.array([float(r["dickman_rho"]) for r in sel])
        ax.errorbar(bits, rate, yerr=[lo, hi], fmt="o-", color=col,
                    capsize=2.5, markersize=4.5, lw=1.8,
                    label=f"curves, {lbl} (Wilson 95%)")
        ax.plot(bits, base, "--", color=col, lw=1.4,
                label=f"exact interval rate, {lbl}")
        ax.plot(bits, dick, ":", color=col, lw=1.1, alpha=0.7)
    ax.set_yscale("log")
    ax.set_xlabel("bit length of the prime $r$")
    ax.set_ylabel("$B$-smooth success probability")
    ax.set_title("Blind curve sampling vs the integer baseline")
    ax.legend(fontsize=8.6, loc="lower left")
    F.finish(fig, os.path.join(OUT, "smoothness.svg"))


def fig_budgets():
    """Exact iid-oracle query budgets for 50% and 95% success.
    Source: random_order_lower_bound_*_e{2,3}_20260629.csv."""
    fig, ax = plt.subplots(figsize=(5.7, 3.3))
    for suff, col, lbl in (("e2", F.PALETTE[0], "$B=L^2$"),
                           ("e3", F.PALETTE[1], "$B=L^3$")):
        data = rows(f"random_order_lower_bound_b12-16-20-24-28-32-36-40"
                    f"_{suff}_20260629.csv")
        bits = np.array([int(r["bits"]) for r in data])
        q50 = np.array([int(r["queries_50_percent"]) for r in data])
        q95 = np.array([int(r["queries_95_percent"]) for r in data])
        ax.plot(bits, q95, "s--", color=col, markersize=4.4, lw=1.5,
                label=f"{lbl}: 95% budget")
        ax.plot(bits, q50, "o-", color=col, markersize=4.6, lw=1.8,
                label=f"{lbl}: 50% budget")
    ax.set_yscale("log")
    ax.set_xlabel("bit length of the prime $r$")
    ax.set_ylabel("least query budget $q_\\delta$")
    ax.set_title("Optimal adaptive budgets in the iid Hasse-order oracle")
    ax.legend(fontsize=8.8, loc="upper left")
    F.finish(fig, os.path.join(OUT, "budgets.svg"))


def fig_cm():
    """CM-reachable smooth-order coverage vs bit size, 12--60 bits.
    Sources: measure_cm_coverage p32 (12-40 bits) and p128 (44-60 bits)
    summary CSVs, discriminant bound L^3."""
    data = (rows("measure_cm_coverage_b12-16-20-24-28-32-36-40"
                 "_p32_e2-3_d3_20260625_summary.csv")
            + rows("measure_cm_coverage_b44-48-52-56-60"
                   "_p128_e2-3_d3_20260625_summary.csv"))
    series = (
        (3, "bounded_cm", F.PALETTE[0], "o-",
         r"bounded CM, $B=|D|_{\max}=L^3$"),
        (2, "bounded_cm", F.PALETTE[1], "s-",
         r"bounded CM, $B=L^2$, $|D|\leq L^3$"),
        (3, "explicit", F.PALETTE[2], "d-",
         r"explicit $j=0,1728$ families, $B=L^3$"),
    )
    fig, ax = plt.subplots(figsize=(5.9, 3.5))
    for exp, kind, col, style, lbl in series:
        sel = [r for r in data if int(r["smoothness_exponent"]) == exp]
        bits = np.array([int(r["bits"]) for r in sel])
        rate = np.array([float(r[f"{kind}_rate"]) for r in sel])
        lo = rate - np.array([float(r[f"{kind}_wilson_95_low"])
                              for r in sel])
        hi = np.array([float(r[f"{kind}_wilson_95_high"])
                       for r in sel]) - rate
        ax.errorbar(bits, rate, yerr=[lo, hi], fmt=style, color=col,
                    capsize=2.2, markersize=4.4, lw=1.7, label=lbl)
    ax.set_xlabel("bit length of the prime $r$")
    ax.set_ylabel("coverage fraction of tested primes")
    ax.set_ylim(-0.04, 1.09)
    ax.set_title("Coverage of the tested prime ensembles by CM orders")
    ax.legend(fontsize=8.6, loc="lower left")
    F.finish(fig, os.path.join(OUT, "cm_coverage.svg"))


def fig_residues():
    """Bounded-CM coverage by residue class mod 12 at 60 bits,
    B=60^3, |D|<=60^2, 4,096 descending primes.
    Source: measure_cm_coverage_b60_p4096_e3_d2_w8_20260625_residues.csv."""
    data = rows("measure_cm_coverage_b60_p4096_e3_d2_w8"
                "_20260625_residues.csv")
    res = [int(r["prime_mod_12"]) for r in data]
    tot = [int(r["primes"]) for r in data]
    suc = [int(r["bounded_cm_successes"]) for r in data]
    rate = np.array([float(r["bounded_cm_rate"]) for r in data])
    lo = rate - np.array([float(r["bounded_cm_wilson_95_low"])
                          for r in data])
    hi = np.array([float(r["bounded_cm_wilson_95_high"])
                   for r in data]) - rate
    x = np.arange(len(res))
    fig, ax = plt.subplots(figsize=(5.3, 3.2))
    bars = ax.bar(x, rate, 0.62, color=F.PALETTE[0],
                  edgecolor=F.SURFACE, linewidth=1.2)
    ax.errorbar(x, rate, yerr=[lo, hi], fmt="none", ecolor=F.INK_SECOND,
                capsize=3, lw=1.1)
    for xi, ri, si, ti in zip(x, rate, suc, tot):
        ax.text(xi, 0.615, f"{si}/{ti}", ha="center", va="bottom",
                fontsize=8.6, color=F.SURFACE)
    ax.set_xticks(x)
    ax.set_xticklabels([f"$r\\equiv{m}$" for m in res])
    ax.set_xlabel("residue of $r$ modulo 12")
    ax.set_ylabel("bounded-CM coverage")
    ax.set_ylim(0.60, 1.02)
    ax.set_title(r"Residue effect at 60 bits: $B=60^3$, $|D|\leq 60^2$")
    F.finish(fig, os.path.join(OUT, "residues.svg"))


if __name__ == "__main__":
    fig_smoothness()
    fig_budgets()
    fig_cm()
    fig_residues()
    print("P2.1 figures written")
