"""Figures for the P3.4 paper (a decision criterion for torsion-point leakage).

All quantitative content is loaded from the problem's own JSON fixtures and
generated data files; nothing is hand-transcribed.
"""
import os, sys, json
from math import gcd, log2
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch, Rectangle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import figstyle as F

F.apply()
# The bundled Libertinus/Cambria serif fails to rasterize small glyphs and tick
# labels under this matplotlib build; DejaVu Serif is bundled and reliable.
mpl.rcParams["font.serif"] = ["DejaVu Serif"]
mpl.rcParams["font.family"] = "serif"

OUT = os.path.dirname(__file__)
PROB = os.path.join(OUT, "..", "..", "..", "problems", "P3.4-torsion-leakage-criterion")
DATA = os.path.join(PROB, "data")
CODE = os.path.join(PROB, "code")

ACCENT_EDGE = "#256abf"


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _light(hexcol, amt):
    r, g, b = mc.to_rgb(hexcol)
    return (r + (1 - r) * amt, g + (1 - g) * amt, b + (1 - b) * amt)


def _dark(hexcol, amt=0.4):
    r, g, b = mc.to_rgb(hexcol)
    return (r * (1 - amt), g * (1 - amt), b * (1 - amt))


def num(x):
    if isinstance(x, str) and "^" in x:
        b, e = x.split("^")
        return int(b) ** int(e)
    return x


# Verdict palette, shared across figures.
VC = {
    "KEY_RECOVERY_POLYNOMIAL":            F.PALETTE[5],  # green
    "KEY_RECOVERY_WITH_SURFACE_WITNESS":  F.PALETTE[2],  # aqua
    "ALGEBRAIC_ONLY":                     F.PALETTE[3],  # yellow
    "WITNESS_DEPENDENT":                  F.PALETTE[1],  # orange
    "NO_PUBLISHED_ROUTE":                 F.PALETTE[7],  # red
    "INSUFFICIENT_PROFILE":               F.MUTED,
}


# ---------------------------------------------------------------------------
def fig_flow():
    """Ordered decision procedure of CHECKLIST.md Section 4 as a flowchart."""
    fig, ax = plt.subplots(figsize=(7.6, 8.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis("off")

    xc, boxw, boxh = 3.35, 5.9, 1.02
    ys = np.linspace(14.3, 1.9, 7)

    steps = [
        "1.  Public endpoints name one\ntarget map  $\\phi:E_0\\to E_1$?",
        "2.  Degree  $d=\\deg\\phi$  exact or\npolynomially enumerable?",
        "3.  Public closure fixes  $\\phi|_{E_0[N]}$\nat rank two for one  $N>1$?",
        "4.  Torsion and factorizations\naccessible at polynomial cost?",
        "5.  After justified peeling,\n$\\gcd(N,d)=1$?",
        "6.  $N^2>d$  and evaluation\nconverts to the secret?",
        "7.  Valid K2-CD / K2-MM\nauxiliary witness constructed?",
    ]

    def rbox(x, y, w, h, text, fc, ec, tc, fs, weight="normal", ha="center"):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                     boxstyle="round,pad=0.03,rounding_size=0.10",
                     linewidth=1.1, facecolor=fc, edgecolor=ec, zorder=3))
        tx = x if ha == "center" else x - w / 2 + 0.22
        ax.text(tx, y, text, ha=ha, va="center", fontsize=fs, color=tc,
                weight=weight, zorder=4)

    def arrow(x0, y0, x1, y1, color, lw=1.2):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                     mutation_scale=12, linewidth=lw, color=color, zorder=2))

    def leaf(src_y, y, text, verdict, h=1.02):
        col = VC[verdict]
        rbox(9.25, y, 5.0, h, text, _light(col, 0.82), col, _dark(col), 7.4,
             weight="bold", ha="left")
        arrow(xc + boxw / 2, src_y, 9.25 - 2.5, y, col, lw=1.0)

    # decision spine
    for text, y in zip(steps, ys):
        rbox(xc, y, boxw, boxh, text, F.SEQ[0], ACCENT_EDGE, F.INK, 8.6, ha="left")
    # yes arrows down the spine
    for i in range(6):
        arrow(xc, ys[i] - boxh / 2, xc, ys[i + 1] + boxh / 2, F.PALETTE[5])
        ax.text(xc + 0.14, (ys[i] + ys[i + 1]) / 2, "yes", fontsize=7.4,
                color=_dark(F.PALETTE[5]), va="center", ha="left")

    # right-hand leaves
    leaf_specs = [
        (0, "no $\\to$ NO_PUBLISHED_ROUTE\n?  $\\to$ INSUFFICIENT_PROFILE", "NO_PUBLISHED_ROUTE"),
        (1, "hidden $\\to$ NO_PUBLISHED_ROUTE\n?  $\\to$ INSUFFICIENT_PROFILE", "NO_PUBLISHED_ROUTE"),
        (2, "no $\\to$ NO_PUBLISHED_ROUTE\n?  $\\to$ INSUFFICIENT_PROFILE", "NO_PUBLISHED_ROUTE"),
        (3, "not poly $\\to$ ALGEBRAIC_ONLY\n?  $\\to$ INSUFFICIENT_PROFILE", "ALGEBRAIC_ONLY"),
        (4, "no / not peeled $\\to$\nWITNESS_DEPENDENT", "WITNESS_DEPENDENT"),
        (5, "yes $\\to$ KEY_RECOVERY_\nPOLYNOMIAL  (R8 route)", "KEY_RECOVERY_POLYNOMIAL"),
    ]
    for i, text, verdict in leaf_specs:
        leaf(ys[i], ys[i], text, verdict)

    # step 7 has two stacked leaves
    leaf(ys[6], ys[6] + 0.62, "witness + poly $\\to$ KEY_RECOVERY_\nWITH_SURFACE_WITNESS", "KEY_RECOVERY_WITH_SURFACE_WITNESS", h=0.9)
    leaf(ys[6], ys[6] - 0.62, "else $\\to$ WITNESS_DEPENDENT\nor ALGEBRAIC_ONLY", "WITNESS_DEPENDENT", h=0.9)

    ax.text(0.15, 15.45,
            "Ordered decision procedure (SG-04): a verdict at every leaf",
            fontsize=11.5, weight="bold", color=F.INK, ha="left")
    ax.text(0.15, 0.7,
            "Green success branch exits right at step 6 (R8); steps 1--3 gate on the "
            "shared template inputs C0--C2.",
            fontsize=7.6, color=F.INK_SECOND, ha="left")
    F.finish(fig, os.path.join(OUT, "criterion_flow.svg"))


