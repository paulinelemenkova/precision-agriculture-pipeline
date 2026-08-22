"""
Sentinel-2 preparation.

Scene-classification cloud masking and median NDVI compositing of
Sentinel-2 imagery (paper Section 2.3).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np, rasterio, glob
from rasterio.enums import Resampling

def scl_cloud_mask(scl):
    # Keep vegetation (4), bare soil (5), water (6); drop cloud,
    # shadow, snow/ice, cirrus and unclassified classes.
    return np.isin(scl, [4, 5, 6])

def boa_to_reflectance(dn, add_offset=-1000, quant=10000.0):
    return (dn.astype("float32") + add_offset) / quant

def ndvi_from_scene(folder):
    red = rasterio.open(glob.glob(f"{folder}/*B04*.jp2")[0])
    nir = rasterio.open(glob.glob(f"{folder}/*B08*.jp2")[0])
    scl = rasterio.open(glob.glob(f"{folder}/*SCL*.jp2")[0])
    r = boa_to_reflectance(red.read(1))
    n = boa_to_reflectance(nir.read(1))
    scl10 = scl.read(1, out_shape=r.shape,
                     resampling=Resampling.nearest)
    mask = scl_cloud_mask(scl10)
    ndvi = np.where(mask, (n - r) / (n + r + 1e-6), np.nan)
    return ndvi, red.profile

def monthly_composite(scene_dirs, out_tif):
    stack, prof = [], None
    for d in sorted(scene_dirs):
        ndvi, prof = ndvi_from_scene(d)
        stack.append(ndvi)
    comp = np.nanmedian(np.stack(stack), axis=0)
    prof.update(driver="GTiff", dtype="float32", count=1, nodata=np.nan)
    with rasterio.open(out_tif, "w", **prof) as dst:
        dst.write(comp.astype("float32"), 1)
    return out_tif
