"""
Minimal, dependency-light demo of two pipeline modules on synthetic inputs.

Runs with only numpy + pandas installed. It shows:
  1. AHP weighting with the consistency-ratio guard (pipeline.ahp)
  2. FAO-56 irrigation scheduling from a short weather series
     (pipeline.irrigation_fao56.schedule)

    python examples/demo_ahp_fao56.py
"""
import sys, os
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipeline.ahp import ahp_weights
from pipeline.irrigation_fao56 import schedule

# --- 1. AHP: a consistent 4-criteria pairwise-comparison matrix ------------
pcm = np.array([
    [1.0, 2.0, 4.0, 3.0],
    [0.5, 1.0, 2.0, 1.5],
    [0.25, 0.5, 1.0, 0.75],
    [1/3, 2/3, 4/3, 1.0],
])
w, cr = ahp_weights(pcm)
print("AHP priority weights:", np.round(w, 3))
print("Consistency ratio   :", round(float(cr), 4),
      "(accepted)" if cr <= 0.10 else "(REJECTED > 0.10)")

# --- 2. FAO-56: 90-day synthetic season -----------------------------------
rng = pd.date_range("2025-06-01", periods=90, freq="D")
df = pd.DataFrame({
    "et0":  4.5 + 1.5 * np.sin(np.linspace(0, 3.14, 90)),   # mm/day
    "rain": np.where(np.random.default_rng(0).random(90) > 0.85, 8.0, 0.0),
}, index=rng)
kc_curve = {6: 0.6, 7: 1.05, 8: 1.15}   # crop coefficient by calendar month
events = schedule(df, kc_curve, taw=120.0, p=0.5)
print(f"\nFAO-56 irrigation events scheduled: {len(events)}")
print(events.head().to_string(index=False))
