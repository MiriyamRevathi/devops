"""
Business rules and compliance checks for auth.
"""
from typing import Tuple, Optional, Dict, Any

class AuthBusinessRules:
    """Enforces business rules and validation constraints for auth."""
    @staticmethod
    def evaluate_compliance(data: Dict[str, Any]) -> Tuple[bool, str]:
        if not data:
            return False, "Data payload cannot be empty."
        name = data.get("name", "")
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters."
        return True, "Compliant."
