from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Environment:
    """Domain model for a deployment environment (Dev, Test, Staging, Production)."""

    HEALTH_HEALTHY = "HEALTHY"
    HEALTH_DEGRADED = "DEGRADED"
    HEALTH_DOWN = "DOWN"

    def __init__(
        self,
        name: str,
        type_name: str,
        cluster_name: str = "local-k8s-cluster",
        env_id: Optional[str] = None,
        health: str = HEALTH_HEALTHY,
        active_version: str = "v1.0.0",
        variables: Optional[Dict[str, str]] = None,
        services_count: int = 4,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = env_id or generate_id("env")
        self.name = name
        self.type_name = type_name
        self.cluster_name = cluster_name
        self.health = health
        self.active_version = active_version
        self.variables = variables or {"LOG_LEVEL": "INFO", "DB_MAX_CONNECTIONS": "50"}
        self.services_count = services_count
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type_name": self.type_name,
            "cluster_name": self.cluster_name,
            "health": self.health,
            "active_version": self.active_version,
            "variables": self.variables,
            "services_count": self.services_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Environment":
        return cls(
            env_id=data.get("id"),
            name=data.get("name", "Development"),
            type_name=data.get("type_name", "development"),
            cluster_name=data.get("cluster_name", "local-k8s-cluster"),
            health=data.get("health", cls.HEALTH_HEALTHY),
            active_version=data.get("active_version", "v1.0.0"),
            variables=data.get("variables", {}),
            services_count=data.get("services_count", 4),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
