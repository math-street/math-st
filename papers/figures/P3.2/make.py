"""Figures for the P3.2 paper (quantum cost of class-group actions).

All data is loaded from the real research artifacts under
problems/P3.2-class-group-quantum-constant/data/.
"""
import os, sys
import csv as csvmod
import json
import math
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..",
                    "problems", "P3.2-class-group-quantum-constant", "data")


def load_json(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as handle:
        return json.load(handle)


def fig_scaling():
    """Simulated sieve query counts n=24..96 with the fitted three-term model."""
    rows = []
    path = os.path.join(DATA, "simulate_sieve_n24-96_seed20260722_20260630.csv")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        for row in csvmod.DictReader(handle):
            rows.append((int(row["n_bits"]), float(row["query_count"])))
    n_vals = np.array([r[0] for r in rows], dtype=float)
    lnq = np.array([math.log(r[1]) for r in rows])

    fit = load_json("fit_sieve_n24-96_20260630.json")
    c = fit["parameters"]["c_sqrt_log_N"]["estimate"]
    d = fit["parameters"]["d_log_log_N"]["estimate"]
    k = fit["parameters"]["k_intercept"]["estimate"]
    rmse = fit["rmse_log_query"]
    res = fit["residuals"]
    sizes = np.array([r["n_bits"] for r in res], dtype=float)
    means = np.array([r["mean_log_query"] for r in res])
    residuals = np.array([r["residual"] for r in res])

    grid = np.linspace(22.0, 98.0, 400)
    lnN = grid * math.log(2.0)
    fitted = c * np.sqrt(lnN) + d * np.log(lnN) + k

    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(6.4, 4.6), sharex=True,
        gridspec_kw={"height_ratios": [2.6, 1.0]})

    rng = np.random.default_rng(0)
    jitter = rng.uniform(-0.9, 0.9, size=len(n_vals))
    ax.scatter(n_vals + jitter, lnq, s=7, color=F.PALETTE[0], alpha=0.16,
               linewidths=0, label="1,000 seeded trials", rasterized=False)
    ax.scatter(sizes, means, s=42, color=F.PALETTE[1], zorder=5,
               edgecolor=F.SURFACE, linewidth=1.0,
               label="per-size mean of $\\ln Q$ (100 trials)")
    ax.plot(grid, fitted, color=F.INK, lw=1.8,
            label="fit $\\ln Q = c\\sqrt{\\ln N} + d\\ln\\ln N + k$")
    ax.set_ylabel("$\\ln(\\mathrm{query\\ count})$")
    ax.set_title("Simplified fixed-batch sieve, $N = 2^n$, seed 20260722")
    ax.text(0.985, 0.06,
            "$c = 2.68677$  [2.65454, 2.71923]\n$d = -0.93996$   $k = 4.85231$",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=9.5,
            color=F.INK_SECOND)
    ax.legend(loc="upper left", fontsize=9)

    axr.axhspan(-rmse, rmse, color=F.PALETTE[0], alpha=0.10, lw=0)
    axr.axhline(0.0, color=F.MUTED, lw=0.9)
    axr.stem(sizes, residuals, basefmt=" ",
             linefmt=F.PALETTE[1], markerfmt="o")
    for artist in axr.collections + axr.lines:
        artist.set_zorder(4)
    axr.set_ylim(-1.0, 1.0)
    axr.set_xlabel("group-order bits $n = \\log_2 N$")
    axr.set_ylabel("residual")
    axr.text(0.985, 0.86, "RMSE = 0.365", transform=axr.transAxes,
             ha="right", va="top", fontsize=9, color=F.INK_SECOND)
    F.finish(fig, os.path.join(OUT, "scaling.svg"))


def fig_endpoints():
    """Logical endpoints and illustrative physical layer for three configurations."""
    configs = [
        ("BS 2020 Sec. 3.3 ($n=257$)",
         "cost_model_n257_bonnetain_schrottenloher_2020_section3_3_20260630.json",
         F.PALETTE[0]),
        ("Peikert 2020 optimistic ($n=257$)",
         "cost_model_n257_peikert_2020_optimistic_endpoint_20260630.json",
         F.PALETTE[2]),
        ("illustrative sieve ($n=64$)",
         "cost_model_n64_illustrative_surface_code_20260630.json",
         F.PALETTE[1]),
    ]
    metrics = []
    for label, name, color in configs:
        rep = load_json(name)
        lg = rep["logical_resources"]
        ph = rep["physical_resources"]
        metrics.append({
            "label": label,
            "color": color,
            "queries": lg["abstract_query_security_bits"],
            "tgates": math.log2(lg["t_gates"]),
            "qubits": math.log2(ph["physical_qubits"]),
            "runtime": math.log2(ph["runtime_seconds"]),
        })

    names = ["oracle queries", "logical T gates",
             "physical qubits", "runtime (seconds)"]
    keys = ["queries", "tgates", "qubits", "runtime"]
    x = np.arange(len(names), dtype=float)
    w = 0.26
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    for i, m in enumerate(metrics):
        vals = [m[k] for k in keys]
        bars = ax.bar(x + (i - 1) * w, vals, w, color=m["color"],
                      edgecolor=F.SURFACE, linewidth=1.0, label=m["label"])
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8,
                     color=F.INK_SECOND)
    ax.axvline(1.5, color=F.MUTED, lw=0.9, ls=":")
    ax.text(0.72, 79, "logical layer", fontsize=9, color=F.MUTED, ha="center")
    ax.text(2.5, 76, "illustrative physical layer\n(named surface-code inputs)",
            fontsize=9, color=F.MUTED, ha="center")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9.5)
    ax.set_ylabel("$\\log_2(\\mathrm{value})$")
    ax.set_ylim(0, 86)
    ax.set_title("Three named configurations of the same calculator")
    fig.legend(loc="lower center", ncol=3, fontsize=8.6, frameon=False,
               bbox_to_anchor=(0.5, -0.045))
    F.finish(fig, os.path.join(OUT, "endpoints.svg"))


