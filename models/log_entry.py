from typing import Dict, Any, Optional
from utils.helpers import get_utc_now_iso, generate_id

class LogEntry:
    """Domain model for a centralized log entry."""

    SEVERITY_INFO = "INFO"
    SEVERITY_WARNING = "WARNING"
    SEVERITY_ERROR = "ERROR"
    SEVERITY_DEBUG = "DEBUG"

    def __init__(
        self,
        service: str,
        environment: str,
        message: str,
        severity: str = SEVERITY_INFO,
        log_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        timestamp: Optional[str] = None
    ):
        self.id = log_id or generate_id("log")
        self.service = service
        self.environment = environment
        self.message = message
        self.severity = severity
        self.trace_id = trace_id or generate_id("trc")[:10]
        self.timestamp = timestamp or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "service": self.service,
            "environment": self.environment,
            "message": self.message,
            "severity": self.severity,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls(
            log_id=data.get("id"),
            service=data.get("service", "system"),
            environment=data.get("environment", "Production"),
            message=data.get("message", ""),
            severity=data.get("severity", cls.SEVERITY_INFO),
            trace_id=data.get("trace_id"),
            timestamp=data.get("timestamp")
        )
