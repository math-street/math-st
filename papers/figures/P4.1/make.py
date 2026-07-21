"""Figures for the P4.1 paper (optimal pairing-friendly families under exTNFS).

All data are loaded from the real research artifacts in
problems/P4.1-extnfs-optimal-families/data/.
"""
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
OUT = os.path.dirname(__file__)
DATA = os.path.join(OUT, "..", "..", "..", "problems",
                    "P4.1-extnfs-optimal-families", "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as fh:
        return list(csv.DictReader(fh))


def fig_bls12_hist():
    """Distribution of the 1,024 exact BLS12 nested-resultant norm bit lengths."""
    rows = read_csv("bls12_norms_n1024_a1169_s20260722_20260704.csv")
    bf = np.array([int(r["bit_length_f"]) for r in rows])
    bg = np.array([int(r["bit_length_g"]) for r in rows])
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.9))
    for ax, b, printed, side, col in (
        (axes[0], bf, 791.2, "f-side norm", F.PALETTE[0]),
        (axes[1], bg, 584.8, "g-side norm", F.PALETTE[1]),
    ):
        ax.hist(b, bins=36, color=col, edgecolor=F.SURFACE, linewidth=0.4)
        ax.axvline(b.mean(), color=F.INK, lw=1.4,
                   label=f"sample mean {b.mean():.1f}")
        ax.axvline(printed, color=F.PALETTE[7], lw=1.4, ls="--",
                   label=f"printed {printed}")
        ax.set_xlabel(f"{side} bit length")
        ax.legend(fontsize=8.2, loc="upper left")
    axes[0].set_ylabel("samples")
    axes[0].set_title("BLS12-128 exact norm sampling (1,024 samples, seed 20260722)")
    F.finish(fig, os.path.join(OUT, "bls12hist.svg"))


def fig_audit():
    """Sampled-minus-printed security bits across the eight audit rows."""
    rows = read_csv("published_norm_regressions_20260715.csv")
    label_map = {
        ("BLS12-128", "exact-domain"): "BLS12-128, paper domain",
        ("BN-128", "exact-domain"): "BN-128, paper domain",
        ("BN-128", "paper-code-bound"): "BN-128, public-code bound",
        ("KSS16-128", "exact-domain"): "KSS16-128, paper domain",
        ("KSS16-128", "paper-code-bound"): "KSS16-128, public-code bound",
        ("BLS24-192", "exact-domain"): "BLS24-192, paper domain (A=9)",
        ("BLS24-192", "paper-code-bound"): "BLS24-192, public-code bound (A=9)",
        ("BLS24-192", "paper-code-bound-sensitivity-a10"):
            "BLS24-192, public-code bound (A=10)",
    }
    labels, diffs, cols = [], [], []
    for r in rows:
        labels.append(label_map[(r["profile"], r["distribution"])])
        d = float(r["sampled_minus_paper_security_bits"])
        diffs.append(d)
        if r["distribution"].endswith("a10"):
            cols.append(F.PALETTE[3])
        elif abs(d) > 1.0:
            cols.append(F.PALETTE[7])
        else:
            cols.append(F.PALETTE[0])
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.barh(y, diffs, color=cols, edgecolor=F.SURFACE, linewidth=0.6, height=0.62)
    ax.axvline(0, color=F.INK, lw=1.0)
    for span in (-0.2, 0.2):
        ax.axvline(span, color=F.MUTED, lw=0.9, ls=":")
    ax.text(-0.23, len(labels) - 0.4, "0.2-bit band", color=F.MUTED,
            fontsize=8.2, ha="right")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.6)
    ax.invert_yaxis()
    ax.set_xlabel("sampled cost minus printed cost (bits)")
    ax.set_title("Finite-size regression audit against Barbulescu–Duquesne rows")
    for yi, d in zip(y, diffs):
        ax.text(d + (0.05 if d >= 0 else -0.05), yi, f"{d:+.2f}",
                va="center", ha="left" if d >= 0 else "right",
                fontsize=8.2, color=F.INK_SECOND)
    ax.set_xlim(-2.9, 0.9)
    F.finish(fig, os.path.join(OUT, "audit.svg"))


