"""
Historical Performance Reporter for alerts.
Aggregates operational activity data into summary reports.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

class AlertsReporter:
    """Generates historical execution and telemetry reports for alerts."""
    def __init__(self, records: List[Dict[str, Any]] = None):
        self.records = records or []

    def generate_monthly_summary(self) -> Dict[str, Any]:
        if not self.records:
            return {"total_records": 0, "status_breakdown": {}}
        df = pd.DataFrame(self.records)
        status_counts = df["status"].value_counts().to_dict() if "status" in df.columns else {}
        return {
            "total_records": len(self.records),
            "status_breakdown": status_counts
        }
