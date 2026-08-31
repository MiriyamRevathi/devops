from typing import Optional, List, Dict, Any
from storage.json_store import JSONStore
from models.pipeline import Pipeline, PipelineRun

class PipelineRepository:
    """Repository handling Pipeline definitions and Run history persistence."""

    def __init__(self, data_directory: str):
        self.pipeline_store = JSONStore(data_directory, "pipelines.json")
        self.runs_store = JSONStore(data_directory, "pipeline_runs.json")
        self._seed_default_pipelines()

    def _seed_default_pipelines(self) -> None:
        if self.pipeline_store.count() == 0:
            pipe = Pipeline(
                name="Main CI/CD Workflow",
                project_id="proj_default",
                description="Default Continuous Integration & Package Pipeline",
                last_run_status="SUCCESS",
                total_runs=12
            )
            self.pipeline_store.insert(pipe.to_dict())

            sample_run = PipelineRun(
                pipeline_id=pipe.id,
                project_id="proj_default",
                branch="main",
                commit_hash="a1b2c3d",
                run_number=1,
                status=PipelineRun.STATE_SUCCESS,
                duration_seconds=14.5,
                stage_results=[
                    {"stage_name": "Checkout", "status": "SUCCESS", "duration": 1.2},
                    {"stage_name": "Install", "status": "SUCCESS", "duration": 3.4},
                    {"stage_name": "Lint", "status": "SUCCESS", "duration": 2.1},
                    {"stage_name": "Unit Test", "status": "SUCCESS", "duration": 4.8},
                    {"stage_name": "Build", "status": "SUCCESS", "duration": 3.0}
                ],
                logs=["[INFO] Starting pipeline execution...", "[SUCCESS] Pipeline finished with code 0."]
            )
            self.runs_store.insert(sample_run.to_dict())

    def get_by_id(self, pipeline_id: str) -> Optional[Pipeline]:
        data = self.pipeline_store.find_by_id(pipeline_id)
        return Pipeline.from_dict(data) if data else None

    def get_by_project(self, project_id: str) -> List[Pipeline]:
        results = self.pipeline_store.find_where(lambda p: p.get("project_id") == project_id)
        return [Pipeline.from_dict(r) for r in results]

    def get_all(self) -> List[Pipeline]:
        return [Pipeline.from_dict(r) for r in self.pipeline_store.read_all()]

    def save(self, pipeline: Pipeline) -> Pipeline:
        existing = self.get_by_id(pipeline.id)
        if existing:
            self.pipeline_store.update(pipeline.id, pipeline.to_dict())
        else:
            self.pipeline_store.insert(pipeline.to_dict())
        return pipeline

    def save_run(self, run: PipelineRun) -> PipelineRun:
        existing = self.runs_store.find_by_id(run.id)
        if existing:
            self.runs_store.update(run.id, run.to_dict())
        else:
            self.runs_store.insert(run.to_dict())
        return run

    def get_run_by_id(self, run_id: str) -> Optional[PipelineRun]:
        data = self.runs_store.find_by_id(run_id)
        return PipelineRun.from_dict(data) if data else None

    def get_runs_for_pipeline(self, pipeline_id: str) -> List[PipelineRun]:
        results = self.runs_store.find_where(lambda r: r.get("pipeline_id") == pipeline_id)
        runs = [PipelineRun.from_dict(r) for r in results]
        return sorted(runs, key=lambda x: x.run_number, reverse=True)

    def get_all_runs(self) -> List[PipelineRun]:
        return [PipelineRun.from_dict(r) for r in self.runs_store.read_all()]
