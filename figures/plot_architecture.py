#!/usr/bin/env python3
# =============================================================================
# IWSN-GIS-AI framework architecture - serious flat journal style (no clip-art).
# Update: Nimbus font + larger text; tight vertical padding (squeezed);
# GIS & Spatial Database sub-blocks laid out in TWO columns.
#
# Output: fig02_architecture.png / .pdf
# Requires: matplotlib
# =============================================================================

import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ------------------------------ font -----------------------------------------
# Prefer Nimbus (URW) if installed; fall back gracefully so it never crashes.
matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "Nimbus Sans Regular",
    "DejaVu Sans", "Arial", "Helvetica",
]

# ------------------------------ palette --------------------------------------
PAL = {
    "data":  ("#1F3A5F", "white", "#EEF2F7", "#1F3A5F"),
    "comm":  ("#2E6B4F", "white", "#EDF4EF", "#2E6B4F"),
    "gis":   ("#2B5C8A", "white", "#EAF1F7", "#2B5C8A"),
    "ai":    ("#5B4B8A", "white", "#F0EDF6", "#5B4B8A"),
    "dss":   ("#B4611E", "white", "#F8EFE6", "#B4611E"),
    "ui":    ("#8A6D1F", "white", "#F7F2E4", "#8A6D1F"),
    "inner": ("white",   "#20242B", "white",  "#B9C2CC"),
    "infra": ("#39404A", "white", "#F2F3F5", "#39404A"),
}
ARROW = {"data": "#2C64B4", "sensor": "#2E7D46",
         "analytics": "#6A3FA0", "decision": "#C8781C", "feedback": "#2C64B4"}

# ---- fonts (larger) ----
FS_H, FS_T, FS_B = 12.5, 12.0, 11.0      # header / title / bullet
FS_GIS = 10.0                            # GIS two-column bullets (a touch smaller)

# ---- tight vertical metrics (data units) ----
LINE    = 1.42      # bullet line spacing
TITLE_H = 1.72      # per title line
PAD_T   = 1.15      # pad above title
PAD_B   = 0.70      # pad below last bullet
GAP     = 0.95      # gap between inner blocks
HEAD_H  = 3.3       # coloured header bar height
IN_PAD  = 1.1       # pad between header and first inner block / bottom

# ------------------------------ helpers --------------------------------------
def box(ax, x, y, w, h, fill, edge, r=0.55, lw=1.2, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z))

def block_height(title, n, ncol=1):
    tlines = title.count("\n") + 1
    rows = math.ceil(n / ncol) if n else 0
    body = rows * LINE if rows else 0.6
    return PAD_T + tlines * TITLE_H + body + PAD_B

def draw_subbox(ax, x, y, w, h, title, bullets, accent, ncol=1, bfs=FS_B):
    box(ax, x, y, w, h, "white", PAL["inner"][3], r=0.45, lw=1.0, z=4)
    tlines = title.count("\n") + 1
    ax.text(x + w / 2, y + h - PAD_T, title, ha="center", va="top",
            color=accent, fontsize=FS_T, fontweight="bold", zorder=5,
            linespacing=0.95)
    if not bullets:
        return
    top = y + h - PAD_T - tlines * TITLE_H
    rows = math.ceil(len(bullets) / ncol)
    if ncol == 1:
        ty = top
        for b in bullets:
            ax.text(x + 0.85, ty, "\u2022 " + b, ha="left", va="top",
                    color="#20242B", fontsize=bfs, zorder=5)
            ty -= LINE
    else:
        colw = (w - 1.4) / ncol
        for c in range(ncol):
            cx = x + 0.85 + c * colw
            ty = top
            for b in bullets[c * rows:(c + 1) * rows]:
                ax.text(cx, ty, "\u2022 " + b, ha="left", va="top",
                        color="#20242B", fontsize=bfs, zorder=5)
                ty -= LINE

def stack(heights, total):
    """Stack blocks from the top; distribute slack into the (n-1) INTERNAL gaps
    only (no trailing gap), so the last block bottom lands exactly at 0 and never
    overflows the band."""
    n = len(heights)
    if n == 1:
        return [total - heights[0]]
    inner = total - sum(heights)          # total free space between blocks
    g = max(inner / (n - 1), 0.0)         # even internal gap (>= 0)
    tops, y = [], total
    for i, h in enumerate(heights):
        y -= h
        tops.append(y)
        if i < n - 1:
            y -= g
    return tops

