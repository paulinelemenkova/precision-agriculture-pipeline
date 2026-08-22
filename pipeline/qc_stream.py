"""
Wireless-sensor stream ingestion and quality control.

Range-checking, robust Hampel despiking, bounded gap filling, and temporal
aggregation of IWSN telemetry (paper Section 2.2).

Reference implementation from the paper's Methods (removed from the article
text and released here). Educational/reference code: functions are the exact
building blocks described in the manuscript.
"""

import pandas as pd, numpy as np

LIMITS = {"soil_moisture": (0, 60), "soil_temp": (-10, 60),
          "humidity": (0, 100)}

def load_stream(csv):
    df = pd.read_csv(csv, parse_dates=["timestamp"])
    return df.set_index("timestamp").sort_index()

def flag_outliers(s, k=3.5):
    # Hampel filter: flag spikes from transient sensor faults
    # without removing genuine rainfall or irrigation responses.
    med = s.rolling("6h", center=True).median()
    mad = (s - med).abs().rolling("6h", center=True).median()
    return (s - med).abs() > k * 1.4826 * mad

def qc_resample(df, freq="1h"):
    out = {}
    for col, (lo, hi) in LIMITS.items():
        s = df[col].where(df[col].between(lo, hi))
        s = s.mask(flag_outliers(s))
        s = s.interpolate("time", limit=3).resample(freq).mean()
        out[col] = s
    q = pd.DataFrame(out)
    q["gap_flag"] = q.isna().any(axis=1).astype(int)
    return q
