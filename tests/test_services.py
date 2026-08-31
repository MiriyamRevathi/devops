import pytest
import shutil
import tempfile
from models.service import Microservice
from repositories.service_repo import ServiceRepository
from services.service_catalog_service import ServiceCatalogService

@pytest.fixture
def temp_svc_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_service_models():
    s = Microservice(name="Cache Service", owner="dev")
    assert s.name == "Cache Service"
    assert s.status == Microservice.STATUS_RUNNING

def test_service_catalog_workflow(temp_svc_dir):
    repo = ServiceRepository(temp_svc_dir)
    service = ServiceCatalogService(repo)

    services = repo.get_all()
    assert len(services) >= 4

    success, new_svc, msg = service.create_service(
        name="Search Service",
        owner="admin",
        team="Search Core",
        version="v1.0.0"
    )
    assert success is True
    assert new_svc is not None

    restart_success, rst_msg = service.restart_service(new_svc.id)
    assert restart_success is True
    updated = repo.get_by_id(new_svc.id)
    assert updated.status == Microservice.STATUS_RUNNING
