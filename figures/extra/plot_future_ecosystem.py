#!/usr/bin/env python3
# =============================================================================
# Future smart-agriculture ecosystem (fig07) - RADIAL "flower" layout.
# A central hub concept with eight thematic petals arranged around it, a
# continuous-learning feedback ring, and a flow legend. No clip-art; all textual
# content preserved. Distinct palette + geometry from the other figures.
#
# Output: fig07_future_ecosystem.png / .pdf   |  Requires: matplotlib, numpy
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
from matplotlib.lines import Line2D

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]
INK, SUBINK = "#20242B", "#4A4F58"

# ------------------------------ content --------------------------------------
# eight petals, clockwise from top; (title, [bullets], colour)
PETALS = [
    ("1. Intelligent Data Acquisition",
     ["Satellites (multi/hyperspectral)", "Drones / UAVs", "Wireless sensor networks",
      "Weather stations", "IoT devices & machinery", "Open data & external sources"],
     "#5884B3"),
    ("2. Cloud & Edge Infrastructure",
     ["Edge gateways", "Cloud storage", "Scalable compute", "Data pipelines"],
     "#91BE64"),
    ("3. AI & Analytics Engine",
     ["Machine & deep learning", "Predictive analytics & forecasting",
      "Optimization & decision-making"],
     "#CC6686"),
    ("4. Digital Twin & Simulation",
     ["Virtual farm models", "Scenario simulation", "What-if analysis",
      "Risk assessment", "Resource optimization"],
     "#E5CF6C"),
    ("5. Decision Support System",
     ["Real-time insights", "Alerts & notifications", "Recommendations",
      "Dashboards & reports", "Mobile & web access"],
     "#E87B70"),
    ("6. Smart Actuation & Automation",
     ["Variable-rate irrigation", "Precision fertilization", "Autonomous machinery",
      "Greenhouse automation", "Robotics & monitoring"],
     "#5BBE94"),
    ("7. Sustainability Outcomes",
     ["Water-use efficiency", "Soil-health monitoring", "Climate resilience",
      "Carbon-footprint reduction", "Food security & quality"],
     "#E5B5C5"),
    ("8. Stakeholders & Beneficiaries",
     ["Farmers", "Agronomists", "Researchers", "Policymakers",
      "Agri-businesses", "Consumers"],
     "#B6E3D1"),
]

def lum(hx):
    c=[int(hx[i:i+2],16)/255 for i in (1,3,5)]
    return 0.299*c[0]+0.587*c[1]+0.114*c[2]
def htext(hx):
    return "white" if lum(hx) < 0.62 else "#20242B"

def tint(hx, f):
    c = tuple(int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    return tuple(x + (1 - x) * f for x in c)
def shade(hx, f):
    c = tuple(int(hx[i:i+2], 16) / 255 for i in (1, 3, 5))
    return tuple(x * (1 - f) for x in c)

FS_HUB, FS_T, FS_B, FS_LBL = 15.0, 12.0, 10.3, 11.0

# ------------------------------ helpers --------------------------------------
def rbox(ax, x, y, w, h, fill, edge, r=0.55, lw=1.5, z=3):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z))

def wrap(t, n):
    words, lines, cur = t.split(" "), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

# =============================================================================
# CANVAS
# =============================================================================
fig, ax = plt.subplots(figsize=(15.5, 15.5))
ax.set_xlim(-108, 108); ax.set_ylim(-108, 108); ax.axis("off"); ax.set_aspect("equal")

# ---- central hub ----
hubR = 20
ax.add_patch(Circle((0, 0), hubR + 2.0, facecolor="none",
             edgecolor="#8A8F98", lw=1.0, ls=(0, (4, 3)), zorder=2))
ax.add_patch(Circle((0, 0), hubR, facecolor="#20303A", edgecolor="#0F1A22",
             lw=2.0, zorder=4))
for i, ln in enumerate(["FUTURE SMART", "AGRICULTURE", "ECOSYSTEM"]):
    ax.text(0, 5.5 - i * 5.0, ln, ha="center", va="center", color="white",
            fontsize=FS_HUB, fontweight="bold", zorder=5)
ax.text(0, -10.5, "data-driven \u00b7 AI-powered", ha="center", va="center",
        color="#BFD8CE", fontsize=FS_B - 0.5, zorder=5)
ax.text(0, -13.6, "connected \u00b7 sustainable", ha="center", va="center",
        color="#BFD8CE", fontsize=FS_B - 0.5, zorder=5)

