"""
Performance & Operational Risk Analytics for monitoring.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

class MonitoringPerformanceMetrics:
    """Calculates performance benchmarks, percentiles, and SLA compliance for monitoring."""
    def __init__(self, data_points: List[Dict[str, Any]] = None):
        self.data_points = data_points or []

    def calculate_percentiles(self, metric_name: str = "duration_seconds") -> Dict[str, float]:
        if not self.data_points:
            return {"p50": 0.0, "p90": 0.0, "p99": 0.0, "mean": 0.0}
        df = pd.DataFrame(self.data_points)
        if metric_name in df.columns:
            arr = np.array(df[metric_name].dropna())
            if len(arr) > 0:
                return {
                    "p50": round(float(np.percentile(arr, 50)), 2),
                    "p90": round(float(np.percentile(arr, 90)), 2),
                    "p99": round(float(np.percentile(arr, 99)), 2),
                    "mean": round(float(np.mean(arr)), 2)
                }
        return {"p50": 0.0, "p90": 0.0, "p99": 0.0, "mean": 0.0}
