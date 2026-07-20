"""Figures for the P1.2 paper (prime-field factor bases: impossibility,
loopholes, and restricted lower bounds). All data loaded from the problem's
real CSVs under problems/P1.2-prime-field-factor-base/data/."""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P1.2-prime-field-factor-base", "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_baseline():
    """SG-01/SG-03: normalized decomposition counts and pair-scan scaling."""
    summary = read_csv(
        "measure_factor_bases_b16-18-20_t96_r3_s12022026_20260622_summary.csv")
    scaling = read_csv(
        "measure_factor_bases_b16-18-20_t96_r3_s12022026_20260622_scaling.csv")

    kinds = ["random_sqrt", "random_matched", "integer_x"]
    labels = {"random_sqrt": r"random, $s=\lfloor\sqrt{p}\rfloor$",
              "random_matched": "random, size-matched",
              "integer_x": "Candidate A (integer $x$)"}
    colors = {"random_sqrt": F.PALETTE[0], "random_matched": F.PALETTE[2],
              "integer_x": F.PALETTE[1]}
    bits = [16, 18, 20]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.2))

    # Panel A: normalized mean decomposition count with 95% CI.
    for k, kind in enumerate(kinds):
        xs, ys, lo, hi = [], [], [], []
        for b in bits:
            row = next(r for r in summary
                       if int(r["bits"]) == b and r["base_kind"] == kind)
            xs.append(b + (k - 1) * 0.28)
            ys.append(float(row["normalized_mean"]))
            lo.append(float(row["normalized_mean"])
                      - float(row["normalized_ci_low"]))
            hi.append(float(row["normalized_ci_high"])
                      - float(row["normalized_mean"]))
        ax1.errorbar(xs, ys, yerr=[lo, hi], fmt="o", capsize=3,
                     color=colors[kind], label=labels[kind], markersize=5.5)
    ax1.axhline(1.0, color=F.MUTED, lw=1.0, ls=":")
    ax1.set_xticks(bits)
    ax1.set_xticklabels([r"$p\approx 2^{16}$", r"$p\approx 2^{18}$",
                         r"$p\approx 2^{20}$"])
    ax1.set_ylabel(r"mean count / exact $s^3/r$")
    ax1.set_title("Normalized three-term decomposition count")
    ax1.set_ylim(0.9, 1.15)
    ax1.legend(loc="upper left", fontsize=8.6)

    # Panel B: pair-scan work vs p (log-log) with the recorded fits.
    for kind in kinds:
        rows = [r for r in scaling if r["base_kind"] == kind]
        ps = np.array([float(r["p"]) for r in rows])
        obs = np.array([float(r["observed_mean_pair_checks"]) for r in rows])
        fit = np.array([float(r["fitted_mean_pair_checks"]) for r in rows])
        slope = float(rows[0]["log_log_slope"])
        order = np.argsort(ps)
        ax2.plot(ps[order], fit[order], "-", color=colors[kind], lw=1.4,
                 alpha=0.7)
        ax2.plot(ps[order], obs[order], "o", color=colors[kind],
                 label=labels[kind] + f" (slope {slope:.3f})", markersize=5.5)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel(r"field size $p$")
    ax2.set_ylabel("mean pair checks to first hit")
    ax2.set_title("Generic pair-scan work grows polynomially")
    ax2.legend(loc="upper left", fontsize=8.2)

    F.finish(fig, os.path.join(OUT, "baseline.svg"))


def fig_loophole():
    """A008: base size below the sqrt diagnostic, but a linear-size table."""
    rows = []
    for name in ["audit_preprocessing_loophole_p65519_m3_20260630.csv",
                 "audit_preprocessing_loophole_p262139_m3_20260630.csv",
                 "audit_preprocessing_loophole_p1048571_m3_20260630.csv"]:
        rows.extend(read_csv(name))
    ps = [int(r["p"]) for r in rows]
    base = [int(r["factor_base_size"]) for r in rows]
    diag = [int(r["sqrt_p_baseline"]) for r in rows]
    table = [int(r["target_table_entries"]) for r in rows]

    x = np.arange(len(ps))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.2, 3.3))
    b1 = ax.bar(x - w / 2, base, w, label=r"radix base size ($m=3$)",
                color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=1.2)
    b2 = ax.bar(x + w / 2, diag, w,
                label=r"$\lfloor\sqrt{p}\rfloor$ diagnostic",
                color=F.PALETTE[3], edgecolor=F.SURFACE, linewidth=1.2)
    ax.bar_label(b1, padding=2, fontsize=9, color=F.INK_SECOND)
    ax.bar_label(b2, padding=2, fontsize=9, color=F.INK_SECOND)
    ax.set_ylabel("points (bars)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"$p={p:,}$".replace(",", r"\,") for p in ps])
    ax.set_ylim(0, 1250)
    ax.set_title("The online-only loophole: small base, linear hidden table")

    ax2 = ax.twinx()
    ax2.plot(x, table, "o--", color=F.PALETTE[7], lw=1.6, markersize=6,
             label="stored target entries")
    for xi, t in zip(x, table):
        ax2.annotate(f"{t:,}", (xi, t), textcoords="offset points",
                     xytext=(0, -16), ha="center", fontsize=8.6,
                     color=F.PALETTE[7])
    ax2.set_yscale("log")
    ax2.set_ylim(3e4, 3e6)
    ax2.set_ylabel("target-table entries (log)", color=F.PALETTE[7])
    ax2.tick_params(axis="y", labelcolor=F.PALETTE[7])
    ax2.grid(False)
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color(F.AXIS)

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "loophole.svg"))


