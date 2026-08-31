from typing import Dict, Any, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Artifact:
    """Domain model for a registered build package artifact (wheel, zip, tar, container image)."""

    def __init__(
        self,
        name: str,
        version: str,
        artifact_type: str = "wheel",  # wheel, zip, tar, container_image
        size_bytes: int = 1048576,
        checksum_sha256: str = "a8f5f167f44f4964e6c998dee827110c",
        artifact_id: Optional[str] = None,
        created_by: str = "admin",
        created_at: Optional[str] = None
    ):
        self.id = artifact_id or generate_id("art")
        self.name = name
        self.version = version
        self.artifact_type = artifact_type
        self.size_bytes = size_bytes
        self.checksum_sha256 = checksum_sha256
        self.created_by = created_by
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "artifact_type": self.artifact_type,
            "size_bytes": self.size_bytes,
            "checksum_sha256": self.checksum_sha256,
            "created_by": self.created_by,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Artifact":
        return cls(
            artifact_id=data.get("id"),
            name=data.get("name", ""),
            version=data.get("version", "v1.0.0"),
            artifact_type=data.get("artifact_type", "wheel"),
            size_bytes=data.get("size_bytes", 1048576),
            checksum_sha256=data.get("checksum_sha256", ""),
            created_by=data.get("created_by", "admin"),
            created_at=data.get("created_at")
        )
