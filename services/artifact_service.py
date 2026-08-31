import secrets
from typing import Tuple, Optional, List, Dict, Any
from repositories.artifact_repo import ArtifactRepository
from models.artifact import Artifact
from core.events import EventBus

class ArtifactService:
    """Artifact Registry Manager Service."""

    def __init__(self, repository: ArtifactRepository):
        self.repo = repository

    def register_artifact(
        self,
        name: str,
        version: str,
        artifact_type: str = "wheel",
        size_bytes: int = 1048576,
        created_by: str = "admin"
    ) -> Tuple[bool, Optional[Artifact], str]:
        if not name or not version:
            return False, None, "Name and version are required."

        art = Artifact(
            name=name.strip(),
            version=version.strip(),
            artifact_type=artifact_type,
            size_bytes=size_bytes,
            checksum_sha256=secrets.token_hex(16),
            created_by=created_by
        )

        saved = self.repo.save(art)
        EventBus.publish("artifact_registered", artifact_id=saved.id, name=saved.name, version=saved.version)
        return True, saved, f"Artifact '{saved.name}:{saved.version}' registered."

    def delete_artifact(self, artifact_id: str) -> Tuple[bool, str]:
        success = self.repo.delete(artifact_id)
        if success:
            EventBus.publish("artifact_deleted", artifact_id=artifact_id)
            return True, "Artifact deleted."
        return False, "Failed to delete artifact."
