import time
import random
from typing import Tuple, Optional, List, Dict, Any
from repositories.pipeline_repo import PipelineRepository
from models.pipeline import Pipeline, PipelineRun, PipelineStage
from utils.helpers import get_utc_now_iso, generate_id
from core.events import EventBus

class PipelineEngine:
    """CI/CD Pipeline Builder and Execution Engine."""

    def __init__(self, repository_or_dir):
        if isinstance(repository_or_dir, str):
            self.repo = PipelineRepository(repository_or_dir)
        else:
            self.repo = repository_or_dir

    def create_pipeline(
        self,
        name: str,
        project_id: str,
        description: str = "",
        stage_names: Optional[List[str]] = None
    ) -> Tuple[bool, Optional[Pipeline], str]:
        if not name:
            return False, None, "Pipeline name is required."

        stages = []
        names = stage_names or ["Checkout", "Install", "Lint", "Unit Test", "Build", "Publish Artifact"]
        for idx, stage_name in enumerate(names, start=1):
            stages.append(PipelineStage(name=stage_name, order=idx).to_dict())

        pipeline = Pipeline(
            name=name,
            project_id=project_id,
            description=description,
            stages=stages
        )

        saved = self.repo.save(pipeline)
        EventBus.publish("pipeline_created", pipeline_id=saved.id, name=saved.name)
        return True, saved, "Pipeline created successfully."

    def trigger_run(
        self,
        pipeline_id: str,
        branch: str = "main",
        commit_hash: str = "latest",
        triggered_by: str = "admin",
        simulate_failure: bool = False
    ) -> Tuple[bool, Optional[PipelineRun], str]:
        pipeline = self.repo.get_by_id(pipeline_id)
        if not pipeline:
            return False, None, "Pipeline not found."

        existing_runs = self.repo.get_runs_for_pipeline(pipeline_id)
        run_number = len(existing_runs) + 1

        run = PipelineRun(
            pipeline_id=pipeline_id,
            project_id=pipeline.project_id,
            branch=branch,
            commit_hash=commit_hash,
            run_number=run_number,
            triggered_by=triggered_by,
            status=PipelineRun.STATE_QUEUED,
            started_at=get_utc_now_iso()
        )

        saved_run = self.repo.save_run(run)

        # Execute run simulation
        self._execute_run_simulation(pipeline, saved_run, simulate_failure=simulate_failure)

        # Update pipeline metadata
        pipeline.total_runs += 1
        pipeline.last_run_status = saved_run.status
        self.repo.save(pipeline)

        EventBus.publish("pipeline_executed", run_id=saved_run.id, status=saved_run.status)
        return True, saved_run, f"Pipeline run #{run_number} finished with status {saved_run.status}."

    def _execute_run_simulation(
        self,
        pipeline: Pipeline,
        run: PipelineRun,
        simulate_failure: bool = False
    ) -> None:
        run.status = PipelineRun.STATE_RUNNING
        run.logs.append(f"[{get_utc_now_iso()}] Pipeline run #{run.run_number} initialized on branch {run.branch}.")

        stage_results = []
        overall_success = True

        for stage in sorted(pipeline.stages, key=lambda s: s.get("order", 1)):
            if not stage.get("enabled", True):
                stage_results.append({
                    "stage_name": stage["name"],
                    "status": "SKIPPED",
                    "duration": 0.0
                })
                run.logs.append(f"[{get_utc_now_iso()}] Stage '{stage['name']}' SKIPPED.")
                continue

            stage_name = stage["name"]
            run.logs.append(f"[{get_utc_now_iso()}] Executing stage: {stage_name}...")

            duration = round(random.uniform(0.8, 3.5), 2)
            
            # Decide pass/fail
            if simulate_failure and stage_name in ["Unit Test", "Integration Test", "Build"]:
                passed = False
            else:
                passed = random.random() > 0.1  # 90% pass rate in simulation

            if passed:
                stage_results.append({
                    "stage_name": stage_name,
                    "status": "SUCCESS",
                    "duration": duration
                })
                run.logs.append(f"[{get_utc_now_iso()}] Stage '{stage_name}' completed in {duration}s -> SUCCESS.")
            else:
                overall_success = False
                stage_results.append({
                    "stage_name": stage_name,
                    "status": "FAILED",
                    "duration": duration
                })
                run.logs.append(f"[{get_utc_now_iso()}] ERROR: Stage '{stage_name}' failed after {duration}s!")
                run.logs.append(f"[{get_utc_now_iso()}] Pipeline execution aborted.")
                break

        run.completed_at = get_utc_now_iso()
        run.duration_seconds = sum(sr["duration"] for sr in stage_results)
        run.status = PipelineRun.STATE_SUCCESS if overall_success else PipelineRun.STATE_FAILED
        run.stage_results = stage_results
        self.repo.save_run(run)
