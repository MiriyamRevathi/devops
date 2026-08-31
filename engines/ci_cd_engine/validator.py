"""
Compliance and Constraint Validator for ci_cd_engine.
"""
from typing import Tuple, List, Dict, Any

class CiCdEngineValidator:
    """Validates compliance and constraint rules for ci_cd_engine."""
    @staticmethod
    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload:
            errors.append("Payload cannot be empty.")
        return len(errors) == 0, errors
