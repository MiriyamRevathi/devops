from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.audit import AuditEvent

class AuditRepository:
    """Repository handling Audit trail log persistence and default seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "audit_events.json")
        self._seed_default_audit_events()

    def _seed_default_audit_events(self) -> None:
        if self.store.count() == 0:
            defaults = [
                AuditEvent("user_login", "admin", "AuthService", "Admin user logged in successfully"),
                AuditEvent("project_created", "admin", "ProjectRepository", "Created project 'DevOpsFlow Platform'"),
                AuditEvent("pipeline_executed", "devops", "PipelineEngine", "Executed pipeline run #1 on branch main"),
                AuditEvent("deployment_completed", "devops", "DeploymentService", "Deployed version v1.0.0 to Production")
            ]
            for evt in defaults:
                self.store.insert(evt.to_dict())

    def get_all(self) -> List[AuditEvent]:
        records = self.store.read_all()
        events = [AuditEvent.from_dict(r) for r in records]
        return sorted(events, key=lambda x: x.timestamp, reverse=True)

    def log_event(self, event: AuditEvent) -> AuditEvent:
        self.store.insert(event.to_dict())
        return event

    def search(self, query: str = "", event_type: str = "", actor: str = "") -> List[AuditEvent]:
        events = self.get_all()
        if event_type and event_type.lower() != "all":
            events = [e for e in events if e.event_type.lower() == event_type.lower()]
        if actor and actor.lower() != "all":
            events = [e for e in events if e.actor.lower() == actor.lower()]
        if query:
            q = query.lower()
            events = [e for e in events if q in e.details.lower() or q in e.resource.lower()]
        return events
