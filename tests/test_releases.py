import pytest
import shutil
import tempfile
from models.release import ReleaseVersion
from repositories.deployment_repo import DeploymentRepository
from services.deployment_service import DeploymentService

@pytest.fixture
def temp_rel_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_release_models():
    rel = ReleaseVersion(
        version_tag="v1.1.0",
        project_id="p1",
        title="Spring Release",
        release_notes="Bug fixes and perf improvements",
        author="dev"
    )
    assert rel.version_tag == "v1.1.0"
    assert rel.is_published is True

def test_release_service_creation(temp_rel_dir):
    repo = DeploymentRepository(temp_rel_dir)
    service = DeploymentService(repo)

    success, release, msg = service.create_release(
        version_tag="v2.0.0",
        project_id="proj_1",
        title="Major v2 Release",
        release_notes="Complete overhaul of authentication engine.",
        author="admin",
        deployment_targets=["Production"]
    )
    assert success is True
    assert release is not None
    assert release.version_tag == "v2.0.0"

    all_rels = repo.get_all_releases()
    assert len(all_rels) >= 2
