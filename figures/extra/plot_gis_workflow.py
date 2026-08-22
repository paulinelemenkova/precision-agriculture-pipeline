#!/usr/bin/env python3
# =============================================================================
# GIS workflow - LAYERED SWIMLANE ARCHITECTURE (compact).
#   Tier 1  - 7-stage process band (4 sub-blocks each, equal height)
#   Tier 2  - GIS Geodatabase + Analysis Tools resource bars
#   Tier 3  - Spatial Outputs (plain labelled product boxes) -> Decision Support
# Palette: gnuplot2 colormap. No clip-art, no schematic maps.
#
# Output: fig05_gis_workflow.png / .pdf   |   Requires: matplotlib, numpy
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]

INK, SUBINK = "#1C1C22", "#44454D"

# ---- gnuplot2 palette --------------------------------------------------------
cmap = plt.get_cmap("gnuplot2")
def tint(c, f):  return tuple(x + (1 - x) * f for x in c[:3])
def shade(c, f): return tuple(x * (1 - f) for x in c[:3])
def lum(c):      return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def htext(c):    return "white" if lum(c) < 0.60 else "#101018"

SPOS = np.linspace(0.14, 0.82, 7)
SBASE = [cmap(p) for p in SPOS]
DBb, TOOLb = cmap(0.22), cmap(0.62)
OUTb, DSSb = cmap(0.34), cmap(0.72)
FLOW = {"data": shade(cmap(0.16), 0.10), "proc": shade(cmap(0.32), 0.10),
        "ana": shade(cmap(0.52), 0.10), "val": shade(cmap(0.66), 0.10),
        "out": shade(cmap(0.40), 0.10), "fb": "#9A93A6"}
TIER = "#6E6A78"

FS_HDR, FS_IT, FS_DET, FS_TITLE, FS_TIER = 14.8, 12.9, 11.9, 14.8, 11.8

# ------------------------------ helpers --------------------------------------
def box(ax, x, y, w, h, fill, edge, r=0.5, lw=1.3, z=2, dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z,
                 linestyle=(0, (4, 2)) if dashed else "-"))

def arrow(ax, p1, p2, color, lw=2.6, dashed=False, ms=15, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                 lw=lw, color=color, zorder=7, shrinkA=1, shrinkB=1,
                 connectionstyle=f"arc3,rad={rad}",
                 linestyle=(0, (4, 2)) if dashed else "-"))

def wrap(text, width):
    words, lines, cur = text.split(" "), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > width:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines

def fit(text, max_units, base, unit_pt, cwf=0.60):
    return max(8.5, min(base, max_units * unit_pt / (cwf * max(len(text), 1))))

# =============================================================================
# CONTENT  (DATA INPUT merged to 4 sub-blocks -> all columns equal height)
# =============================================================================
stages = [
    ("1. DATA INPUT", [
        ("Satellite & UAV Imagery", "Sentinel-2, Landsat, UAV; NDVI, LST, DSM, Land cover"),
        ("Wireless Sensors", "Soil moisture, Temp., Humidity, EC, pH"),
        ("Weather Data", "Rainfall, Temp., Radiation, Wind, ET$_0$"),
        ("Ancillary Data", "Soil maps, DEM, Land use, Roads, Irrigation, Boundaries"),
    ]),
    ("2. DATA PREPROCESSING", [
        ("Image Preprocessing", "Radiometric, Atmospheric, Geometric; Cloud masking"),
        ("Data Harmonization", "Projection/resampling, Temporal alignment, Standardization"),
        ("Data Cleaning", "Missing values, Outlier detection, Noise filtering"),
        ("Quality Control", "Accuracy assessment, Consistency check"),
    ]),
    ("3. DATA INTEGRATION", [
        ("Layer Integration", "Overlay & stacking of all datasets"),
        ("Spatial Database", "Storage in GIS geodatabase"),
        ("Attribute Integration", "Link spatial layers with tabular data"),
        ("Time-series Management", "Organize temporal datasets"),
    ]),
    ("4. SPATIAL ANALYSIS", [
        ("Terrain Analysis", "Slope, Aspect, Curvature, Watersheds"),
        ("Proximity Analysis", "Distance to rivers, roads, irrigation"),
        ("Overlay Analysis", "Intersect, Union, Clip"),
        ("Zonal Statistics", "Summarize raster values by zones"),
    ]),
    ("5. MODELING & EVALUATION", [
        ("Multi-Criteria Analysis", "Weighted Overlay, AHP / TOPSIS"),
        ("Interpolation", "IDW, Kriging, Spline, Natural Neighbor"),
        ("Suitability Modeling", "Land, Crop, Irrigation suitability maps"),
        ("Risk Modeling", "Drought, Erosion, Flood, Disease risk"),
    ]),
    ("6. VALIDATION", [
        ("Model Validation", "Ground truth data, Field surveys, Confusion matrix"),
        ("Accuracy Metrics", "Overall Accuracy, Kappa, RMSE / MAE"),
        ("Sensitivity Analysis", "Parameter sensitivity, Scenario analysis"),
        ("Expert Review", "Agronomist review, Stakeholder feedback"),
    ]),
    ("7. OUTPUT & VISUALIZATION", [
        ("Map Production", "Thematic maps, Layout & symbology"),
        ("3D Visualization", "3D terrain, surfaces, profiles"),
        ("Dashboard", "Interactive maps, charts, indicators"),
        ("Reporting", "Automated reports, statistics, exports"),
    ]),
]

