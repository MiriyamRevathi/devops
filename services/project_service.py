from typing import Tuple, Optional, List, Dict, Any
from repositories.project_repo import ProjectRepository
from models.project import Project
from utils.validators import DataValidator
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class ProjectService:
    """Business logic for DevOps Project management lifecycle."""

    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    def create_project(
        self,
        name: str,
        description: str,
        owner: str,
        team: str = "Core DevOps",
        repository: str = "",
        default_branch: str = "main",
        environment: str = "Production",
        tags: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[Project], str]:
        valid, msg = DataValidator.validate_project_name(name)
        if not valid:
            return False, None, msg or "Invalid project name."

        # Check existing project name collision
        existing = [p for p in self.repo.get_all(include_archived=True) if p.name.lower() == name.lower().strip()]
        if existing and existing[0].status != Project.STATUS_DELETED:
            return False, None, "A project with this name already exists."

        project = Project(
            name=name.strip(),
            description=description.strip(),
            owner=owner,
            team=team,
            repository=repository,
            default_branch=default_branch or "main",
            environment=environment,
            tags=tags or ["devops"]
        )

        created = self.repo.create(project)
        EventBus.publish("project_created", project_id=created.id, name=created.name, owner=created.owner)
        return True, created, "Project created successfully."

    def update_project(
        self,
        project_id: str,
        name: str,
        description: str,
        team: str,
        environment: str,
        default_branch: str
    ) -> Tuple[bool, Optional[Project], str]:
        project = self.repo.get_by_id(project_id)
        if not project:
            return False, None, "Project not found."

        project.name = name.strip()
        project.description = description.strip()
        project.team = team
        project.environment = environment
        project.default_branch = default_branch
        project.updated_at = get_utc_now_iso()

        updated = self.repo.update(project)
        EventBus.publish("project_updated", project_id=project.id, name=project.name)
        return True, updated, "Project updated successfully."

    def archive_project(self, project_id: str) -> Tuple[bool, str]:
        project = self.repo.get_by_id(project_id)
        if not project:
            return False, "Project not found."

        project.status = Project.STATUS_ARCHIVED
        project.updated_at = get_utc_now_iso()
        self.repo.update(project)
        EventBus.publish("project_archived", project_id=project.id)
        return True, "Project archived."

    def delete_project(self, project_id: str) -> Tuple[bool, str]:
        success = self.repo.delete(project_id)
        if success:
            EventBus.publish("project_deleted", project_id=project_id)
            return True, "Project deleted successfully."
        return False, "Failed to delete project."

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.repo.get_by_id(project_id)

    def list_projects(self, query: str = "", status: str = "", team: str = "") -> List[Project]:
        return self.repo.search(query=query, status=status, team=team)
