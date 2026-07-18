"""
figstyle — shared matplotlib style for the ECC-research papers.

A single, print-oriented (light-surface) academic style with a validated,
colorblind-safe categorical palette. Import and call `apply()` at the top of
any figure script, then use `PALETTE`, `SEQ`, and the helper savers.

Palette source: dataviz reference instance (light mode), fixed slot order.
"""
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt

# Categorical palette — fixed slot order (dataviz light mode). Never cycle.
PALETTE = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Sequential blue ramp (light->dark), 100->700.
SEQ = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec",
    "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
    "#184f95", "#104281", "#0d366b",
]

# Ink / chrome.
INK        = "#0b0b0b"
INK_SECOND = "#52514e"
MUTED      = "#898781"
GRID       = "#e1e0d9"
AXIS       = "#c3c2b7"
SURFACE    = "#fcfcfb"

# Diverging poles.
DIV_LOW  = "#2a78d6"  # blue
DIV_HIGH = "#e34948"  # red


def apply():
    """Install the shared rcParams. Call once per script."""
    mpl.rcParams.update({
        "figure.facecolor":  SURFACE,
        "axes.facecolor":    SURFACE,
        "savefig.facecolor": SURFACE,
        "figure.dpi":        160,
        "savefig.dpi":       160,
        "font.family":       "serif",
        "font.serif":        ["Libertinus Serif", "Cambria", "Georgia",
                              "DejaVu Serif", "Times New Roman"],
        "mathtext.fontset":  "cm",
        "font.size":         12,
        "axes.titlesize":    13,
        "axes.labelsize":    12,
        "axes.titlelocation": "left",
        "axes.titlepad":     8,
        "axes.edgecolor":    AXIS,
        "axes.linewidth":    0.9,
        "axes.labelcolor":   INK,
        "axes.titlecolor":   INK,
        "axes.grid":         True,
        "axes.axisbelow":    True,
        "grid.color":        GRID,
        "grid.linewidth":    0.7,
        "xtick.color":       MUTED,
        "ytick.color":       MUTED,
        "xtick.labelcolor":  INK_SECOND,
        "ytick.labelcolor":  INK_SECOND,
        "xtick.labelsize":   10.5,
        "ytick.labelsize":   10.5,
        "legend.frameon":    False,
        "legend.fontsize":   10.5,
        "lines.linewidth":   2.0,
        "lines.markersize":  6,
        "axes.spines.top":   False,
        "axes.spines.right": False,
    })


def finish(fig, path, pad=0.25):
    """Tight-layout, save to `path` (SVG + implied), and close."""
    fig.tight_layout(pad=pad)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path
