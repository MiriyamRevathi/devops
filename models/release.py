from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class ReleaseVersion:
    """Domain model for a platform release version."""

    def __init__(
        self,
        version_tag: str,
        project_id: str,
        title: str,
        release_notes: str,
        author: str,
        release_id: Optional[str] = None,
        artifacts: Optional[List[str]] = None,
        deployment_targets: Optional[List[str]] = None,
        is_published: bool = True,
        created_at: Optional[str] = None
    ):
        self.id = release_id or generate_id("rel")
        self.version_tag = version_tag
        self.project_id = project_id
        self.title = title
        self.release_notes = release_notes
        self.author = author
        self.artifacts = artifacts or [f"{version_tag}.tar.gz"]
        self.deployment_targets = deployment_targets or ["Development", "Staging"]
        self.is_published = is_published
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "version_tag": self.version_tag,
            "project_id": self.project_id,
            "title": self.title,
            "release_notes": self.release_notes,
            "author": self.author,
            "artifacts": self.artifacts,
            "deployment_targets": self.deployment_targets,
            "is_published": self.is_published,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReleaseVersion":
        return cls(
            release_id=data.get("id"),
            version_tag=data.get("version_tag", "v1.0.0"),
            project_id=data.get("project_id", ""),
            title=data.get("title", ""),
            release_notes=data.get("release_notes", ""),
            author=data.get("author", "admin"),
            artifacts=data.get("artifacts", []),
            deployment_targets=data.get("deployment_targets", []),
            is_published=data.get("is_published", True),
            created_at=data.get("created_at")
        )
