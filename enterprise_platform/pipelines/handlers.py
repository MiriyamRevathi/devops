"""
Event Handlers and Event Stream Subscriptions for pipelines.
Subscribes to system event bus notifications and triggers audit events.
"""
from typing import Dict, Any, Optional
from core.events import EventBus
from utils.helpers import get_utc_now_iso

class PipelinesEventHandler:
    """Handles system events for pipelines."""
    def __init__(self, handler_id: str = "hdr_pip"):
        self.handler_id = handler_id
        self.handled_count = 0

    def on_domain_event(self, event_name: str, payload: Dict[str, Any]) -> bool:
        self.handled_count += 1
        EventBus.publish(f"pipelines_event_processed", handler=self.handler_id, event=event_name)
        return True
