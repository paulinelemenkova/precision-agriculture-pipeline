#!/usr/bin/env python3
# =============================================================================
# IWSN node architecture + communication topology (fig08) - corrected to match
# the paper methodology (Sec. 4.2-4.3, communication paragraphs) and Listing
# lst:iwsn. Same general flat design as before.
#
# Corrections vs. previous figure:
#   * gateway -> edge link relabelled as a plain LOCAL link (paper says the edge
#     device is local to the gateway); the spurious "wired / Wi-Fi" is removed.
#   * "despiking (QC)" -> "Hampel despiking" (the exact method in lst:iwsn).
#   * added "store-and-forward buffer" at the gateway/edge (the paper's edge-
#     buffering / intermittent-connectivity robustness claim).
#
# Output: fig08_iwsn_node_topology.png / .pdf   |  Requires: matplotlib
# =============================================================================

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from matplotlib.lines import Line2D

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]

# ------------------------------ palette --------------------------------------
GREEN  = ("#3E7A2E", "#9CC08A", "#EDF5E7")   # node / sensors
BLUE   = ("#2B6CB0", "#8FB8E0", "#E6F0FA")   # gateway
ORANGE = ("#B4611E", "#E3B583", "#FBF1E6")   # edge device
VIOLET = ("#5B4B8A", "#B7ACD6", "#F0EDF8")   # cloud
GREY   = ("#39404A", "#9AA3AD", "#F0F1F3")   # node enclosure
INK, SUBINK = "#20242B", "#4A4F58"
A_LORA, A_LOCAL, A_BACK, A_DOWN = "#2E7D32", "#2B6CB0", "#B4611E", "#5B4B8A"

FS_T, FS_B, FS_LBL = 16.5, 14.5, 14.5

# ------------------------------ helpers --------------------------------------
def box(ax, x, y, w, h, fill, edge, r=0.35, lw=1.6, z=2, dashed=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={r}",
                 facecolor=fill, edgecolor=edge, linewidth=lw, zorder=z,
                 linestyle=(0, (5, 3)) if dashed else "-"))

def arrow(ax, p1, p2, color, lw=3.0, dashed=False, ms=20, rad=0.0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=ms,
                 lw=lw, color=color, zorder=6, shrinkA=2, shrinkB=2,
                 connectionstyle=f"arc3,rad={rad}",
                 linestyle=(0, (2, 2)) if dashed else "-"))

# =============================================================================
# CANVAS
# =============================================================================
fig, ax = plt.subplots(figsize=(19.0, 7.1))
ax.set_xlim(0, 110); ax.set_ylim(0, 41); ax.axis("off")

