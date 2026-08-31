"""
Business rules and compliance checks for containers.
"""
from typing import Tuple, Optional, Dict, Any

class ContainersBusinessRules:
    """Enforces business rules and validation constraints for containers."""
    @staticmethod
    def evaluate_compliance(data: Dict[str, Any]) -> Tuple[bool, str]:
        if not data:
            return False, "Data payload cannot be empty."
        name = data.get("name", "")
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters."
        return True, "Compliant."
