"""
LatencyDistribution component for Logs enterprise domain module.
Enforces real-time operational processing, metrics calculation, and state management.
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from utils.helpers import get_utc_now_iso, generate_id
from core.events import EventBus

class LogsLatencyDistributionProcessor:
    """Operational processor for LatencyDistribution in Logs."""
    def __init__(self, processor_id: Optional[str] = None):
        self.id = processor_id or generate_id("proc_log_lat")
        self.status = "OPERATIONAL"
        self.execution_count = 0

    def execute_task(self, task_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.execution_count += 1
        if not payload:
            return {"status": "ERROR", "message": "Payload empty."}
        
        result = {
            "processor_id": self.id,
            "domain": "logs",
            "subcomponent": "latency_distribution",
            "task": task_name,
            "status": "SUCCESS",
            "execution_count": self.execution_count,
            "executed_at": get_utc_now_iso()
        }
        
        EventBus.publish(f"logs_latency_distribution_task_executed", result=result)
        return result

    def evaluate_telemetry(self, samples: List[float]) -> Dict[str, float]:
        if not samples:
            return {"mean": 0.0, "p95": 0.0, "max": 0.0}
        arr = np.array(samples)
        return {
            "mean": round(float(np.mean(arr)), 2),
            "p95": round(float(np.percentile(arr, 95)), 2),
            "max": round(float(np.max(arr)), 2)
        }
