#!/usr/bin/env python3
# =============================================================================
# GIS spatial-database figure - serious flat journal style (no clip-art).
# Distinct from fig02: hub-and-spoke layout, a NESTED central "database engine"
# container, converging/fanning thin connectors, dashed governance arrows, and a
# different palette (teal -> indigo -> plum).  All original content preserved.
#
# Output: fig03_gis_database.png / .pdf
# Requires: matplotlib
# =============================================================================

import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ------------------------------ font -----------------------------------------
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]

# ------------------------------ palette (teal / indigo / plum) ---------------
IN   = ("#0F766E", "#6FB3AC", "#EAF5F3")   # inputs  - teal   (title, border, fill)
DBC  = ("#3730A3", "#4338CA", "#F4F3FC")   # db outer - indigo (dashed)
STORE= ("#0E7490", "#67B0C8", "#E9F4F8")   # data store - cyan
MGMT = ("#B45309", "#E0B77F", "#FBF3E7")   # management - amber
PROC = ("#2F7D4F", "#86C2A0", "#EAF5EE")   # processing - green
OUT  = ("#7E22CE", "#C4A0DE", "#F6EFFB")   # outputs - plum
SEC  = ("#334155", "#7B8794", "#F1F5F9")   # security - slate (dashed)
INK  = "#20242B"
A_IN, A_OUT, A_INT, A_GOV = "#0F766E", "#7E22CE", "#2F7D4F", "#64748B"

FS_ZONE, FS_T, FS_SUB, FS_B = 15.0, 13.5, 11.5, 12.0

# tight vertical metrics
LINE, TITLE_H, PAD_T, PAD_B, GAP = 1.55, 1.95, 1.05, 0.65, 0.8

# ------------------------------ helpers --------------------------------------
def box(ax, x, y, w, h, fill, edge, r=0.5, lw=1.3, z=2, dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z,
                 linestyle=(0, (4, 2)) if dashed else "-"))

def card_h(title, n):
    return PAD_T + (title.count("\n") + 1) * TITLE_H + 0.5 + n * LINE + PAD_B

def card(ax, x, y, w, h, title, bullets, pal, bfs=FS_B):
    box(ax, x, y, w, h, pal[2], pal[1], r=0.45, lw=1.3, z=4)
    ax.text(x + w / 2, y + h - PAD_T, title, ha="center", va="top",
            color=pal[0], fontsize=FS_T, fontweight="bold", zorder=5, linespacing=0.95)
    hair = y + h - PAD_T - (title.count("\n") + 1) * TITLE_H - 0.15
    ax.add_line(Line2D([x + 0.9, x + w - 0.9], [hair, hair], color=pal[1],
                lw=0.8, zorder=5))
    ty = hair - 0.7
    for b in bullets:
        ax.text(x + 1.0, ty, "\u2022 " + b, ha="left", va="top",
                color=INK, fontsize=bfs, zorder=5)
        ty -= LINE

def stack(heights, total):
    # spread across the band (used where we want blocks to fill it)
    n = len(heights)
    if n == 1:
        return [total - heights[0]]
    g = max((total - sum(heights)) / (n - 1), 0.0)
    tops, y = [], total
    for i, h in enumerate(heights):
        y -= h; tops.append(y); y -= g if i < n - 1 else 0
    return tops

def pack(top, heights, gap):
    # stack blocks from absolute y=top downward, fixed gap; return absolute bottoms
    tops, y = [], top
    for h in heights:
        y -= h; tops.append(y); y -= gap
    return tops

def flow(ax, p1, p2, color, rad=0.0, lw=1.6, dashed=False, ms=13):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                 lw=lw, color=color, zorder=6, shrinkA=1, shrinkB=3,
                 connectionstyle=f"arc3,rad={rad}",
                 linestyle=(0, (4, 2)) if dashed else "-"))

# =============================================================================
# CONTENT
# =============================================================================
inputs = [
    ("Satellite Imagery",
     ["Sentinel-2, Landsat 8/9", "NDVI, LST, EVI, NDWI", "Land cover, Crop maps"]),
    ("Aerial / UAV Data",
     ["High-resolution images", "Orthomosaics, DSM", "Crop health monitoring"]),
    ("Weather Data",
     ["Temperature, Rainfall", "Humidity, Wind, Radiation", "Weather stations / ERA5"]),
    ("Wireless Sensor Networks",
     ["Soil moisture, Soil temp.", "Air temp., Humidity", "Nutrients, EC, pH"]),
    ("Ancillary Data",
     ["Soil maps, DEM", "Land use / Land cover", "Administrative boundaries",
      "Irrigation networks"]),
    ("Agricultural Records",
     ["Crop type, Sowing date", "Yield data, Fertilizer use", "Irrigation schedules"]),
]

