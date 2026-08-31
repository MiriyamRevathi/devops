"""
Compliance and Constraint Validator for dora_analytics_engine.
"""
from typing import Tuple, List, Dict, Any

class DoraAnalyticsEngineValidator:
    """Validates compliance and constraint rules for dora_analytics_engine."""
    @staticmethod
    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload:
            errors.append("Payload cannot be empty.")
        return len(errors) == 0, errors