def fig_tornado():
    """One-at-a-time sensitivity of physical qubit-seconds at n=64."""
    sens = load_json("sensitivity_n64_20260630.json")
    labels = {
        "logical_architecture.parallel_workers": "parallel workers",
        "operation_costs.oracle_logical_depth": "oracle logical depth",
        "surface_code.physical_error_rate": "physical error rate",
        "surface_code.code_cycle_seconds": "code-cycle time (s)",
        "surface_code.data_physical_qubits_per_d2": "data qubits per $d^2$",
        "surface_code.t_states_per_factory_per_code_cycle":
            "T states per factory-cycle",
        "logical_architecture.oracle_workspace_logical_qubits_per_worker":
            "workspace qubits per worker",
        "logical_architecture.magic_factory_count": "magic-state factories",
        "surface_code.failure_budget": "failure budget",
    }
    entries = sens["ranking"]           # already sorted by impact, descending
    names, lows, highs, ranges = [], [], [], []
    for entry in entries:
        changes = [e["log2_change_from_base"] for e in entry["endpoints"]]
        values = [e["value"] for e in entry["endpoints"]]
        names.append(labels[entry["parameter"]])
        lows.append(min(changes + [0.0]))
        highs.append(max(changes + [0.0]))
        ranges.append("%g - %g" % (min(values), max(values)))

    y = np.arange(len(names))[::-1]
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.barh(y, np.array(highs) - np.array(lows), left=lows, height=0.62,
            color=F.PALETTE[0], edgecolor=F.SURFACE, linewidth=1.0)
    ax.axvline(0.0, color=F.INK, lw=1.0)
    for yi, lo, hi, rng_text in zip(y, lows, highs, ranges):
        ax.text(hi + 0.12, yi, rng_text, va="center", fontsize=8,
                color=F.MUTED)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9.5)
    ax.set_xlabel("$\\log_2$ change in physical qubit-seconds from base")
    ax.set_xlim(-3.6, 7.6)
    ax.set_title("One-at-a-time endpoints, illustrative $n=64$ configuration")
    ax.grid(axis="y", visible=False)
    F.finish(fig, os.path.join(OUT, "tornado.svg"))


def fig_toyaction():
    """Verified toy class-group actions at p=59 and p=419 as orbit graphs."""
    reports = [
        ("verify_toy_action_p59_20260630.json",
         "$p=59$:  $h(-236)=9$, degrees 3, 5"),
        ("verify_toy_action_p419_20260630.json",
         "$p=419$:  $h(-1676)=27$, degrees 3, 5, 7"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.4))
    for ax, (name, title) in zip(axes, reports):
        rep = load_json(name)
        n = rep["orbit_size"]
        trans = rep["transitions"]
        theta = 2 * np.pi * np.arange(n) / n + np.pi / 2
        px, py = np.cos(theta), np.sin(theta)
        for g in range(len(rep["degrees"])):
            color = F.PALETTE[g]
            for i in range(n):
                j = trans[i][g]
                ax.plot([px[i], px[j]], [py[i], py[j]], color=color,
                        lw=1.0, alpha=0.55, zorder=1)
        ax.scatter(px, py, s=26, color=F.INK, zorder=3)
        ax.set_title(title, fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-1.25, 1.25)
        ax.set_ylim(-1.25, 1.25)
        ax.axis("off")
    handles = [plt.Line2D([], [], color=F.PALETTE[i], lw=2,
                          label="$\\ell = %d$" % ell)
               for i, ell in enumerate([3, 5, 7])]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=9.5,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    F.finish(fig, os.path.join(OUT, "toyaction.svg"))


if __name__ == "__main__":
    fig_scaling()
    fig_endpoints()
    fig_tornado()
    fig_toyaction()
    print("P3.2 figures written")