db_cols = [
    ("Raster Data", "Imagery, DEM, Indices"),
    ("Vector Data", "Boundaries, Roads, Rivers, Parcels, Irrigation"),
    ("Tabular Data", "Sensors, Weather, Soil, Crops, Yields"),
    ("Metadata", "Standards, Descriptions"),
]
tools = ["Spatial Analyst (ArcGIS)", "QGIS Processing", "GRASS GIS",
         "Google Earth Engine", "Python (PyQGIS, Rasterio)", "R (raster, sf, sp)",
         "Machine Learning / AI", "Cloud Computing"]
outputs = ["Land Use / Land Cover Map", "NDVI / Vegetation Health Map",
           "Soil Moisture Map", "Land Suitability Map", "Irrigation Suitability Map",
           "Drought Risk Map", "Disease Risk Map"]
dss = ["Scenario Evaluation", "What-if Analysis", "Recommendations",
       "Alerts & Notifications", "Web / Mobile Access"]

# =============================================================================
# CANVAS + geometry
# =============================================================================
XW, FIGW = 100.0, 16.8
YT = 90.0
fig, ax = plt.subplots(figsize=(FIGW, FIGW * YT / XW))
ax.set_xlim(0, XW); ax.set_ylim(0, YT); ax.axis("off")
UNIT_PT = FIGW / XW * 72.0

n = 7
GAPC = 0.7
CW = (XW - 2.0 - GAPC * (n - 1)) / n
X0 = 1.0
colx = [X0 + i * (CW + GAPC) for i in range(n)]
centers = [c + CW / 2 for c in colx]

T1_TOP, HDR_H = 84.0, 3.2
IT_H, IT_GAP = 7.0, 0.7
nit = 4
body_h = nit * IT_H + (nit - 1) * IT_GAP + 1.0
body_top = T1_TOP - HDR_H - 0.5
body_y = body_top - body_h

ax.text(0.55, T1_TOP - HDR_H / 2, "TIER 1", rotation=90, ha="center", va="center",
        color=TIER, fontsize=FS_TIER, fontweight="bold")

FLOWKEY = ["data", "proc", "proc", "ana", "ana", "val", "out"]
for i, (header, items) in enumerate(stages):
    x = colx[i]; hf = shade(SBASE[i], 0.08)
    bd = tint(hf, 0.45); bf = tint(hf, 0.90); tcol = shade(hf, 0.35)
    box(ax, x, body_y, CW, body_h, bf, bd, r=0.5, lw=1.3, z=2)
    box(ax, x, T1_TOP - HDR_H, CW, HDR_H, hf, hf, r=0.5, lw=0, z=3)
    ax.text(x + CW / 2, T1_TOP - HDR_H / 2, header, ha="center", va="center",
            color=htext(hf), fontsize=fit(header, CW - 1.6, FS_HDR, UNIT_PT),
            fontweight="bold", zorder=4)
    iy = body_top - 0.6
    for title, det in items:
        iy -= IT_H
        box(ax, x + 0.5, iy, CW - 1.0, IT_H, "white", bd, r=0.3, lw=0.9, z=4)
        ax.text(x + 0.95, iy + IT_H - 1.35, title, ha="left", va="top",
                color=tcol, fontsize=fit(title, CW - 1.8, FS_IT, UNIT_PT, 0.62),
                fontweight="bold", zorder=5)
        ty = iy + IT_H - 2.75
        for ln in wrap(det, 22)[:4]:
            ax.text(x + 0.95, ty, ln, ha="left", va="top",
                    color=SUBINK, fontsize=FS_DET, zorder=5)
            ty -= 1.32

