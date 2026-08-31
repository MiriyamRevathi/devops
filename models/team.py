from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Team:
    """Domain model for a DevOps Engineering Team."""

    def __init__(
        self,
        name: str,
        description: str,
        lead: str,
        team_id: Optional[str] = None,
        members: Optional[List[str]] = None,
        projects: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        self.id = team_id or generate_id("team")
        self.name = name
        self.description = description
        self.lead = lead
        self.members = members or [lead]
        self.projects = projects or []
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "lead": self.lead,
            "members": self.members,
            "projects": self.projects,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        return cls(
            team_id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            lead=data.get("lead", "admin"),
            members=data.get("members", []),
            projects=data.get("projects", []),
            created_at=data.get("created_at")
        )
