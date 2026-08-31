from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class SecurityFinding:
    """Domain model for a local security audit finding."""

    SEV_LOW = "LOW"
    SEV_MEDIUM = "MEDIUM"
    SEV_HIGH = "HIGH"
    SEV_CRITICAL = "CRITICAL"

    def __init__(
        self,
        title: str,
        category: str,  # Dependency, Secret, Misconfig
        description: str,
        recommendation: str,
        finding_id: Optional[str] = None,
        severity: str = SEV_MEDIUM,
        status: str = "OPEN",
        target_file: str = "requirements.txt",
        created_at: Optional[str] = None
    ):
        self.id = finding_id or generate_id("sec")
        self.title = title
        self.category = category
        self.description = description
        self.recommendation = recommendation
        self.severity = severity
        self.status = status
        self.target_file = target_file
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "recommendation": self.recommendation,
            "severity": self.severity,
            "status": self.status,
            "target_file": self.target_file,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecurityFinding":
        return cls(
            finding_id=data.get("id"),
            title=data.get("title", ""),
            category=data.get("category", "Dependency"),
            description=data.get("description", ""),
            recommendation=data.get("recommendation", ""),
            severity=data.get("severity", cls.SEV_MEDIUM),
            status=data.get("status", "OPEN"),
            target_file=data.get("target_file", ""),
            created_at=data.get("created_at")
        )