# inter-stage arrows
arr_y = body_top - 1.9
for i in range(n - 1):
    arrow(ax, (colx[i] + CW + 0.05, arr_y), (colx[i + 1] - 0.05, arr_y),
          FLOW[FLOWKEY[i + 1]], lw=2.6, ms=15)

# feedback / iteration arc - bows ABOVE the band, right -> left
arrow(ax, (centers[6], T1_TOP + 0.5), (centers[0], T1_TOP + 0.5), FLOW["fb"],
      lw=2.1, dashed=True, ms=17, rad=0.06)
ax.text((centers[0] + centers[6]) / 2, T1_TOP + 2.1, "feedback / iteration",
        ha="center", va="center", color=FLOW["fb"], fontsize=FS_DET,
        fontstyle="italic")

# =============================================================================
# TIER 2 : resource bars
# =============================================================================
T2_TOP = body_y - 3.0
BARH = 12.5
ax.text(0.55, T2_TOP - BARH / 2, "TIER 2", rotation=90, ha="center", va="center",
        color=TIER, fontsize=FS_TIER, fontweight="bold")

dbx, dbw = 1.0, 55.0
dtc = shade(DBb, 0.35); dbd = tint(DBb, 0.5); dbf = tint(DBb, 0.90)
box(ax, dbx, T2_TOP - BARH, dbw, BARH, dbf, dbd, r=0.6, lw=1.5, z=2)
ax.text(dbx + dbw / 2, T2_TOP - 1.7, "SPATIAL DATABASE  (GIS Geodatabase)",
        ha="center", va="center", color=dtc, fontsize=FS_TITLE, fontweight="bold")
ax.add_line(Line2D([dbx + 2, dbx + dbw - 2], [T2_TOP - 3.2, T2_TOP - 3.2], color=dbd, lw=0.9))
cwd = (dbw - 3) / 4
for k, (nm, det) in enumerate(db_cols):
    cx = dbx + 1.8 + k * cwd
    ax.text(cx, T2_TOP - 5.0, nm, ha="left", va="top", color=dtc,
            fontsize=FS_IT, fontweight="bold")
    ty = T2_TOP - 6.5
    for ln in wrap(det, 17):
        ax.text(cx, ty, ln, ha="left", va="top", color=SUBINK, fontsize=FS_DET)
        ty -= 1.3

tlx, tlw = 58.0, 41.0
ttc = shade(TOOLb, 0.4); tbd = tint(TOOLb, 0.5); tbf = tint(TOOLb, 0.90)
box(ax, tlx, T2_TOP - BARH, tlw, BARH, tbf, tbd, r=0.6, lw=1.5, z=2)
ax.text(tlx + tlw / 2, T2_TOP - 1.7, "ANALYSIS METHODS & TOOLS",
        ha="center", va="center", color=ttc, fontsize=FS_TITLE, fontweight="bold")
ax.add_line(Line2D([tlx + 2, tlx + tlw - 2], [T2_TOP - 3.2, T2_TOP - 3.2], color=tbd, lw=0.9))
for c in range(2):
    cx = tlx + 2.4 + c * (tlw / 2)
    ty = T2_TOP - 4.9
    for t in tools[c * 4:(c + 1) * 4]:
        ax.text(cx, ty, "\u2022 " + t, ha="left", va="top", color=INK, fontsize=FS_DET)
        ty -= 2.0

# connectors: geodatabase -> stages 0-3 (data), tools -> stages 4-6 (analysis)
for i in (0, 1, 2, 3):
    arrow(ax, (centers[i], T2_TOP), (centers[i], body_y), FLOW["data"], lw=1.9, ms=12)
for i in (4, 5, 6):
    arrow(ax, (centers[i], T2_TOP), (centers[i], body_y), FLOW["ana"], lw=1.9, ms=12)
arrow(ax, (dbx + dbw, T2_TOP - BARH / 2), (tlx, T2_TOP - BARH / 2), FLOW["data"], lw=1.9, ms=12)

# =============================================================================
# TIER 3 : Spatial Outputs (plain labelled boxes) -> DSS
# =============================================================================
T3_TOP = T2_TOP - BARH - 2.6
STRIPH = 11.5
ax.text(0.55, T3_TOP - STRIPH / 2, "TIER 3", rotation=90, ha="center", va="center",
        color=TIER, fontsize=FS_TIER, fontweight="bold")

