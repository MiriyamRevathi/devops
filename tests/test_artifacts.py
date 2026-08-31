import pytest
import shutil
import tempfile
from models.artifact import Artifact
from repositories.artifact_repo import ArtifactRepository
from services.artifact_service import ArtifactService

@pytest.fixture
def temp_art_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_artifact_registry(temp_art_dir):
    repo = ArtifactRepository(temp_art_dir)
    service = ArtifactService(repo)

    artifacts = repo.get_all()
    assert len(artifacts) >= 3

    success, art, msg = service.register_artifact("analytics-pkg", "v3.0.0", "wheel", 2048576, "dev")
    assert success is True
    assert art is not None
    assert art.name == "analytics-pkg"

    del_success, del_msg = service.delete_artifact(art.id)
    assert del_success is True