def arrow(ax, p1, p2, kind, style="-|>", lw=2.3, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=17,
                 lw=lw, color=ARROW[kind], linestyle=ls,
                 connectionstyle="arc3,rad=0", zorder=6, shrinkA=2, shrinkB=2))

# =============================================================================
# CONTENT DEFINITION
# =============================================================================
data_cards = ["Satellite Imagery\n(Sentinel-2, Landsat)", "UAV / Drone Imagery",
              "Weather Stations", "IWSN Field Sensors", "Soil & Laboratory Data",
              "Agricultural Records"]

comm_blocks = [
    ("Wireless Sensor\nNetworks (IWSN)", []),
    ("Communication\nTechnologies", ["LoRaWAN", "ZigBee", "NB-IoT / 4G / 5G", "Wi-Fi"]),
    ("Edge / Gateway\n(Pre-processing)", []),
    ("Secure Data\nTransmission", []),
]

gis_blocks = [   # ncol = 2
    ("Data Ingestion & Preprocessing",
     ["Quality Control", "Georeferencing", "Resampling", "Feature Extraction"]),
    ("GIS Spatial Database",
     ["Raster Layers", "Vector Layers", "Time-Series Data", "Metadata"]),
    ("Thematic Data Layers",
     ["Topography (DEM, Slope)", "Land Use / Land Cover", "Soil Properties",
      "Hydrology & Irrigation", "Climate Data", "Sensor Observations",
      "Crop Information"]),
    ("GIS Analysis & Spatial Processing",
     ["Overlay Analysis", "Interpolation (Kriging, IDW)", "Buffer & Proximity",
      "Zonal Statistics", "Network Analysis"]),
]

ai_blocks = [
    ("Machine Learning Models",
     ["Random Forest", "XGBoost", "SVM", "Gradient Boosting"]),
    ("Deep Learning Models",
     ["CNN (Image Analysis)", "LSTM (Time Series)", "Vision Transformer (ViT)"]),
    ("AI Applications",
     ["Crop Classification", "Yield Prediction", "Irrigation Scheduling",
      "Disease Detection", "Soil Moisture Forecasting",
      "Drought Risk Assessment", "Fertilizer Recommendation"]),
    ("Model Outputs",
     ["Predictions", "Probability Maps", "Risk Maps", "Recommendations"]),
]

dss_blocks = [
    ("Spatial Decision Support\nSystem (SDSS)",
     ["Irrigation Recommendations", "Alert & Early Warnings",
      "Crop Management Plans", "Resource Optimization", "Scenario Analysis"]),
    ("Integrated Outputs", ["Maps", "Reports", "Statistics", "Alerts"]),
]

ui_blocks = [
    ("Web GIS Dashboard", []),
    ("Stakeholders",
     ["Farmers", "Agricultural Engineers", "Researchers",
      "Government Agencies", "Policy Makers"]),
    ("Access", ["Web Portal", "Mobile App", "API Services"]),
]

# ----- compute per-column content heights ------------------------------------
def col_total(blocks, ncol=1):
    hs = [block_height(t, len(b), ncol) for t, b in blocks]
    return hs, sum(hs) + GAP * (len(hs) - 1)

data_h  = [block_height(c, 0) for c in data_cards]
comm_hs, comm_tot = col_total(comm_blocks)
gis_hs,  gis_tot  = col_total(gis_blocks, ncol=2)
ai_hs,   ai_tot   = col_total(ai_blocks)
dss_hs,  dss_tot  = col_total(dss_blocks)
ui_hs,   ui_tot   = col_total(ui_blocks)
data_tot = sum(data_h) + GAP * (len(data_h) - 1)

H = max(data_tot, comm_tot, gis_tot, ai_tot, dss_tot, ui_tot)   # content band
LH = H + HEAD_H + 2 * IN_PAD                                     # layer height
Y = 12.5

# =============================================================================
# CANVAS  (height derived from content so the figure is tightly squeezed)
# =============================================================================
XW = 116
FIGW = 19.4
top = Y + LH + 1.0
YTOT = top + 1.0
fig, ax = plt.subplots(figsize=(FIGW, FIGW * YTOT / XW))   # square units, no distortion
ax.set_xlim(0, XW); ax.set_ylim(0, YTOT); ax.axis("off")

cols = {"data": (1.0, 15.0), "comm": (17.0, 12.5), "gis": (30.5, 32.0),
        "ai": (63.5, 16.0), "dss": (80.5, 18.0), "ui": (99.5, 15.0)}

