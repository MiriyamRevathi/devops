import random
from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Microservice:
    """Domain model for a microservice in the enterprise service catalog."""

    STATUS_RUNNING = "RUNNING"
    STATUS_DEGRADED = "DEGRADED"
    STATUS_STOPPED = "STOPPED"
    STATUS_RESTARTING = "RESTARTING"

    def __init__(
        self,
        name: str,
        owner: str,
        team: str = "Backend Platform",
        version: str = "v1.0.0",
        environment: str = "Production",
        service_id: Optional[str] = None,
        status: str = STATUS_RUNNING,
        cpu_usage: float = 12.5,
        memory_usage: float = 256.0,
        request_count: int = 4500,
        error_rate: float = 0.02,
        uptime_percentage: float = 99.98,
        last_deployment: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        self.id = service_id or generate_id("svc")
        self.name = name
        self.owner = owner
        self.team = team
        self.version = version
        self.environment = environment
        self.status = status
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.request_count = request_count
        self.error_rate = error_rate
        self.uptime_percentage = uptime_percentage
        self.last_deployment = last_deployment or get_utc_now_iso()
        self.dependencies = dependencies or []
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "team": self.team,
            "version": self.version,
            "environment": self.environment,
            "status": self.status,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "request_count": self.request_count,
            "error_rate": self.error_rate,
            "uptime_percentage": self.uptime_percentage,
            "last_deployment": self.last_deployment,
            "dependencies": self.dependencies,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Microservice":
        return cls(
            service_id=data.get("id"),
            name=data.get("name", ""),
            owner=data.get("owner", "admin"),
            team=data.get("team", "Backend Platform"),
            version=data.get("version", "v1.0.0"),
            environment=data.get("environment", "Production"),
            status=data.get("status", cls.STATUS_RUNNING),
            cpu_usage=data.get("cpu_usage", 12.5),
            memory_usage=data.get("memory_usage", 256.0),
            request_count=data.get("request_count", 4500),
            error_rate=data.get("error_rate", 0.02),
            uptime_percentage=data.get("uptime_percentage", 99.98),
            last_deployment=data.get("last_deployment"),
            dependencies=data.get("dependencies", []),
            created_at=data.get("created_at")
        )
