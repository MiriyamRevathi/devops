"""
Compliance and Constraint Validator for security_scanner_engine.
"""
from typing import Tuple, List, Dict, Any

class SecurityScannerEngineValidator:
    """Validates compliance and constraint rules for security_scanner_engine."""
    @staticmethod
    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload:
            errors.append("Payload cannot be empty.")
        return len(errors) == 0, errors
