from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.alert import AlertRule

class AlertRepository:
    """Repository managing Alert Rules persistence and seeds."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "alert_rules.json")
        self._seed_default_rules()

    def _seed_default_rules(self) -> None:
        if self.store.count() == 0:
            defaults = [
                AlertRule("High CPU Usage Alert", "CPU", ">", 80.0, service="All"),
                AlertRule("Memory Saturation Warning", "Memory", ">", 85.0, service="All"),
                AlertRule("Elevated Error Rate Alert", "Error Rate", ">", 0.05, service="Payment Service"),
                AlertRule("Latency Spike Alert", "Response Time", ">", 1000.0, service="API Gateway")
            ]
            for rule in defaults:
                self.store.insert(rule.to_dict())

    def get_by_id(self, alert_id: str) -> Optional[AlertRule]:
        data = self.store.find_by_id(alert_id)
        return AlertRule.from_dict(data) if data else None

    def get_all(self) -> List[AlertRule]:
        return [AlertRule.from_dict(r) for r in self.store.read_all()]

    def save(self, rule: AlertRule) -> AlertRule:
        existing = self.get_by_id(rule.id)
        if existing:
            self.store.update(rule.id, rule.to_dict())
        else:
            self.store.insert(rule.to_dict())
        return rule
