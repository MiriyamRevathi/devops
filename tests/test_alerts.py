import pytest
import shutil
import tempfile
from models.alert import AlertRule
from repositories.alert_repo import AlertRepository
from services.alert_service import AlertService

@pytest.fixture
def temp_alt_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_alert_models():
    rule = AlertRule("Disk Usage > 90%", "Disk", ">", 90.0)
    assert rule.threshold == 90.0
    assert rule.triggered is False

def test_alert_service_workflow(temp_alt_dir):
    repo = AlertRepository(temp_alt_dir)
    service = AlertService(repo)

    rules = repo.get_all()
    assert len(rules) >= 4
    rule_id = rules[0].id

    trg_success, trg_msg = service.trigger_simulation(rule_id)
    assert trg_success is True
    assert repo.get_by_id(rule_id).triggered is True

    res_success, res_msg = service.resolve_alert(rule_id)
    assert res_success is True
    assert repo.get_by_id(rule_id).triggered is False
