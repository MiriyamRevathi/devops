import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.deployment_repo import DeploymentRepository
from models.deployment import Deployment
from models.release import ReleaseVersion
from utils.helpers import get_utc_now_iso, generate_id
from core.events import EventBus

class DeploymentService:
    """CD Deployment Engine and Release Lifecycle Orchestrator."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = DeploymentRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def trigger_deployment(
        self,
        project_id: str,
        environment: str,
        version: str,
        deployed_by: str,
        require_approval: bool = False
    ) -> Tuple[bool, Optional[Deployment], str]:
        approval_status = "PENDING_APPROVAL" if (require_approval or environment == "Production") else "APPROVED"

        deployment = Deployment(
            project_id=project_id,
            environment=environment,
            version=version,
            deployed_by=deployed_by,
            status=Deployment.STATE_PENDING if approval_status == "PENDING_APPROVAL" else Deployment.STATE_DEPLOYING,
            approval_status=approval_status
        )

        deployment.logs.append(f"[{get_utc_now_iso()}] Deployment request submitted for {version} -> {environment}.")

        if approval_status == "APPROVED":
            self._execute_deployment_simulation(deployment)

        saved = self.repo.save_deployment(deployment)
        EventBus.publish("deployment_triggered", deployment_id=saved.id, environment=environment, status=saved.status)
        return True, saved, f"Deployment {saved.id[:6]} created with status '{saved.status}'."

    def approve_deployment(self, deployment_id: str, approver: str) -> Tuple[bool, str]:
        deployment = self.repo.get_deployment_by_id(deployment_id)
        if not deployment:
            return False, "Deployment not found."

        if deployment.approval_status == "APPROVED":
            return False, "Deployment is already approved."

        deployment.approval_status = "APPROVED"
        deployment.approved_by = approver
        deployment.status = Deployment.STATE_DEPLOYING
        deployment.logs.append(f"[{get_utc_now_iso()}] Deployment approved by {approver}. Commencing deployment...")

        self._execute_deployment_simulation(deployment)
        self.repo.save_deployment(deployment)
        EventBus.publish("deployment_approved", deployment_id=deployment_id, approved_by=approver)
        return True, "Deployment approved and initiated."

    def rollback_deployment(self, deployment_id: str, operator: str) -> Tuple[bool, Optional[Deployment], str]:
        current_dep = self.repo.get_deployment_by_id(deployment_id)
        if not current_dep:
            return False, None, "Deployment not found."

        current_dep.status = Deployment.STATE_ROLLED_BACK
        current_dep.logs.append(f"[{get_utc_now_iso()}] Rollback initiated by {operator}.")
        self.repo.save_deployment(current_dep)

        # Trigger new rollback deployment
        rollback_dep = Deployment(
            project_id=current_dep.project_id,
            environment=current_dep.environment,
            version=f"{current_dep.version}-rollback",
            deployed_by=operator,
            status=Deployment.STATE_DEPLOYING,
            approval_status="APPROVED",
            approved_by=operator
        )
        rollback_dep.logs.append(f"[{get_utc_now_iso()}] Rollback deployment started to restore previous stable state.")
        self._execute_deployment_simulation(rollback_dep)
        saved_rollback = self.repo.save_deployment(rollback_dep)

        EventBus.publish("deployment_rolled_back", original_id=deployment_id, rollback_id=saved_rollback.id)
        return True, saved_rollback, "Rollback executed successfully."

    def create_release(
        self,
        version_tag: str,
        project_id: str,
        title: str,
        release_notes: str,
        author: str,
        deployment_targets: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[ReleaseVersion], str]:
        if not version_tag or not title:
            return False, None, "Version tag and release title are required."

        rel = ReleaseVersion(
            version_tag=version_tag,
            project_id=project_id,
            title=title,
            release_notes=release_notes,
            author=author,
            deployment_targets=deployment_targets or ["Development", "Staging"]
        )

        saved = self.repo.save_release(rel)
        EventBus.publish("release_created", release_id=saved.id, version=version_tag)
        return True, saved, f"Release {version_tag} created successfully."

    def _execute_deployment_simulation(self, deployment: Deployment) -> None:
        deployment.status = Deployment.STATE_DEPLOYING
        deployment.logs.append(f"[{get_utc_now_iso()}] Provisioning container targets in {deployment.environment}...")
        deployment.logs.append(f"[{get_utc_now_iso()}] Pulling container image metadata for version {deployment.version}...")
        
        # Simulate high success rate
        success = random.random() > 0.05
        if success:
            deployment.status = Deployment.STATE_SUCCESS
            deployment.logs.append(f"[{get_utc_now_iso()}] Health checks passed (200 OK). Deployment SUCCESS.")
        else:
            deployment.status = Deployment.STATE_FAILED
            deployment.logs.append(f"[{get_utc_now_iso()}] ERROR: Health check timeout (503 Service Unavailable). Deployment FAILED.")

        deployment.completed_at = get_utc_now_iso()
