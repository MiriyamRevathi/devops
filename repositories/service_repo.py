from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.service import Microservice

class ServiceRepository:
    """Repository handling Service catalog persistence and seed data."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "services.json")
        self._seed_default_services()

    def _seed_default_services(self) -> None:
        if self.store.count() == 0:
            defaults = [
                Microservice(
                    name="API Gateway",
                    owner="admin",
                    team="Infrastructure",
                    version="v1.2.0",
                    environment="Production",
                    cpu_usage=18.4,
                    memory_usage=512.0,
                    request_count=12400,
                    error_rate=0.01,
                    dependencies=["Auth Service"]
                ),
                Microservice(
                    name="Auth Service",
                    owner="developer",
                    team="Security & Identity",
                    version="v1.1.2",
                    environment="Production",
                    cpu_usage=8.2,
                    memory_usage=256.0,
                    request_count=8900,
                    error_rate=0.005
                ),
                Microservice(
                    name="Payment Service",
                    owner="devops",
                    team="FinTech Core",
                    version="v2.0.1",
                    environment="Production",
                    cpu_usage=24.1,
                    memory_usage=1024.0,
                    request_count=3200,
                    error_rate=0.03,
                    dependencies=["Auth Service", "Notification Service"]
                ),
                Microservice(
                    name="Notification Service",
                    owner="devops",
                    team="Product Comms",
                    version="v1.0.4",
                    environment="Staging",
                    cpu_usage=5.5,
                    memory_usage=128.0,
                    request_count=1500,
                    error_rate=0.00
                )
            ]
            for svc in defaults:
                self.store.insert(svc.to_dict())

    def get_by_id(self, service_id: str) -> Optional[Microservice]:
        data = self.store.find_by_id(service_id)
        return Microservice.from_dict(data) if data else None

    def get_all(self) -> List[Microservice]:
        return [Microservice.from_dict(r) for r in self.store.read_all()]

    def save(self, service: Microservice) -> Microservice:
        existing = self.get_by_id(service.id)
        if existing:
            self.store.update(service.id, service.to_dict())
        else:
            self.store.insert(service.to_dict())
        return service

    def delete(self, service_id: str) -> bool:
        return self.store.delete(service_id)
