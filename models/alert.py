from typing import Dict, Any, Optional
from utils.helpers import get_utc_now_iso, generate_id

class AlertRule:
    """Domain model for an automated Alert Rule."""

    def __init__(
        self,
        name: str,
        metric: str,
        condition: str,
        threshold: float,
        service: str = "All",
        alert_id: Optional[str] = None,
        enabled: bool = True,
        triggered: bool = False,
        last_triggered_at: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.id = alert_id or generate_id("alt")
        self.name = name
        self.metric = metric
        self.condition = condition  # '>', '<', '>='
        self.threshold = threshold
        self.service = service
        self.enabled = enabled
        self.triggered = triggered
        self.last_triggered_at = last_triggered_at
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "metric": self.metric,
            "condition": self.condition,
            "threshold": self.threshold,
            "service": self.service,
            "enabled": self.enabled,
            "triggered": self.triggered,
            "last_triggered_at": self.last_triggered_at,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AlertRule":
        return cls(
            alert_id=data.get("id"),
            name=data.get("name", ""),
            metric=data.get("metric", "CPU"),
            condition=data.get("condition", ">"),
            threshold=data.get("threshold", 80.0),
            service=data.get("service", "All"),
            enabled=data.get("enabled", True),
            triggered=data.get("triggered", False),
            last_triggered_at=data.get("last_triggered_at"),
            created_at=data.get("created_at")
        )
