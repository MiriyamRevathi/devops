from typing import List, Optional, Tuple, Dict, Any
from repositories.log_repo import LogRepository
from models.log_entry import LogEntry
from core.events import EventBus

class LogService:
    """Centralized Log Management Service."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = LogRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def log(
        self,
        service: str,
        environment: str,
        message: str,
        severity: str = LogEntry.SEVERITY_INFO,
        trace_id: Optional[str] = None
    ) -> LogEntry:
        entry = LogEntry(
            service=service,
            environment=environment,
            message=message,
            severity=severity,
            trace_id=trace_id
        )
        return self.repo.save(entry)

    def search_logs(
        self,
        service: str = "",
        environment: str = "",
        severity: str = "",
        query: str = ""
    ) -> List[LogEntry]:
        return self.repo.filter_logs(service=service, environment=environment, severity=severity, query=query)
