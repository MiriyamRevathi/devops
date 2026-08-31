from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.change import ChangeRequest

class ChangeRepository:
    """Repository handling Change Requests persistence and default seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "change_requests.json")
        self._seed_default_changes()

    def _seed_default_changes(self) -> None:
        if self.store.count() == 0:
            defaults = [
                ChangeRequest(
                    title="Production Database Engine Major Version Upgrade",
                    description="Upgrade PostgreSQL 14 to PostgreSQL 15 on primary cluster.",
                    affected_services="Payment Service, Auth Service",
                    risk_level="HIGH",
                    impact="CRITICAL",
                    rollback_plan="Failover to standby v14 replica",
                    requester="devops",
                    status=ChangeRequest.STATUS_APPROVED,
                    approvers=["admin"]
                ),
                ChangeRequest(
                    title="API Gateway TLS 1.3 Strict Enforcement",
                    description="Disable TLS 1.0/1.1 protocols across all ingress routes.",
                    affected_services="API Gateway",
                    risk_level="LOW",
                    impact="MODERATE",
                    rollback_plan="Re-enable TLS 1.2 fallback",
                    requester="developer",
                    status=ChangeRequest.STATUS_REVIEW
                )
            ]
            for c in defaults:
                self.store.insert(c.to_dict())

    def get_by_id(self, change_id: str) -> Optional[ChangeRequest]:
        data = self.store.find_by_id(change_id)
        return ChangeRequest.from_dict(data) if data else None

    def get_all(self) -> List[ChangeRequest]:
        return [ChangeRequest.from_dict(r) for r in self.store.read_all()]

    def save(self, change: ChangeRequest) -> ChangeRequest:
        existing = self.get_by_id(change.id)
        if existing:
            self.store.update(change.id, change.to_dict())
        else:
            self.store.insert(change.to_dict())
        return change
