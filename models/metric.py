from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class MetricSample:
    """Domain model for a single metric data point."""

    def __init__(
        self,
        cpu_percent: float,
        memory_percent: float,
        disk_percent: float,
        response_time_ms: float = 120.0,
        error_rate: float = 0.01,
        request_rate: float = 150.0,
        timestamp: Optional[str] = None
    ):
        self.cpu_percent = cpu_percent
        self.memory_percent = memory_percent
        self.disk_percent = disk_percent
        self.response_time_ms = response_time_ms
        self.error_rate = error_rate
        self.request_rate = request_rate
        self.timestamp = timestamp or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "disk_percent": self.disk_percent,
            "response_time_ms": self.response_time_ms,
            "error_rate": self.error_rate,
            "request_rate": self.request_rate,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MetricSample":
        return cls(
            cpu_percent=data.get("cpu_percent", 10.0),
            memory_percent=data.get("memory_percent", 45.0),
            disk_percent=data.get("disk_percent", 60.0),
            response_time_ms=data.get("response_time_ms", 120.0),
            error_rate=data.get("error_rate", 0.01),
            request_rate=data.get("request_rate", 150.0),
            timestamp=data.get("timestamp")
        )

class DORAMetricsResult:
    """Domain model holding calculated DORA metrics results and performance rating."""

    def __init__(
        self,
        deployment_frequency_per_day: float,
        lead_time_hours: float,
        change_failure_rate_percent: float,
        mttr_hours: float,
        rating: str = "High",
        evaluated_at: Optional[str] = None
    ):
        self.deployment_frequency_per_day = deployment_frequency_per_day
        self.lead_time_hours = lead_time_hours
        self.change_failure_rate_percent = change_failure_rate_percent
        self.mttr_hours = mttr_hours
        self.rating = rating
        self.evaluated_at = evaluated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deployment_frequency_per_day": self.deployment_frequency_per_day,
            "lead_time_hours": self.lead_time_hours,
            "change_failure_rate_percent": self.change_failure_rate_percent,
            "mttr_hours": self.mttr_hours,
            "rating": self.rating,
            "evaluated_at": self.evaluated_at
        }
