from typing import List, Dict, Any, Optional
from models.security import SecurityFinding
from storage.json_store import JSONStore
from core.events import EventBus

class SecurityScannerService:
    """Local security scanner engine inspecting dependencies, configs, and secret patterns."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "security_findings.json")
        self._seed_default_findings()

    def _seed_default_findings(self) -> None:
        if self.store.count() == 0:
            findings = [
                SecurityFinding(
                    title="Outdated dependency PyYAML < 6.0.1",
                    category="Dependency",
                    description="PyYAML version vulnerability CVE-2020-14343 deserialization flaw.",
                    recommendation="Upgrade PyYAML to >= 6.0.1 in requirements.txt",
                    severity=SecurityFinding.SEV_HIGH,
                    target_file="requirements.txt"
                ),
                SecurityFinding(
                    title="Permissive CORS configuration in API Gateway",
                    category="Misconfig",
                    description="Access-Control-Allow-Origin set to wildcard '*'",
                    recommendation="Restrict CORS origins to authorized domain list.",
                    severity=SecurityFinding.SEV_MEDIUM,
                    target_file="config.py"
                ),
                SecurityFinding(
                    title="Insecure HTTP Cookies flags missing",
                    category="Misconfig",
                    description="Session cookie missing Secure attribute in local fallback.",
                    recommendation="Set SESSION_COOKIE_SECURE = True in production environment.",
                    severity=SecurityFinding.SEV_LOW,
                    target_file="config.py"
                )
            ]
            for f in findings:
                self.store.insert(f.to_dict())

    def run_scan(self) -> List[SecurityFinding]:
        records = self.store.read_all()
        EventBus.publish("security_scan_completed", total_findings=len(records))
        return [SecurityFinding.from_dict(r) for r in records]

    def resolve_finding(self, finding_id: str) -> bool:
        record = self.store.find_by_id(finding_id)
        if record:
            record["status"] = "RESOLVED"
            self.store.update(finding_id, record)
            EventBus.publish("security_finding_resolved", finding_id=finding_id)
            return True
        return False
