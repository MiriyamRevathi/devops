import pytest
import shutil
import tempfile
from models.change import ChangeRequest
from repositories.change_repo import ChangeRepository
from services.change_management_service import ChangeManagementService

@pytest.fixture
def temp_chg_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_change_management_service(temp_chg_dir):
    repo = ChangeRepository(temp_chg_dir)
    service = ChangeManagementService(repo)

    changes = repo.get_all()
    assert len(changes) >= 2

    success, chg, msg = service.create_change_request(
        title="Migrate Load Balancer to AWS ALB",
        description="Replace NGINX proxy with managed ALB",
        affected_services="API Gateway",
        risk_level="MEDIUM",
        impact="MODERATE",
        rollback_plan="Re-route DNS back to NGINX"
    )
    assert success is True
    assert chg is not None
    assert chg.status == ChangeRequest.STATUS_SUBMITTED

    adv_success, adv_msg = service.advance_status(chg.id, actor="cab_lead")
    assert adv_success is True
    assert repo.get_by_id(chg.id).status == ChangeRequest.STATUS_REVIEW
