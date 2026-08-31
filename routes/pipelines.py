from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.pipeline_engine import PipelineEngine
from repositories.pipeline_repo import PipelineRepository
from models.pipeline import PipelineStage

pipelines_bp = Blueprint("pipelines", __name__, url_prefix="/pipelines")

def get_pipeline_engine() -> PipelineEngine:
    repo = PipelineRepository(current_app.config["PIPELINES_DATA_DIR"])
    return PipelineEngine(repo)

@pipelines_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_pipeline_engine()
    pipelines = engine.repo.get_all()
    all_runs = engine.repo.get_all_runs()
    return render_template("pipelines/list.html", pipelines=pipelines, runs=all_runs)

@pipelines_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        project_id = request.form.get("project_id", "proj_default").strip()
        description = request.form.get("description", "").strip()
        selected_stages = request.form.getlist("stages")

        engine = get_pipeline_engine()
        success, pipe, msg = engine.create_pipeline(
            name=name,
            project_id=project_id,
            description=description,
            stage_names=selected_stages
        )

        if success and pipe:
            flash(msg, "success")
            return redirect(url_for("pipelines.detail", pipeline_id=pipe.id))
        else:
            flash(msg, "danger")

    return render_template("pipelines/create.html", available_stages=PipelineStage.STAGES)

@pipelines_bp.route("/<pipeline_id>")
def detail(pipeline_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_pipeline_engine()
    pipe = engine.repo.get_by_id(pipeline_id)
    if not pipe:
        flash("Pipeline not found.", "warning")
        return redirect(url_for("pipelines.index"))

    runs = engine.repo.get_runs_for_pipeline(pipeline_id)
    return render_template("pipelines/detail.html", pipeline=pipe, runs=runs)

@pipelines_bp.route("/<pipeline_id>/run", methods=["POST"])
def run_pipeline(pipeline_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    branch = request.form.get("branch", "main").strip()
    simulate_fail = request.form.get("simulate_failure") == "true"
    triggered_by = session.get("username", "admin")

    engine = get_pipeline_engine()
    success, run, msg = engine.trigger_run(
        pipeline_id=pipeline_id,
        branch=branch,
        triggered_by=triggered_by,
        simulate_failure=simulate_fail
    )

    flash(msg, "success" if success and run and run.status == "SUCCESS" else "warning")
    if run:
        return redirect(url_for("pipelines.run_detail", run_id=run.id))
    return redirect(url_for("pipelines.detail", pipeline_id=pipeline_id))

@pipelines_bp.route("/runs/<run_id>")
def run_detail(run_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_pipeline_engine()
    run = engine.repo.get_run_by_id(run_id)
    if not run:
        flash("Pipeline run not found.", "warning")
        return redirect(url_for("pipelines.index"))

    pipeline = engine.repo.get_by_id(run.pipeline_id)
    return render_template("pipelines/run_detail.html", run=run, pipeline=pipeline)
