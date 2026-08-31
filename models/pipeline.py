import random
from typing import Dict, Any, List, Optional
from utils.helpers import get_utc_now_iso, generate_id

class PipelineStage:
    """Domain model for a single stage within a CI/CD pipeline."""

    STAGES = [
        "Checkout", "Install", "Lint", "Validate",
        "Unit Test", "Integration Test", "Build",
        "Package", "Security Scan", "Publish Artifact"
    ]

    def __init__(
        self,
        name: str,
        order: int,
        commands: Optional[List[str]] = None,
        enabled: bool = True,
        stage_id: Optional[str] = None
    ):
        self.id = stage_id or generate_id("stg")
        self.name = name
        self.order = order
        self.commands = commands or [f"echo 'Running {name}...'"]
        self.enabled = enabled

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "order": self.order,
            "commands": self.commands,
            "enabled": self.enabled
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PipelineStage":
        return cls(
            stage_id=data.get("id"),
            name=data.get("name", "Checkout"),
            order=data.get("order", 1),
            commands=data.get("commands", []),
            enabled=data.get("enabled", True)
        )

class PipelineRun:
    """Domain model representing an execution run of a CI pipeline."""

    STATE_CREATED = "CREATED"
    STATE_QUEUED = "QUEUED"
    STATE_RUNNING = "RUNNING"
    STATE_SUCCESS = "SUCCESS"
    STATE_FAILED = "FAILED"
    STATE_CANCELLED = "CANCELLED"

    def __init__(
        self,
        pipeline_id: str,
        project_id: str,
        branch: str = "main",
        commit_hash: str = "latest",
        run_number: int = 1,
        triggered_by: str = "admin",
        run_id: Optional[str] = None,
        status: str = STATE_CREATED,
        stage_results: Optional[List[Dict[str, Any]]] = None,
        logs: Optional[List[str]] = None,
        duration_seconds: float = 0.0,
        started_at: Optional[str] = None,
        completed_at: Optional[str] = None
    ):
        self.id = run_id or generate_id("run")
        self.pipeline_id = pipeline_id
        self.project_id = project_id
        self.branch = branch
        self.commit_hash = commit_hash
        self.run_number = run_number
        self.triggered_by = triggered_by
        self.status = status
        self.stage_results = stage_results or []
        self.logs = logs or []
        self.duration_seconds = duration_seconds
        self.started_at = started_at
        self.completed_at = completed_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pipeline_id": self.pipeline_id,
            "project_id": self.project_id,
            "branch": self.branch,
            "commit_hash": self.commit_hash,
            "run_number": self.run_number,
            "triggered_by": self.triggered_by,
            "status": self.status,
            "stage_results": self.stage_results,
            "logs": self.logs,
            "duration_seconds": self.duration_seconds,
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PipelineRun":
        return cls(
            run_id=data.get("id"),
            pipeline_id=data.get("pipeline_id", ""),
            project_id=data.get("project_id", ""),
            branch=data.get("branch", "main"),
            commit_hash=data.get("commit_hash", "latest"),
            run_number=data.get("run_number", 1),
            triggered_by=data.get("triggered_by", "admin"),
            status=data.get("status", cls.STATE_CREATED),
            stage_results=data.get("stage_results", []),
            logs=data.get("logs", []),
            duration_seconds=data.get("duration_seconds", 0.0),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at")
        )

class Pipeline:
    """Domain model representing a CI/CD Pipeline definition."""

    def __init__(
        self,
        name: str,
        project_id: str,
        description: str = "",
        pipeline_id: Optional[str] = None,
        stages: Optional[List[Dict[str, Any]]] = None,
        is_active: bool = True,
        trigger: str = "on_push",
        last_run_status: str = "NONE",
        total_runs: int = 0,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = pipeline_id or generate_id("pipe")
        self.name = name
        self.project_id = project_id
        self.description = description
        self.stages = stages or [
            PipelineStage("Checkout", 1, ["git checkout main"]).to_dict(),
            PipelineStage("Install", 2, ["pip install -r requirements.txt"]).to_dict(),
            PipelineStage("Lint", 3, ["flake8 ."]).to_dict(),
            PipelineStage("Unit Test", 4, ["pytest tests/"]).to_dict(),
            PipelineStage("Build", 5, ["docker build -t app:latest ."]).to_dict(),
            PipelineStage("Publish Artifact", 6, ["push-artifact --dest local"]).to_dict()
        ]
        self.is_active = is_active
        self.trigger = trigger
        self.last_run_status = last_run_status
        self.total_runs = total_runs
        self.created_at = created_at or get_utc_now_iso()
        self.updated_at = updated_at or get_utc_now_iso()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "description": self.description,
            "stages": self.stages,
            "is_active": self.is_active,
            "trigger": self.trigger,
            "last_run_status": self.last_run_status,
            "total_runs": self.total_runs,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pipeline":
        return cls(
            pipeline_id=data.get("id"),
            name=data.get("name", ""),
            project_id=data.get("project_id", ""),
            description=data.get("description", ""),
            stages=data.get("stages", []),
            is_active=data.get("is_active", True),
            trigger=data.get("trigger", "on_push"),
            last_run_status=data.get("last_run_status", "NONE"),
            total_runs=data.get("total_runs", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