def fig_probe():
    """A009: exhaustive translate-probe audit on the order-19 fixture."""
    rows = read_csv("audit_translate_probe_r19_s4_t1-4_20260707.csv")
    T = np.array([int(r["probe_count"]) for r in rows])
    bound = np.array([int(r["union_bound"]) for r in rows])
    mx = np.array([int(r["maximum_support"]) for r in rows])
    mn = np.array([int(r["minimum_support"]) for r in rows])
    sched = [int(r["shift_schedules"]) for r in rows]

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.plot(T, bound, "s-", color=F.PALETTE[7], lw=1.8,
            label=r"union bound $T\,|\mathcal{F}|$")
    ax.fill_between(T, mn, mx, color=F.PALETTE[0], alpha=0.18, lw=0)
    ax.plot(T, mx, "o-", color=F.PALETTE[0], lw=1.8,
            label="max observed support")
    ax.plot(T, mn, "o--", color=F.PALETTE[0], lw=1.4, alpha=0.65,
            label="min observed support")
    ax.axhline(19, color=F.MUTED, lw=1.0, ls=":")
    ax.text(1.02, 19.35, "group order $r=19$", color=F.MUTED, fontsize=9)
    for t, s in zip(T, sched):
        ax.annotate(f"{s:,} schedules", (t, mn[t - 1]),
                    textcoords="offset points", xytext=(0, -14),
                    ha="center", fontsize=8.2, color=F.INK_SECOND)
    ax.set_xticks(T)
    ax.set_xlabel(r"probe count $T$")
    ax.set_ylabel("targets covered")
    ax.set_ylim(0, 22)
    ax.set_title(r"Exhaustive audit: support never exceeds $T\,|\mathcal{F}|$")
    ax.legend(loc="upper left", fontsize=8.8)
    F.finish(fig, os.path.join(OUT, "probe.svg"))


def fig_groebner():
    """A010: direct vs chain Groebner encodings, completions and timeouts."""
    rows = read_csv("benchmark_smooth_groebner_p17-65537_to5s_20260713.csv")
    ps = [17, 257, 65537]
    encs = ["direct", "chain"]
    colors = {"direct": F.PALETTE[0], "chain": F.PALETTE[1]}

    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    w = 0.36
    x = np.arange(len(ps))
    for k, enc in enumerate(encs):
        heights, timed = [], []
        for p in ps:
            row = next(r for r in rows
                       if int(r["p"]) == p and r["encoding"] == enc)
            if row["status"] == "completed":
                heights.append(float(row["elapsed_s"]))
                timed.append(False)
            else:
                heights.append(float(row["timeout_s"]))
                timed.append(True)
        pos = x + (k - 0.5) * w
        for xi, h, t in zip(pos, heights, timed):
            ax.bar(xi, h, w * 0.92, color=colors[enc],
                   edgecolor=F.SURFACE, linewidth=1.0,
                   alpha=0.45 if t else 1.0,
                   hatch="//" if t else None)
        ax.bar(np.nan, np.nan, color=colors[enc], label=enc + " encoding")
    ax.axhline(5.0, color=F.PALETTE[7], lw=1.3, ls="--")
    ax.text(-0.42, 5.15, "5 s timeout", color=F.PALETTE[7], fontsize=9)
    # annotate completed runs with elapsed times
    for k, enc in enumerate(encs):
        row = next(r for r in rows
                   if int(r["p"]) == 17 and r["encoding"] == enc)
        ax.annotate(f'{float(row["elapsed_s"]):.2f} s',
                    (0 + (k - 0.5) * w, float(row["elapsed_s"])),
                    textcoords="offset points", xytext=(0, 3), ha="center",
                    fontsize=8.6, color=F.INK_SECOND)
    ax.annotate("timeout\n(both encodings)", (1, 5.0),
                textcoords="offset points", xytext=(0, -34), ha="center",
                fontsize=8.6, color=F.INK)
    ax.annotate("timeout\n(both encodings)", (2, 5.0),
                textcoords="offset points", xytext=(0, -34), ha="center",
                fontsize=8.6, color=F.INK)
    ax.set_xticks(x)
    ax.set_xticklabels([r"$p=17$, $|H|=4$", r"$p=257$, $|H|=16$",
                        r"$p=65537$, $|H|=64$"])
    ax.set_ylabel("wall time (s)")
    ax.set_ylim(0, 6.0)
    ax.set_title("Smooth-subgroup decomposition systems: solver behavior")
    ax.legend(loc="center left", fontsize=9)
    F.finish(fig, os.path.join(OUT, "groebner.svg"))


if __name__ == "__main__":
    fig_baseline()
    fig_loophole()
    fig_probe()
    fig_groebner()
    print("P1.2 figures written")
