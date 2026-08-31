import pytest
import shutil
import tempfile
from models.container import Container
from repositories.container_repo import ContainerRepository
from services.container_engine import ContainerEngine

@pytest.fixture
def temp_cnt_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_container_models():
    c = Container("nginx-web", "nginx", "alpine")
    assert c.name == "nginx-web"
    assert c.status == Container.STATUS_RUNNING

def test_container_engine_operations(temp_cnt_dir):
    repo = ContainerRepository(temp_cnt_dir)
    engine = ContainerEngine(repo)

    containers = repo.get_all()
    assert len(containers) >= 4
    target_id = containers[0].id

    # Stop container
    stop_success, stop_msg = engine.stop_container(target_id)
    assert stop_success is True
    assert repo.get_by_id(target_id).status == Container.STATUS_STOPPED

    # Start container
    start_success, start_msg = engine.start_container(target_id)
    assert start_success is True
    assert repo.get_by_id(target_id).status == Container.STATUS_RUNNING
