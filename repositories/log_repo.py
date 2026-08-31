from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.log_entry import LogEntry

class LogRepository:
    """Repository handling Log entry persistence and seed logs."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "logs.json")
        self._seed_default_logs()

    def _seed_default_logs(self) -> None:
        if self.store.count() == 0:
            defaults = [
                LogEntry("API Gateway", "Production", "HTTP 200 GET /api/v1/health", LogEntry.SEVERITY_INFO),
                LogEntry("Auth Service", "Production", "JWT verification cache hit ratio 98.4%", LogEntry.SEVERITY_INFO),
                LogEntry("Payment Service", "Production", "Database pool latency spike > 120ms", LogEntry.SEVERITY_WARNING),
                LogEntry("Payment Service", "Production", "Connection timeout connecting to DB replica 2", LogEntry.SEVERITY_ERROR),
                LogEntry("Notification Service", "Staging", "SMTP debug connection established", LogEntry.SEVERITY_DEBUG)
            ]
            for log in defaults:
                self.store.insert(log.to_dict())

    def get_all(self) -> List[LogEntry]:
        records = self.store.read_all()
        logs = [LogEntry.from_dict(r) for r in records]
        return sorted(logs, key=lambda x: x.timestamp, reverse=True)

    def filter_logs(
        self,
        service: str = "",
        environment: str = "",
        severity: str = "",
        query: str = ""
    ) -> List[LogEntry]:
        logs = self.get_all()
        if service and service.lower() != "all":
            logs = [l for l in logs if l.service.lower() == service.lower()]
        if environment and environment.lower() != "all":
            logs = [l for l in logs if l.environment.lower() == environment.lower()]
        if severity and severity.lower() != "all":
            logs = [l for l in logs if l.severity.lower() == severity.lower()]
        if query:
            q = query.lower()
            logs = [l for l in logs if q in l.message.lower() or q in l.trace_id.lower()]
        return logs

    def save(self, log: LogEntry) -> LogEntry:
        self.store.insert(log.to_dict())
        return log
