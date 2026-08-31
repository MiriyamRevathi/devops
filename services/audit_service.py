from typing import List, Optional, Dict, Any
from repositories.audit_repo import AuditRepository
from models.audit import AuditEvent
from core.events import EventBus

class AuditService:
    """System-wide Audit Trail Service listening to EventBus events."""

    def __init__(self, repository: AuditRepository):
        self.repo = repository
        self._register_event_bus_listeners()

    def _register_event_bus_listeners(self) -> None:
        def on_event(event_name: str):
            def handler(**kwargs: Any):
                actor = kwargs.get("username") or kwargs.get("actor") or "system"
                resource = kwargs.get("project_id") or kwargs.get("pipeline_id") or kwargs.get("deployment_id") or "system"
                details = f"Event '{event_name}' published with parameters: {kwargs}"
                self.record_event(event_type=event_name, actor=actor, resource=resource, details=details)
            return handler

        for event in ["user_logged_in", "project_created", "pipeline_executed", "deployment_triggered", "iac_plan_applied"]:
            EventBus.subscribe(event, on_event(event))

    def record_event(self, event_type: str, actor: str, resource: str, details: str = "") -> AuditEvent:
        event = AuditEvent(event_type=event_type, actor=actor, resource=resource, details=details)
        return self.repo.log_event(event)

    def query_audit_trail(self, query: str = "", event_type: str = "", actor: str = "") -> List[AuditEvent]:
        return self.repo.search(query=query, event_type=event_type, actor=actor)