def layer(ax, key, header):
    x, w = cols[key]
    hf, ht, bf, bd = PAL[key]
    box(ax, x, Y, w, LH, bf, bd, r=0.7, lw=1.7, z=2)
    box(ax, x, Y + LH - HEAD_H, w, HEAD_H, hf, bd, r=0.7, lw=1.7, z=3)
    ax.text(x + w / 2, Y + LH - HEAD_H / 2, header, ha="center", va="center",
            color=ht, fontsize=FS_H, fontweight="bold", zorder=4, linespacing=0.95)

for key, header in [
    ("data", "DATA ACQUISITION\nLAYER"), ("comm", "COMMUNICATION &\nIWSN LAYER"),
    ("gis", "GIS & SPATIAL DATABASE LAYER"), ("ai", "AI & ANALYTICS LAYER"),
    ("dss", "DECISION SUPPORT\nLAYER"), ("ui", "USER INTERFACE &\nSTAKEHOLDERS")]:
    layer(ax, key, header)

base = Y + IN_PAD          # bottom of content band

# ---------- DATA ACQUISITION : label cards -----------------------------------
dx, dw = cols["data"]
for i, top_y in enumerate(stack(data_h, H)):
    h = data_h[i]; yy = base + top_y
    box(ax, dx + 0.7, yy, dw - 1.4, h, "white", PAL["inner"][3], r=0.4, lw=1.0, z=4)
    ax.text(dx + dw / 2, yy + h / 2, data_cards[i], ha="center", va="center",
            color="#1F3A5F", fontsize=FS_B + 0.5, fontweight="bold",
            zorder=5, linespacing=0.95)

# ---------- COMMUNICATION -----------------------------------------------------
cx, cw = cols["comm"]
for (t, bl), h, top_y in zip(comm_blocks, comm_hs, stack(comm_hs, H)):
    yy = base + top_y
    if bl:
        draw_subbox(ax, cx + 0.7, yy, cw - 1.4, h, t, bl, "#2E6B4F", ncol=1)
    else:
        box(ax, cx + 0.7, yy, cw - 1.4, h, "white", PAL["inner"][3], r=0.45, lw=1.0, z=4)
        ax.text(cx + cw / 2, yy + h / 2, t, ha="center", va="center",
                color="#2E6B4F", fontsize=FS_T, fontweight="bold",
                zorder=5, linespacing=0.95)

# ---------- GIS  (TWO COLUMNS) -----------------------------------------------
gx, gw = cols["gis"]
for (t, bl), h, top_y in zip(gis_blocks, gis_hs, stack(gis_hs, H)):
    yy = base + top_y
    draw_subbox(ax, gx + 0.9, yy, gw - 1.8, h, t, bl, "#2B5C8A", ncol=2, bfs=FS_GIS)

# ---------- AI ----------------------------------------------------------------
axx, aw = cols["ai"]
for (t, bl), h, top_y in zip(ai_blocks, ai_hs, stack(ai_hs, H)):
    yy = base + top_y
    draw_subbox(ax, axx + 0.9, yy, aw - 1.8, h, t, bl, "#5B4B8A", ncol=1)

# ---------- DSS ---------------------------------------------------------------
sx, sw = cols["dss"]
for (t, bl), h, top_y in zip(dss_blocks, dss_hs, stack(dss_hs, H)):
    yy = base + top_y
    draw_subbox(ax, sx + 0.9, yy, sw - 1.8, h, t, bl, "#B4611E", ncol=1)

# ---------- UI ----------------------------------------------------------------
ux, uw = cols["ui"]
for (t, bl), h, top_y in zip(ui_blocks, ui_hs, stack(ui_hs, H)):
    yy = base + top_y
    if bl:
        draw_subbox(ax, ux + 0.7, yy, uw - 1.4, h, t, bl, "#8A6D1F", ncol=1)
    else:
        box(ax, ux + 0.7, yy, uw - 1.4, h, "white", PAL["inner"][3], r=0.45, lw=1.0, z=4)
        ax.text(ux + uw / 2, yy + h / 2, t, ha="center", va="center",
                color="#8A6D1F", fontsize=FS_T, fontweight="bold",
                zorder=5, linespacing=0.95)

