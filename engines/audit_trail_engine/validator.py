"""
Compliance and Constraint Validator for audit_trail_engine.
"""
from typing import Tuple, List, Dict, Any

class AuditTrailEngineValidator:
    """Validates compliance and constraint rules for audit_trail_engine."""
    @staticmethod
    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload:
            errors.append("Payload cannot be empty.")
        return len(errors) == 0, errors