# ---------------------------------------------------------------------------
def _profile_gates(p):
    """Map a raw leakage profile to pass/fail/NA cells per decision gate."""
    P, Fl, NA = 2, 0, 1

    def tri(cond):
        return P if cond is True else (Fl if cond is False else NA)

    endpoints = tri(p.get("target_endpoints_public"))
    dvis = p.get("degree_visibility")
    degree_ok = P if dvis in ("exact", "polynomial_candidates") else (Fl if dvis == "hidden" else NA)
    rank = p.get("torsion_rank")
    action = p.get("target_action_derivable")
    if action is False or (rank is not None and rank < 2):
        rank2 = Fl
    elif action is True and rank is not None and rank >= 2:
        rank2 = P
    else:
        rank2 = NA
    same = tri(p.get("same_secret_across_samples"))
    d, N = num(p.get("degree")), num(p.get("torsion_order"))
    if d is None or N is None:
        coprime = size = NA
    else:
        coprime = P if gcd(d, N) == 1 else Fl
        size = P if N * N > d else Fl
    smooth = tri(p.get("smooth_arithmetic"))
    return [endpoints, degree_ok, rank2, same, coprime, size, smooth]


def _grid(cases, verdicts, title, outfile, figh):
    gate_labels = ["endpoints\nC0", "degree\nC1", "rank-2\nC2", "same\nsecret",
                   "$\\gcd(N,d)$\n$=1$", "$N^2>d$", "smooth\narith."]
    cmap = {2: F.PALETTE[5], 0: F.PALETTE[7], 1: F.SURFACE}
    n = len(cases)
    fig, ax = plt.subplots(figsize=(8.6, figh))
    M = np.array([_profile_gates(c) for c in cases])
    ng = M.shape[1]
    for i in range(n):
        for j in range(ng):
            v = M[i, j]
            ax.add_patch(Rectangle((j, i), 0.9, 0.9, facecolor=cmap[v],
                         edgecolor=F.GRID, linewidth=0.8))
            mark = {2: "P", 0: "x", 1: "-"}[v]
            tc = F.SURFACE if v in (2, 0) else F.MUTED
            ax.text(j + 0.45, i + 0.45, mark, ha="center", va="center",
                    color=tc, fontsize=9.5, weight="bold")
    xv = ng + 0.3
    for i, c in enumerate(cases):
        vd = verdicts[c["case_id"]]
        col = VC[vd]
        ax.add_patch(FancyBboxPatch((xv, i + 0.06), 5.0, 0.78,
                     boxstyle="round,pad=0.02,rounding_size=0.08",
                     facecolor=_light(col, 0.82), edgecolor=col, linewidth=1.0))
        ax.text(xv + 0.16, i + 0.45, vd, ha="left", va="center",
                fontsize=7.6, color=_dark(col), weight="bold")
    ax.set_xlim(0, ng + 5.6)
    ax.set_ylim(0, n)
    ax.set_xticks(np.arange(ng) + 0.45)
    ax.set_xticklabels(gate_labels, fontsize=8.2)
    ax.set_yticks(np.arange(n) + 0.45)
    ax.set_yticklabels([c["case_id"] for c in cases], fontsize=8.4)
    ax.xaxis.tick_top(); ax.xaxis.set_label_position("top")
    ax.invert_yaxis()
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title(title, fontsize=11, weight="bold", loc="left", pad=28)
    F.finish(fig, os.path.join(OUT, outfile))


