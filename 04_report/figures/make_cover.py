"""Build the README cover (cover.png, 1600x900) and the GitHub social preview (social_preview.png, 1280x640).

Run from this folder after notebooks 01-06:  python make_cover.py

Figures shown:
- value at stake by segment: read from 01_data/output/segment_playbook_metrics.csv [NB06]
- AUC by method: NB04, Section 4 (copied below, as NB04 does not save the AUC table)
- headline tiles: NB05 and NB06, as tagged next to each tile
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch
from PIL import Image

HERE = Path(__file__).parent
NAVY, CARD, GRID = "#0d1a33", "#16264a", "#2a3b63"
GOLD, WHITE, MUTED, BLUE = "#f2b705", "#ffffff", "#aab4c8", "#5b8def"
plt.rcParams["font.family"] = "Segoe UI"

cards = pd.read_csv(HERE.parents[1] / "01_data/output/segment_playbook_metrics.csv", index_col="kmeans_segment")
AUC = {  # [NB04, Section 4]
    "Tier × K-means segment": 0.606, "Tier × RFM segment": 0.604, "Loyalty tier": 0.570,
    "K-means segment": 0.502, "RFM segment": 0.502, "RFM Recency score": 0.495, "Days since last order": 0.495,
}

fig = plt.figure(figsize=(16, 9), dpi=100, facecolor=NAVY)


def card(x, y, w, h):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                                      transform=fig.transFigure, facecolor=CARD, edgecolor=GRID, linewidth=1, zorder=-1))


# Left: title block
fig.text(0.053, 0.885, "PYTHON CASE STUDY · CUSTOMER SEGMENTATION · JUN 2024–JUN 2026", color=GOLD, fontsize=13,
         fontweight="semibold")
fig.text(0.053, 0.735, "E-Commerce Customer\nSegmentation", color=WHITE, fontsize=44, fontweight="bold",
         linespacing=1.05, va="bottom")
fig.patches.append(plt.Rectangle((0.053, 0.705), 0.04, 0.006, transform=fig.transFigure, color=GOLD))
fig.text(0.053, 0.555, "Three segments hold 80% of the revenue at stake.\nPast behaviour does not predict who leaves, "
         "and\ncoupons buy nothing the business would not get anyway.", color="#d9deea", fontsize=16.5, linespacing=1.45)

# Left: four headline tiles
tiles = [("79.6%", "of revenue at risk sits in\nthree segments"),
         ("0.50", "AUC of recency and segments\nfor predicting lapse: chance"),
         ("+1.5%", "larger orders with a coupon,\nand no effect on retention"),
         ("₹9.7M", "saved per six months by\ncapping SAVE10 at ₹1,000")]
for i, (big, small) in enumerate(tiles):
    x = 0.053 + (i % 2) * 0.205
    y = 0.315 - (i // 2) * 0.175
    card(x, y, 0.19, 0.155)
    fig.text(x + 0.015, y + 0.085, big, color=GOLD, fontsize=30, fontweight="bold")
    fig.text(x + 0.015, y + 0.022, small, color=MUTED, fontsize=12, linespacing=1.3)
fig.text(0.053, 0.075, "39.8K customers · 250K orders · 7 segments · tested on Jan–Jun 2026", color=WHITE, fontsize=13)
fig.text(0.053, 0.04, "Python · pandas · scikit-learn · SciPy · matplotlib", color=GOLD, fontsize=13, fontweight="semibold")


def style(ax, title):
    ax.set_facecolor(CARD)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(title, color=WHITE, fontsize=13, fontweight="semibold", loc="left", pad=10)


# Right top: value at stake
card(0.515, 0.505, 0.45, 0.43)
ax = fig.add_axes([0.70, 0.585, 0.24, 0.285])
style(ax, "Revenue at risk, Jul–Dec 2026 (₹ M)")
c = cards.sort_values("expected_revenue_at_risk")
ax.barh(range(len(c)), c.six_month_value / 1e6, color=GRID, height=0.7)
ax.barh(range(len(c)), c.expected_revenue_at_risk / 1e6, color=GOLD, height=0.7)
ax.set_yticks(range(len(c)), c.index, color=WHITE, fontsize=10.5)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
for i, (risk, val) in enumerate(zip(c.expected_revenue_at_risk / 1e6, c.six_month_value / 1e6)):
    ax.text(val + 8, i, f"{risk:,.0f}", va="center", color=GOLD, fontsize=10, fontweight="semibold")
ax.set_xlim(0, c.six_month_value.max() / 1e6 * 1.15)
fig.text(0.53, 0.52, "Gold: expected at risk · grey: six-month revenue", color=MUTED, fontsize=10)

# Right bottom: AUC
card(0.515, 0.065, 0.45, 0.415)
ax = fig.add_axes([0.70, 0.15, 0.24, 0.26])
style(ax, "Who stops buying? AUC on Jan–Jun 2026")
names, vals = list(AUC)[::-1], list(AUC.values())[::-1]
colours = [GOLD if "tier" in n.lower() else BLUE for n in names]
ax.hlines(range(len(vals)), 0.48, vals, color=GRID, linewidth=2)
ax.scatter(vals, range(len(vals)), color=colours, s=70, zorder=3)
for i, v in enumerate(vals):
    ax.text(v + 0.004, i, f"{v:.3f}", va="center", color=WHITE, fontsize=10)
ax.axvline(0.5, color=MUTED, linewidth=1, linestyle="--")
ax.set_yticks(range(len(names)), names, color=WHITE, fontsize=10.5)
ax.set_xlim(0.48, 0.63)
fig.text(0.53, 0.08, "Dashed line: 0.5, no better than chance", color=MUTED, fontsize=10)

fig.savefig(HERE / "cover.png", facecolor=NAVY)

# Social preview: the cover scaled onto GitHub's 1280x640 canvas
cover = Image.open(HERE / "cover.png").convert("RGB")
scaled = cover.resize((1138, 640), Image.LANCZOS)
preview = Image.new("RGB", (1280, 640), NAVY)
preview.paste(scaled, ((1280 - 1138) // 2, 0))
preview.save(HERE / "social_preview.png")
print("Saved cover.png and social_preview.png")
