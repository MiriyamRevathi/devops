from typing import Dict, Any
from utils.helpers import get_utc_now_iso

class ProjectHealthReport:
    def __init__(
        self,
        project_id: str,
        build_success_rate: float,
        open_incidents_count: int,
        active_deployments_count: int,
        health_score: float = 100.0
    ):
        self.project_id = project_id
        self.build_success_rate = build_success_rate
        self.open_incidents_count = open_incidents_count
        self.active_deployments_count = active_deployments_count
        self.health_score = max(0.0, min(100.0, health_score - (open_incidents_count * 15.0) + (build_success_rate * 0.2)))
        self.evaluated_at = get_utc_now_iso()

    def get_status_badge(self) -> str:
        if self.health_score >= 85.0:
            return "HEALTHY"
        elif self.health_score >= 60.0:
            return "DEGRADED"
        return "CRITICAL"
