from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Container:
    """Domain model representing a simulated container instance."""

    STATUS_RUNNING = "RUNNING"
    STATUS_STOPPED = "STOPPED"
    STATUS_EXITED = "EXITED"
    STATUS_RESTARTING = "RESTARTING"

    def __init__(
        self,
        name: str,
        image: str,
        tag: str = "latest",
        ports: str = "8080:80",
        container_id: Optional[str] = None,
        status: str = STATUS_RUNNING,
        cpu_percent: float = 2.4,
        memory_usage_mb: float = 180.5,
        created_at: Optional[str] = None
    ):
        self.id = container_id or generate_id("cnt")[:12]
        self.name = name
        self.image = image
        self.tag = tag
        self.ports = ports
        self.status = status
        self.cpu_percent = cpu_percent
        self.memory_usage_mb = memory_usage_mb
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "tag": self.tag,
            "ports": self.ports,
            "status": self.status,
            "cpu_percent": self.cpu_percent,
            "memory_usage_mb": self.memory_usage_mb,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Container":
        return cls(
            container_id=data.get("id"),
            name=data.get("name", ""),
            image=data.get("image", "nginx"),
            tag=data.get("tag", "latest"),
            ports=data.get("ports", "80:80"),
            status=data.get("status", cls.STATUS_RUNNING),
            cpu_percent=data.get("cpu_percent", 2.4),
            memory_usage_mb=data.get("memory_usage_mb", 180.5),
            created_at=data.get("created_at")
        )
