"""
Predictive Analytics and Metrics Estimator for pipelines.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

class PipelinesPredictiveAnalytics:
    """Calculates statistical forecasts and performance metrics for pipelines."""
    def __init__(self, historical_data: List[Dict[str, Any]] = None):
        self.historical_data = historical_data or []

    def forecast_failure_probability(self) -> float:
        if not self.historical_data:
            return 0.05
        failures = sum(1 for d in self.historical_data if d.get("status") in ["FAILED", "ERROR", "DOWN"])
        total = len(self.historical_data)
        return round(float(failures / total), 4) if total > 0 else 0.05

    def calculate_percentile_distribution(self, key: str = "duration_seconds") -> Dict[str, float]:
        if not self.historical_data:
            return {"p50": 0.0, "p90": 0.0, "p99": 0.0}
        vals = [float(d[key]) for d in self.historical_data if key in d and isinstance(d[key], (int, float))]
        if not vals:
            return {"p50": 0.0, "p90": 0.0, "p99": 0.0}
        arr = np.array(vals)
        return {
            "p50": round(float(np.percentile(arr, 50)), 2),
            "p90": round(float(np.percentile(arr, 90)), 2),
            "p99": round(float(np.percentile(arr, 99)), 2)
        }
