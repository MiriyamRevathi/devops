"""
Policy Engine and Compliance Auditor for artifacts.
Calculates security compliance, policy violations, and risk scoring.
"""
from typing import Dict, Any, List, Tuple
from utils.helpers import get_utc_now_iso

class ArtifactsPolicyEngine:
    """Policy engine enforcing operational governance for artifacts."""
    def __init__(self, policy_name: str = "artifacts_default_policy"):
        self.policy_name = policy_name
        self.rules_evaluated = 0

    def evaluate_resource_policy(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        self.rules_evaluated += 1
        violations = []
        if not resource_data:
            violations.append("Resource payload is empty.")
        
        status = resource_data.get("status", "ACTIVE")
        if status not in ["ACTIVE", "RUNNING", "SUCCESS", "APPROVED", "HEALTHY", "PLANNED", "APPLIED", "OPEN", "RESOLVED"]:
            violations.append(f"Unapproved resource status: {status}")
            
        risk_score = min(100.0, len(violations) * 25.0)
        return {
            "policy_name": self.policy_name,
            "is_compliant": len(violations) == 0,
            "violations": violations,
            "risk_score": risk_score,
            "evaluated_at": get_utc_now_iso()
        }
