from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.incident import Incident

class IncidentRepository:
    """Repository handling Incident lifecycle persistence and seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "incidents.json")
        self._seed_default_incidents()

    def _seed_default_incidents(self) -> None:
        if self.store.count() == 0:
            defaults = [
                Incident(
                    title="High Latency on Payment Gateway DB Pool",
                    service="Payment Service",
                    environment="Production",
                    assignee="devops",
                    severity=Incident.SEV_HIGH,
                    status=Incident.STATUS_INVESTIGATING,
                    summary="Database connection pool saturation causing 504 Gateway Timeouts."
                ),
                Incident(
                    title="Auth Service Token Verification Failure",
                    service="Auth Service",
                    environment="Staging",
                    assignee="developer",
                    severity=Incident.SEV_MEDIUM,
                    status=Incident.STATUS_RESOLVED,
                    summary="Expired secret key rotation caused brief authentication failures."
                )
            ]
            for inc in defaults:
                self.store.insert(inc.to_dict())

    def get_by_id(self, incident_id: str) -> Optional[Incident]:
        data = self.store.find_by_id(incident_id)
        return Incident.from_dict(data) if data else None

    def get_all(self) -> List[Incident]:
        records = self.store.read_all()
        incidents = [Incident.from_dict(r) for r in records]
        return sorted(incidents, key=lambda x: x.created_at, reverse=True)

    def save(self, incident: Incident) -> Incident:
        existing = self.get_by_id(incident.id)
        if existing:
            self.store.update(incident.id, incident.to_dict())
        else:
            self.store.insert(incident.to_dict())
        return incident
