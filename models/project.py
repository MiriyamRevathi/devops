from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Project:
    """Project entity domain model."""

    STATUS_ACTIVE = "ACTIVE"
    STATUS_ARCHIVED = "ARCHIVED"
    STATUS_DELETED = "DELETED"

    def __init__(
        self,
        name: str,
        description: str,
        owner: str,
        team: str = "Core DevOps",
        repository: str = "",
        default_branch: str = "main",
        environment: str = "Production",
        status: str = STATUS_ACTIVE,
        project_id: Optional[str] = None,
        members: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = project_id or generate_id("proj")
        self.name = name
        self.description = description
        self.owner = owner
        self.team = team
        self.repository = repository or f"git@devopsflow.local:{name.lower().replace(' ', '-')}.git"
        self.default_branch = default_branch
        self.environment = environment
        self.status = status
        self.members = members or [owner]
        self.tags = tags or ["devops", "microservice"]
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "team": self.team,
            "repository": self.repository,
            "default_branch": self.default_branch,
            "environment": self.environment,
            "status": self.status,
            "members": self.members,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        return cls(
            project_id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            owner=data.get("owner", ""),
            team=data.get("team", "Core DevOps"),
            repository=data.get("repository", ""),
            default_branch=data.get("default_branch", "main"),
            environment=data.get("environment", "Production"),
            status=data.get("status", cls.STATUS_ACTIVE),
            members=data.get("members", []),
            tags=data.get("tags", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def is_active(self) -> bool:
        return self.status == self.STATUS_ACTIVE
