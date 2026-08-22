"""
Ordinary kriging with variance surface.

Ordinary kriging of wireless-sensor observations onto the analysis grid,
returning both the interpolated surface and its variance (paper Section 2.6).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np, rasterio
from pykrige.ok import OrdinaryKriging
from rasterio.transform import from_origin

def krige_to_raster(x, y, z, bounds, res, out_tif, crs="EPSG:5254"):
    xmin, ymin, xmax, ymax = bounds
    gx = np.arange(xmin, xmax, res)
    gy = np.arange(ymin, ymax, res)
    ok = OrdinaryKriging(x, y, z, variogram_model="spherical",
                         enable_plotting=False)
    zhat, variance = ok.execute("grid", gx, gy)
    grid = np.flipud(np.asarray(zhat))
    prof = dict(driver="GTiff", height=grid.shape[0],
                width=grid.shape[1], count=1, dtype="float32",
                crs=crs, transform=from_origin(xmin, ymax, res, res))
    with rasterio.open(out_tif, "w", **prof) as dst:
        dst.write(grid.astype("float32"), 1)
    return out_tif, np.asarray(variance)
