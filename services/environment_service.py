import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.environment_repo import EnvironmentRepository
from models.environment import Environment
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class EnvironmentService:
    """Business logic for target deployment environment management."""

    def __init__(self, repository: EnvironmentRepository):
        self.repo = repository

    def list_environments(self) -> List[Environment]:
        return self.repo.get_all()

    def get_environment(self, env_id: str) -> Optional[Environment]:
        return self.repo.get_by_id(env_id)

    def set_environment_variable(self, env_id: str, key: str, value: str) -> Tuple[bool, str]:
        env = self.repo.get_by_id(env_id)
        if not env:
            return False, "Environment not found."

        env.variables[key.strip()] = value.strip()
        env.updated_at = get_utc_now_iso()
        self.repo.save(env)
        EventBus.publish("environment_var_updated", env_id=env_id, key=key)
        return True, f"Environment variable '{key}' set successfully."

    def trigger_health_check(self, env_id: str) -> Tuple[bool, str, str]:
        env = self.repo.get_by_id(env_id)
        if not env:
            return False, "UNKNOWN", "Environment not found."

        # Simulate health evaluation
        val = random.random()
        if val > 0.15:
            env.health = Environment.HEALTH_HEALTHY
        elif val > 0.05:
            env.health = Environment.HEALTH_DEGRADED
        else:
            env.health = Environment.HEALTH_DOWN

        env.updated_at = get_utc_now_iso()
        self.repo.save(env)
        EventBus.publish("environment_health_checked", env_id=env_id, health=env.health)
        return True, env.health, f"Health check completed: {env.health}"
