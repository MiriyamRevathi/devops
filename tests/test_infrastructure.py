import pytest
import shutil
import tempfile
from models.infrastructure import InfraResource, IaCPlan
from repositories.infra_repo import InfrastructureRepository
from services.iac_engine import IaCEngine

@pytest.fixture
def temp_infra_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_infra_models():
    r = InfraResource("web-node", "server")
    assert r.name == "web-node"
    assert r.status == InfraResource.STATE_PLANNED

def test_iac_engine_plan_and_apply(temp_infra_dir):
    repo = InfrastructureRepository(temp_infra_dir)
    engine = IaCEngine(repo)

    yaml_def = """
resources:
  - name: test-redis-cache
    type: cache
  - name: test-lb
    type: load_balancer
"""

    success, plan, msg = engine.create_plan(
        project_id="proj_1",
        environment="Staging",
        yaml_definition=yaml_def
    )
    assert success is True
    assert plan is not None
    assert plan.to_add == 2

    apply_success, apply_msg = engine.apply_plan(plan.id)
    assert apply_success is True
    assert repo.get_plan_by_id(plan.id).status == "APPLIED"

    # Check newly created resources
    res_list = repo.get_all_resources()
    names = [r.name for r in res_list]
    assert "test-redis-cache" in names
    assert "test-lb" in names
