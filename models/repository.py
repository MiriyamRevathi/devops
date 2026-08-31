from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class Commit:
    """Domain model for a Git commit in the local source control simulator."""

    def __init__(
        self,
        commit_hash: str,
        message: str,
        author: str,
        branch: str = "main",
        additions: int = 10,
        deletions: int = 2,
        changed_files: Optional[List[str]] = None,
        timestamp: Optional[str] = None
    ):
        self.hash = commit_hash or generate_id("cmt")[:8]
        self.message = message
        self.author = author
        self.branch = branch
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files or ["src/main.py", "README.md"]
        self.timestamp = timestamp or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hash": self.hash,
            "message": self.message,
            "author": self.author,
            "branch": self.branch,
            "additions": self.additions,
            "deletions": self.deletions,
            "changed_files": self.changed_files,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Commit":
        return cls(
            commit_hash=data.get("hash", ""),
            message=data.get("message", ""),
            author=data.get("author", ""),
            branch=data.get("branch", "main"),
            additions=data.get("additions", 0),
            deletions=data.get("deletions", 0),
            changed_files=data.get("changed_files", []),
            timestamp=data.get("timestamp")
        )

class Branch:
    """Domain model for a Git branch."""

    def __init__(self, name: str, is_default: bool = False, head_commit_hash: str = ""):
        self.name = name
        self.is_default = is_default
        self.head_commit_hash = head_commit_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_default": self.is_default,
            "head_commit_hash": self.head_commit_hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Branch":
        return cls(
            name=data.get("name", "main"),
            is_default=data.get("is_default", False),
            head_commit_hash=data.get("head_commit_hash", "")
        )

class PullRequest:
    """Domain model for a Git Pull Request review and merge workflow."""

    STATUS_OPEN = "OPEN"
    STATUS_MERGED = "MERGED"
    STATUS_CLOSED = "CLOSED"

    def __init__(
        self,
        title: str,
        description: str,
        author: str,
        source_branch: str,
        target_branch: str = "main",
        pr_id: Optional[str] = None,
        status: str = STATUS_OPEN,
        reviewers: Optional[List[str]] = None,
        commits: Optional[List[Dict[str, Any]]] = None,
        created_at: Optional[str] = None,
        merged_at: Optional[str] = None
    ):
        self.id = pr_id or generate_id("pr")
        self.title = title
        self.description = description
        self.author = author
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.status = status
        self.reviewers = reviewers or ["admin"]
        self.commits = commits or []
        self.created_at = created_at or get_utc_now_iso()
        self.merged_at = merged_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "source_branch": self.source_branch,
            "target_branch": self.target_branch,
            "status": self.status,
            "reviewers": self.reviewers,
            "commits": self.commits,
            "created_at": self.created_at,
            "merged_at": self.merged_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PullRequest":
        return cls(
            pr_id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            author=data.get("author", ""),
            source_branch=data.get("source_branch", ""),
            target_branch=data.get("target_branch", "main"),
            status=data.get("status", cls.STATUS_OPEN),
            reviewers=data.get("reviewers", []),
            commits=data.get("commits", []),
            created_at=data.get("created_at"),
            merged_at=data.get("merged_at")
        )

class GitRepository:
    """Domain model representing a source code repository containing commits, branches, and PRs."""

    def __init__(
        self,
        name: str,
        project_id: str,
        clone_url: str = "",
        repo_id: Optional[str] = None,
        branches: Optional[List[Dict[str, Any]]] = None,
        commits: Optional[List[Dict[str, Any]]] = None,
        pull_requests: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        self.id = repo_id or generate_id("repo")
        self.name = name
        self.project_id = project_id
        self.clone_url = clone_url or f"git@devopsflow.local:{name.lower()}.git"
        self.branches = branches or [Branch("main", is_default=True).to_dict()]
        self.commits = commits or []
        self.pull_requests = pull_requests or []
        self.tags = tags or ["v1.0.0"]
        self.created_at = created_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "clone_url": self.clone_url,
            "branches": self.branches,
            "commits": self.commits,
            "pull_requests": self.pull_requests,
            "tags": self.tags,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitRepository":
        return cls(
            repo_id=data.get("id"),
            name=data.get("name", ""),
            project_id=data.get("project_id", ""),
            clone_url=data.get("clone_url", ""),
            branches=data.get("branches", []),
            commits=data.get("commits", []),
            pull_requests=data.get("pull_requests", []),
            tags=data.get("tags", []),
            created_at=data.get("created_at")
        )
