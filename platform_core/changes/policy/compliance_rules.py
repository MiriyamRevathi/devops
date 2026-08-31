"""
Compliance & Security Policy Rules for changes.
"""
from typing import Tuple, List, Dict, Any

class ChangesComplianceRules:
    """Audits compliance rules and governance controls for changes."""
    @staticmethod
    def audit_governance_rules(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        violations = []
        if not payload:
            violations.append("Payload structure is empty.")
            return False, violations
        if "id" not in payload:
            violations.append("Record missing immutable ID.")
        return len(violations) == 0, violations
