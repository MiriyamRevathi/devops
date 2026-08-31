from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.project import Project

class ProjectRepository:
    """Repository managing Project data persistence and default seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "projects.json")
        self._seed_default_projects()

    def _seed_default_projects(self) -> None:
        if self.store.count() == 0:
            seeds = [
                Project(
                    name="DevOpsFlow Platform",
                    description="Enterprise DevOps Lifecycle Management System",
                    owner="admin",
                    team="Platform Infrastructure",
                    repository="git@devopsflow.local:devopsflow-core.git",
                    default_branch="main",
                    environment="Production",
                    status=Project.STATUS_ACTIVE,
                    tags=["core", "devops", "platform"]
                ),
                Project(
                    name="Payment Gateway Service",
                    description="High-throughput payment processing microservice",
                    owner="devops",
                    team="FinTech Core",
                    repository="git@devopsflow.local:payment-gateway.git",
                    default_branch="main",
                    environment="Production",
                    status=Project.STATUS_ACTIVE,
                    tags=["payment", "microservice", "pci"]
                ),
                Project(
                    name="User Auth Subsystem",
                    description="OAuth2 and Identity Provider Service",
                    owner="developer",
                    team="Security & Identity",
                    repository="git@devopsflow.local:user-auth.git",
                    default_branch="main",
                    environment="Staging",
                    status=Project.STATUS_ACTIVE,
                    tags=["auth", "security"]
                )
            ]
            for proj in seeds:
                self.store.insert(proj.to_dict())

    def get_by_id(self, project_id: str) -> Optional[Project]:
        data = self.store.find_by_id(project_id)
        return Project.from_dict(data) if data else None

    def get_all(self, include_archived: bool = False) -> List[Project]:
        records = self.store.read_all()
        projects = [Project.from_dict(r) for r in records]
        if not include_archived:
            return [p for p in projects if p.status != Project.STATUS_DELETED]
        return projects

    def search(self, query: str = "", status: str = "", team: str = "") -> List[Project]:
        projects = self.get_all(include_archived=True)
        if query:
            q = query.lower()
            projects = [
                p for p in projects
                if q in p.name.lower() or q in p.description.lower() or q in p.owner.lower()
            ]
        if status:
            projects = [p for p in projects if p.status.upper() == status.upper()]
        if team:
            projects = [p for p in projects if p.team.lower() == team.lower()]
        return projects

    def create(self, project: Project) -> Project:
        self.store.insert(project.to_dict())
        return project

    def update(self, project: Project) -> Optional[Project]:
        updated = self.store.update(project.id, project.to_dict())
        return Project.from_dict(updated) if updated else None

    def delete(self, project_id: str) -> bool:
        project = self.get_by_id(project_id)
        if project:
            project.status = Project.STATUS_DELETED
            self.update(project)
            return True
        return False
