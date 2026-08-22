#!/usr/bin/env python3
# =============================================================================
# AI / ML workflow for precision agriculture - serious flat journal style.
# Six-stage pipeline + four foundation blocks + dashed vertical feedback risers.
# No clip-art. Colours sampled from the TURBO colormap.
#
# Output: fig04_ai_workflow.png / .pdf   |   Requires: matplotlib, numpy
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

INK, SUBINK = "#20242B", "#4A4F58"

# ---- fonts (minimum detail = 11, others scaled ~x1.17) ----
FS_HDR, FS_IT, FS_DET, FS_FND = 16.5, 14.5, 13.0, 15.0
LINE = 1.72

# ---- Turbo palette ----------------------------------------------------------
turbo = plt.get_cmap("turbo")
def tint(c, f):  return tuple(x + (1 - x) * f for x in c[:3])   # toward white
def shade(c, f): return tuple(x * (1 - f) for x in c[:3])       # toward black
def lum(c):      return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

SPOS = np.linspace(0.07, 0.93, 6)                 # 6 stages across turbo
SBASE = [turbo(p) for p in SPOS]
GOLD = (1.0, 0.851, 0.0)                   # #ffd900 for stage 4
SBASE[3] = GOLD                            # replace Turbo khaki
FPOS = np.linspace(0.13, 0.87, 4)                 # 4 foundation blocks
FBASE = [turbo(p) for p in FPOS]
# inter-stage arrow colours (midpoints) + legend flow colours
def _mix(a, b):
    return tuple((a[k] + b[k]) / 2 for k in range(3))
ARR = [shade(_mix(SBASE[i], SBASE[i + 1]), 0.10) for i in range(5)]
LEGCOL = [shade(SBASE[0], 0.10), shade(SBASE[2], 0.10),
          shade(SBASE[3], 0.10), shade(SBASE[5], 0.10)]
FB = "#8A93A0"

def hdr_text(c):  # readable header text colour
    return "white" if lum(c) < 0.6 else "#101418"

# ------------------------------ helpers --------------------------------------
def box(ax, x, y, w, h, fill, edge, r=0.5, lw=1.3, z=2, dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z,
                 linestyle=(0, (4, 2)) if dashed else "-"))

def arrow(ax, p1, p2, color, lw=3.0, dashed=False, ms=18):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                 lw=lw, color=color, zorder=6, shrinkA=1, shrinkB=1,
                 connectionstyle="arc3,rad=0",
                 linestyle=(0, (4, 2)) if dashed else "-"))

# =============================================================================
# CONTENT
# =============================================================================
stages = [
    ("1. DATA COLLECTION", [
        ("Satellite Imagery", "Sentinel-2, Landsat, NDVI, EVI, LST"),
        ("UAV Data", "Multispectral, RGB, DSM"),
        ("Wireless Sensors", "Soil moisture, Temperature, Humidity, EC, pH"),
        ("Weather Data", "Rainfall, Temp., Wind, Radiation, ET$_0$"),
        ("Agricultural Records", "Yield, Irrigation, Fertilizer, Crop type, Sowing date"),
    ]),
    ("2. DATA PREPROCESSING", [
        ("Data Cleaning", "Missing values, Outliers, Noise"),
        ("Data Integration", "Spatial & temporal alignment"),
        ("Resampling &\nProjection", "Common resolution & CRS"),
        ("Feature Extraction", "Indices (NDVI, EVI), Terrain, Soil props., Climate"),
        ("Normalization & Encoding", "Scaling, Categorical encoding"),
    ]),
    ("3. FEATURE ENGINEERING", [
        ("Temporal Features", "Trends, Seasonality, Growing Degree Days"),
        ("Spatial Features", "Neighborhood stats., Distances, Topography"),
        ("Interaction Features", "Climate $\\times$ Soil, Soil $\\times$ Crop, etc."),
        ("Dimensionality\nReduction", "PCA, Feature Selection"),
        ("Feature Set for Modeling", "Final structured dataset"),
    ]),
    ("4. MODEL TRAINING", [
        ("Train/Test Split", "e.g., 70% Train / 30% Test"),
        ("Model Training", "RF, XGBoost, CNN, LSTM, ViT, etc."),
        ("Hyperparameter\nTuning", "Grid Search / Bayesian Opt."),
        ("Cross-Validation", "K-fold CV for robustness"),
        ("Trained Models", "Best performing models saved"),
    ]),
    ("5. MODEL VALIDATION", [
        ("Performance\nEvaluation", "RMSE, MAE, R$^2$, Accuracy, F1-score"),
        ("Model Comparison", "Compare multiple algorithms"),
        ("Error Analysis", "Residuals, Bias, Overfitting check"),
        ("Explainability", "SHAP, Feature Importance"),
        ("Final Model Selection", "Choose best model for prediction"),
    ]),
    ("6. PREDICTION & OUTPUT", [
        ("Prediction", "Yield, Irrigation demand, Disease risk, Soil moisture"),
        ("Spatial Mapping", "Convert predictions to GIS layers"),
        ("Time-Series Forecasting", "Future conditions, Trends"),
        ("Alerts &\nRecommendations", "Irrigation advice, Disease alerts, Plans"),
        ("Export & Reporting", "Maps, Reports, API, Dashboards"),
    ]),
]