def fig_protocol_grid():
    cases = load(os.path.join(CODE, "protocol_cases.json"))["cases"]
    verdicts = {r["case_id"]: r["verdict"]
                for r in load(os.path.join(DATA, "leakage_checklist_protocol_20260630.json"))}
    _grid(cases, verdicts,
          "Protocol classification: decision gates and verdicts (SG-03)",
          "protocol_grid.svg", 3.2)


def fig_boundary_grid():
    cases = load(os.path.join(CODE, "boundary_cases.json"))["cases"]
    verdicts = {r["case_id"]: r["verdict"]
                for r in load(os.path.join(DATA, "leakage_checklist_boundary_20260630.json"))}
    _grid(cases, verdicts,
          "Boundary stress tests: where each synthetic profile exits (SG-05)",
          "boundary_grid.svg", 4.3)


# ---------------------------------------------------------------------------
def fig_r8_boundary():
    """The R8 size test log2(N^2) vs log2(d) for the cases that reach step 6."""
    prot = load(os.path.join(CODE, "protocol_cases.json"))["cases"]
    bnd = load(os.path.join(CODE, "boundary_cases.json"))["cases"]
    pv = {r["case_id"]: r["verdict"]
          for r in load(os.path.join(DATA, "leakage_checklist_protocol_20260630.json"))}
    bv = {r["case_id"]: r["verdict"]
          for r in load(os.path.join(DATA, "leakage_checklist_boundary_20260630.json"))}

    def reaches_size_test(c):
        """Replicate CHECKLIST.md steps 1--5: only these cases reach step 6."""
        if c.get("target_endpoints_public") is not True:
            return False
        if c.get("degree_visibility") not in ("exact", "polynomial_candidates"):
            return False
        if c.get("target_action_derivable") is not True:
            return False
        if c.get("torsion_rank") is None or c.get("torsion_rank") < 2:
            return False
        if c.get("same_secret_across_samples") is False:
            return False
        d, N = num(c.get("degree")), num(c.get("torsion_order"))
        return d is not None and N is not None and gcd(d, N) == 1

    rows = []
    for c in prot:
        if reaches_size_test(c):
            rows.append((c["case_id"], num(c["degree"]), num(c["torsion_order"]), pv[c["case_id"]]))
    for c in bnd:
        if reaches_size_test(c):
            rows.append((c["case_id"], num(c["degree"]), num(c["torsion_order"]), bv[c["case_id"]]))
    reach = sorted(rows, key=lambda t: 2 * log2(t[2]) - log2(t[1]))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ypos = np.arange(len(reach))
    for y, (cid, d, N, vd) in zip(ypos, reach):
        ld, lN2 = log2(d), 2 * log2(N)
        col = VC[vd]
        ax.plot([ld, lN2], [y, y], color=col, lw=2.6, zorder=2, solid_capstyle="round")
        ax.scatter([ld], [y], color=F.PALETTE[7], s=36, zorder=3, marker="o",
                   edgecolor=F.SURFACE, linewidth=0.8)
        ax.scatter([lN2], [y], color=F.PALETTE[5], s=44, zorder=3, marker="s",
                   edgecolor=F.SURFACE, linewidth=0.8)
        ax.text(max(ld, lN2) + 7, y, f"margin {lN2 - ld:+.3g} bits", va="center",
                fontsize=7.6, color=_dark(col))
    ax.set_yticks(ypos)
    ax.set_yticklabels([t[0] for t in reach], fontsize=8.2)
    ax.set_xlabel(r"bits:   $\log_2 d$  (circle)   vs   $\log_2 N^2$  (square)")
    ax.set_title(r"R8 direct-recovery boundary  $N^2>d$  (checklist step 6)",
                 fontsize=11, weight="bold", loc="left")
    ax.set_xlim(0, 500)
    ax.margins(y=0.10)
    leg = [Patch(facecolor=F.PALETTE[5], label=r"$N^2$ (square): larger $\Rightarrow$ R8 passes"),
           Patch(facecolor=F.PALETTE[7], label=r"$d$ (circle)")]
    ax.legend(handles=leg, loc="lower right", fontsize=8.4)
    F.finish(fig, os.path.join(OUT, "r8_boundary.svg"))