osx, osw = 1.0, 62.0
otc = shade(OUTb, 0.4); obd = tint(OUTb, 0.5); obf = tint(OUTb, 0.92)
box(ax, osx, T3_TOP - STRIPH, osw, STRIPH, obf, obd, r=0.6, lw=1.5, z=2)
ax.text(osx + osw / 2, T3_TOP - 1.8, "SPATIAL OUTPUTS / PRODUCTS",
        ha="center", va="center", color=otc,
        fontsize=FS_TITLE, fontweight="bold")
# 7 plain product boxes (labels only)
bw = (osw - 2.2) / 7
by = T3_TOP - STRIPH + 1.3
bh = STRIPH - 4.6
for k, name in enumerate(outputs):
    bx = osx + 1.1 + k * bw
    box(ax, bx, by, bw - 0.8, bh, "white", obd, r=0.3, lw=1.0, z=4)
    lines = wrap(name, 12)
    y0 = by + bh / 2 + (len(lines) - 1) * 0.85
    for ln in lines:
        ax.text(bx + (bw - 0.8) / 2, y0, ln, ha="center", va="center",
                color=INK, fontsize=FS_DET, zorder=5)
        y0 -= 1.7

# results (Tier 2) -> products (Tier 3): short down arrows, no crossing
_t2_bot = T2_TOP - BARH
for xr in (18.0, 37.0, 56.0):
    arrow(ax, (xr, _t2_bot), (xr, T3_TOP), FLOW["out"], lw=1.9, ms=12)

# Decision Support System
dsx, dsw = 65.0, 34.0
stc = shade(DSSb, 0.4); sbd = tint(DSSb, 0.5); sbf = tint(DSSb, 0.90)
box(ax, dsx, T3_TOP - STRIPH, dsw, STRIPH, sbf, sbd, r=0.6, lw=1.6, z=2)
ax.text(dsx + dsw / 2, T3_TOP - 1.8, "DECISION SUPPORT SYSTEM",
        ha="center", va="center", color=stc, fontsize=FS_TITLE, fontweight="bold")
ax.add_line(Line2D([dsx + 2, dsx + dsw - 2], [T3_TOP - 3.2, T3_TOP - 3.2], color=sbd, lw=0.9))
dss_cols = [dss[:3], dss[3:]]
dcolx = [dsx + 2.2, dsx + 2.2 + dsw / 2]
for c, items in enumerate(dss_cols):
    ty = T3_TOP - 4.8
    for it in items:
        ax.text(dcolx[c], ty, "\u2022 " + it, ha="left", va="top", color=INK, fontsize=FS_IT)
        ty -= 2.0
arrow(ax, (osx + osw, T3_TOP - STRIPH / 2), (dsx, T3_TOP - STRIPH / 2),
      FLOW["val"], lw=2.4, ms=16)

# =============================================================================
# LEGEND
# =============================================================================
leg = [("Data Flow", FLOW["data"], "-"), ("Processing Flow", FLOW["proc"], "-"),
       ("Analysis Flow", FLOW["ana"], "-"), ("Validation Flow", FLOW["val"], "-"),
       ("Output Flow", FLOW["out"], "-"), ("Feedback / Iteration", FLOW["fb"], (0, (4, 2)))]
ly = T3_TOP - STRIPH - 2.6
x = 11.0; step = 14.8
ax.text(x - 2.0, ly, "FLOW:", ha="right", va="center", color=INK,
        fontsize=FS_TITLE, fontweight="bold")
for i, (label, col, ls) in enumerate(leg):
    lx0 = x + i * step
    ax.add_line(Line2D([lx0, lx0 + 2.6], [ly, ly], color=col, lw=2.6, linestyle=ls))
    ax.annotate("", xy=(lx0 + 3.0, ly), xytext=(lx0 + 2.5, ly),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6))
    ax.text(lx0 + 3.6, ly, label, ha="left", va="center", color=INK, fontsize=FS_DET)

YMIN = ly - 2.8
ax.set_ylim(YMIN, YT)
fig.set_size_inches(FIGW, FIGW * (YT - YMIN) / XW)
plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
fig.savefig("fig05_gis_workflow.png", dpi=300, bbox_inches="tight")
fig.savefig("fig05_gis_workflow.pdf", bbox_inches="tight")
print("wrote fig05_gis_workflow.png and fig05_gis_workflow.pdf")
