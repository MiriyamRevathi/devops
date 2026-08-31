from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.repository import GitRepository, Commit, Branch, PullRequest

class SourceControlRepository:
    """Repository handling Git simulator storage and seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "repositories.json")
        self._seed_default_repositories()

    def _seed_default_repositories(self) -> None:
        if self.store.count() == 0:
            initial_commit = Commit(
                commit_hash="a1b2c3d",
                message="Initial commit: DevOpsFlow architecture setup",
                author="admin",
                branch="main",
                additions=120,
                deletions=0,
                changed_files=["app.py", "config.py", "README.md"]
            ).to_dict()

            feature_commit = Commit(
                commit_hash="e5f6g7h",
                message="feat: add CI pipeline step execution engine",
                author="devops",
                branch="feature/ci-engine",
                additions=85,
                deletions=12,
                changed_files=["core/pipeline.py", "tests/test_pipeline.py"]
            ).to_dict()

            sample_pr = PullRequest(
                title="feat: implement interactive CI pipeline engine",
                description="Adds stage ordering, status transition state machine, and log stream.",
                author="devops",
                source_branch="feature/ci-engine",
                target_branch="main",
                status=PullRequest.STATUS_OPEN,
                commits=[feature_commit]
            ).to_dict()

            repo = GitRepository(
                name="devopsflow-core",
                project_id="proj_default",
                branches=[
                    Branch("main", is_default=True, head_commit_hash="a1b2c3d").to_dict(),
                    Branch("feature/ci-engine", is_default=False, head_commit_hash="e5f6g7h").to_dict()
                ],
                commits=[initial_commit, feature_commit],
                pull_requests=[sample_pr],
                tags=["v1.0.0", "v1.1.0-rc1"]
            )
            self.store.insert(repo.to_dict())

    def get_by_id(self, repo_id: str) -> Optional[GitRepository]:
        data = self.store.find_by_id(repo_id)
        return GitRepository.from_dict(data) if data else None

    def get_by_project_id(self, project_id: str) -> Optional[GitRepository]:
        results = self.store.find_where(lambda r: r.get("project_id") == project_id)
        return GitRepository.from_dict(results[0]) if results else None

    def get_all(self) -> List[GitRepository]:
        return [GitRepository.from_dict(r) for r in self.store.read_all()]

    def save(self, repo: GitRepository) -> GitRepository:
        existing = self.get_by_id(repo.id)
        if existing:
            self.store.update(repo.id, repo.to_dict())
        else:
            self.store.insert(repo.to_dict())
        return repo