def fig_optimum():
    """Extrapolated rho optima and the cost-scenario sensitivity of field size."""
    rows = read_csv("optimization_extrapolated_20260715.csv")
    fams = ["BN", "BLS12", "BLS24", "KSS16"]
    targets = [128, 192, 256]
    models = ["bn254-calibrated", "sextnfs-o1less", "extnfs-composite"]
    model_labels = {
        "bn254-calibrated": "calibrated SexTNFS",
        "sextnfs-o1less": "o(1)-less SexTNFS",
        "extnfs-composite": "composite exTNFS",
    }
    rho = {(r["model"], int(r["target_bits"]), r["family"]):
           float(r["rho_estimate"]) for r in rows}
    fld = {(r["model"], int(r["target_bits"]), r["family"]):
           float(r["estimated_field_bits"]) for r in rows}

    fig, axes = plt.subplots(1, 2, figsize=(6.9, 3.0))
    ax = axes[0]
    w = 0.24
    for i, t in enumerate(targets):
        vals = [rho[("bn254-calibrated", t, f)] for f in fams]
        ax.bar(np.arange(len(fams)) + (i - 1) * w, vals, w,
               color=F.SEQ[3 + 3 * i], edgecolor=F.SURFACE, linewidth=0.6,
               label=f"{t}-bit target")
    ax.axhline(1.0, color=F.MUTED, lw=0.9, ls=":")
    ax.set_xticks(np.arange(len(fams)))
    ax.set_xticklabels(fams)
    ax.set_ylabel(r"estimated $\rho$")
    ax.set_ylim(0.9, 1.6)
    ax.set_title("Leading-term rho by family")
    ax.legend(fontsize=8.2, loc="upper left")

    ax = axes[1]
    w = 0.24
    for i, m in enumerate(models):
        vals = [fld[(m, t, "BN")] / 1000 for t in targets]
        ax.bar(np.arange(len(targets)) + (i - 1) * w, vals, w,
               color=F.PALETTE[i], edgecolor=F.SURFACE, linewidth=0.6,
               label=model_labels[m])
    ax.set_xticks(np.arange(len(targets)))
    ax.set_xticklabels([str(t) for t in targets])
    ax.set_xlabel("target security (bits)")
    ax.set_ylabel(r"BN required field size (kbit)")
    ax.set_title("Scenario sensitivity of the BN optimum")
    ax.legend(fontsize=8.2, loc="upper left")
    F.finish(fig, os.path.join(OUT, "optimum.svg"))


def fig_search():
    """The 302 accepted toy candidates from the exhaustive bounded seed sweep."""
    rows = read_csv("search_families_m10000_10000_20260626.csv")
    fig, ax = plt.subplots(figsize=(6.2, 3.1))
    style = {"BN": (F.PALETTE[0], "o", 14), "BLS12": (F.PALETTE[1], "s", 22),
             "BLS24": (F.PALETTE[5], "D", 30)}
    for fam, (col, mk, sz) in style.items():
        pts = [(int(r["p_bits"]), float(r["rho"])) for r in rows
               if r["family"] == fam]
        x = [p[0] for p in pts]
        yv = [p[1] for p in pts]
        ax.scatter(x, yv, s=sz, c=col, marker=mk, alpha=0.75,
                   edgecolors="none", label=f"{fam} ({len(pts)})")
    ax.axhline(1.0, color=F.MUTED, lw=0.9, ls=":")
    ax.set_xlabel("field size $p$ (bits)")
    ax.set_ylabel(r"$\rho=\log p/\log r$")
    ax.set_title(r"Accepted toy candidates, seeds $|u|\leq 10^4$, $p<2^{60}$")
    ax.legend(loc="center right", fontsize=8.6)
    F.finish(fig, os.path.join(OUT, "search.svg"))


if __name__ == "__main__":
    fig_bls12_hist()
    fig_audit()
    fig_optimum()
    fig_search()
    print("P4.1 figures written")
