from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.container import Container

class ContainerRepository:
    """Repository handling local container persistence and seed data."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "containers.json")
        self._seed_default_containers()

    def _seed_default_containers(self) -> None:
        if self.store.count() == 0:
            defaults = [
                Container("devopsflow-web-prod", "devopsflow/web", "v1.0.0", "5000:5000", cpu_percent=4.2, memory_usage_mb=210.0),
                Container("postgres-primary-db", "postgres", "15-alpine", "5432:5432", cpu_percent=8.5, memory_usage_mb=420.0),
                Container("redis-cache-cluster", "redis", "7.0", "6379:6379", cpu_percent=1.1, memory_usage_mb=95.0),
                Container("rabbitmq-event-queue", "rabbitmq", "3.11-management", "5672:5672", cpu_percent=3.6, memory_usage_mb=310.0)
            ]
            for cnt in defaults:
                self.store.insert(cnt.to_dict())

    def get_by_id(self, container_id: str) -> Optional[Container]:
        data = self.store.find_by_id(container_id)
        return Container.from_dict(data) if data else None

    def get_all(self) -> List[Container]:
        return [Container.from_dict(r) for r in self.store.read_all()]

    def save(self, container: Container) -> Container:
        existing = self.get_by_id(container.id)
        if existing:
            self.store.update(container.id, container.to_dict())
        else:
            self.store.insert(container.to_dict())
        return container

    def delete(self, container_id: str) -> bool:
        return self.store.delete(container_id)
