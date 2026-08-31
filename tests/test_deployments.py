import pytest
import shutil
import tempfile
from models.deployment import Deployment
from repositories.deployment_repo import DeploymentRepository
from services.deployment_service import DeploymentService

@pytest.fixture
def temp_dep_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_deployment_models():
    dep = Deployment(
        project_id="p1",
        environment="Staging",
        version="v2.0.0",
        deployed_by="devops"
    )
    assert dep.version == "v2.0.0"
    assert dep.environment == "Staging"

def test_deployment_service_workflow(temp_dep_dir):
    repo = DeploymentRepository(temp_dep_dir)
    service = DeploymentService(repo)

    # Trigger deployment
    success, dep, msg = service.trigger_deployment(
        project_id="proj_test",
        environment="Production",
        version="v1.2.0",
        deployed_by="admin",
        require_approval=True
    )
    assert success is True
    assert dep is not None
    assert dep.status == Deployment.STATE_PENDING
    assert dep.approval_status == "PENDING_APPROVAL"

    # Approve deployment
    appr_success, appr_msg = service.approve_deployment(dep.id, "lead_admin")
    assert appr_success is True
    updated_dep = repo.get_deployment_by_id(dep.id)
    assert updated_dep.status in [Deployment.STATE_SUCCESS, Deployment.STATE_FAILED]

    # Rollback deployment
    rb_success, rb_dep, rb_msg = service.rollback_deployment(dep.id, "lead_admin")
    assert rb_success is True
    assert rb_dep is not None
    assert rb_dep.version == f"{updated_dep.version}-rollback"
