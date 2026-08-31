import pytest
import shutil
import tempfile
from models.repository import GitRepository, Commit, Branch, PullRequest
from repositories.source_control_repo import SourceControlRepository
from services.repository_service import RepositoryService

@pytest.fixture
def temp_repo_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_source_control_models():
    c = Commit(commit_hash="h123", message="test commit", author="dev")
    assert c.hash == "h123"
    assert c.author == "dev"

    pr = PullRequest(
        title="New Feature",
        description="PR desc",
        author="dev",
        source_branch="feature/x",
        target_branch="main"
    )
    assert pr.status == PullRequest.STATUS_OPEN
    assert pr.source_branch == "feature/x"

def test_repository_service_workflow(temp_repo_dir):
    store = SourceControlRepository(temp_repo_dir)
    service = RepositoryService(store)

    repos = store.get_all()
    assert len(repos) > 0
    repo_id = repos[0].id

    # Create Branch
    success, msg = service.create_branch(repo_id, "feature/auth-service")
    assert success is True

    # Commit Changes
    cmt_success, commit, cmt_msg = service.commit_changes(
        repo_id=repo_id,
        branch_name="feature/auth-service",
        message="feat: add user auth handler",
        author="dev",
        changed_files=["auth.py"]
    )
    assert cmt_success is True
    assert commit is not None

    # Create PR
    pr_success, pr, pr_msg = service.create_pull_request(
        repo_id=repo_id,
        title="Add user authentication",
        description="Adds local JWT / session auth",
        author="dev",
        source_branch="feature/auth-service",
        target_branch="main"
    )
    assert pr_success is True
    assert pr is not None

    # Merge PR
    merge_success, merge_msg = service.merge_pull_request(repo_id, pr.id, "admin")
    assert merge_success is True
