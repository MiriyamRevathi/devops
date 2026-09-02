from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from core.security import login_required, permission_required, SecurityManager
from services.iac_engine import IaCEngine
from repositories.infra_repo import InfrastructureRepository
from services.audit_service import AuditService
from models.infrastructure import IaCPlan, InfraResource

infrastructure_bp = Blueprint("infrastructure", __name__, url_prefix="/infrastructure")

def get_iac_engine() -> IaCEngine:
    repo = InfrastructureRepository(current_app.config["INFRASTRUCTURE_DATA_DIR"])
    return IaCEngine(repo)

def get_infra_repo() -> InfrastructureRepository:
    return InfrastructureRepository(current_app.config["INFRASTRUCTURE_DATA_DIR"])

def get_audit_service() -> AuditService:
    return AuditService(current_app.config["AUDIT_DATA_DIR"])

@infrastructure_bp.route("/", methods=["GET"])
@login_required
@permission_required("infrastructure.view")
def list_plans():
    repo = get_infra_repo()
    plans = repo.get_all_plans()
    resources = repo.get_all_resources()
    return render_template("infrastructure/list.html", plans=plans, resources=resources)

@infrastructure_bp.route("/plan", methods=["GET", "POST"])
@login_required
@permission_required("infrastructure.plan")
def create_plan():
    if request.method == "POST":
        name = SecurityManager.sanitize_input(request.form.get("name", "AWS EKS Cluster"))
        environment = request.form.get("environment", "Production")
        config_hcl = request.form.get("config_hcl", "resources:\n  - name: eks-cluster-primary\n    type: kubernetes_cluster\n")
        created_by = session.get("username", "admin")

        engine = get_iac_engine()
        success, plan, msg = engine.create_plan(project_id="PROJ-101", environment=environment, yaml_definition=config_hcl)

        if success and plan:
            plan.name = name
            plan.created_by = created_by
            repo = get_infra_repo()
            repo.save_plan(plan)

            audit = get_audit_service()
            audit.record_event(
                actor=created_by,
                event_type="INFRA_PLAN_GENERATED",
                resource=f"InfraPlan:{plan.id}",
                details=f"Generated IaC plan '{name}' for environment '{environment}'."
            )
            flash(f"IaC Plan '{name}' generated.", "success")
            return redirect(url_for("infrastructure.plan_detail", plan_id=plan.id))
        else:
            flash(msg, "danger")

    return render_template("infrastructure/plan.html")

@infrastructure_bp.route("/plans/<plan_id>", methods=["GET"])
@login_required
@permission_required("infrastructure.view")
def plan_detail(plan_id: str):
    repo = get_infra_repo()
    plan = repo.get_plan_by_id(plan_id)
    if not plan:
        flash("IaC Plan not found.", "danger")
        return redirect(url_for("infrastructure.list_plans"))
    return render_template("infrastructure/plan_detail.html", plan=plan)

@infrastructure_bp.route("/plans/<plan_id>/apply", methods=["POST"])
@login_required
@permission_required("infrastructure.apply")
def apply_plan(plan_id: str):
    engine = get_iac_engine()
    success, msg = engine.apply_plan(plan_id)
    if success:
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="INFRA_APPLIED",
            resource=f"InfraPlan:{plan_id}",
            details=msg
        )
        flash(msg, "success")
    else:
        flash(msg, "danger")
    return redirect(url_for("infrastructure.list_plans"))

@infrastructure_bp.route("/plans/<plan_id>/destroy", methods=["POST"])
@login_required
@permission_required("infrastructure.destroy")
def destroy_plan(plan_id: str):
    user_role = session.get("role", "Viewer")
    if user_role not in ["Admin", "DevOps Engineer"]:
        if request.is_json:
            return jsonify({
                "error": "Forbidden",
                "message": "Access Denied: Infrastructure destroy operations are restricted to Admin and DevOps Engineers."
            }), 403
        return render_template("errors/403.html", required_role="Admin, DevOps Engineer", user_role=user_role), 403

    repo = get_infra_repo()
    plan = repo.get_plan_by_id(plan_id)
    if plan:
        plan.status = "DESTROYED"
        repo.save_plan(plan)
        audit = get_audit_service()
        audit.record_event(
            actor=session.get("username", "Unknown"),
            event_type="INFRA_DESTROYED",
            resource=f"InfraPlan:{plan_id}",
            details=f"Destroyed infrastructure plan '{plan_id}'."
        )
        flash(f"Infrastructure Plan #{plan_id} destroyed.", "info")
    return redirect(url_for("infrastructure.list_plans"))
