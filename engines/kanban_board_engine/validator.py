"""
Compliance and Constraint Validator for kanban_board_engine.
"""
from typing import Tuple, List, Dict, Any

class KanbanBoardEngineValidator:
    """Validates compliance and constraint rules for kanban_board_engine."""
    @staticmethod
    def validate_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload:
            errors.append("Payload cannot be empty.")
        return len(errors) == 0, errors
