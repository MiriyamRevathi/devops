import pytest
import shutil
import tempfile
from models.pipeline import Pipeline, PipelineRun, PipelineStage
from repositories.pipeline_repo import PipelineRepository
from services.pipeline_engine import PipelineEngine

@pytest.fixture
def temp_pipe_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_pipeline_models():
    stg = PipelineStage(name="Lint", order=2)
    assert stg.name == "Lint"

    run = PipelineRun(pipeline_id="p1", project_id="proj1", run_number=3)
    assert run.status == PipelineRun.STATE_CREATED

def test_pipeline_engine_execution(temp_pipe_dir):
    repo = PipelineRepository(temp_pipe_dir)
    engine = PipelineEngine(repo)

    success, pipe, msg = engine.create_pipeline(
        name="Build Pipeline",
        project_id="proj_test",
        description="Test CI pipeline",
        stage_names=["Checkout", "Build"]
    )
    assert success is True
    assert pipe is not None

    run_success, run, run_msg = engine.trigger_run(
        pipeline_id=pipe.id,
        branch="main",
        triggered_by="tester"
    )
    assert run_success is True
    assert run is not None
    assert run.status in [PipelineRun.STATE_SUCCESS, PipelineRun.STATE_FAILED]
    assert len(run.stage_results) > 0

def test_pipeline_failure_simulation(temp_pipe_dir):
    repo = PipelineRepository(temp_pipe_dir)
    engine = PipelineEngine(repo)

    pipelines = repo.get_all()
    pipe_id = pipelines[0].id

    run_success, run, _ = engine.trigger_run(
        pipeline_id=pipe_id,
        branch="main",
        simulate_failure=True
    )
    assert run_success is True
    assert run.status == PipelineRun.STATE_FAILED
