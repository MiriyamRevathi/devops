import secrets
from typing import Tuple, Optional, List, Dict, Any
from repositories.source_control_repo import SourceControlRepository
from models.repository import GitRepository, Commit, Branch, PullRequest
from utils.helpers import get_utc_now_iso, generate_id
from core.events import EventBus

class RepositoryService:
    """Service handling simulated Git operations, branches, commits, PRs, and merge workflow."""

    def __init__(self, repository: SourceControlRepository):
        self.repo_store = repository

    def create_repository(self, name: str, project_id: str) -> GitRepository:
        initial_commit = Commit(
            commit_hash=secrets.token_hex(4),
            message=f"Initial commit for {name}",
            author="admin",
            branch="main",
            additions=50,
            deletions=0,
            changed_files=["README.md", ".gitignore"]
        ).to_dict()

        new_repo = GitRepository(
            name=name,
            project_id=project_id,
            branches=[Branch("main", is_default=True, head_commit_hash=initial_commit["hash"]).to_dict()],
            commits=[initial_commit]
        )
        return self.repo_store.save(new_repo)

    def create_branch(self, repo_id: str, branch_name: str, from_branch: str = "main") -> Tuple[bool, str]:
        repo = self.repo_store.get_by_id(repo_id)
        if not repo:
            return False, "Repository not found."

        existing_branches = [b["name"] for b in repo.branches]
        if branch_name in existing_branches:
            return False, f"Branch '{branch_name}' already exists."

        # Find head commit of from_branch
        from_head = ""
        for b in repo.branches:
            if b["name"] == from_branch:
                from_head = b.get("head_commit_hash", "")
                break

        new_branch = Branch(name=branch_name, is_default=False, head_commit_hash=from_head).to_dict()
        repo.branches.append(new_branch)
        self.repo_store.save(repo)
        EventBus.publish("branch_created", repo_id=repo_id, branch=branch_name)
        return True, f"Branch '{branch_name}' created successfully."

    def commit_changes(
        self,
        repo_id: str,
        branch_name: str,
        message: str,
        author: str,
        changed_files: List[str],
        additions: int = 15,
        deletions: int = 3
    ) -> Tuple[bool, Optional[Commit], str]:
        repo = self.repo_store.get_by_id(repo_id)
        if not repo:
            return False, None, "Repository not found."

        branch_exists = any(b["name"] == branch_name for b in repo.branches)
        if not branch_exists:
            return False, None, f"Branch '{branch_name}' does not exist."

        commit = Commit(
            commit_hash=secrets.token_hex(4),
            message=message,
            author=author,
            branch=branch_name,
            additions=additions,
            deletions=deletions,
            changed_files=changed_files
        )

        repo.commits.insert(0, commit.to_dict())

        # Update branch head commit
        for b in repo.branches:
            if b["name"] == branch_name:
                b["head_commit_hash"] = commit.hash
                break

        self.repo_store.save(repo)
        EventBus.publish("commit_created", repo_id=repo_id, commit_hash=commit.hash)
        return True, commit, "Commit created successfully."

    def create_pull_request(
        self,
        repo_id: str,
        title: str,
        description: str,
        author: str,
        source_branch: str,
        target_branch: str = "main"
    ) -> Tuple[bool, Optional[PullRequest], str]:
        repo = self.repo_store.get_by_id(repo_id)
        if not repo:
            return False, None, "Repository not found."

        if source_branch == target_branch:
            return False, None, "Source and target branch cannot be the same."

        pr_commits = [c for c in repo.commits if c.get("branch") == source_branch]

        pr = PullRequest(
            title=title,
            description=description,
            author=author,
            source_branch=source_branch,
            target_branch=target_branch,
            commits=pr_commits
        )

        repo.pull_requests.insert(0, pr.to_dict())
        self.repo_store.save(repo)
        EventBus.publish("pr_created", pr_id=pr.id, title=pr.title)
        return True, pr, "Pull request created successfully."

    def merge_pull_request(self, repo_id: str, pr_id: str, merger: str) -> Tuple[bool, str]:
        repo = self.repo_store.get_by_id(repo_id)
        if not repo:
            return False, "Repository not found."

        target_pr = None
        for pr in repo.pull_requests:
            if pr.get("id") == pr_id:
                target_pr = pr
                break

        if not target_pr:
            return False, "Pull request not found."

        if target_pr.get("status") == PullRequest.STATUS_MERGED:
            return False, "Pull request is already merged."

        # Simulate merge commit
        merge_commit = Commit(
            commit_hash=secrets.token_hex(4),
            message=f"Merge pull request #{pr_id[:6]} from {target_pr['source_branch']}",
            author=merger,
            branch=target_pr["target_branch"],
            additions=20,
            deletions=5,
            changed_files=["MERGE_HEAD"]
        ).to_dict()

        repo.commits.insert(0, merge_commit)
        target_pr["status"] = PullRequest.STATUS_MERGED
        target_pr["merged_at"] = get_utc_now_iso()

        # Update target branch head
        for b in repo.branches:
            if b["name"] == target_pr["target_branch"]:
                b["head_commit_hash"] = merge_commit["hash"]
                break

        self.repo_store.save(repo)
        EventBus.publish("pr_merged", pr_id=pr_id, repo_id=repo_id)
        return True, "Pull request merged successfully."
