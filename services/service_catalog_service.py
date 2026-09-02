import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.service_repo import ServiceRepository
from models.service import Microservice
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class ServiceCatalogService:
    """Service catalog management and simulated lifecycle operation engine."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = ServiceRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def create_service(
        self,
        name: str,
        owner: str,
        team: str = "Backend Platform",
        version: str = "v1.0.0",
        environment: str = "Production"
    ) -> Tuple[bool, Optional[Microservice], str]:
        if not name:
            return False, None, "Service name is required."

        svc = Microservice(
            name=name.strip(),
            owner=owner,
            team=team,
            version=version,
            environment=environment
        )

        saved = self.repo.save(svc)
        EventBus.publish("service_created", service_id=saved.id, name=saved.name)
        return True, saved, "Microservice registered successfully."

    def restart_service(self, service_id: str) -> Tuple[bool, str]:
        svc = self.repo.get_by_id(service_id)
        if not svc:
            return False, "Service not found."

        svc.status = Microservice.STATUS_RESTARTING
        self.repo.save(svc)

        # Simulate completion
        svc.status = Microservice.STATUS_RUNNING
        svc.cpu_usage = round(random.uniform(5.0, 25.0), 1)
        svc.memory_usage = round(random.uniform(128.0, 512.0), 1)
        self.repo.save(svc)

        EventBus.publish("service_restarted", service_id=service_id)
        return True, f"Service '{svc.name}' restarted successfully."

    def update_metrics(self, service_id: str) -> Optional[Microservice]:
        svc = self.repo.get_by_id(service_id)
        if not svc:
            return None

        svc.cpu_usage = round(random.uniform(5.0, 65.0), 1)
        svc.memory_usage = round(random.uniform(100.0, 1024.0), 1)
        svc.request_count += random.randint(10, 200)
        svc.error_rate = round(random.uniform(0.00, 0.04), 3)
        return self.repo.save(svc)
