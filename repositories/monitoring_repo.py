import random
from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.metric import MetricSample

class MonitoringRepository:
    """Repository handling system metric history persistence and seed samples."""

    def __init__(self, data_directory: str):
        self.store = JSONStore(data_directory, "metrics.json")
        self._seed_default_metrics()

    def _seed_default_metrics(self) -> None:
        if self.store.count() == 0:
            # Seed 20 historical metric samples
            for i in range(20):
                sample = MetricSample(
                    cpu_percent=round(random.uniform(15.0, 75.0), 1),
                    memory_percent=round(random.uniform(40.0, 80.0), 1),
                    disk_percent=round(random.uniform(55.0, 65.0), 1),
                    response_time_ms=round(random.uniform(80.0, 350.0), 1),
                    error_rate=round(random.uniform(0.001, 0.035), 3),
                    request_rate=round(random.uniform(100.0, 500.0), 1)
                )
                self.store.insert(sample.to_dict())

    def get_all_samples(self) -> List[MetricSample]:
        return [MetricSample.from_dict(r) for r in self.store.read_all()]

    def save_sample(self, sample: MetricSample) -> MetricSample:
        self.store.insert(sample.to_dict())
        return sample
