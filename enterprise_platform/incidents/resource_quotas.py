"""
Resource Quotas and Capacity Limits for incidents.
"""
from typing import Tuple, Dict, Any

class IncidentsResourceQuotas:
    """Enforces resource allocation quotas for incidents."""
    def __init__(self, max_allowed: int = 100):
        self.max_allowed = max_allowed

    def check_quota(self, current_usage: int, requested: int) -> Tuple[bool, str]:
        if current_usage + requested > self.max_allowed:
            return False, f"Quota exceeded: current {current_usage} + requested {requested} > max {self.max_allowed}."
        return True, "Quota check passed."
