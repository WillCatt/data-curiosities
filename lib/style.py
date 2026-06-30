"""Shared chart styling for the Skilljar Data Exploration pieces.

The portfolio repeats its matplotlib rcParams block inline in every figure
script. This project will accumulate many small figure scripts, so the palette
and rcParams live here once and get imported. One source of truth.

Palette is the portfolio house palette (warm ivory background, brown ink, amber
accent) so any figure can later slot straight into williamcatt.dev.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# --- palette -------------------------------------------------------------
BG = "#faf8f4"      # warm ivory background
INK = "#1a1714"     # dark brown text
MUTED = "#7a6e63"   # muted / secondary
GRID = "#e6ded2"    # gridlines, axis edges
AMBER = "#b06a16"   # accent / highlight
GREY = "#cdbfae"    # non-highlighted
GREEN = "#3a8f57"   # safe / "after"
TEAL = "#2a8f8f"
RED = "#b3402a"
PURPLE = "#7e57c2"
GOLD = "#c89a3c"

PALETTE = {
    "bg": BG, "ink": INK, "muted": MUTED, "grid": GRID,
    "amber": AMBER, "grey": GREY, "green": GREEN, "teal": TEAL, "red": RED,
}

# A small ordered set of band colours for "split by group" charts.
BAND_COLORS = [AMBER, TEAL, GREEN, PURPLE, RED, GOLD]


def apply_rcParams() -> None:
    """Set the house matplotlib defaults. Call once before plotting."""
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": MUTED,
        "axes.edgecolor": GRID, "axes.grid": True, "grid.color": GRID,
        "axes.axisbelow": True, "font.size": 12,
    })


def despine(ax) -> None:
    """Hide the top and right spines (house convention)."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def title_left(ax, text: str, **kw) -> None:
    """Left-aligned bold title (house convention)."""
    ax.set_title(text, loc="left", fontweight="bold", **kw)


def save(fig, path: str) -> None:
    """Save at the house export resolution."""
    fig.savefig(path, dpi=200, bbox_inches="tight")
