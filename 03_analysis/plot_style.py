"""Shared chart style for every notebook in this repository.

Colours follow a validated, colour-blind-checked palette: categorical hues are
assigned in a fixed order, magnitude uses a single blue ramp, and polarity
(e.g. correlations) uses a blue <-> red diverging scale with a grey midpoint.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"

# Categorical slots, fixed order (never cycled)
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]

# Single-hue sequential ramp (blue), light -> dark
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#1c5cab", "#104281", "#0d366b"]

# Diverging: blue (negative) <-> grey midpoint <-> red (positive)
DIVERGING = LinearSegmentedColormap.from_list(
    "blue_grey_red", ["#184f95", "#6da7ec", "#f0efec", "#ec8a89", "#b8302f"]
)


def apply():
    """Set matplotlib defaults: recessive grid and axes, text in ink tokens."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.titlecolor": TEXT_PRIMARY,
        "axes.labelcolor": TEXT_SECONDARY,
        "axes.edgecolor": BASELINE,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "text.color": TEXT_PRIMARY,
        "legend.frameon": False,
        "lines.linewidth": 2,
        "axes.prop_cycle": mpl.cycler(color=SERIES),
    })


def bar_kwargs():
    """Thin bars separated by a 2px surface gap."""
    return {"color": SERIES[0], "edgecolor": SURFACE, "linewidth": 1.5}


def rupees(x, _pos=None):
    """Axis formatter: Rs values as K / M."""
    if abs(x) >= 1e6:
        return f"₹{x / 1e6:.1f}M"
    if abs(x) >= 1e3:
        return f"₹{x / 1e3:.0f}K"
    return f"₹{x:.0f}"


def save(fig, name, figures_dir="../04_report/figures"):
    fig.savefig(f"{figures_dir}/{name}.png")