foundations = [
    ("DATA MANAGEMENT",
     ["Secure Storage", "Metadata", "Data Versioning", "Quality Control"]),
    ("COMPUTING INFRASTRUCTURE",
     ["Cloud / Edge Computing", "High Performance GPUs", "Scalable Storage",
      "Parallel Processing"]),
    ("CONTINUOUS LEARNING",
     ["New Data Ingestion", "Model Retraining", "Performance Monitoring",
      "Model Update"]),
    ("DECISION SUPPORT SYSTEM",
     ["Web GIS Dashboard", "Interactive Visualization", "User Feedback",
      "Decision Support"]),
]

# =============================================================================
# GEOMETRY
# =============================================================================
XW, FIGW = 100.0, 19.6
n = 6
GAPC = 1.3
CW = (XW - 2.0 - GAPC * (n - 1)) / n
X0 = 1.0
colx = [X0 + i * (CW + GAPC) for i in range(n)]
centers = [c + CW / 2 for c in colx]

HDR_H = 3.9
IT_H, IT_GAP = 8.6, 0.6
TOP = 82.0
body_top = TOP - HDR_H - 0.8
body_h = len(stages[0][1]) * IT_H + (len(stages[0][1]) - 1) * IT_GAP + 1.6
body_y = body_top - body_h

fig, ax = plt.subplots(figsize=(FIGW, FIGW * 85.0 / XW))
ax.set_xlim(0, XW); ax.set_ylim(0, 85); ax.axis("off")

UNIT_PT = FIGW / XW * 72.0                    # points per data unit
def fit(text, max_units, base, cwf=0.60):
    allowed = max_units * UNIT_PT
    return max(9.5, min(base, allowed / (cwf * max(len(text), 1))))

WRAP = 26
def wrap(det):
    words, lines, cur = det.split(" "), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > WRAP:
            lines.append(cur); cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines[:3]

# ---- stages ----
for i, (header, items) in enumerate(stages):
    x = colx[i]; base = SBASE[i]
    hf = base
    bf = tint(base, 0.90); bd = tint(base, 0.42); tcol = shade(base, 0.38)
    box(ax, x, body_y, CW, body_h, bf, bd, r=0.6, lw=1.4, z=2)
    box(ax, x, TOP - HDR_H, CW, HDR_H, hf, hf, r=0.6, lw=0, z=3)
    ax.text(x + CW / 2, TOP - HDR_H / 2, header, ha="center", va="center",
            color=hdr_text(base), fontsize=fit(header, CW - 2.2, FS_HDR),
            fontweight="bold", zorder=4)
    iy = body_top - 0.7
    for title, det in items:
        iy -= IT_H
        box(ax, x + 0.7, iy, CW - 1.4, IT_H, "white", bd, r=0.4, lw=1.0, z=4)
        ntl = title.count("\n") + 1
        longest = max(title.split("\n"), key=len)
        tfs = fit(longest, CW - 2.0, FS_IT)
        ax.text(x + 1.3, iy + IT_H - 1.4, title, ha="left", va="top",
                color=tcol, fontsize=tfs, fontweight="bold", zorder=5,
                linespacing=0.98)
        ty = iy + IT_H - 1.4 - ntl * 1.78 - 0.55
        for ln in wrap(det):
            ax.text(x + 1.3, ty, ln, ha="left", va="top",
                    color=SUBINK, fontsize=FS_DET, zorder=5)
            ty -= LINE

