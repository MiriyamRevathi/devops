import pytest
import shutil
import tempfile
from models.incident import Incident
from repositories.incident_repo import IncidentRepository
from services.incident_service import IncidentService

@pytest.fixture
def temp_inc_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_incident_models():
    inc = Incident("API Downtime", "Gateway", "Production", severity=Incident.SEV_CRITICAL)
    assert inc.severity == Incident.SEV_CRITICAL
    assert inc.status == Incident.STATUS_OPEN

def test_incident_service_workflow(temp_inc_dir):
    repo = IncidentRepository(temp_inc_dir)
    service = IncidentService(repo)

    success, inc, msg = service.create_incident(
        title="Cache node failure",
        service="Redis",
        environment="Production",
        severity=Incident.SEV_HIGH,
        summary="Redis master OOM crash"
    )
    assert success is True
    assert inc is not None

    upd_success, upd_msg = service.update_status(inc.id, Incident.STATUS_INVESTIGATING, actor="devops")
    assert upd_success is True

    asgn_success, asgn_msg = service.assign_incident(inc.id, "senior_devops", actor="admin")
    assert asgn_success is True
    updated = repo.get_by_id(inc.id)
    assert updated.assignee == "senior_devops"
    assert len(updated.timeline) == 3
