import pytest
import shutil
import tempfile
from models.project import Project
from repositories.project_repo import ProjectRepository
from services.project_service import ProjectService

@pytest.fixture
def temp_project_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_project_model():
    p = Project(
        name="Test Service",
        description="Testing project model",
        owner="admin",
        team="DevTeam"
    )
    assert p.name == "Test Service"
    assert p.is_active() is True
    assert "admin" in p.members

def test_project_repository(temp_project_dir):
    repo = ProjectRepository(temp_project_dir)
    projects = repo.get_all()
    assert len(projects) >= 3

    proj = repo.get_by_id(projects[0].id)
    assert proj is not None

def test_project_service_creation(temp_project_dir):
    repo = ProjectRepository(temp_project_dir)
    service = ProjectService(repo)

    success, proj, msg = service.create_project(
        name="Analytics Engine",
        description="Real-time analytics engine",
        owner="devops",
        team="Data Engineering"
    )
    assert success is True
    assert proj is not None
    assert proj.name == "Analytics Engine"

    # Duplicate name check
    dup_success, _, _ = service.create_project("Analytics Engine", "dup", "admin")
    assert dup_success is False

def test_project_service_update_and_archive(temp_project_dir):
    repo = ProjectRepository(temp_project_dir)
    service = ProjectService(repo)

    projects = repo.get_all()
    target_id = projects[0].id

    success, updated, msg = service.update_project(
        project_id=target_id,
        name="Updated Name",
        description="Updated Desc",
        team="New Team",
        environment="Staging",
        default_branch="develop"
    )
    assert success is True
    assert updated.name == "Updated Name"

    arch_success, arch_msg = service.archive_project(target_id)
    assert arch_success is True
    assert service.get_project(target_id).status == Project.STATUS_ARCHIVED