# =============================================================================
# FLOW ARROWS
# =============================================================================
midY = Y + LH / 2
r = lambda k: (cols[k][0] + cols[k][1], midY)
l = lambda k: (cols[k][0], midY)
arrow(ax, r("data"), l("comm"), "data")
arrow(ax, r("comm"), l("gis"),  "sensor")
arrow(ax, r("gis"),  l("ai"),   "data")
arrow(ax, r("ai"),   l("dss"),  "analytics")
arrow(ax, r("dss"),  l("ui"),   "decision")

# feedback loop along the bottom (dashed, right -> left)
fb_y = Y - 1.4
xc_ui = cols["ui"][0] + cols["ui"][1] / 2
xc_dt = cols["data"][0] + cols["data"][1] / 2
ax.add_patch(FancyArrowPatch((xc_ui, Y), (xc_ui, fb_y), arrowstyle="-",
             lw=1.7, color=ARROW["feedback"], linestyle=(0, (2, 2)), zorder=1))
ax.add_patch(FancyArrowPatch((xc_ui, fb_y), (xc_dt, fb_y), arrowstyle="-|>",
             mutation_scale=15, lw=1.7, color=ARROW["feedback"],
             linestyle=(0, (2, 2)), zorder=1))
for key in ("data", "gis", "dss"):
    xc = cols[key][0] + cols[key][1] / 2
    ax.add_patch(FancyArrowPatch((xc, fb_y), (xc, Y), arrowstyle="-|>",
                 mutation_scale=14, lw=1.6, color=ARROW["feedback"],
                 linestyle=(0, (2, 2)), zorder=1))

# =============================================================================
# SYSTEM INFRASTRUCTURE STRIP + INFORMATION-FLOW LEGEND
# =============================================================================
strip_h = 8.6
ix, iy, iw = 1.0, 1.0, 84.0
box(ax, ix, iy, iw, strip_h, PAL["infra"][2], PAL["infra"][3], r=0.7, lw=1.5, z=2)
ax.text(ix + iw / 2, iy + strip_h - 1.4, "SYSTEM INFRASTRUCTURE", ha="center",
        va="center", color=PAL["infra"][0], fontsize=FS_H, fontweight="bold")
infra = ["Cloud / Server\nInfrastructure", "Data Storage\n(Spatial DB)",
         "Backup & Disaster\nRecovery", "Security & Access\nControl",
         "Scalability & High\nAvailability", "APIs & Interoperability\n(OGC Standards)"]
ew = iw / len(infra)
for i, t in enumerate(infra):
    cxi = ix + ew * (i + 0.5)
    box(ax, cxi - ew / 2 + 0.6, iy + 0.8, ew - 1.2, strip_h - 3.0,
        "white", PAL["inner"][3], r=0.4, lw=0.9, z=3)
    ax.text(cxi, iy + (strip_h - 2.2) / 2 + 0.2, t, ha="center", va="center",
            color="#20242B", fontsize=FS_B, zorder=4, linespacing=0.95)

lx, lw_ = 87.0, 28.0
box(ax, lx, iy, lw_, strip_h, "white", PAL["infra"][3], r=0.7, lw=1.5, z=2)
ax.text(lx + lw_ / 2, iy + strip_h - 1.4, "INFORMATION FLOW", ha="center",
        va="center", color="#20242B", fontsize=FS_H, fontweight="bold")
legend = [("Data Flow", "data", "-"), ("Sensor / Communication Flow", "sensor", "-"),
          ("Analytics Flow", "analytics", "-"), ("Decision / Output Flow", "decision", "-"),
          ("Feedback / Update Flow", "feedback", (0, (2, 2)))]
ly0 = iy + strip_h - 3.0
for label, kind, ls in legend:
    ax.add_line(Line2D([lx + 1.2, lx + 3.9], [ly0, ly0], color=ARROW[kind],
                lw=2.5, linestyle=ls, zorder=4))
    ax.annotate("", xy=(lx + 4.2, ly0), xytext=(lx + 3.8, ly0),
                arrowprops=dict(arrowstyle="-|>", color=ARROW[kind], lw=2.5), zorder=4)
    ax.text(lx + 4.8, ly0, label, ha="left", va="center",
            color="#20242B", fontsize=FS_B, zorder=4)
    ly0 -= 1.18

# =============================================================================
plt.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
fig.savefig("fig02_architecture.png", dpi=300, bbox_inches="tight")
fig.savefig("fig02_architecture.pdf", bbox_inches="tight")
print("wrote fig02_architecture.png and fig02_architecture.pdf")
