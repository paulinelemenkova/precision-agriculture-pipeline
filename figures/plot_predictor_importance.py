#!/usr/bin/env python3
# =============================================================================
# fig09 - Schematic predictor-importance (mean |SHAP|, normalized) for
#   (a) crop-yield regression   and   (b) irrigation-demand regression.
#
# Corrected to be CONSISTENT with the paper (Sec. 8 / Fig. caption):
#   * Panel (a) YIELD: vegetation indices (NDVI/EVI) and rainfall dominate, as
#     the text explicitly states; soil moisture is present but not the top driver.
#   * Panel (b) IRRIGATION DEMAND: the real-time IWSN soil-moisture stream
#     dominates (the contribution that distinguishes the IWSN-coupled framework).
#   * Colour-by-data-source is now consistent across both panels:
#       IWSN sensor = soil moisture; Climate = rainfall, air temp.&humidity;
#       Remote sensing = NDVI/EVI, land-surface temp.; Soil = texture & pH;
#       Terrain = elevation / slope.
# Values remain ILLUSTRATIVE (each panel sums to 1.00), matching the caption.
#
# Output: fig09_predictor_importance.png / .pdf   |  Requires: matplotlib, numpy
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]

# ---- data-source categories (one consistent colour per source) --------------
SOURCE = {
    "IWSN sensor":    "#3B3B8F",   # indigo
    "Climate":        "#22B7C9",   # cyan
    "Remote sensing": "#7DD53F",   # green
    "Soil":           "#F5A03C",   # orange
    "Terrain":        "#A81E1E",   # dark red
}
# each predictor -> its data source (consistent across BOTH panels)
CAT = {
    "Soil moisture (IWSN)": "IWSN sensor",
    "Rainfall":             "Climate",
    "Air temp. & humidity": "Climate",
    "NDVI / EVI":           "Remote sensing",
    "Land surface temp.":   "Remote sensing",
    "Soil texture & pH":    "Soil",
    "Elevation / slope":    "Terrain",
}

# ---- illustrative importances (sum = 1.00 per panel) ------------------------
# (a) YIELD: vegetation + rainfall dominate (per Sec. 8 text)
YIELD = [
    ("NDVI / EVI",           0.23),
    ("Rainfall",             0.20),
    ("Air temp. & humidity", 0.16),
    ("Land surface temp.",   0.14),
    ("Soil moisture (IWSN)", 0.12),
    ("Soil texture & pH",    0.08),
    ("Elevation / slope",    0.07),
]
# (b) IRRIGATION DEMAND: real-time IWSN soil moisture dominates
IRRIG = [
    ("Soil moisture (IWSN)", 0.30),
    ("Rainfall",             0.18),
    ("Air temp. & humidity", 0.15),
    ("NDVI / EVI",           0.12),
    ("Land surface temp.",   0.10),
    ("Soil texture & pH",    0.09),
    ("Elevation / slope",    0.06),
]

FS_TITLE, FS_LBL, FS_TICK, FS_VAL, FS_LEG = 17, 15, 13, 14, 14

def panel(ax, data, title, xmax):
    data = sorted(data, key=lambda t: t[1], reverse=True)   # largest at top
    names = [d[0] for d in data]
    vals  = [d[1] for d in data]
    y = np.arange(len(names))[::-1]
    cols = [SOURCE[CAT[n]] for n in names]
    ax.barh(y, vals, color=cols, edgecolor="black", linewidth=1.2, height=0.72,
            zorder=3)
    # value labels (inside if bar long enough, else just outside)
    for yi, v, c in zip(y, vals, cols):
        inside = v > xmax * 0.18
        tx = v - xmax * 0.012 if inside else v + xmax * 0.012
        ax.text(tx, yi, f"{v:.2f}", va="center",
                ha="right" if inside else "left",
                color="white" if inside else "black", fontsize=FS_VAL, zorder=4)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=FS_LBL)
    ax.set_xlim(0, xmax)
    ax.set_xlabel("Relative predictor importance\n(mean |SHAP|, normalized)",
                  fontsize=FS_LBL)
    ax.set_title(title, fontsize=FS_TITLE, fontweight="bold", pad=12)
    ax.tick_params(axis="x", labelsize=FS_TICK)
    ax.grid(axis="x", color="#CCCCCC", lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.0, 7.6))
panel(ax1, YIELD, "(a) Crop-yield regression",       0.30)
panel(ax2, IRRIG, "(b) Irrigation-demand regression", 0.34)

# shared legend (data sources, in a sensible order)
order = ["IWSN sensor", "Climate", "Remote sensing", "Soil", "Terrain"]
handles = [Patch(facecolor=SOURCE[k], edgecolor="black", label=k) for k in order]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
           fontsize=FS_LEG, bbox_to_anchor=(0.5, -0.02), handlelength=1.4,
           columnspacing=1.8)

fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig("fig09_predictor_importance.png", dpi=300, bbox_inches="tight")
fig.savefig("fig09_predictor_importance.pdf", bbox_inches="tight")
print("wrote fig09_predictor_importance.png and .pdf")
print("panel (a) sum:", round(sum(v for _,v in YIELD),3),
      "| panel (b) sum:", round(sum(v for _,v in IRRIG),3))
