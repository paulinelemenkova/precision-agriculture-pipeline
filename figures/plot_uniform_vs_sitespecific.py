#!/usr/bin/env python3
# =============================================================================
# fig10 - Conceptual uniform vs site-specific irrigation over a heterogeneous
# field. Panels are SCHEMATIC (as the caption states) but now internally
# CONSISTENT with the mechanism:
#   (a) crop water demand D(x,y)            [relative depth, 0-1]
#   (b) site-specific applied depth  A_ss = D + small model error   (~= a)
#   (c) mismatch under UNIFORM        A_uni - D,  A_uni = mean(D) (one rate)
#   (d) mismatch under SITE-SPECIFIC  A_ss  - D   (small, unsystematic)
# => (c) is large & systematic (structural), (d) is small & unsystematic
#    (model error), exactly as the caption/Sec.7 describe.
#
# Output: fig10_uniform_vs_sitespecific.png / .pdf | Requires: matplotlib, numpy
# =============================================================================

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = [
    "Nimbus Sans", "Nimbus Sans L", "NimbusSans", "DejaVu Sans", "Arial", "Helvetica",
]

rng = np.random.default_rng(11)
ny, nx = 10, 10

# --- (a) smooth, spatially-structured crop water demand in [~0.15, ~1.0] -----
yy, xx = np.mgrid[0:ny, 0:nx] / (ny - 1)
D = 0.25 + 0.6*xx + 0.5*yy - 0.35*(xx-0.5)**2      # gradient + curvature
D += 0.06 * rng.standard_normal((ny, nx))          # mild texture
D = np.clip(D, 0.12, 1.0)

# --- (b) site-specific applied depth = demand + small model error ------------
A_ss = np.clip(D + 0.04 * rng.standard_normal((ny, nx)), 0.05, 1.05)

# --- uniform applied depth: ONE field-wide rate (spatially invariant) --------
A_uni = np.full_like(D, D.mean())

# --- mismatches (applied - demand) -------------------------------------------
M_uni = A_uni - D          # (c) large, systematic
M_ss  = A_ss  - D          # (d) small, unsystematic

# consistent diverging scale for both mismatch panels
mmax = max(abs(M_uni).max(), abs(M_ss).max())
dnorm = TwoSlopeNorm(vmin=-mmax, vcenter=0.0, vmax=mmax)

FS_TITLE, FS_CBAR = 16, 13

fig, axes = plt.subplots(2, 2, figsize=(12.6, 11.2))
(a, b), (c, d) = axes

# top row: relative depth (demand vs site-specific applied), shared 0-1 scale
im_top = a.imshow(D, cmap="viridis", vmin=0, vmax=1, aspect="equal")
b.imshow(A_ss, cmap="viridis", vmin=0, vmax=1, aspect="equal")
a.set_title("(a) Crop water demand", fontsize=FS_TITLE, fontweight="bold")
b.set_title("(b) Site-specific applied depth", fontsize=FS_TITLE, fontweight="bold")

# bottom row: mismatches, shared diverging scale
c.imshow(M_uni, cmap="RdBu_r", norm=dnorm, aspect="equal")
im_bot = d.imshow(M_ss, cmap="RdBu_r", norm=dnorm, aspect="equal")
c.set_title("(c) Mismatch under uniform", fontsize=FS_TITLE, fontweight="bold")
d.set_title("(d) Mismatch under site-specific", fontsize=FS_TITLE, fontweight="bold")

for ax in axes.ravel():
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(1.4)

# colourbars
cb1 = fig.colorbar(im_top, ax=[a, b], fraction=0.046, pad=0.02, shrink=0.9)
cb1.set_label("Relative depth\n(0 = none, 1 = full demand)", fontsize=FS_CBAR)
cb1.ax.tick_params(labelsize=FS_CBAR - 1)
cb2 = fig.colorbar(im_bot, ax=[c, d], fraction=0.046, pad=0.02, shrink=0.9)
cb2.set_label("Applied \u2212 demand (relative)\nred: over  \u00b7  blue: under", fontsize=FS_CBAR)
cb2.ax.tick_params(labelsize=FS_CBAR - 1)

fig.suptitle("")  # keep clean; caption in the paper carries the explanation
fig.savefig("fig10_uniform_vs_sitespecific.png", dpi=300, bbox_inches="tight")
fig.savefig("fig10_uniform_vs_sitespecific.pdf", bbox_inches="tight")
print("wrote fig10_uniform_vs_sitespecific.png and .pdf")
print(f"uniform rate = {A_uni.mean():.3f} | RMS mismatch  uniform={np.sqrt((M_uni**2).mean()):.3f}"
      f"  site-specific={np.sqrt((M_ss**2).mean()):.3f}")
