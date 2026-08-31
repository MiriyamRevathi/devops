from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.deployment import Deployment
from models.release import ReleaseVersion

class DeploymentRepository:
    """Repository handling Deployment and Release data persistence."""

    def __init__(self, data_directory: str):
        self.deployment_store = JSONStore(data_directory, "deployments.json")
        self.release_store = JSONStore(data_directory, "releases.json")
        self._seed_default_deployments()

    def _seed_default_deployments(self) -> None:
        if self.deployment_store.count() == 0:
            rel = ReleaseVersion(
                version_tag="v1.0.0",
                project_id="proj_default",
                title="Initial Release v1.0.0",
                release_notes="Initial production release with complete DevOps functionality.",
                author="admin",
                deployment_targets=["Development", "Staging", "Production"]
            )
            self.release_store.insert(rel.to_dict())

            dep = Deployment(
                project_id="proj_default",
                environment="Production",
                version="v1.0.0",
                deployed_by="devops",
                status=Deployment.STATE_SUCCESS,
                commit_hash="a1b2c3d",
                approval_status="APPROVED",
                approved_by="admin",
                logs=["[INFO] Deploying v1.0.0 to Production...", "[SUCCESS] Deployment completed successfully."]
            )
            self.deployment_store.insert(dep.to_dict())

    def get_deployment_by_id(self, dep_id: str) -> Optional[Deployment]:
        data = self.deployment_store.find_by_id(dep_id)
        return Deployment.from_dict(data) if data else None

    def get_all_deployments(self) -> List[Deployment]:
        records = self.deployment_store.read_all()
        deps = [Deployment.from_dict(r) for r in records]
        return sorted(deps, key=lambda x: x.created_at, reverse=True)

    def save_deployment(self, deployment: Deployment) -> Deployment:
        existing = self.get_deployment_by_id(deployment.id)
        if existing:
            self.deployment_store.update(deployment.id, deployment.to_dict())
        else:
            self.deployment_store.insert(deployment.to_dict())
        return deployment

    def get_release_by_id(self, rel_id: str) -> Optional[ReleaseVersion]:
        data = self.release_store.find_by_id(rel_id)
        return ReleaseVersion.from_dict(data) if data else None

    def get_all_releases(self) -> List[ReleaseVersion]:
        records = self.release_store.read_all()
        rels = [ReleaseVersion.from_dict(r) for r in records]
        return sorted(rels, key=lambda x: x.created_at, reverse=True)

    def save_release(self, release: ReleaseVersion) -> ReleaseVersion:
        existing = self.get_release_by_id(release.id)
        if existing:
            self.release_store.update(release.id, release.to_dict())
        else:
            self.release_store.insert(release.to_dict())
        return release
