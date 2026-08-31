from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class ChangeRequest:
    """Domain model for a DevOps Change Request (CAB workflow)."""

    STATUS_DRAFT = "DRAFT"
    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_REVIEW = "REVIEW"
    STATUS_APPROVED = "APPROVED"
    STATUS_IMPLEMENTING = "IMPLEMENTING"
    STATUS_VERIFIED = "VERIFIED"
    STATUS_CLOSED = "CLOSED"

    WORKFLOW = [STATUS_DRAFT, STATUS_SUBMITTED, STATUS_REVIEW, STATUS_APPROVED, STATUS_IMPLEMENTING, STATUS_VERIFIED, STATUS_CLOSED]

    def __init__(
        self,
        title: str,
        description: str,
        affected_services: str,
        risk_level: str = "MEDIUM",
        impact: str = "MODERATE",
        rollback_plan: str = "Revert to previous container tag.",
        requester: str = "admin",
        change_id: Optional[str] = None,
        status: str = STATUS_DRAFT,
        approvers: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = change_id or generate_id("chg")
        self.title = title
        self.description = description
        self.affected_services = affected_services
        self.risk_level = risk_level
        self.impact = impact
        self.rollback_plan = rollback_plan
        self.requester = requester
        self.status = status
        self.approvers = approvers or []
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "affected_services": self.affected_services,
            "risk_level": self.risk_level,
            "impact": self.impact,
            "rollback_plan": self.rollback_plan,
            "requester": self.requester,
            "status": self.status,
            "approvers": self.approvers,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChangeRequest":
        return cls(
            change_id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            affected_services=data.get("affected_services", ""),
            risk_level=data.get("risk_level", "MEDIUM"),
            impact=data.get("impact", "MODERATE"),
            rollback_plan=data.get("rollback_plan", ""),
            requester=data.get("requester", "admin"),
            status=data.get("status", cls.STATUS_DRAFT),
            approvers=data.get("approvers", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
