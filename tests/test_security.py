import pytest
import shutil
import tempfile
from models.security import SecurityFinding
from services.security_scanner import SecurityScannerService

@pytest.fixture
def temp_sec_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_security_scanner(temp_sec_dir):
    service = SecurityScannerService(temp_sec_dir)
    findings = service.run_scan()
    assert len(findings) >= 3

    target_id = findings[0].id
    resolved = service.resolve_finding(target_id)
    assert resolved is True
    assert service.store.find_by_id(target_id)["status"] == "RESOLVED"
