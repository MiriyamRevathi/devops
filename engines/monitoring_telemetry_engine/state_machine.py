"""
State Machine Manager for monitoring_telemetry_engine.
"""
from typing import Tuple, List, Dict, Any

class MonitoringTelemetryEngineStateMachine:
    """Manages lifecycle state transitions for monitoring_telemetry_engine."""
    VALID_STATES = ["INITIALIZED", "QUEUED", "RUNNING", "PAUSED", "SUCCESS", "FAILED", "COMPLETED"]

    def __init__(self, current_state: str = "INITIALIZED"):
        self.current_state = current_state if current_state in self.VALID_STATES else "INITIALIZED"
        self.transition_history: List[Dict[str, str]] = []

    def transition_to(self, new_state: str, reason: str = "") -> Tuple[bool, str]:
        if new_state not in self.VALID_STATES:
            return False, f"Invalid state transition target: {new_state}"
        
        self.transition_history.append({"from": self.current_state, "to": new_state, "reason": reason})
        self.current_state = new_state
        return True, f"Transitioned to {new_state}"
