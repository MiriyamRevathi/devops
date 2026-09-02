from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from core.security import login_required, permission_required, SecurityManager
from services.pipeline_engine import PipelineEngine
from repositories.pipeline_repo import PipelineRepository
from services.audit_service import AuditService
from models.pipeline import Pipeline

pipelines_bp = Blueprint("pipelines", __name__, url_prefix="/pipelines")

def get_pipeline_engine() -> PipelineEngine:
    repo = PipelineRepository(current_app.config["PIPELINES_DATA_DIR"])
    return PipelineEngine(repo)

def get_pipeline_repo() -> PipelineRepository:
    return PipelineRepository(current_app.config["PIPELINES_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@pipelines_bp.route("/", methods=["GET"])
@login_required
@permission_required("pipeline.view")
def index():
    repo = get_pipeline_repo()
    pipelines = repo.get_all()
    return render_template("pipelines/list.html", pipelines=pipelines)

@pipelines_bp.route("/builds", methods=["GET"])
@login_required
@permission_required("builds.view")
def builds():
    repo = get_pipeline_repo()
    all_runs = repo.get_all_runs()
    build_list = []
    for run in all_runs:
        pipeline = repo.get_by_id(run.pipeline_id)
        build_list.append({"pipeline": pipeline or Pipeline(name="CI Pipeline", project_id=run.project_id), "run": run})
    return render_template("pipelines/builds.html", builds=build_list)

@pipelines_bp.route("/<pipeline_id>", methods=["GET"])
@login_required
@permission_required("pipeline.view")
def detail(pipeline_id: str):
    repo = get_pipeline_repo()
    pipeline = repo.get_by_id(pipeline_id)
    if not pipeline:
        flash("Pipeline not found.", "danger")
        return redirect(url_for("pipelines.index"))
    runs = repo.get_runs_for_pipeline(pipeline_id)
    return render_template("pipelines/detail.html", pipeline=pipeline, runs=runs)

@pipelines_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("pipeline.create")
def create():
    if request.method == "POST":
        name = SecurityManager.sanitize_input(request.form.get("name", ""))
        project_id = request.form.get("project_id", "PROJ-101")
        description = SecurityManager.sanitize_input(request.form.get("description", ""))

        if not name:
            flash("Pipeline Name is required.", "danger")
            return render_template("pipelines/create.html")

        engine = get_pipeline_engine()
        success, new_p, msg = engine.create_pipeline(name=name, project_id=project_id, description=description)

        if success and new_p:
            audit = get_audit_service()
            audit.record_event(
                actor=session.get("username", "Unknown"),
                event_type="PIPELINE_CREATED",
                resource=f"Pipeline:{new_p.id}",
                details=f"Created pipeline '{name}' for project '{project_id}'."
            )
            flash(f"Pipeline '{name}' created.", "success")
            return redirect(url_for("pipelines.index"))
        else:
            flash(msg, "danger")

    return render_template("pipelines/create.html")

@pipelines_bp.route("/<pipeline_id>/run", methods=["POST"], endpoint="run_pipeline")
@login_required
@permission_required("pipeline.run")
def trigger_run(pipeline_id: str):
    engine = get_pipeline_engine()
    branch = request.form.get("branch", "main")
    triggered_by = session.get("username", "user")

    success, run, msg = engine.trigger_run(pipeline_id=pipeline_id, branch=branch, triggered_by=triggered_by)
    if success and run:
        audit = get_audit_service()
        audit.record_event(
            actor=triggered_by,
            event_type="PIPELINE_EXECUTED",
            resource=f"Pipeline:{pipeline_id}",
            details=f"Executed pipeline run #{run.run_number} with status '{run.status}'."
        )
        flash(f"Pipeline run #{run.run_number} executed ({run.status}).", "info")
    else:
        flash(msg, "danger")

    return redirect(url_for("pipelines.detail", pipeline_id=pipeline_id))

@pipelines_bp.route("/<pipeline_id>/runs/<run_id>", methods=["GET"])
@login_required
@permission_required("pipeline.view")
def run_detail(pipeline_id: str, run_id: str):
    repo = get_pipeline_repo()
    pipeline = repo.get_by_id(pipeline_id)
    run = repo.get_run_by_id(run_id)
    if not pipeline or not run:
        flash("Pipeline run details not found.", "danger")
        return redirect(url_for("pipelines.index"))
    return render_template("pipelines/run_detail.html", pipeline=pipeline, run=run)
