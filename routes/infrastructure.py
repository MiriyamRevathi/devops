from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from services.iac_engine import IaCEngine
from repositories.infra_repo import InfrastructureRepository

infrastructure_bp = Blueprint("infrastructure", __name__, url_prefix="/infrastructure")

def get_iac_engine() -> IaCEngine:
    repo = InfrastructureRepository(current_app.config["INFRASTRUCTURE_DATA_DIR"])
    return IaCEngine(repo)

@infrastructure_bp.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_iac_engine()
    resources = engine.repo.get_all_resources()
    plans = engine.repo.get_all_plans()
    return render_template("infrastructure/list.html", resources=resources, plans=plans)

@infrastructure_bp.route("/plan", methods=["GET", "POST"])
def plan():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        project_id = request.form.get("project_id", "proj_default").strip()
        environment = request.form.get("environment", "Production").strip()
        yaml_definition = request.form.get("yaml_definition", "").strip()

        engine = get_iac_engine()
        success, iac_plan, msg = engine.create_plan(
            project_id=project_id,
            environment=environment,
            yaml_definition=yaml_definition
        )

        if success and iac_plan:
            flash(msg, "success")
            return redirect(url_for("infrastructure.plan_detail", plan_id=iac_plan.id))
        else:
            flash(msg, "danger")

    return render_template("infrastructure/plan.html")

@infrastructure_bp.route("/plans/<plan_id>")
def plan_detail(plan_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_iac_engine()
    iac_plan = engine.repo.get_plan_by_id(plan_id)
    if not iac_plan:
        flash("Plan not found.", "warning")
        return redirect(url_for("infrastructure.index"))

    return render_template("infrastructure/plan_detail.html", plan=iac_plan)

@infrastructure_bp.route("/plans/<plan_id>/apply", methods=["POST"])
def apply_plan(plan_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_iac_engine()
    success, msg = engine.apply_plan(plan_id)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("infrastructure.plan_detail", plan_id=plan_id))

@infrastructure_bp.route("/resources/<resource_id>/destroy", methods=["POST"])
def destroy_resource(resource_id: str):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    engine = get_iac_engine()
    success, msg = engine.destroy_resource(resource_id)
    flash(msg, "info" if success else "danger")
    return redirect(url_for("infrastructure.index"))
