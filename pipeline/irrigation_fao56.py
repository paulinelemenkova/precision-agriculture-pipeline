"""
FAO-56 soil-water balance and irrigation map.

FAO-56 soil-water balance for irrigation scheduling and PyGMT rendering of
the gross irrigation requirement (paper Section 2.7).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np, pandas as pd
# NOTE: pygmt is imported lazily inside map_requirement() so that the
# soil-water-balance functions below work without the GMT stack installed.

def fao56_requirement(et0, kc, rain, eff=0.75):
    etc = et0 * kc
    net = np.maximum(etc - rain, 0.0)
    return etc, net / eff

def schedule(df, kc_curve, taw, p=0.5):
    raw, depletion, events = p * taw, 0.0, []
    for t, row in df.iterrows():
        etc, gross = fao56_requirement(row.et0, kc_curve[t.month], row.rain)
        depletion = max(depletion + etc - row.rain, 0.0)
        if depletion >= raw:
            events.append((t, round(gross, 1)))
            depletion = 0.0
    return pd.DataFrame(events, columns=["date", "gross_mm"])

def map_requirement(grid, region, out_png):
    import pygmt
    fig = pygmt.Figure()
    pygmt.makecpt(cmap="viridis", series=[0, 300, 25])
    fig.grdimage(grid, region=region, projection="M14c", frame=["af"])
    fig.coast(shorelines="0.5p,black", borders="1/0.5p,gray30")
    fig.colorbar(frame=["x+lGross irrigation requirement", "y+lmm"])
    fig.savefig(out_png, dpi=300)
    return out_png
