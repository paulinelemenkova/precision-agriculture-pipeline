"""
Hyperparameter search and SHAP attribution.

Randomized hyperparameter search for the gradient-boosting model with SHAP
attribution of predictor contributions (paper Section 2.4).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import numpy as np, pandas as pd, shap
from scipy.stats import randint, uniform
from sklearn.model_selection import RandomizedSearchCV, GroupKFold
from xgboost import XGBRegressor

SPACE = {"n_estimators": randint(300, 1200),
         "max_depth": randint(3, 10),
         "learning_rate": uniform(0.01, 0.2),
         "subsample": uniform(0.6, 0.4),
         "colsample_bytree": uniform(0.6, 0.4),
         "reg_lambda": uniform(0.0, 5.0)}

def tune_and_explain(X, y, groups, names, n_iter=60, seed=42):
    search = RandomizedSearchCV(
        XGBRegressor(objective="reg:squarederror", n_jobs=-1,
                     random_state=seed),
        SPACE, n_iter=n_iter, cv=GroupKFold(5),
        scoring="neg_root_mean_squared_error", random_state=seed)
    search.fit(X, y, groups=groups)
    best = search.best_estimator_
    sv = shap.TreeExplainer(best).shap_values(X)
    importance = pd.Series(np.abs(sv).mean(axis=0), index=names)
    return best, search.best_params_, importance.sort_values(ascending=False)
