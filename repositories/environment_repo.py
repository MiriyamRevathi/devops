from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.environment import Environment

class EnvironmentRepository:
    """Repository managing environment targets persistence and seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "environments.json")
        self._seed_default_environments()

    def _seed_default_environments(self) -> None:
        if self.store.count() == 0:
            default_envs = [
                Environment("Development", "development", "local-dev-cluster", active_version="v1.2.0-dev"),
                Environment("Testing", "qa", "qa-k8s-cluster", active_version="v1.1.0-rc2"),
                Environment("Staging", "staging", "staging-us-east-1", active_version="v1.0.1"),
                Environment("Production", "production", "prod-us-east-1", active_version="v1.0.0")
            ]
            for env in default_envs:
                self.store.insert(env.to_dict())

    def get_by_id(self, env_id: str) -> Optional[Environment]:
        data = self.store.find_by_id(env_id)
        return Environment.from_dict(data) if data else None

    def get_by_name(self, name: str) -> Optional[Environment]:
        results = self.store.find_where(lambda e: e.get("name", "").lower() == name.lower().strip())
        return Environment.from_dict(results[0]) if results else None

    def get_all(self) -> List[Environment]:
        return [Environment.from_dict(r) for r in self.store.read_all()]

    def save(self, env: Environment) -> Environment:
        existing = self.get_by_id(env.id)
        if existing:
            self.store.update(env.id, env.to_dict())
        else:
            self.store.insert(env.to_dict())
        return env
