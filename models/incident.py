from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Incident:
    """Domain model for a DevOps Incident."""

    SEV_LOW = "LOW"
    SEV_MEDIUM = "MEDIUM"
    SEV_HIGH = "HIGH"
    SEV_CRITICAL = "CRITICAL"

    STATUS_OPEN = "OPEN"
    STATUS_INVESTIGATING = "INVESTIGATING"
    STATUS_MITIGATING = "MITIGATING"
    STATUS_RESOLVED = "RESOLVED"
    STATUS_CLOSED = "CLOSED"

    def __init__(
        self,
        title: str,
        service: str,
        environment: str,
        assignee: str = "unassigned",
        severity: str = SEV_HIGH,
        incident_id: Optional[str] = None,
        status: str = STATUS_OPEN,
        summary: str = "",
        timeline: Optional[List[Dict[str, Any]]] = None,
        created_at: Optional[str] = None,
        resolved_at: Optional[str] = None
    ):
        self.id = incident_id or generate_id("inc")
        self.title = title
        self.service = service
        self.environment = environment
        self.assignee = assignee
        self.severity = severity
        self.status = status
        self.summary = summary or title
        self.timeline = timeline or [{
            "timestamp": get_utc_now_iso(),
            "actor": assignee,
            "action": "Incident Created",
            "notes": summary or title
        }]
        self.created_at = created_at or get_utc_now_iso()
        self.resolved_at = resolved_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "service": self.service,
            "environment": self.environment,
            "assignee": self.assignee,
            "severity": self.severity,
            "status": self.status,
            "summary": self.summary,
            "timeline": self.timeline,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Incident":
        return cls(
            incident_id=data.get("id"),
            title=data.get("title", ""),
            service=data.get("service", "API Gateway"),
            environment=data.get("environment", "Production"),
            assignee=data.get("assignee", "unassigned"),
            severity=data.get("severity", cls.SEV_HIGH),
            status=data.get("status", cls.STATUS_OPEN),
            summary=data.get("summary", ""),
            timeline=data.get("timeline", []),
            created_at=data.get("created_at"),
            resolved_at=data.get("resolved_at")
        )