# ---------------------------------------------------------------------------
def fig_closure_certificates():
    """Closure statuses and surface-certificate statuses across the fixtures."""
    closure = load(os.path.join(DATA, "leakage_closure_leakage_records_20260703.json"))
    certs = load(os.path.join(DATA, "surface_certificates_surface_certificate_cases_20260703.json"))

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(8.6, 3.9),
                                   gridspec_kw={"width_ratios": [1.05, 1.0]})

    cstat = {
        "FULL_ACTION": F.PALETTE[5],
        "PARTIAL_SPAN": F.PALETTE[1],
        "INCONSISTENT_IMAGES": F.PALETTE[7],
        "MIXED_TARGET_MAPS": F.PALETTE[4],
        "INCOMPATIBLE_BASES": F.PALETTE[3],
    }
    ids = [r["case_id"] for r in closure]
    stat = [r["status"] for r in closure]
    y = np.arange(len(ids))
    axL.barh(y, [1] * len(ids), color=[cstat[s] for s in stat],
             edgecolor=F.SURFACE, height=0.74)
    for yi, s in zip(y, stat):
        axL.text(0.5, yi, s, ha="center", va="center", fontsize=7.2,
                 color=F.SURFACE, weight="bold")
    axL.set_yticks(y)
    axL.set_yticklabels(ids, fontsize=7.8)
    axL.invert_yaxis()
    axL.set_xticks([])
    axL.set_xlim(0, 1)
    for s in axL.spines.values():
        s.set_visible(False)
    axL.tick_params(length=0)
    axL.set_title("Leakage closure (SG-08): 6 record sets", fontsize=10,
                  weight="bold", loc="left", pad=20)
    l1 = next(r for r in closure if r["case_id"] == "L1-composite-collective-span")
    cert = l1["certificate"]
    axL.text(0.0, -0.95,
             "L1 mod 6:  cols $(1,0),(0,2),(0,3)$;  minors "
             + ",".join(str(m) for m in cert["source_minors"])
             + f";  gcd$=1$;  action ${cert['action']}$",
             fontsize=6.9, color=F.INK_SECOND, va="top")

    sstat = {"NUMERICALLY_VALID": F.PALETTE[5], "INVALID": F.PALETTE[7],
             "UNSUPPORTED_ROUTE": F.MUTED}
    cids = [r["case_id"] for r in certs]
    cst = [r["status"] for r in certs]
    routes = [r["route"] for r in certs]
    y2 = np.arange(len(cids))
    axR.barh(y2, [1] * len(cids), color=[sstat[s] for s in cst],
             edgecolor=F.SURFACE, height=0.74)
    for yi, s, rt in zip(y2, cst, routes):
        axR.text(0.5, yi, f"{rt}: {s}", ha="center", va="center", fontsize=7.0,
                 color=F.SURFACE, weight="bold")
    axR.set_yticks(y2)
    axR.set_yticklabels(cids, fontsize=7.8)
    axR.invert_yaxis()
    axR.set_xticks([])
    axR.set_xlim(0, 1)
    for s in axR.spines.values():
        s.set_visible(False)
    axR.tick_params(length=0)
    axR.set_title("Surface certificates (SG-09): 5 cases", fontsize=10,
                  weight="bold", loc="left", pad=20)
    F.finish(fig, os.path.join(OUT, "closure_certificates.svg"))


if __name__ == "__main__":
    fig_flow()
    fig_protocol_grid()
    fig_boundary_grid()
    fig_r8_boundary()
    fig_closure_certificates()
    print("P3.4 figures written")