outputs = [
    ("Spatial Analysis Outputs",
     ["Land suitability maps", "Soil maps", "Slope, Aspect, Watershed",
      "Interpolated surfaces"]),
    ("AI / ML Model Outputs",
     ["Yield prediction maps", "Disease risk maps", "Irrigation demand maps",
      "Crop classification"]),
    ("Decision Support Products",
     ["Irrigation recommendations", "Fertilizer recommendations",
      "Risk alerts & early warning", "Management zones"]),
    ("Visualization & Dashboards",
     ["Interactive GIS maps", "Time-series monitoring", "KPIs & Reports",
      "Mobile / Web access"]),
    ("Users / Stakeholders",
     ["Farmers", "Agronomists", "Policymakers", "Researchers"]),
]

store_cards = [   # (name, parenthetical detail)
    ("Raster Data", "Imagery, DEM, Indexes"),
    ("Vector Data", "Boundaries, Roads, Irrigation, Rivers, Parcels"),
    ("Tabular Data", "Sensor Observations, Weather, Soil, Records"),
]
mgmt = ("Database Management",
        ["Data Storage", "Data Integration", "Metadata Management", "Quality Control"])
proc = ("Spatial Processing & Analysis",
        ["Spatial Analysis", "Interpolation", "Overlay / Modelling",
         "Multi-criteria Analysis"])
security = ("Data Security & Standards",
            ["Access Control", "Data Backup", "Interoperability (OGC, ISO)",
             "Cloud / Edge Storage", "Data Privacy"])

# =============================================================================
# CANVAS
# =============================================================================
XW, FIGW = 100, 17.2
Y0, Y1 = 12.0, 90.0                 # column band
top = 100
fig, ax = plt.subplots(figsize=(FIGW, FIGW * top / XW))
ax.set_xlim(0, XW); ax.set_ylim(0, top); ax.axis("off")

LX, LW = 3.0, 24.0                  # left column
DX, DW = 37.0, 26.0                 # centre database
RX, RW = 73.0, 24.0                 # right column
band = Y1 - Y0
YTOP = Y1                          # common top edge for cards + engine

# ---- zone header pills -------------------------------------------------------
def pill(cx, text, pal):
    w = 21.5
    box(ax, cx - w / 2, 92.0, w, 4.2, pal[0], pal[0], r=0.9, lw=0, z=3)
    ax.text(cx, 94.1, text, ha="center", va="center", color="white",
            fontsize=FS_ZONE, fontweight="bold", zorder=4)
pill(LX + LW / 2, "DATA SOURCES", IN)
pill(DX + DW / 2, "GIS SPATIAL DATABASE", DBC)
pill(RX + RW / 2, "APPLICATIONS & OUTPUTS", OUT)

# ---- left input cards --------------------------------------------------------
SIDE_GAP = 1.4                      # minimal gap between side cards
in_h = [card_h(t, len(b)) for t, b in inputs]
in_mid = []
for (t, b), h, yy in zip(inputs, in_h, pack(YTOP, in_h, SIDE_GAP)):
    card(ax, LX, yy, LW, h, t, b, IN)
    in_mid.append(yy + h / 2)

# ---- right output cards ------------------------------------------------------
out_h = [card_h(t, len(b)) for t, b in outputs]
out_mid = []
for (t, b), h, yy in zip(outputs, out_h, pack(YTOP, out_h, SIDE_GAP)):
    card(ax, RX, yy, RW, h, t, b, OUT)
    out_mid.append(yy + h / 2)

# =============================================================================
# CENTRE : nested database container (compact, vertically centred)
# =============================================================================
MCH, MCG = 3.6, 0.5                          # store mini-card height / gap
store_h = (PAD_T + TITLE_H + 0.4 + len(store_cards) * MCH
           + (len(store_cards) - 1) * MCG + PAD_B)
mgmt_h  = card_h(mgmt[0], len(mgmt[1]))
proc_h  = card_h(proc[0], len(proc[1]))
GP_ENG, HEADA, BOTP = 3.4, 3.9, 1.7          # short internal gap / header area / bottom pad
engine_h = HEADA + store_h + mgmt_h + proc_h + 2 * GP_ENG + BOTP

DBy1 = YTOP                                   # engine top hugs its title
DBy0 = DBy1 - engine_h
cyE  = (DBy0 + DBy1) / 2                       # funnel centre = engine centre
box(ax, DX, DBy0, DW, engine_h, DBC[2], DBC[1], r=0.9, lw=1.8, z=2, dashed=True)
ax.text(DX + DW / 2, DBy1 - 2.0, "Spatial Database Engine", ha="center", va="top",
        color=DBC[0], fontsize=FS_T + 0.5, fontweight="bold", zorder=5)

inx, inw = DX + 1.6, DW - 3.2
sy  = DBy1 - HEADA - store_h                  # Data Store
my_ = sy - GP_ENG - mgmt_h                    # Database Management
py_ = my_ - GP_ENG - proc_h                   # Spatial Processing

# --- Data Store (nested mini-cards) ---
box(ax, inx, sy, inw, store_h, STORE[2], STORE[1], r=0.5, lw=1.3, z=4)
ax.text(inx + inw / 2, sy + store_h - PAD_T, "Data Store", ha="center", va="top",
        color=STORE[0], fontsize=FS_T, fontweight="bold", zorder=5)