# ---- inter-stage arrows (centred in the pipeline band) ----
arr_y = body_y + body_h / 2
for i in range(n - 1):
    arrow(ax, (colx[i] + CW + 0.1, arr_y), (colx[i + 1] - 0.1, arr_y),
          ARR[i], lw=3.4, ms=22)

# =============================================================================
# FOUNDATION BLOCKS + strictly-vertical connected risers
# =============================================================================
FGAP = 2.0
FW = (XW - 2.0 - FGAP * 3) / 4
fnd_x = [1.0 + j * (FW + FGAP) for j in range(4)]
FH = 14.4
FY = body_y - 2.4 - FH

for j, (title, items) in enumerate(foundations):
    x = fnd_x[j]; base = FBASE[j]
    tcol = shade(base, 0.34); bd = tint(base, 0.46); bf = tint(base, 0.92)
    box(ax, x, FY, FW, FH, bf, bd, r=0.6, lw=1.4, z=2)
    ax.text(x + FW / 2, FY + FH - 1.9, title, ha="center", va="center",
            color=tcol, fontsize=FS_FND, fontweight="bold", zorder=4)
    ax.add_line(Line2D([x + 2, x + FW - 2], [FY + FH - 3.2, FY + FH - 3.2],
                color=bd, lw=0.9, zorder=4))
    ty = FY + FH - 4.9
    for it in items:
        ax.text(x + 2.4, ty, "\u2022 " + it, ha="left", va="center",
                color=INK, fontsize=FS_DET, zorder=4)
        ty -= 2.15

# risers: start at each block's top (snapped to the nearest stage centre, which
# lies inside the block) and go straight UP into that stage's body. Colour = block.
for j in range(4):
    fc = fnd_x[j] + FW / 2
    xc = min(centers, key=lambda c: abs(c - fc))     # nearest stage centre
    arrow(ax, (xc, FY + FH), (xc, body_y), shade(FBASE[j], 0.10),
          lw=1.9, dashed=True, ms=13)

# =============================================================================
# LEGEND (horizontal, close under the foundation blocks)
# =============================================================================
leg = [("Data Flow", LEGCOL[0], "-"), ("Processing Flow", LEGCOL[1], "-"),
       ("Modeling Flow", LEGCOL[2], "-"), ("Output Flow", LEGCOL[3], "-"),
       ("Feedback / Iteration", FB, (0, (4, 2)))]
ly = FY - 2.6
x = 20.0
ax.text(x - 2.0, ly, "FLOW:", ha="right", va="center", color=INK,
        fontsize=FS_FND, fontweight="bold", zorder=5)
step = 15.6
for i, (label, col, ls) in enumerate(leg):
    lx0 = x + i * step
    ax.add_line(Line2D([lx0, lx0 + 2.9], [ly, ly], color=col, lw=2.8,
                linestyle=ls, zorder=5))
    ax.annotate("", xy=(lx0 + 3.3, ly), xytext=(lx0 + 2.8, ly),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=2.8), zorder=5)
    ax.text(lx0 + 4.0, ly, label, ha="left", va="center", color=INK,
            fontsize=FS_DET, zorder=5)

# crop to content
YMIN = ly - 3.0
ax.set_ylim(YMIN, 85)
fig.set_size_inches(FIGW, FIGW * (85 - YMIN) / XW)
plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
fig.savefig("fig04_ai_workflow.png", dpi=300, bbox_inches="tight")
fig.savefig("fig04_ai_workflow.pdf", bbox_inches="tight")
print("wrote fig04_ai_workflow.png and fig04_ai_workflow.pdf")
