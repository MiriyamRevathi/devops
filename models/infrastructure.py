import yaml
from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class InfraResource:
    """Domain model for Infrastructure-as-Code resource state."""

    RESOURCE_TYPES = ["server", "database", "cache", "queue", "load_balancer", "network", "storage"]

    STATE_PLANNED = "PLANNED"
    STATE_APPLIED = "APPLIED"
    STATE_DESTROYED = "DESTROYED"

    def __init__(
        self,
        name: str,
        resource_type: str,
        provider: str = "local-cloud",
        environment: str = "Production",
        res_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        status: str = STATE_PLANNED,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = res_id or generate_id("res")
        self.name = name
        self.resource_type = resource_type
        self.provider = provider
        self.environment = environment
        self.config = config or {"instance_type": "t3.medium", "region": "us-east-1"}
        self.status = status
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "resource_type": self.resource_type,
            "provider": self.provider,
            "environment": self.environment,
            "config": self.config,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InfraResource":
        return cls(
            res_id=data.get("id"),
            name=data.get("name", ""),
            resource_type=data.get("resource_type", "server"),
            provider=data.get("provider", "local-cloud"),
            environment=data.get("environment", "Production"),
            config=data.get("config", {}),
            status=data.get("status", cls.STATE_PLANNED),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

class IaCPlan:
    """Domain model for a Terraform-like Infrastructure Plan execution."""

    def __init__(
        self,
        project_id: str,
        environment: str,
        plan_id: Optional[str] = None,
        to_add: int = 2,
        to_change: int = 1,
        to_destroy: int = 0,
        yaml_definition: str = "",
        status: str = "PLANNED",
        logs: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        self.id = plan_id or generate_id("plan")
        self.project_id = project_id
        self.environment = environment
        self.to_add = to_add
        self.to_change = to_change
        self.to_destroy = to_destroy
        self.yaml_definition = yaml_definition or (
            "resources:\n"
            "  - name: prod-web-server\n"
            "    type: server\n"
            "    cpu: 4\n"
            "    ram_gb: 16\n"
            "  - name: prod-primary-db\n"
            "    type: database\n"
            "    engine: postgresql\n"
            "    allocated_storage_gb: 250\n"
        )
        self.status = status
        self.logs = logs or []
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "environment": self.environment,
            "to_add": self.to_add,
            "to_change": self.to_change,
            "to_destroy": self.to_destroy,
            "yaml_definition": self.yaml_definition,
            "status": self.status,
            "logs": self.logs,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IaCPlan":
        return cls(
            plan_id=data.get("id"),
            project_id=data.get("project_id", ""),
            environment=data.get("environment", "Production"),
            to_add=data.get("to_add", 2),
            to_change=data.get("to_change", 1),
            to_destroy=data.get("to_destroy", 0),
            yaml_definition=data.get("yaml_definition", ""),
            status=data.get("status", "PLANNED"),
            logs=data.get("logs", []),
            created_at=data.get("created_at")
        )
