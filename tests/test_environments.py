import pytest
import shutil
import tempfile
from models.environment import Environment
from repositories.environment_repo import EnvironmentRepository
from services.environment_service import EnvironmentService

@pytest.fixture
def temp_env_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_environment_models():
    env = Environment("Staging", "staging")
    assert env.name == "Staging"
    assert env.health == Environment.HEALTH_HEALTHY

def test_environment_service_workflow(temp_env_dir):
    repo = EnvironmentRepository(temp_env_dir)
    service = EnvironmentService(repo)

    envs = service.list_environments()
    assert len(envs) == 4

    env_id = envs[0].id
    success, msg = service.set_environment_variable(env_id, "FEATURE_FLAG_X", "enabled")
    assert success is True
    updated = service.get_environment(env_id)
    assert updated.variables.get("FEATURE_FLAG_X") == "enabled"

    hc_success, status, hc_msg = service.trigger_health_check(env_id)
    assert hc_success is True
    assert status in [Environment.HEALTH_HEALTHY, Environment.HEALTH_DEGRADED, Environment.HEALTH_DOWN]
