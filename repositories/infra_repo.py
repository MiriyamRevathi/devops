from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.infrastructure import InfraResource, IaCPlan

class InfrastructureRepository:
    """Repository handling Infrastructure resources and IaC plan persistence."""

    def __init__(self, data_directory: str):
        self.resource_store = JSONStore(data_directory, "infra_resources.json")
        self.plan_store = JSONStore(data_directory, "infra_plans.json")
        self._seed_default_infrastructure()

    def _seed_default_infrastructure(self) -> None:
        if self.resource_store.count() == 0:
            resources = [
                InfraResource("k8s-master-node-01", "server", environment="Production", status=InfraResource.STATE_APPLIED, config={"cpus": 8, "memory_gb": 32}),
                InfraResource("postgres-db-cluster", "database", environment="Production", status=InfraResource.STATE_APPLIED, config={"engine": "postgresql", "storage_gb": 500}),
                InfraResource("redis-session-store", "cache", environment="Production", status=InfraResource.STATE_APPLIED, config={"memory_gb": 8}),
                InfraResource("main-load-balancer", "load_balancer", environment="Production", status=InfraResource.STATE_APPLIED, config={"scheme": "internet-facing"})
            ]
            for r in resources:
                self.resource_store.insert(r.to_dict())

    def get_resource_by_id(self, res_id: str) -> Optional[InfraResource]:
        data = self.resource_store.find_by_id(res_id)
        return InfraResource.from_dict(data) if data else None

    def get_all_resources(self) -> List[InfraResource]:
        return [InfraResource.from_dict(r) for r in self.resource_store.read_all()]

    def save_resource(self, res: InfraResource) -> InfraResource:
        existing = self.get_resource_by_id(res.id)
        if existing:
            self.resource_store.update(res.id, res.to_dict())
        else:
            self.resource_store.insert(res.to_dict())
        return res

    def get_plan_by_id(self, plan_id: str) -> Optional[IaCPlan]:
        data = self.plan_store.find_by_id(plan_id)
        return IaCPlan.from_dict(data) if data else None

    def get_all_plans(self) -> List[IaCPlan]:
        records = self.plan_store.read_all()
        plans = [IaCPlan.from_dict(r) for r in records]
        return sorted(plans, key=lambda x: x.created_at, reverse=True)

    def save_plan(self, plan: IaCPlan) -> IaCPlan:
        existing = self.get_plan_by_id(plan.id)
        if existing:
            self.plan_store.update(plan.id, plan.to_dict())
        else:
            self.plan_store.insert(plan.to_dict())
        return plan
