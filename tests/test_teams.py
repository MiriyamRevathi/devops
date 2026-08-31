import pytest
import shutil
import tempfile
from models.team import Team
from repositories.team_repo import TeamRepository
from services.team_service import TeamService

@pytest.fixture
def temp_team_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_team_service(temp_team_dir):
    repo = TeamRepository(temp_team_dir)
    service = TeamService(repo)

    teams = repo.get_all()
    assert len(teams) >= 3

    success, t, msg = service.create_team("SRE Operations", "Site reliability engineering", "devops")
    assert success is True
    assert t is not None

    add_success, add_msg = service.add_member(t.id, "new_sre")
    assert add_success is True
    updated = repo.get_by_id(t.id)
    assert "new_sre" in updated.members
