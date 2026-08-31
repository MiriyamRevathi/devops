"""
Extended Analytics Engine for alerts module.
Calculates historical percentiles, trend regression, and operational efficiency metrics.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

class AlertsExtendedAnalytics:
    """Advanced telemetry and trend analyzer for alerts."""
    def __init__(self, data_series: List[Dict[str, Any]] = None):
        self.data_series = data_series or []

    def calculate_percentiles(self, metric_key: str = "duration") -> Dict[str, float]:
        if not self.data_series:
            return {"p50": 0.0, "p90": 0.0, "p99": 0.0}
        values = [r.get(metric_key, 0.0) for r in self.data_series if metric_key in r]
        if not values:
            return {"p50": 0.0, "p90": 0.0, "p99": 0.0}
        arr = np.array(values)
        return {
            "p50": round(float(np.percentile(arr, 50)), 2),
            "p90": round(float(np.percentile(arr, 90)), 2),
            "p99": round(float(np.percentile(arr, 99)), 2)
        }

    def calculate_rolling_average(self, window_size: int = 5) -> List[float]:
        if not self.data_series:
            return []
        df = pd.DataFrame(self.data_series)
        if "value" in df.columns:
            return list(df["value"].rolling(window=window_size, min_periods=1).mean())
        return []
