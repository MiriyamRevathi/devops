import pytest
import shutil
import tempfile
from models.metric import MetricSample, DORAMetricsResult
from repositories.monitoring_repo import MonitoringRepository
from services.monitoring_service import MonitoringService

@pytest.fixture
def temp_mon_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_metric_models():
    sample = MetricSample(cpu_percent=15.2, memory_percent=55.0, disk_percent=40.0)
    assert sample.cpu_percent == 15.2

    dora = DORAMetricsResult(
        deployment_frequency_per_day=4.2,
        lead_time_hours=1.5,
        change_failure_rate_percent=3.5,
        mttr_hours=0.8,
        rating="Elite"
    )
    assert dora.rating == "Elite"

def test_monitoring_service_analytics(temp_mon_dir):
    repo = MonitoringRepository(temp_mon_dir)
    service = MonitoringService(repo)

    sample = service.collect_current_sample()
    assert sample is not None
    assert sample.cpu_percent >= 0.0

    dora = service.calculate_dora_metrics()
    assert dora is not None
    assert dora.rating in ["Elite", "High", "Medium", "Low"]

    stats = service.get_aggregated_stats()
    assert "avg_cpu" in stats
    assert "avg_memory" in stats
