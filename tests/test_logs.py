import pytest
import shutil
import tempfile
from models.log_entry import LogEntry
from repositories.log_repo import LogRepository
from services.log_service import LogService

@pytest.fixture
def temp_log_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_log_models():
    l = LogEntry("Payment", "Production", "Connection timeout", LogEntry.SEVERITY_ERROR)
    assert l.severity == LogEntry.SEVERITY_ERROR
    assert l.service == "Payment"

def test_log_service_search(temp_log_dir):
    repo = LogRepository(temp_log_dir)
    service = LogService(repo)

    logs = service.search_logs()
    assert len(logs) >= 5

    service.log("Auth Service", "Production", "User token validated", LogEntry.SEVERITY_INFO)
    filtered = service.search_logs(service="Auth Service")
    assert len(filtered) > 0
