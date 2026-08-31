"""
Business Logic Engine for deployments.
Enforces business rules, validation matrices, state transitions, and compliance.
"""
from typing import Dict, Any, List, Optional, Tuple
from utils.helpers import get_utc_now_iso, generate_id
from utils.validators import DataValidator

class DeploymentsBusinessEngine:
    """Primary business rule processing engine for deployments."""
    def __init__(self, engine_id: Optional[str] = None):
        self.engine_id = engine_id or generate_id("eng_dep")
        self.rules_passed = 0
        self.rules_failed = 0

    def validate_and_process(self, payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], str]:
        if not payload:
            self.rules_failed += 1
            return False, {}, "Payload cannot be empty."

        name = payload.get("name", "")
        if "name" in payload and (not name or len(name.strip()) < 2):
            self.rules_failed += 1
            return False, {}, "Name field must be at least 2 characters."

        self.rules_passed += 1
        processed = dict(payload)
        processed["processed_by_engine"] = self.engine_id
        processed["processed_at"] = get_utc_now_iso()
        return True, processed, "Successfully validated and processed."

    def calculate_risk_score(self, entity_data: Dict[str, Any]) -> float:
        base_score = 10.0
        status = entity_data.get("status", "ACTIVE")
        if status in ["FAILED", "DOWN", "DEGRADED", "CRITICAL"]:
            base_score += 45.0
        if entity_data.get("error_rate", 0) > 0.05:
            base_score += 30.0
        return min(100.0, base_score)
