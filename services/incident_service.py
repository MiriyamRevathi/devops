from typing import Tuple, Optional, List, Dict, Any
from repositories.incident_repo import IncidentRepository
from models.incident import Incident
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class IncidentService:
    """Incident Response Lifecycle Engine."""

    def __init__(self, repository: IncidentRepository):
        self.repo = repository

    def create_incident(
        self,
        title: str,
        service: str,
        environment: str,
        severity: str = Incident.SEV_HIGH,
        summary: str = "",
        assignee: str = "unassigned"
    ) -> Tuple[bool, Optional[Incident], str]:
        if not title:
            return False, None, "Incident title is required."

        inc = Incident(
            title=title,
            service=service,
            environment=environment,
            severity=severity,
            summary=summary,
            assignee=assignee
        )

        saved = self.repo.save(inc)
        EventBus.publish("incident_created", incident_id=saved.id, title=saved.title, severity=saved.severity)
        return True, saved, "Incident reported successfully."

    def update_status(self, incident_id: str, new_status: str, actor: str, notes: str = "") -> Tuple[bool, str]:
        inc = self.repo.get_by_id(incident_id)
        if not inc:
            return False, "Incident not found."

        inc.status = new_status
        if new_status in [Incident.STATUS_RESOLVED, Incident.STATUS_CLOSED]:
            inc.resolved_at = get_utc_now_iso()

        inc.timeline.append({
            "timestamp": get_utc_now_iso(),
            "actor": actor,
            "action": f"Status updated to {new_status}",
            "notes": notes or f"Status changed by {actor}"
        })

        self.repo.save(inc)
        EventBus.publish("incident_status_changed", incident_id=incident_id, status=new_status)
        return True, f"Incident status updated to {new_status}."

    def assign_incident(self, incident_id: str, assignee: str, actor: str) -> Tuple[bool, str]:
        inc = self.repo.get_by_id(incident_id)
        if not inc:
            return False, "Incident not found."

        inc.assignee = assignee
        inc.timeline.append({
            "timestamp": get_utc_now_iso(),
            "actor": actor,
            "action": f"Assigned to {assignee}",
            "notes": f"Incident ownership assigned to {assignee}"
        })

        self.repo.save(inc)
        return True, f"Incident assigned to {assignee}."
