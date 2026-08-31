"""
Notification Dispatcher and Alert Handler for source_control.
"""
from typing import Dict, Any, List
from core.events import EventBus
from utils.helpers import get_utc_now_iso

class SourceControlNotifier:
    """Dispatches alert notifications and webhooks for source_control."""
    def __init__(self, channel: str = "#devops-source_control"):
        self.channel = channel

    def send_alert_notification(self, title: str, message: str, severity: str = "INFO") -> Dict[str, Any]:
        payload = {
            "channel": self.channel,
            "title": title,
            "message": message,
            "severity": severity,
            "dispatched_at": get_utc_now_iso()
        }
        EventBus.publish(f"source_control_notification_sent", payload=payload)
        return payload