# =============================================================================
# 1) IWSN SENSOR NODE (dashed enclosure with sensor + hardware cards)
# =============================================================================
nx, ny, nw, nh = 1.0, 2.5, 20.0, 36.5
box(ax, nx, ny, nw, nh, "#F2F3F4", GREY[0], r=0.6, lw=1.8, z=1, dashed=True)
ax.text(nx + nw / 2, ny + nh - 2.2, "IWSN sensor node", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
ax.text(nx + nw / 2, ny + nh - 4.3, "(internal architecture)", ha="center",
        va="center", color=SUBINK, fontsize=FS_B - 1.0)

sensors = ["Soil moisture", "Soil temperature", "Air temp. & humidity",
           "Nutrients (EC probe)"]
hw = ["MCU + LoRa radio", "Battery + solar"]
card_h, gap = 3.5, 0.7
cy = ny + nh - 5.4
for s in sensors:
    cy -= card_h
    box(ax, nx + 1.4, cy, nw - 2.8, card_h, GREEN[2], GREEN[1], r=0.3, lw=1.3, z=3)
    ax.text(nx + nw / 2, cy + card_h / 2, s, ha="center", va="center",
            color=GREEN[0], fontsize=FS_B, fontweight="bold")
    cy -= gap
cy -= 0.6
for h in hw:
    cy -= card_h
    box(ax, nx + 1.4, cy, nw - 2.8, card_h, "white", GREY[0], r=0.3, lw=1.3, z=3)
    ax.text(nx + nw / 2, cy + card_h / 2, h, ha="center", va="center",
            color=INK, fontsize=FS_B)
    cy -= gap

# =============================================================================
# 2) FIELD NODES (three) -> converge to gateway
# =============================================================================
fnx, fnw, fnh = 24.5, 9.0, 5.6
node_y = [26.0, 18.0, 10.0]
node_mid = []
for i, yy in enumerate(node_y):
    box(ax, fnx, yy, fnw, fnh, GREEN[2], GREEN[0], r=0.35, lw=1.6, z=3)
    ax.text(fnx + fnw / 2, yy + fnh / 2, f"Node {i+1}", ha="center", va="center",
            color=INK, fontsize=FS_B, fontweight="bold")
    node_mid.append((fnx + fnw, yy + fnh / 2))
# The enclosure is the internal architecture of EACH field node (not one
# specific node). Show this with a curly brace spanning the node stack and a
# single "expands to" arrow, instead of lines that single out particular nodes.
bx = nx + nw + 0.6                    # brace x, just right of the enclosure
b_top, b_bot = node_y[0] + fnh, node_y[2]   # span the whole node stack
b_mid = (b_top + b_bot) / 2
# vertical brace
ax.add_line(Line2D([bx, bx], [b_bot, b_top], color=GREY[0], lw=1.6, zorder=2))
ax.add_line(Line2D([bx, bx + 0.9], [b_top, b_top], color=GREY[0], lw=1.6, zorder=2))
ax.add_line(Line2D([bx, bx + 0.9], [b_bot, b_bot], color=GREY[0], lw=1.6, zorder=2))
# short arrow from the enclosure into the brace, with an explanatory label
ax.add_patch(FancyArrowPatch((nx + nw, b_mid), (fnx - 0.3, b_mid),
             arrowstyle="-|>", mutation_scale=15, lw=1.6, color=GREY[0], zorder=2))


# =============================================================================
# 3) LoRaWAN GATEWAY (packet concentrator + store-and-forward)
# =============================================================================
gx, gy, gw, gh = 40.0, 14.0, 15.0, 14.5
box(ax, gx, gy, gw, gh, BLUE[2], BLUE[0], r=0.4, lw=1.8, z=3)
ax.text(gx + gw / 2, gy + gh - 2.6, "LoRaWAN", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
ax.text(gx + gw / 2, gy + gh - 5.0, "gateway", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
ax.text(gx + gw / 2, gy + gh - 8.2, "packet concentrator", ha="center", va="center",
        color=SUBINK, fontsize=FS_B)
ax.text(gx + gw / 2, gy + gh - 11.0, "store-and-forward\nbuffer", ha="center",
        va="center", color=SUBINK, fontsize=FS_B, linespacing=0.95)
# little antenna (mast + node) with a small grey explanatory label
ax.add_line(Line2D([gx + gw / 2, gx + gw / 2], [gy + gh, gy + gh + 3.0],
            color=BLUE[0], lw=2.2, zorder=4))
ax.add_patch(Circle((gx + gw / 2, gy + gh + 3.3), 0.7, color=BLUE[0], zorder=5))
ax.text(gx + gw / 2 + 1.4, gy + gh + 3.3, "antenna\n(radio front-end)", ha="left",
        va="center", color="#7A7F87", fontsize=FS_B - 3.0, linespacing=0.95)

# LoRaWAN uplinks node -> gateway: land on three DISTINCT points on the gateway
# left edge so all three arrows read clearly (Node 2 no longer hidden).
gin_pts = [(gx, gy + gh * 0.72),   # Node 1 -> upper
           (gx, gy + gh * 0.50),   # Node 2 -> middle
           (gx, gy + gh * 0.28)]   # Node 3 -> lower
for (mx, my), gpt in zip(node_mid, gin_pts):
    rad = 0.10 * (my - gpt[1]) / 20.0
    arrow(ax, (mx, my), gpt, A_LORA, lw=3.0, ms=20, rad=rad)
ax.text(34.0, 32.2, "LoRaWAN uplink", ha="left", va="center",
        color=A_LORA, fontsize=FS_LBL, fontweight="bold")
ax.text(34.0, 30.0, "(868 MHz, low power)", ha="left", va="center",
        color=A_LORA, fontsize=FS_B)

# =============================================================================
# 4) EDGE DEVICE (local link from gateway) - QC chain from Listing lst:iwsn
# =============================================================================
ex, ey, ew, eh = 64.0, 11.5, 16.0, 19.5
box(ax, ex, ey, ew, eh, ORANGE[2], ORANGE[0], r=0.4, lw=1.8, z=3)
ax.text(ex + ew / 2, ey + eh - 2.6, "Edge device", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
ax.text(ex + ew / 2, ey + eh - 4.6, "(local to gateway)", ha="center", va="center",
        color=SUBINK, fontsize=FS_B)
qc = ["range checks", "Hampel despiking", "gap flagging", "edge AI inference"]
qy = ey + eh - 7.0
for q in qc:
    ax.text(ex + ew / 2, qy, q, ha="center", va="center",
            color=INK, fontsize=FS_B)
    qy -= 2.9

# local link gateway -> edge (plain solid; co-located, not Wi-Fi)
arrow(ax, (gx + gw, gy + gh / 2), (ex, ey + eh / 2), A_LOCAL, lw=3.0, ms=20)
ax.text((gx + gw + ex) / 2, gy + gh / 2 + 3.0, "local link", ha="center",
        va="center", color=A_LOCAL, fontsize=FS_B - 0.5)

# =============================================================================
# 5) CLOUD (backhaul up, downlink back)
# =============================================================================
cx, cy2, cw, ch = 94.0, 11.5, 13.0, 21.5
box(ax, cx, cy2, cw, ch, VIOLET[2], VIOLET[0], r=0.4, lw=1.8, z=3)
ax.text(cx + cw / 2, cy2 + ch - 2.6, "Cloud", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
cloud_items = ["GIS spatial\ndatabase", "AI model\ntraining", "SDSS &\ndashboards"]
ciy = cy2 + ch - 6.8
for it in cloud_items:
    ax.text(cx + cw / 2, ciy, it, ha="center", va="center",
            color=SUBINK, fontsize=FS_B, linespacing=0.95)
    ciy -= 5.4

# backhaul edge -> cloud : HORIZONTAL, upper level; label stacked above it
gap_x = (ex + ew + cx) / 2
y_up = ey + eh / 2 + 3.0
arrow(ax, (ex + ew, y_up), (cx, y_up), A_BACK, lw=3.2, ms=22)
ax.text(gap_x, y_up + 5.4, "NB-IoT / 4G-5G", ha="center",
        va="center", color=A_BACK, fontsize=FS_LBL, fontweight="bold")
ax.text(gap_x, y_up + 3.1, "backhaul (uplink)", ha="center",
        va="center", color=A_BACK, fontsize=FS_B)

# downlink cloud -> edge : HORIZONTAL, lower level; label stacked below it
y_dn = ey + eh / 2 - 3.0
arrow(ax, (cx, y_dn), (ex + ew, y_dn), A_DOWN, lw=2.6, dashed=True, ms=18)
ax.text(gap_x, y_dn - 3.1, "downlink:", ha="center",
        va="center", color=A_DOWN, fontsize=FS_B, fontweight="bold")
ax.text(gap_x, y_dn - 5.4, "alerts, advice", ha="center",
        va="center", color=A_DOWN, fontsize=FS_B)

# =============================================================================
# "Field nodes" label under the node stack
# =============================================================================
ax.text(fnx + fnw / 2, 6.0, "Field nodes", ha="center", va="center",
        color=INK, fontsize=FS_T, fontweight="bold")
ax.text(fnx + fnw / 2, 3.7, "each = one IWSN sensor node", ha="center",
        va="center", color=SUBINK, fontsize=FS_B - 1.5)

plt.subplots_adjust(left=0.004, right=0.996, top=0.996, bottom=0.004)
fig.savefig("fig08_iwsn_node_topology.png", dpi=300, bbox_inches="tight")
fig.savefig("fig08_iwsn_node_topology.pdf", bbox_inches="tight")
print("wrote fig08_iwsn_node_topology.png and .pdf")
