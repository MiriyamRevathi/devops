"""
Analytics calculations and metrics aggregator for projects.
"""
from typing import List, Dict, Any

class ProjectsAnalyticsEngine:
    """Calculates performance metrics and historical trends for projects."""
    def __init__(self, records: List[Dict[str, Any]] = None):
        self.records = records or []

    def compute_summary_stats(self) -> Dict[str, Any]:
        total = len(self.records)
        active = sum(1 for r in self.records if r.get("status") == "ACTIVE")
        success_rate = round((active / total * 100), 2) if total > 0 else 100.0
        return {
            "total_count": total,
            "active_count": active,
            "success_rate": success_rate
        }
