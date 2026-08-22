"""
Spectral indices and multi-source predictor stack.

Derivation of spectral indices (NDVI, GNDVI, EVI, SAVI, NDWI, NDMI) and
assembly of the multi-source predictor stack (paper Section 2.3).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np, rasterio
from rasterio.enums import Resampling

BANDS = {"blue": "B02", "green": "B03", "red": "B04",
         "nir": "B08", "swir": "B11"}

def read_band(path, shape):
    with rasterio.open(path) as src:
        return src.read(1, out_shape=shape,
                        resampling=Resampling.bilinear).astype("float32")

def spectral_indices(b):
    eps = 1e-6
    ndvi = (b["nir"] - b["red"]) / (b["nir"] + b["red"] + eps)
    gndvi = (b["nir"] - b["green"]) / (b["nir"] + b["green"] + eps)
    savi = 1.5 * (b["nir"] - b["red"]) / (b["nir"] + b["red"] + 0.5)
    evi = 2.5 * (b["nir"] - b["red"]) / (
        b["nir"] + 6 * b["red"] - 7.5 * b["blue"] + 1 + eps)
    ndwi = (b["green"] - b["nir"]) / (b["green"] + b["nir"] + eps)
    ndmi = (b["nir"] - b["swir"]) / (b["nir"] + b["swir"] + eps)
    return {"NDVI": ndvi, "GNDVI": gndvi, "EVI": evi,
            "SAVI": savi, "NDWI": ndwi, "NDMI": ndmi}

def build_stack(scene, terrain, sensors, shape):
    bands = {k: read_band(scene[v], shape) for k, v in BANDS.items()}
    feats = spectral_indices(bands)
    feats.update({k: read_band(p, shape) for k, p in terrain.items()})
    feats.update({k: read_band(p, shape) for k, p in sensors.items()})
    names = sorted(feats)
    X = np.stack([feats[n] for n in names], axis=-1)
    return X.reshape(-1, len(names)), names
