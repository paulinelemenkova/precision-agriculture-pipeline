"""
AHP weighting and weighted overlay.

Analytic Hierarchy Process weighting with a consistency-ratio guard and GIS
weighted overlay for land-suitability classification (paper Section 2.5).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np

def ahp_weights(pcm):
    # Priority vector and consistency ratio of a pairwise
    # comparison matrix of expert judgements.
    norm = pcm / pcm.sum(axis=0)
    w = norm.mean(axis=1)
    n = pcm.shape[0]
    lambda_max = (pcm @ w / w).mean()
    ci = (lambda_max - n) / (n - 1)
    ri = {2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24,
          7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}[n]
    return w, ci / (ri if ri > 0 else 1.0)

def weighted_overlay(criteria, pcm, names):
    w, cr = ahp_weights(pcm)
    if cr > 0.10:
        raise ValueError(f"inconsistent judgements (CR={cr:.2f})")
    suitability = sum(w[i] * criteria[n] for i, n in enumerate(names))
    classes = np.digitize(suitability, [1.5, 2.5, 3.5])
    return suitability, classes, dict(zip(names, w.round(3)))
