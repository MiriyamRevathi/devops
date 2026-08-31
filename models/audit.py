from typing import Dict, Any, Optional
from utils.helpers import get_utc_now_iso, generate_id

class AuditEvent:
    """Domain model for an immutable system audit trail event."""

    def __init__(
        self,
        event_type: str,
        actor: str,
        resource: str,
        details: str = "",
        event_id: Optional[str] = None,
        ip_address: str = "127.0.0.1",
        timestamp: Optional[str] = None
    ):
        self.id = event_id or generate_id("aud")
        self.event_type = event_type
        self.actor = actor
        self.resource = resource
        self.details = details
        self.ip_address = ip_address
        self.timestamp = timestamp or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event_type": self.event_type,
            "actor": self.actor,
            "resource": self.resource,
            "details": self.details,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        return cls(
            event_id=data.get("id"),
            event_type=data.get("event_type", "action"),
            actor=data.get("actor", "system"),
            resource=data.get("resource", "system"),
            details=data.get("details", ""),
            ip_address=data.get("ip_address", "127.0.0.1"),
            timestamp=data.get("timestamp")
        )
