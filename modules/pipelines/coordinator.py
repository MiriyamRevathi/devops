"""
Operations Coordinator and Event Handler for pipelines.
"""
from typing import Dict, Any, Optional
from core.events import EventBus
from utils.helpers import get_utc_now_iso

class PipelinesCoordinator:
    """Coordinates background events, notifications, and workflow state changes for pipelines."""
    def __init__(self, name: str = "pipelines"):
        self.name = name
        self.status = "INITIALIZED"

    def handle_system_event(self, event_name: str, payload: Dict[str, Any]) -> bool:
        EventBus.publish(f"pipelines_event_handled", event_name=event_name, payload=payload)
        return True
