import yaml
from typing import Tuple, Optional, List, Dict, Any
from repositories.infra_repo import InfrastructureRepository
from models.infrastructure import InfraResource, IaCPlan
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class IaCEngine:
    """Infrastructure-as-Code Plan -> Review -> Apply -> Destroy Execution Engine."""

    def __init__(self, repository: InfrastructureRepository):
        self.repo = repository

    def create_plan(
        self,
        project_id: str,
        environment: str,
        yaml_definition: str
    ) -> Tuple[bool, Optional[IaCPlan], str]:
        try:
            parsed = yaml.safe_load(yaml_definition) or {}
            resources = parsed.get("resources", [])
            to_add = len(resources)
            to_change = 0
            to_destroy = 0
        except Exception as e:
            return False, None, f"YAML Syntax Error: {e}"

        plan = IaCPlan(
            project_id=project_id,
            environment=environment,
            to_add=to_add,
            to_change=to_change,
            to_destroy=to_destroy,
            yaml_definition=yaml_definition,
            status="PLANNED",
            logs=[
                f"[{get_utc_now_iso()}] Terraform-style Plan generated.",
                f"[{get_utc_now_iso()}] Plan: {to_add} to add, {to_change} to change, {to_destroy} to destroy."
            ]
        )

        saved = self.repo.save_plan(plan)
        EventBus.publish("iac_plan_created", plan_id=saved.id, environment=environment)
        return True, saved, "IaC Plan generated successfully."

    def apply_plan(self, plan_id: str) -> Tuple[bool, str]:
        plan = self.repo.get_plan_by_id(plan_id)
        if not plan:
            return False, "IaC Plan not found."

        if plan.status == "APPLIED":
            return False, "Plan is already applied."

        plan.status = "APPLIED"
        plan.logs.append(f"[{get_utc_now_iso()}] Executing 'apply' phase...")

        try:
            parsed = yaml.safe_load(plan.yaml_definition) or {}
            resources = parsed.get("resources", [])
            for res_data in resources:
                res = InfraResource(
                    name=res_data.get("name", "unnamed-res"),
                    resource_type=res_data.get("type", "server"),
                    environment=plan.environment,
                    config=res_data,
                    status=InfraResource.STATE_APPLIED
                )
                self.repo.save_resource(res)
                plan.logs.append(f"[{get_utc_now_iso()}] Applied resource: {res.name} ({res.resource_type})")
        except Exception as e:
            plan.status = "FAILED"
            plan.logs.append(f"[{get_utc_now_iso()}] ERROR during apply: {e}")
            self.repo.save_plan(plan)
            return False, f"Apply failed: {e}"

        plan.logs.append(f"[{get_utc_now_iso()}] Apply complete! Resources provisioned.")
        self.repo.save_plan(plan)
        EventBus.publish("iac_plan_applied", plan_id=plan_id)
        return True, "Infrastructure Plan applied successfully."

    def destroy_resource(self, resource_id: str) -> Tuple[bool, str]:
        res = self.repo.get_resource_by_id(resource_id)
        if not res:
            return False, "Resource not found."

        res.status = InfraResource.STATE_DESTROYED
        res.updated_at = get_utc_now_iso()
        self.repo.save_resource(res)
        EventBus.publish("iac_resource_destroyed", resource_id=resource_id)
        return True, f"Resource '{res.name}' destroyed."
