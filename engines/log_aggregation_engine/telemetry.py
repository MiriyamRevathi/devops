"""
Telemetry & Performance Aggregator for log_aggregation_engine.
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any

class LogAggregationEngineTelemetryAggregator:
    """Aggregates performance telemetry for log_aggregation_engine."""
    def __init__(self, samples: List[Dict[str, Any]] = None):
        self.samples = samples or []

    def compute_performance_metrics(self) -> Dict[str, float]:
        if not self.samples:
            return {"mean": 0.0, "std_dev": 0.0, "max": 0.0}
        df = pd.DataFrame(self.samples)
        if "duration" in df.columns:
            return {
                "mean": round(float(df["duration"].mean()), 2),
                "std_dev": round(float(df["duration"].std()), 2),
                "max": round(float(df["duration"].max()), 2)
            }
        return {"mean": 0.0, "std_dev": 0.0, "max": 0.0}
