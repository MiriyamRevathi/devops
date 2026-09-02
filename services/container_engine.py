import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.container_repo import ContainerRepository
from models.container import Container
from core.events import EventBus

class ContainerEngine:
    """Safe local container lifecycle simulator engine."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = ContainerRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def start_container(self, container_id: str) -> Tuple[bool, str]:
        cnt = self.repo.get_by_id(container_id)
        if not cnt:
            return False, "Container not found."

        cnt.status = Container.STATUS_RUNNING
        cnt.cpu_percent = round(random.uniform(1.5, 12.0), 1)
        self.repo.save(cnt)
        EventBus.publish("container_started", container_id=container_id)
        return True, f"Container '{cnt.name}' started."

    def stop_container(self, container_id: str) -> Tuple[bool, str]:
        cnt = self.repo.get_by_id(container_id)
        if not cnt:
            return False, "Container not found."

        cnt.status = Container.STATUS_STOPPED
        cnt.cpu_percent = 0.0
        self.repo.save(cnt)
        EventBus.publish("container_stopped", container_id=container_id)
        return True, f"Container '{cnt.name}' stopped."

    def restart_container(self, container_id: str) -> Tuple[bool, str]:
        cnt = self.repo.get_by_id(container_id)
        if not cnt:
            return False, "Container not found."

        cnt.status = Container.STATUS_RESTARTING
        self.repo.save(cnt)

        cnt.status = Container.STATUS_RUNNING
        cnt.cpu_percent = round(random.uniform(2.0, 15.0), 1)
        self.repo.save(cnt)
        EventBus.publish("container_restarted", container_id=container_id)
        return True, f"Container '{cnt.name}' restarted."

    def remove_container(self, container_id: str) -> Tuple[bool, str]:
        success = self.repo.delete(container_id)
        if success:
            EventBus.publish("container_removed", container_id=container_id)
            return True, "Container removed."
        return False, "Failed to remove container."
