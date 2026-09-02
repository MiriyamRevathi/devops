import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.alert_repo import AlertRepository
from models.alert import AlertRule
from utils.helpers import get_utc_now_iso
from core.events import EventBus

class AlertService:
    """Alert Rules Management and Automated Trigger Evaluation Engine."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = AlertRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def create_rule(
        self,
        name: str,
        metric: str,
        condition: str,
        threshold: float,
        service: str = "All"
    ) -> Tuple[bool, Optional[AlertRule], str]:
        if not name:
            return False, None, "Alert rule name is required."

        rule = AlertRule(
            name=name,
            metric=metric,
            condition=condition,
            threshold=threshold,
            service=service
        )

        saved = self.repo.save(rule)
        EventBus.publish("alert_rule_created", alert_id=saved.id, name=saved.name)
        return True, saved, "Alert rule created successfully."

    def trigger_simulation(self, alert_id: str) -> Tuple[bool, str]:
        rule = self.repo.get_by_id(alert_id)
        if not rule:
            return False, "Alert rule not found."

        rule.triggered = True
        rule.last_triggered_at = get_utc_now_iso()
        self.repo.save(rule)
        EventBus.publish("alert_triggered", alert_id=alert_id, name=rule.name)
        return True, f"Alert rule '{rule.name}' triggered!"

    def resolve_alert(self, alert_id: str) -> Tuple[bool, str]:
        rule = self.repo.get_by_id(alert_id)
        if not rule:
            return False, "Alert rule not found."

        rule.triggered = False
        self.repo.save(rule)
        EventBus.publish("alert_resolved", alert_id=alert_id)
        return True, f"Alert '{rule.name}' resolved."
