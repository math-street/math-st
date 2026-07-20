"""Figures for the P1.3 paper (first fall degree vs solving degree)."""
import os, sys, csv, json
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems", "P1.3-first-fall-degree", "data")


def _load_main_rows():
    path = os.path.join(DATA, "first_fall_vs_solving_20260701.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh)
                if r["target_mode"] == "known" and r["m"] == "2"]


def fig_growth():
    """Measured invariants vs q for the m=2 known-target rows (n=2 and n=3)."""
    rows = _load_main_rows()
    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.15))
    panels = (("2", r"$n=m=2$: the gap grows with $q$"),
              ("3", r"$n=3,\ m=2$: solving degree stays at 4"))
    for ax, (n, title) in zip(axes, panels):
        sub = sorted((r for r in rows if r["n"] == n), key=lambda r: int(r["q"]))
        q = [int(r["q"]) for r in sub]
        dff = [int(r["first_fall_degree"]) for r in sub]
        dreg = [int(r["degree_of_regularity"]) for r in sub]
        qs = [int(r["q"]) for r in sub if r["solving_degree"]]
        sd = [int(r["solving_degree"]) for r in sub if r["solving_degree"]]
        ax.plot(q, dreg, marker="s", markersize=9, markerfacecolor="none",
                color=F.PALETTE[2], linewidth=1.5, linestyle="--",
                label=r"$d_{\mathrm{reg}}$")
        ax.plot(qs, sd, marker="o", markersize=5.5, color=F.PALETTE[0],
                linewidth=2.0, label=r"$\mathrm{sd}_{\mathrm{grevlex}}$")
        ax.plot(q, dff, marker="D", markersize=5, color=F.PALETTE[1],
                linewidth=2.0, label=r"$d_{\mathrm{ff}}$")
        ax.set_title(title, fontsize=11.5)
        ax.set_xlabel("base field size $q$")
        ax.set_xticks(sorted(set(q)))
        ax.set_ylim(0, 25)
    axes[0].set_ylabel("degree")
    axes[0].annotate("gap 18", xy=(23, 23), xytext=(17.4, 15.5),
                     fontsize=10, color=F.INK_SECOND,
                     arrowprops=dict(arrowstyle="-|>", color=F.INK_SECOND, lw=1.0))
    axes[0].annotate("", xy=(23, 5.6), xytext=(20.2, 14.2),
                     arrowprops=dict(arrowstyle="-|>", color=F.INK_SECOND, lw=1.0))
    axes[0].legend(loc="upper left", fontsize=9.5)
    axes[1].legend(loc="upper left", fontsize=9.5)
    F.finish(fig, os.path.join(OUT, "growth.svg"))


def fig_redundancy():
    """Exhaustive rational-core-zero census and the q=7 counterexample zeros."""
    with open(os.path.join(DATA, "search_quadratic_redundancy_20260716.json"),
              encoding="utf-8") as fh:
        search = json.load(fh)
    with open(os.path.join(DATA, "certify_quadratic_field_equations_20260716.json"),
              encoding="utf-8") as fh:
        cert = json.load(fh)

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(7.8, 3.2),
                                  gridspec_kw={"width_ratios": [1.6, 1.0]})
    ks = list(range(9))
    w = 0.27
    cols = [F.PALETTE[0], F.PALETTE[1], F.PALETTE[2]]
    for i, res in enumerate(search["results"]):
        hist = res["rational_core_zero_histogram"]
        vals = [hist.get(str(k), 0) for k in ks]
        ax.bar([k + (i - 1) * w for k in ks], vals, w, color=cols[i],
               edgecolor=F.SURFACE, linewidth=0.6,
               label=rf"$q={res['q']}$")
    ax.set_yscale("log")
    ax.set_ylim(0.6, 4e5)
    ax.axvspan(7.5, 8.5, color=F.PALETTE[7], alpha=0.10, zorder=0)
    ax.annotate("6 redundant systems\n($q=7$ only)", xy=(8.05, 6),
                xytext=(4.6, 3e4), fontsize=9.5, color=F.INK_SECOND,
                arrowprops=dict(arrowstyle="-|>", color=F.INK_SECOND, lw=1.0))
    ax.set_xticks(ks)
    ax.set_xlabel("rational zeros of the core ideal")
    ax.set_ylabel("eligible systems (log)")
    ax.set_title("Exhaustive census at $q=5,7,9$", fontsize=11.5)
    ax.legend(loc="upper right", fontsize=9.5)

    zeros = [tuple(z) for z in
             cert["concrete_counterexample"]["base_field_core_zeros"]]
    gx, gy = np.meshgrid(range(7), range(7))
    ax2.scatter(gx, gy, s=12, color=F.GRID, zorder=1)
    b1 = [z for z in zeros if (z[0] + z[1]) % 7 == 0]
    b2 = [z for z in zeros if z not in b1]
    ax2.scatter([z[0] for z in b1], [z[1] for z in b1], s=95,
                color=F.PALETTE[0], zorder=3, label="$x+y=0$")
    ax2.scatter([z[0] for z in b2], [z[1] for z in b2], s=95,
                color=F.PALETTE[7], zorder=3, marker="s", label="$xy=4$")
    ax2.set_xticks(range(7)); ax2.set_yticks(range(7))
    ax2.set_xlim(-0.6, 6.6); ax2.set_ylim(-0.6, 6.6)
    ax2.set_aspect("equal")
    ax2.grid(False)
    ax2.set_xlabel("$x$"); ax2.set_ylabel("$y$")
    ax2.set_title(r"Eight core zeros over $\mathbb{F}_7$", fontsize=11.5)
    ax2.legend(loc="upper right", fontsize=8.5, handletextpad=0.15,
               borderaxespad=0.2)
    F.finish(fig, os.path.join(OUT, "redundancy.svg"))


def fig_semaev():
    """Exact sparse expansion statistics of the summation polynomials."""
    path = os.path.join(DATA, "measure_semaev_stats_20260623.csv")
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    for i, r in enumerate(rows):
        idx = int(r["index"])
        if r["status"] == "complete":
            t = int(r["term_count"])
            ax.bar(i, t, 0.62, color=F.PALETTE[0], edgecolor=F.SURFACE)
            ax.text(i, t * 1.35, f"{t:,}", ha="center", fontsize=9.5,
                    color=F.INK_SECOND)
            ax.text(i, 0.32, f"deg {r['total_degree']}", ha="center",
                    fontsize=9, color=F.SURFACE, zorder=4)
        else:
            lim = int(r["term_limit"])
            ax.bar(i, lim, 0.62, color=F.SURFACE, edgecolor=F.PALETTE[7],
                   hatch="///", linewidth=1.2)
            ax.text(i, lim * 1.35, "censored\n(30 s / 250,000 terms)",
                    ha="center", fontsize=8.5, color=F.PALETTE[7])
    ax.set_yscale("log")
    ax.set_ylim(0.2, 9e6)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels([f"$f_{int(r['index'])}$" for r in rows])
    ax.set_xlabel("summation polynomial")
    ax.set_ylabel("terms in exact sparse expansion (log)")
    ax.set_title("Generic expansion boundary", fontsize=11.5)
    F.finish(fig, os.path.join(OUT, "semaev.svg"))


if __name__ == "__main__":
    fig_growth()
    fig_redundancy()
    fig_semaev()
    print("P1.3 figures written")
