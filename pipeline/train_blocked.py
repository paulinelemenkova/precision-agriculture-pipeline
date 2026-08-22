"""
Spatially blocked cross-validation.

Spatially blocked cross-validation of a Random Forest regressor, holding out
whole parcels rather than pixels to estimate transfer to unseen fields
(paper Section 2.4).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupKFold
from sklearn.metrics import mean_squared_error, r2_score

def spatial_cv(X, y, blocks, n_splits=5, seed=42):
    # Hold out whole parcels so spatial autocorrelation cannot
    # leak into the test folds.
    cv = GroupKFold(n_splits=n_splits)
    rmse, r2 = [], []
    for tr, te in cv.split(X, y, groups=blocks):
        m = RandomForestRegressor(
            n_estimators=500, min_samples_leaf=5,
            max_features="sqrt", n_jobs=-1, random_state=seed)
        m.fit(X[tr], y[tr])
        p = m.predict(X[te])
        rmse.append(mean_squared_error(y[te], p, squared=False))
        r2.append(r2_score(y[te], p))
    return float(np.mean(rmse)), float(np.mean(r2)), m
