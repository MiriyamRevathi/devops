import pytest
import shutil
import tempfile
from models.audit import AuditEvent
from repositories.audit_repo import AuditRepository
from services.audit_service import AuditService

@pytest.fixture
def temp_aud_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_audit_service(temp_aud_dir):
    repo = AuditRepository(temp_aud_dir)
    service = AuditService(repo)

    events = service.query_audit_trail()
    assert len(events) >= 4

    evt = service.record_event("custom_action", "admin", "TargetResource", "Custom audit details")
    assert evt is not None

    queried = service.query_audit_trail(event_type="custom_action")
    assert len(queried) > 0
