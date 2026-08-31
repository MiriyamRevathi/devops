"""
Notification Dispatcher and Alert Handler for incidents.
"""
from typing import Dict, Any, List
from core.events import EventBus
from utils.helpers import get_utc_now_iso

class IncidentsNotifier:
    """Dispatches alert notifications and webhooks for incidents."""
    def __init__(self, channel: str = "#devops-incidents"):
        self.channel = channel

    def send_alert_notification(self, title: str, message: str, severity: str = "INFO") -> Dict[str, Any]:
        payload = {
            "channel": self.channel,
            "title": title,
            "message": message,
            "severity": severity,
            "dispatched_at": get_utc_now_iso()
        }
        EventBus.publish(f"incidents_notification_sent", payload=payload)
        return payload