mc_top = sy + store_h - PAD_T - TITLE_H - 0.2
for i, (nm, det) in enumerate(store_cards):
    my = mc_top - (i + 1) * MCH - i * MCG
    box(ax, inx + 0.9, my, inw - 1.8, MCH, "white", STORE[1], r=0.35, lw=1.0, z=5)
    ax.text(inx + 1.7, my + MCH - 1.0, nm, ha="left", va="center",
            color=STORE[0], fontsize=FS_B, fontweight="bold", zorder=6)
    ax.text(inx + 1.7, my + MCH - 2.4, det, ha="left", va="center",
            color=INK, fontsize=FS_SUB - 1.5, zorder=6)

# --- Management + Processing ---
card(ax, inx, my_, inw, mgmt_h, mgmt[0], mgmt[1], MGMT)
card(ax, inx, py_, inw, proc_h, proc[0], proc[1], PROC)

# --- short internal arrows ---
xc = inx + inw / 2
flow(ax, (xc, sy), (xc, my_ + mgmt_h), A_INT, lw=2.0, ms=14)
flow(ax, (xc, my_), (xc, py_ + proc_h), A_INT, lw=2.0, ms=14)

# =============================================================================
# CONVERGING (inputs -> engine centre) and FANNING (engine centre -> outputs)
# symmetric / mirrored, both meeting the vertical centre of the engine
# =============================================================================
entry = (DX, cyE)
for ym in in_mid:
    rad = 0.16 * (ym - cyE) / band
    flow(ax, (LX + LW, ym), entry, A_IN, rad=rad, lw=1.6, ms=13)

exit_ = (DX + DW, cyE)
for ym in out_mid:
    rad = 0.16 * (cyE - ym) / band
    flow(ax, exit_, (RX, ym), A_OUT, rad=rad, lw=1.6, ms=13)

# =============================================================================
# SECURITY & STANDARDS foundation (compact, just below the engine)
# =============================================================================
sww, shh = 44.0, 8.6
sxx = DX + DW / 2 - sww / 2                  # centred under the engine
syy = DBy0 - 3.6 - shh                       # close under the engine
box(ax, sxx, syy, sww, shh, SEC[2], SEC[1], r=0.7, lw=1.5, z=2, dashed=True)
# title centred on top
ax.text(sxx + sww / 2, syy + shh - 1.5, security[0], ha="center", va="center",
        color=SEC[0], fontsize=FS_T, fontweight="bold", zorder=5)
ax.add_line(Line2D([sxx + 2.0, sxx + sww - 2.0], [syy + shh - 2.8, syy + shh - 2.8],
            color=SEC[1], lw=0.8, zorder=5))
# bullets in two centred rows: 3 on top, 2 below
rows = [security[1][:3], security[1][3:]]
row_y = [syy + shh - 4.5, syy + shh - 6.7]
for items, ry in zip(rows, row_y):
    k = len(items)
    for i, b in enumerate(items):
        bx = sxx + sww * (i + 0.5) / k
        ax.text(bx, ry, "\u2022 " + b, ha="center", va="center",
                color=INK, fontsize=FS_SUB - 0.5, zorder=5)
# short dashed governance links: engine bottom corners -> security top
flow(ax, (DX + 5, DBy0), (sxx + sww * 0.30, syy + shh), A_GOV, rad=-0.12,
     lw=1.4, dashed=True, ms=11)
flow(ax, (sxx + sww * 0.70, syy + shh), (DX + DW - 5, DBy0), A_GOV, rad=-0.12,
     lw=1.4, dashed=True, ms=11)

# =============================================================================
# LEGEND (horizontal, along the bottom - uses the empty space, no overlap)
# =============================================================================
leg = [("Data input", A_IN, "-"), ("Products / outputs", A_OUT, "-"),
       ("Internal processing", A_INT, "-"), ("Governance / standards", A_GOV, (0, (4, 2)))]
leg_y = syy - 4.5
x0 = 26.0
ax.text(x0 - 2.0, leg_y, "FLOW:", ha="right", va="center", color=INK,
        fontsize=FS_T, fontweight="bold", zorder=5)
step = 18.0
for i, (label, col, ls) in enumerate(leg):
    lx0 = x0 + i * step
    ax.add_line(Line2D([lx0, lx0 + 3.0], [leg_y, leg_y], color=col, lw=2.6,
                linestyle=ls, zorder=5))
    ax.annotate("", xy=(lx0 + 3.4, leg_y), xytext=(lx0 + 2.9, leg_y),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6), zorder=5)
    ax.text(lx0 + 4.2, leg_y, label, ha="left", va="center", color=INK,
            fontsize=FS_B, zorder=5)

# crop the canvas to the content (remove the empty lower band)
YMIN = leg_y - 3.5
ax.set_ylim(YMIN, 98)
fig.set_size_inches(FIGW, FIGW * (98 - YMIN) / XW)

# =============================================================================
plt.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
fig.savefig("fig03_gis_database.png", dpi=300, bbox_inches="tight")
fig.savefig("fig03_gis_database.pdf", bbox_inches="tight")
print("wrote fig03_gis_database.png and fig03_gis_database.pdf")
