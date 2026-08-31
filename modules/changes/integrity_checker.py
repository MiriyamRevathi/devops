"""
Data Integrity and Schema Validator for changes domain entities.
"""
from typing import Tuple, List, Dict, Any

class ChangesIntegrityChecker:
    """Validates schema integrity and constraint checks for changes."""
    @classmethod
    def validate_entity_schema(cls, entity: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not entity:
            return False, ["Entity dictionary cannot be null or empty."]
        if "id" not in entity:
            errors.append("Missing required field: 'id'")
        if "name" not in entity:
            errors.append("Missing required field: 'name'")
        return len(errors) == 0, errors