# =============================================================================
# eight petals around the hub
# =============================================================================
n = len(PETALS)
R = 66.2                                 # petal-centre radius (mean connector ~30 units)
PW, base_h = 45, 8.5                     # petal width / base height per petal
ang0 = 90                                # first petal at top
PH_CONST = base_h + 6 * 3.1 + 3.0        # uniform petal height (largest content)
for i, (title, bullets, col) in enumerate(PETALS):
    a = np.deg2rad(ang0 - i * (360 / n))     # clockwise (equal 45 deg spacing)
    cx, cy = R * np.cos(a), R * np.sin(a)
    ph = PH_CONST                             # UNIFORM height -> even visual spacing
    fill, edge = tint(col, 0.90), col
    rbox(ax, cx, cy, PW, ph, fill, edge, r=0.7, lw=1.8, z=3)
    # colour header strip
    hstrip = 5.2
    ax.add_patch(FancyBboxPatch((cx - PW/2, cy + ph/2 - hstrip), PW, hstrip,
                 boxstyle="round,pad=0.02,rounding_size=0.7",
                 facecolor=col, edgecolor=col, zorder=4))
    tlines = wrap(title, 26)
    for j, hl in enumerate(tlines):
        ax.text(cx, cy + ph/2 - 2.0 - j*2.4, hl, ha="center", va="center",
                color=htext(col), fontsize=FS_T, fontweight="bold", zorder=5)
    # vertically CENTRE the bullet block in the remaining space
    body_top = cy + ph/2 - hstrip - 1.2
    body_bot = cy - ph/2 + 2.0
    blk = (len(bullets) - 1) * 3.1
    ty = (body_top + body_bot) / 2 + blk / 2
    for b in bullets:
        ax.text(cx - PW/2 + 2.4, ty, "\u2022 " + b, ha="left", va="center",
                color=INK, fontsize=FS_B, zorder=5)
        ty -= 3.1
    # connector hub -> petal (colour = petal), behind boxes
    ex, ey = (hubR + 1.5) * np.cos(a), (hubR + 1.5) * np.sin(a)
    px, py = cx - (PW/2 - 3) * np.cos(a), cy - (ph/2 - 3) * np.sin(a)
    ax.add_patch(FancyArrowPatch((ex, ey), (px, py), arrowstyle="-|>",
                 mutation_scale=15, lw=2.0, color=col, zorder=2,
                 shrinkA=1, shrinkB=1))

# =============================================================================
# continuous-learning feedback ring (dashed arc arrows around the hub)
# =============================================================================
fbR = hubR + 10
for k in range(4):
    t0 = 20 + k * 90
    ax.add_patch(Wedge((0, 0), fbR, t0, t0 + 55, width=0.1, fill=False,
                 edgecolor="#5A9E6F", lw=2.0, ls=(0, (5, 3)), zorder=2))
    # arrowhead at each arc end
    ae = np.deg2rad(t0 + 55)
    ax.add_patch(FancyArrowPatch((fbR*np.cos(ae-0.02), fbR*np.sin(ae-0.02)),
                 (fbR*np.cos(ae), fbR*np.sin(ae)), arrowstyle="-|>",
                 mutation_scale=13, lw=2.0, color="#5A9E6F", zorder=2))
ax.text(0, hubR + 12.6, "continuous learning & improvement", ha="center",
        va="center", color="#3E7A2E", fontsize=FS_B - 0.5, fontstyle="italic",
        zorder=6)

# =============================================================================
# outcome banner + flow legend (bottom)
# =============================================================================
ax.text(0, -99, "Better decisions  \u00b7  higher yields  \u00b7  lower costs  "
        "\u00b7  sustainable future", ha="center", va="center",
        color=INK, fontsize=FS_LBL, fontweight="bold")

leg = [("Data flow", "#2B6CB0", (0,(1,2))), ("Analytics flow", "#5B4B8A", (0,(1,2))),
       ("Decision flow", "#2E6B4F", "-"), ("Actuation flow", "#B4611E", (0,(4,3))),
       ("Feedback loop", "#5A9E6F", (0,(4,3)))]
x0, y0, step = -74, -106, 30
for i,(lb,cc,ls) in enumerate(leg):
    lx = x0 + i*step
    ax.add_line(Line2D([lx, lx+5], [y0, y0], color=cc, lw=2.2, linestyle=ls, zorder=5))
    ax.annotate("", xy=(lx+5.6, y0), xytext=(lx+5.0, y0),
                arrowprops=dict(arrowstyle="-|>", color=cc, lw=2.2), zorder=5)
    ax.text(lx+7.0, y0, lb, ha="left", va="center", color=INK, fontsize=FS_B-0.5)

plt.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
fig.savefig("fig07_future_ecosystem.png", dpi=300, bbox_inches="tight")
fig.savefig("fig07_future_ecosystem.pdf", bbox_inches="tight")
print("wrote fig07_future_ecosystem.png and .pdf")
