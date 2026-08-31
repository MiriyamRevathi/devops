from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Deployment:
    """Domain model for a CD deployment lifecycle."""

    STATE_PENDING = "PENDING"
    STATE_APPROVED = "APPROVED"
    STATE_DEPLOYING = "DEPLOYING"
    STATE_SUCCESS = "SUCCESS"
    STATE_FAILED = "FAILED"
    STATE_ROLLED_BACK = "ROLLED_BACK"

    def __init__(
        self,
        project_id: str,
        environment: str,
        version: str,
        deployed_by: str,
        deployment_id: Optional[str] = None,
        status: str = STATE_PENDING,
        commit_hash: str = "latest",
        approval_status: str = "NOT_REQUIRED",
        approved_by: Optional[str] = None,
        logs: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        completed_at: Optional[str] = None
    ):
        self.id = deployment_id or generate_id("dep")
        self.project_id = project_id
        self.environment = environment
        self.version = version
        self.deployed_by = deployed_by
        self.status = status
        self.commit_hash = commit_hash
        self.approval_status = approval_status
        self.approved_by = approved_by
        self.logs = logs or []
        self.created_at = created_at or get_utc_now_iso()
        self.completed_at = completed_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "environment": self.environment,
            "version": self.version,
            "deployed_by": self.deployed_by,
            "status": self.status,
            "commit_hash": self.commit_hash,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "logs": self.logs,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Deployment":
        return cls(
            deployment_id=data.get("id"),
            project_id=data.get("project_id", ""),
            environment=data.get("environment", "Development"),
            version=data.get("version", "v1.0.0"),
            deployed_by=data.get("deployed_by", "admin"),
            status=data.get("status", cls.STATE_PENDING),
            commit_hash=data.get("commit_hash", "latest"),
            approval_status=data.get("approval_status", "NOT_REQUIRED"),
            approved_by=data.get("approved_by"),
            logs=data.get("logs", []),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at")
        )
