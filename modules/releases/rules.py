"""
Business rules and compliance checks for releases.
"""
from typing import Tuple, Optional, Dict, Any

class ReleasesBusinessRules:
    """Enforces business rules and validation constraints for releases."""
    @staticmethod
    def evaluate_compliance(data: Dict[str, Any]) -> Tuple[bool, str]:
        if not data:
            return False, "Data payload cannot be empty."
        name = data.get("name", "")
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters."
        return True, "Compliant."
